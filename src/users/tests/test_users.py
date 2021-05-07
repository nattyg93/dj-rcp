"""Tests for users endpoint."""
from __future__ import annotations

from typing import Dict, Type

from django import test
from django.conf import settings
from django.contrib.auth.models import Group
from django.core import mail
from rest_framework import status

from common.test import JsonApiTestCase, mixins
from common.test.schemas import JsonApiSchema
from users.models import User, get_role_choices
from users.tests import factories, schemas


class EndpointConfig(
    mixins.FactoryDataMixin, mixins.DefaultDataMixin, mixins.PermissionCodeMixin
):
    """Define endpoint-wide configuration."""

    factory = factories.UserFactory
    permission_model_name = "user"
    app_label = "users"
    schema: Type[JsonApiSchema] = schemas.UsersSchema

    permission_mapping = {
        **mixins.PermissionCodeMixin.permission_mapping,
        "set_password": "{app_label}.set_{permission_model_name}_password",
        "set_roles": "{app_label}.set_{permission_model_name}_roles",
    }

    admin_perms = ["set_roles", "retrieve", "update"]

    def get_default_post_values(self):
        """Return default values required for a successful post."""
        return {
            "email": "email@example.com",
            "password": "hellopass123",
        }

    def get_default_patch_values(self):
        """Return default values required for a successful patch."""
        return {}


class AnonTestCase(EndpointConfig, mixins.failure.AnonTestCaseMixin, JsonApiTestCase):
    """Test validation for anon users."""


class UserTestCase(
    EndpointConfig,
    mixins.failure.CreateTestCaseMixin,
    mixins.failure.DeleteTestCaseMixin,
    mixins.failure.ErrorCodeMixin,
    mixins.failure.ErrorStatusMixin,
    mixins.success.UserTestCaseMixin,
    JsonApiTestCase,
):
    """Test validation for authed users."""

    batch_size = 1
    expected_error_code = "403"
    error_code_kwargs: Dict[str, str] = {}
    expected_error_status = status.HTTP_403_FORBIDDEN

    def get_expected_error_code(self, action, **context):
        """Return 405s for DELETEs."""
        if action == "delete":
            return "405", {"method": "DELETE"}
        return super().get_expected_error_code(action, **context)

    def get_expected_error_status(self, action, **context):
        """Return 405s for DELETEs."""
        if action == "delete":
            return status.HTTP_405_METHOD_NOT_ALLOWED
        return super().get_expected_error_status(action, **context)

    def setUp(self):
        """Set the instances' user to be the currently authed user."""
        super().setUp()
        # replace the authed user with self.instance
        # and bust the permission cache
        self.auth(User.objects.get(pk=self.instance.pk))

    def test_list(self):
        """Users can only list their own user."""
        # make sure there is more than one user so we are sure
        # that the test is actually checking that only the authed
        # user is returned in the response
        self.assertGreater(User.objects.count(), 1)
        super().test_list()

    def test_retrieve_other(self):
        """User cannot retrieve other users."""
        other_user = self.factory()
        json = self.get(
            f"/{self.resource_name}/{other_user.pk}/",
            asserted_status=status.HTTP_404_NOT_FOUND,
        ).json()
        # check has correct error
        self.assertHasError(json, "", self.ERRORS["404"])

    def test_update_other(self):
        """User cannot change other users."""
        other_user = self.factory()
        json = self.patch(
            f"/{self.resource_name}/{other_user.pk}/",
            data=self.get_patch_data(id=other_user.pk),
            asserted_status=status.HTTP_404_NOT_FOUND,
        ).json()
        # check has correct error
        self.assertHasError(json, "", self.ERRORS["404"])

    def test_delete_other(self):
        """User cannot delete other user."""
        other_user = self.factory()
        json = self.delete(
            f"/{self.resource_name}/{other_user.pk}/",
            asserted_status=status.HTTP_405_METHOD_NOT_ALLOWED,
        ).json()
        # check has correct error
        self.assertHasError(json, "data", self.ERRORS["405"].format(method="DELETE"))

    def test_change_password(self):
        """User can change their own password."""
        password = "pass"
        new_password = "hellopass123"
        user = self.factory(email="user@example.com", password=password)
        self.auth(user)
        # sanity check
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.check_password(new_password))
        self.patch(
            f"/{self.resource_name}/{user.pk}/",
            data=self.get_patch_data(
                id=user.pk, current_password=password, password=new_password
            ),
            asserted_status=status.HTTP_200_OK,
            asserted_schema=self.schema.get_matcher(),
        )
        # check password was successfully updated
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))

    def test_current_password_required(self):
        """User cannot change own password without current password."""
        password = "pass"
        new_password = "hellopass123"
        user = self.factory(password=password)
        self.auth(user)
        json = self.patch(
            f"/{self.resource_name}/{user.pk}/",
            data=self.get_patch_data(id=user.pk, password=new_password),
            asserted_status=status.HTTP_400_BAD_REQUEST,
        ).json()
        # check has correct error
        self.assertHasError(
            json,
            "current_password",
            "This field is required when changing your password.",
        )

    def test_current_password_correct(self):
        """User cannot change own password without correct current password."""
        new_password = "hellopass123"
        user = self.instance
        self.auth(user)
        json = self.patch(
            f"/{self.resource_name}/{user.pk}/",
            data=self.get_patch_data(
                id=user.pk, current_password="wrong pass", password=new_password
            ),
            asserted_status=status.HTTP_400_BAD_REQUEST,
        ).json()
        # check has correct error
        self.assertHasError(
            json, "current_password", "Your current password is incorrect."
        )

    def test_update_roles(self):
        """User cannot change own roles."""
        user = self.instance
        self.auth(user)
        # sanity check
        self.assertEqual(user.groups.count(), 0)
        json = self.patch(
            f"/{self.resource_name}/{user.pk}/",
            data=self.get_patch_data(id=user.pk, roles=[settings.ADMINS_GROUP_NAME]),
            asserted_status=status.HTTP_400_BAD_REQUEST,
        ).json()
        # check has correct error
        self.assertHasError(
            json, "roles", "You do not have permission to set this field."
        )


