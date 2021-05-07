"""Project wide test runners."""
from django.conf import settings
from django.test.runner import DiscoverRunner

from common.test.utils import wipe_directory_recursive


class MediaCleanupDiscoverRunner(DiscoverRunner):
    """DiscoverRunner which cleans up media on tear down."""

    def teardown_test_environment(self, **kwargs):
        """Remove media files during tear down."""
        if settings.MEDIA_URL == getattr(settings, "TEST_MEDIA_URL", None):
            if self.verbosity >= 1:
                print("Destroying test media...")
            try:
                wipe_directory_recursive("")
            except NotImplementedError:
                if self.verbosity >= 1:
                    print(
                        "Not able to clear out test uploads - this will need to "
                        "be done manually. Currently: `settings.MEDIA_URL = "
                        f"{settings.MEDIA_URL}`"
                    )
        super().teardown_test_environment(**kwargs)
