"""Mixins global mixins for tests."""
from typing import Dict, Iterable

from django.db.models import Model
from rest_framework import status

from users.models import User
from users.tests.factories import UserFactory


class ErrorCodeMixin:
    """Provide mixin for getting the expected error code."""

    expected_error_code: str
    error_code_kwargs: Dict[str, str]

    def get_expected_error_code(
        self, action, **context
    ):  # pylint: disable=unused-argument
        """
        Return the expected error code.

        Override this method to provide a different error code on
        a per action basis.
        """
        return (self.expected_error_code, self.error_code_kwargs)


class ErrorStatusMixin:
    """Provide mixin for getting the expected error status."""

    expected_error_status: int

    def get_expected_error_status(
        self, action, **context
    ):  # pylint: disable=unused-argument
        """
        Return the expected error status.

        Override this method to provide a different error status
        on a per action basis.
        """
        return self.expected_error_status


class CreateTestCaseMixin:
    """Provide a default implementation of test_create."""

    def test_create(self):
        """The user cannot create instances."""
        json = self.post(
            f"/{self.resource_name}/",
            data=self.get_post_data(),
            asserted_status=self.get_expected_error_status("create"),
        ).json()
        # check has correct error
        error_code, error_kwargs = self.get_expected_error_code("create")
        self.assertHasError(
            json, "data", self.ERRORS[error_code].format(**error_kwargs)
        )


class ListTestCaseMixin:
    """Provide a default implementation of test_list."""

    instances: Iterable[Model]

    def test_list(self):
        """The user cannot list instances."""
        json = self.get(
            f"/{self.resource_name}/",
            asserted_status=self.get_expected_error_status("list"),
        ).json()
        # check has correct error
        error_code, error_kwargs = self.get_expected_error_code("list")
        self.assertHasError(
            json, "data", self.ERRORS[error_code].format(**error_kwargs)
        )


class RetrieveTestCaseMixin:
    """Provide a default implementation of test_retrieve."""

    instance: Model

    def test_retrieve(self):
        """The user cannot retrieve instances."""
        json = self.get(
            f"/{self.resource_name}/{self.instance.pk}/",
            asserted_status=self.get_expected_error_status("retrieve"),
        ).json()
        # check has correct error
        error_code, error_kwargs = self.get_expected_error_code("retrieve")
        self.assertHasError(
            json, "data", self.ERRORS[error_code].format(**error_kwargs)
        )


class UpdateTestCaseMixin:
    """Provide a default implementation of test_update."""

    instance: Model

    def test_update(self):
        """The user cannot update instances."""
        json = self.patch(
            f"/{self.resource_name}/{self.instance.pk}/",
            data=self.get_patch_data(),
            asserted_status=self.get_expected_error_status("update"),
        ).json()
        # check has correct error
        error_code, error_kwargs = self.get_expected_error_code("update")
        self.assertHasError(
            json, "data", self.ERRORS[error_code].format(**error_kwargs)
        )


class DeleteTestCaseMixin:
    """Provide a default implementation of test_delete."""

    instance: Model

    def test_delete(self):
        """The user cannot delete instances."""
        json = self.delete(
            f"/{self.resource_name}/{self.instance.pk}/",
            data=self.get_patch_data(),
            asserted_status=self.get_expected_error_status("delete"),
        ).json()
        # check has correct error
        error_code, error_kwargs = self.get_expected_error_code("delete")
        self.assertHasError(
            json, "data", self.ERRORS[error_code].format(**error_kwargs)
        )


class AnonTestCaseMixin(
    CreateTestCaseMixin,
    ListTestCaseMixin,
    RetrieveTestCaseMixin,
    UpdateTestCaseMixin,
    DeleteTestCaseMixin,
    ErrorCodeMixin,
    ErrorStatusMixin,
):
    """Ensure all actions fail with the correct status and code."""

    expected_error_status = status.HTTP_401_UNAUTHORIZED
    expected_error_code = "401"
    error_code_kwargs: Dict[str, str] = {}


class UserTestCaseMixin(
    CreateTestCaseMixin,
    ListTestCaseMixin,
    RetrieveTestCaseMixin,
    UpdateTestCaseMixin,
    DeleteTestCaseMixin,
    ErrorCodeMixin,
    ErrorStatusMixin,
):
    """Ensure all actions fail with the correct status and code."""

    user: User
    expected_error_status = status.HTTP_403_FORBIDDEN
    expected_error_code = "403"
    error_code_kwargs: Dict[str, str] = {}

    @classmethod
    def setUpClass(cls):  # pylint: disable=invalid-name
        """Set up the required attributes for the tests."""
        super().setUpClass()
        cls.user = UserFactory()

    def setUp(self):  # pylint: disable=invalid-name
        """Authenticate as a user before each test."""
        self.auth(self.user)