class PrivilegedTestCase(
    EndpointConfig,
    mixins.failure.DeleteTestCaseMixin,
    mixins.failure.ErrorCodeMixin,
    mixins.failure.ErrorStatusMixin,
    mixins.success.PrivilegedTestCaseMixin,
    JsonApiTestCase,
):
    """Test validation on users endpoint."""

    expected_error_code = "405"
    error_code_kwargs: Dict[str, str] = {"method": "DELETE"}
    expected_error_status = status.HTTP_405_METHOD_NOT_ALLOWED

    def test_list(self):
        """Users with permissions can list users."""
        user = User.objects.get(pk=self.instance.pk)
        self.auth(user)
        self.give_perms("retrieve")
        json = self.get(
            f"/{self.resource_name}/",
            asserted_status=status.HTTP_200_OK,
            asserted_schema=self.schema.get_matcher(many=True),
        ).json()
        # check has correct items
        users = self.instances
        self.assertCountEqual(
            [data["id"] for data in json["data"]], [str(user.pk) for user in users]
        )

    def test_delete(self):
        """Users with privileges cannot delete users."""
        user = User.objects.get(pk=self.instance.pk)
        self.auth(user)
        self.give_perms("delete")
        super().test_delete()

    def test_create_set_roles(self):
        """User with perms can create a user with roles set."""
        test_roles = [
            [],
            [settings.ADMINS_GROUP_NAME],
        ]
        self.auth(
            self.factory(permission_codes=self.perms(*self.admin_perms, "create"))
        )
        for index, roles in enumerate(test_roles):
            with self.subTest(roles=roles):
                json = self.post(
                    f"/{self.resource_name}/",
                    data=self.get_post_data(email=f"{index}@example.com", roles=roles),
                    asserted_status=status.HTTP_201_CREATED,
                    asserted_schema=self.schema.get_matcher(),
                ).json()
                # check the roles are set
                self.assertCountEqual(json["data"]["attributes"]["roles"], roles)

    def test_retrieve_other(self):
        """User with perms can get other users."""
        user = self.factory(permission_codes=self.perms("retrieve"))
        other_user = self.instance
        self.auth(user)
        json = self.get(
            f"/{self.resource_name}/{other_user.pk}/",
            asserted_status=status.HTTP_200_OK,
            asserted_schema=self.schema.get_matcher(),
        ).json()
        # check parameters are correct
        self.assertEqual(json["data"]["id"], str(other_user.pk))
        self.assertEqual(json["data"]["attributes"]["email"], other_user.email)

    def test_update_other(self):
        """User with proper perms can patch other user."""
        password = "pass"
        new_password = "hellopass123"
        user = self.factory(permission_codes=self.perms("update"))
        other_user = self.instance
        self.auth(user)
        json = self.patch(
            f"/{self.resource_name}/{other_user.pk}/",
            data=self.get_patch_data(
                id=other_user.pk, current_password=password, password=new_password
            ),
            asserted_status=status.HTTP_200_OK,
            asserted_schema=self.schema.get_matcher(),
        ).json()
        # check parameters are correct
        self.assertEqual(json["data"]["id"], str(other_user.pk))
        self.assertEqual(json["data"]["attributes"]["email"], other_user.email)
        # check password was successfully updated
        other_user.refresh_from_db()
        self.assertTrue(other_user.check_password(new_password))

    def test_delete_other(self):
        """User with perms cannot delete other user."""
        self.auth(self.factory(permission_codes=self.perms("delete")))
        other_user = self.instance
        json = self.delete(
            f"/{self.resource_name}/{other_user.pk}/",
            asserted_status=status.HTTP_405_METHOD_NOT_ALLOWED,
        ).json()
        # check has correct error
        self.assertHasError(json, "data", self.ERRORS["405"].format(method="DELETE"))

    def test_blank_password(self):
        """Blank password is treated like it was not supplied."""
        self.auth(self.factory(permission_codes=self.perms("create")))
        email_address = "asdf@example.com"
        self.post(
            f"/{self.resource_name}/",
            data=self.get_post_data(email=email_address, password=""),
            asserted_status=status.HTTP_201_CREATED,
            asserted_schema=self.schema.get_matcher(),
        )

    def test_set_password_email(self):
        """Users created without passwords are sent "set password" emails."""
        self.auth(self.factory(permission_codes=self.perms("create")))
        email_address = "asdf@example.com"
        # sanity check
        self.assertEqual(len(mail.outbox), 0)
        self.post(
            f"/{self.resource_name}/",
            data=self.get_post_data(email=email_address, exclude=["password"]),
            asserted_status=status.HTTP_201_CREATED,
            asserted_schema=self.schema.get_matcher(),
        )
        # check the email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertListEqual(email.to, [email_address])
        self.assertEqual(email.subject, "Set Your Password")

    def test_set_password(self):
        """Users with perms can set passwords sans current_password."""
        new_password = "hellopass123"
        self.auth(self.factory(permission_codes=self.perms("update", "set_password")))
        other_user = self.instance
        # sanity check
        other_user.check_password(new_password)
        json = self.patch(
            f"/{self.resource_name}/{other_user.pk}/",
            data=self.get_patch_data(id=other_user.id, password=new_password),
            asserted_status=status.HTTP_200_OK,
            asserted_schema=self.schema.get_matcher(),
        ).json()
        # check parameters are correct
        self.assertEqual(json["data"]["id"], str(other_user.pk))
        self.assertEqual(json["data"]["attributes"]["email"], other_user.email)
        # check password was successfully updated
        other_user.refresh_from_db()
        self.assertTrue(other_user.check_password(new_password))

    def test_update_roles(self):
        """Users with perms can change roles."""
        self.auth(self.factory(permission_codes=self.perms(*self.admin_perms)))
        user = self.factory()
        # sanity check
        self.assertEqual(user.groups.count(), 0)
        # check the roles can be changed
        roles = [settings.ADMINS_GROUP_NAME]
        json = self.patch(
            f"/{self.resource_name}/{user.pk}/",
            data=self.get_patch_data(id=user.pk, roles=roles),
            asserted_status=status.HTTP_200_OK,
            asserted_schema=self.schema.get_matcher(),
        ).json()
        # check user is an admin
        self.assertCountEqual(
            json["data"]["attributes"]["roles"], [settings.ADMINS_GROUP_NAME]
        )
        # check the group is set in the db
        user = User.objects.get(pk=user.pk)
        self.assertIsNotNone(user)
        self.assertCountEqual(list(user.groups.values_list("name", flat=True)), roles)


