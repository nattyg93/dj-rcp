"""Mixins global mixins for tests."""
from rest_framework import status

from common.test.mixins import failure, success
from users.models import User
from users.tests.factories import UserFactory


class AnonTestCaseMixin(
    failure.CreateTestCaseMixin,
    success.ListTestCaseMixin,
    success.RetrieveTestCaseMixin,
    failure.UpdateTestCaseMixin,
    failure.DeleteTestCaseMixin,
    success.SuccessStatusMixin,
    failure.ErrorCodeMixin,
    failure.ErrorStatusMixin,
):
    """Ensure all actions fail with the correct status and code."""

    expected_error_status = status.HTTP_401_UNAUTHORIZED
    expected_error_code = "401"
    error_code_kwargs: dict = {}


class UserTestCaseMixin(
    failure.CreateTestCaseMixin,
    success.ListTestCaseMixin,
    success.RetrieveTestCaseMixin,
    failure.UpdateTestCaseMixin,
    failure.DeleteTestCaseMixin,
    success.SuccessStatusMixin,
    failure.ErrorCodeMixin,
    failure.ErrorStatusMixin,
):
    """Ensure all actions fail with the correct status and code."""

    user: User
    expected_error_status = status.HTTP_403_FORBIDDEN
    expected_error_code = "403"
    error_code_kwargs: dict = {}

    @classmethod
    def setUpClass(cls):  # pylint: disable=invalid-name
        """Set up the required attributes for the tests."""
        super().setUpClass()
        cls.user = UserFactory()

    def setUp(self):  # pylint: disable=invalid-name
        """Authenticate as a user before each test."""
        self.auth(self.user)


class PrivilegedTestCaseMixin(
    failure.CreateTestCaseMixin,
    success.ListTestCaseMixin,
    success.RetrieveTestCaseMixin,
    failure.UpdateTestCaseMixin,
    failure.DeleteTestCaseMixin,
    success.SuccessStatusMixin,
    failure.ErrorCodeMixin,
    failure.ErrorStatusMixin,
):
    """Ensure all actions fail with the correct status and code."""

    user: User
    expected_error_status = status.HTTP_405_METHOD_NOT_ALLOWED
    expected_error_code = "405"
    error_code_kwargs: dict = {}

    def test_create(self):
        """Users with permissions cannot create instances."""
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
        """Users with permissions cannot update instances."""
        self.auth(UserFactory(permission_codes=self.perms("update")))
        super().test_update()

    def test_delete(self):
        """Users with permissions cannot delete instances."""
        self.auth(UserFactory(permission_codes=self.perms("delete")))
        super().test_delete()


class TrueReadOnlyMixin:
    """Expect 405s for destructive actions."""

    action_map = {
        "create": {"method": "POST"},
        "update": {"method": "PATCH"},
        "delete": {"method": "DELETE"},
    }

    def get_expected_error_code(self, action, **context):
        """Expect 405s for destructive actions."""
        if action in self.action_map:
            return "405", self.action_map[action]
        return super().get_expected_error_code(action, **context)

    def get_expected_error_status(self, action, **context):
        """Expect 405s for destructive actions."""
        if action in self.action_map:
            return status.HTTP_405_METHOD_NOT_ALLOWED
        return super().get_expected_error_status(action, **context)
