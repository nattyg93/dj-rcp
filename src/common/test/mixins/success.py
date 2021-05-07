"""Mixins global mixins for tests."""
from typing import Iterable

from django.db.models import Model
from rest_framework import status

from users.models import User
from users.tests.factories import UserFactory


class SuccessStatusMixin:
    """Provide mixin for getting the expected success status."""

    def get_expected_success_status(
        self, action, **context
    ):  # pylint: disable=no-self-use,unused-argument
        """
        Return the expected success status.

        Override this method to provide a different success code
        on a per action basis.
        """
        if action == "create":
            return status.HTTP_201_CREATED
        if action == "delete":
            return status.HTTP_204_NO_CONTENT
        return status.HTTP_200_OK


class CreateTestCaseMixin:
    """Provide a default implementation of test_create."""

    def test_create(self):
        """The user can create instances."""
        self.post(
            f"/{self.resource_name}/",
            data=self.get_post_data(),
            asserted_status=self.get_expected_success_status("create"),
            asserted_schema=self.schema.get_matcher(),
        )


class ListTestCaseMixin:
    """Provide a default implementation of test_list."""

    instances: Iterable[Model]

    def test_list(self):
        """The user can list instances."""
        json = self.get(
            f"/{self.resource_name}/",
            asserted_status=self.get_expected_success_status("list"),
            asserted_schema=self.schema.get_matcher(many=True),
        ).json()
        # check has correct items
        self.assertCountEqual(
            [data["id"] for data in json["data"]],
            [str(instance.pk) for instance in self.instances],
        )


class RetrieveTestCaseMixin:
    """Provide a default implementation of test_retrieve."""

    instance: Model

    def test_retrieve(self):
        """Anons can retrieve airlines."""
        json = self.get(
            f"/{self.resource_name}/{self.instance.pk}/",
            asserted_status=self.get_expected_success_status("retrieve"),
            asserted_schema=self.schema.get_matcher(),
        ).json()
        # check id is correct
        self.assertEqual(json["data"]["id"], str(self.instance.pk))


class UpdateTestCaseMixin:
    """Provide a default implementation of test_update."""

    instance: Model

    def test_update(self):
        """The user can update instances."""
        data = self.get_patch_data(id=self.instance.pk)
        json = self.patch(
            f"/{self.resource_name}/{self.instance.pk}/",
            data=data,
            asserted_status=self.get_expected_success_status("update"),
            asserted_schema=self.schema.get_matcher(),
        ).json()
        # check all specified attributes were successfully updated
        attributes = json["data"]["attributes"]
        for key, value in data["data"].get("attributes", {}).items():
            self.assertIn(key, attributes)
            self.assertEqual(attributes[key], value)
        # check all specified relationships were successfully updated
        relationships = json["data"].get("relationships", {})
        for key, value in data.get("relationships", {}).items():
            self.assertIn(key, relationships)
            self.assertEqual(relationships[key], value)


class DeleteTestCaseMixin:
    """Provide a default implementation of test_delete."""

    instance: Model

    def test_delete(self):
        """The user can delete instances."""
        self.delete(
            f"/{self.resource_name}/{self.instance.pk}/",
            data=self.get_patch_data(),
            asserted_status=self.get_expected_success_status("delete"),
        )


class AnonTestCaseMixin(
    CreateTestCaseMixin,
    ListTestCaseMixin,
    RetrieveTestCaseMixin,
    UpdateTestCaseMixin,
    DeleteTestCaseMixin,
    SuccessStatusMixin,
):
    """Ensure all actions succeed with the correct code."""


class UserTestCaseMixin(
    CreateTestCaseMixin,
    ListTestCaseMixin,
    RetrieveTestCaseMixin,
    UpdateTestCaseMixin,
    DeleteTestCaseMixin,
    SuccessStatusMixin,
):
    """Ensure all actions succeed with the correct code."""

    user: User

    @classmethod
    def setUpClass(cls):  # pylint: disable=invalid-name
        """Set up the required attributes for the tests."""
        super().setUpClass()
        cls.user = UserFactory()

    def setUp(self):  # pylint: disable=invalid-name
        """Authenticate as a user before each test."""
        self.auth(self.user)


class PrivilegedTestCaseMixin(
    CreateTestCaseMixin,
    ListTestCaseMixin,
    RetrieveTestCaseMixin,
    UpdateTestCaseMixin,
    DeleteTestCaseMixin,
    SuccessStatusMixin,
):
    """Ensure all actions succeed with the correct code."""

    def test_create(self):
        """Users with permissions can create instances."""
        self.auth(UserFactory(permission_codes=self.perms("create")))
        super().test_create()

    def test_list(self):
        """Users with permissions can list instances."""
        self.auth(UserFactory(permission_codes=self.perms("retrieve")))
        super().test_list()

    def test_retrieve(self):
        """Users with permissions can retrieve instances."""
        self.auth(UserFactory(permission_codes=self.perms("retrieve")))
        super().test_retrieve()

    def test_update(self):
        """Users with permissions can update instances."""
        self.auth(UserFactory(permission_codes=self.perms("update")))
        super().test_update()

    def test_delete(self):
        """Users with permissions can delete instances."""
        self.auth(UserFactory(permission_codes=self.perms("delete")))
        super().test_delete()