class RolesTestCase(EndpointConfig, JsonApiTestCase):
    """Test behaviour related to roles."""

    @classmethod
    def setUpClass(cls):
        """Remove any users created during setup."""
        super().setUpClass()
        # delete any users created during setup
        User.objects.all().delete()

    def test_roles_set(self):
        """Expected roles are set."""
        user = self.factory()
        admin = self.factory()
        admin.groups.set(Group.objects.filter(name=settings.ADMINS_GROUP_NAME))
        user_roles = [(user, []), (admin, [settings.ADMINS_GROUP_NAME])]
        self.auth(self.factory(permission_codes=self.perms("retrieve")))
        for user, expected_roles in user_roles:
            with self.subTest(expected_roles=expected_roles):
                json = self.get(
                    f"/{self.resource_name}/{user.pk}/",
                    asserted_status=status.HTTP_200_OK,
                    asserted_schema=self.schema.get_matcher(),
                ).json()
                # check the correct roles are provided
                self.assertCountEqual(
                    json["data"]["attributes"]["roles"], expected_roles
                )

    def test_roles_is_list(self):
        """Roles must be a list."""
        self.auth(self.factory(permission_codes=self.perms(*self.admin_perms)))
        user = self.factory()
        json = self.patch(
            f"/{self.resource_name}/{user.pk}/",
            data=self.get_patch_data(id=user.pk, roles={"asdf": "fdsa"}),
            asserted_status=status.HTTP_400_BAD_REQUEST,
        ).json()
        # check has correct error
        self.assertHasError(json, "roles", "Expected a list of strings.")

    def test_roles_valid(self):
        """Each roles must be a valid role."""
        self.auth(self.factory(permission_codes=self.perms(*self.admin_perms)))
        user = self.factory()
        invalid_role = "asdf"
        # sanity check
        self.assertFalse(Group.objects.filter(name=invalid_role).exists())
        self.assertNotIn(
            invalid_role, [role_choice[0] for role_choice in get_role_choices()]
        )
        json = self.patch(
            f"/{self.resource_name}/{user.pk}/",
            data=self.get_patch_data(
                id=user.pk, roles=[settings.ADMINS_GROUP_NAME, invalid_role]
            ),
            asserted_status=status.HTTP_400_BAD_REQUEST,
        ).json()
        # check has correct error
        self.assertHasError(json, "roles/1", '"asdf" is not a valid choice.')

    def test_role_other_group(self):
        """Groups not in the roles' choices are validated."""
        self.auth(self.factory(permission_codes=self.perms(*self.admin_perms)))
        user = self.factory()
        test_group = factories.GroupFactory()
        # sanity check
        self.assertNotIn(
            test_group.name, [role_choice[0] for role_choice in get_role_choices()]
        )
        json = self.patch(
            f"/{self.resource_name}/{user.pk}/",
            data=self.get_patch_data(id=user.pk, roles=[test_group.name]),
            asserted_status=status.HTTP_400_BAD_REQUEST,
        ).json()
        # check has correct error
        self.assertHasError(
            json, "roles/0", f'"{test_group.name}" is not a valid choice.'
        )

    def test_roles_unique(self):
        """User can not have duplicate roles."""
        self.auth(self.factory(permission_codes=self.perms(*self.admin_perms)))
        user = self.factory()
        json = self.patch(
            f"/{self.resource_name}/{user.pk}/",
            data=self.get_patch_data(
                id=user.pk,
                roles=[settings.ADMINS_GROUP_NAME, settings.ADMINS_GROUP_NAME],
            ),
            asserted_status=status.HTTP_400_BAD_REQUEST,
        ).json()
        # check has correct error
        self.assertHasError(
            json, "roles", "This field cannot contain duplicate entries."
        )

    def test_filter_roles(self):
        """Users are filtered to those with the given role."""
        self.auth(self.factory(permission_codes=self.perms(*self.admin_perms)))
        num_instances = 2
        admins = self.factory.create_batch(size=num_instances)
        self.factory.create_batch(size=num_instances)
        admin_group = Group.objects.get(name=settings.ADMINS_GROUP_NAME)
        for admin in admins:
            admin.groups.add(admin_group)
        # sanity check
        self.assertEqual(User.objects.count(), 1 + num_instances * 2)
        json = self.get(
            f"/{self.resource_name}/",
            data={"filter[roles__in]": settings.ADMINS_GROUP_NAME},
            asserted_status=status.HTTP_200_OK,
            asserted_schema=self.schema.get_matcher(many=True),
        ).json()
        # check only the correct users are returned
        self.assertCountEqual(
            [data["id"] for data in json["data"]], [str(admin.pk) for admin in admins]
        )

    def test_filter_roles_no_users(self):
        """No users are returned if there are no users with the role."""
        self.auth(self.factory(permission_codes=self.perms(*self.admin_perms)))
        self.factory.create_batch(size=2)
        # sanity check
        json = self.get(
            f"/{self.resource_name}/",
            asserted_status=status.HTTP_200_OK,
            asserted_schema=self.schema.get_matcher(many=True),
        ).json()
        # check all users are returned
        self.assertEqual(len(json["data"]), User.objects.count())
        # check no users are returned
        json = self.get(
            f"/{self.resource_name}/",
            data={"filter[roles__in]": settings.ADMINS_GROUP_NAME},
            asserted_status=status.HTTP_200_OK,
            asserted_schema=self.schema.get_matcher(many=True, optional=True),
        ).json()
        # check there are no users returned
        self.assertEqual(len(json["data"]), 0)

    def test_filter_role_validation(self):
        """Invalid role filter choices are validated."""
        self.auth(self.factory(permission_codes=self.perms(*self.admin_perms)))
        json = self.get(
            f"/{self.resource_name}/",
            data={"filter[roles__in]": "INVALID_ROLE_CHOICE"},
            asserted_status=status.HTTP_400_BAD_REQUEST,
        ).json()
        # check has correct error
        self.assertHasError(
            json,
            "roles__in",
            "Select a valid choice. INVALID_ROLE_CHOICE is not "
            "one of the available choices.",
        )

    def test_filter_role_other_group(self):
        """Groups not in the filter role's choices are validated."""
        self.auth(self.factory(permission_codes=self.perms("retrieve")))
        test_group = factories.GroupFactory()
        json = self.get(
            f"/{self.resource_name}/",
            data={"filter[roles__in]": test_group.name},
            asserted_status=status.HTTP_400_BAD_REQUEST,
        ).json()
        # check has correct error
        self.assertHasError(
            json,
            "roles__in",
            f"Select a valid choice. {test_group.name} is not "
            "one of the available choices.",
        )


class RolesMethodTestCase(test.TestCase):
    """Unit test the user model."""

    admins_group: Group

    @classmethod
    def setUpClass(cls):
        """Set user wide data."""
        super().setUpClass()
        cls.admins_group, _ = Group.objects.get_or_create(
            name=settings.ADMINS_GROUP_NAME
        )

    def test_roles_empty(self):
        """Roles property returns empty list when user has no groups."""
        user = factories.UserFactory()
        # sanity check
        self.assertCountEqual(user.groups.all(), [])
        # check roles is an empty list
        self.assertListEqual(user.roles, [])

    def test_roles_not_in_choices(self):
        """Roles not in the choices are not returned."""
        test_group = factories.GroupFactory()
        user = factories.UserFactory()
        user.groups.add(test_group)
        # sanity check
        self.assertCountEqual(user.groups.all(), [test_group])
        # check the test group is in roles
        self.assertCountEqual(user.roles, [])

    def test_role_correct(self):
        """Roles in choices are returned."""
        test_group = factories.GroupFactory()
        user = factories.UserFactory()
        user.groups.set([self.admins_group, test_group])
        # sanity check
        self.assertCountEqual(user.groups.all(), [self.admins_group, test_group])
        # check the test group is in roles
        self.assertListEqual(user.roles, [self.admins_group.name])


class RoleChoicesTestCase(test.TestCase):
    """Test get_role_choices function behaviour."""

    @test.override_settings(AUTH_GROUPS=[])
    def test_get_role_choices_empty(self):
        """Empty list is returned if no AUTH_GROUPS."""
        self.assertListEqual(get_role_choices(), [])

    @test.override_settings(
        AUTH_GROUPS=[
            {"name": "group_name", "permissions": set()},
            {"name": "other_group", "permissions": set()},
        ]
    )
    def test_get_role_choices(self):
        """The group names make up the choices."""
        self.assertCountEqual(
            get_role_choices(),
            [("group_name", "group_name"), ("other_group", "other_group")],
        )

    @test.override_settings(AUTH_GROUPS=[{"name": "group_name", "permissions": set()}])
    def test_groups_not_in_choices(self):
        """Empty list if no AUTH_GROUPS."""
        group = factories.GroupFactory()
        self.assertNotIn(group.name, [choice[0] for choice in get_role_choices()])
