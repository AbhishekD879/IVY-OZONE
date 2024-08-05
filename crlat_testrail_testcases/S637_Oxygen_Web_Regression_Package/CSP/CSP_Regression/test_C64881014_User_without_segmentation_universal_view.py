import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64881014_User_without_segmentation_universal_view(Common):
    """
    TR_ID: C64881014
    NAME: User without segmentation â€“ universal view
    DESCRIPTION: This test case verifies user without segmentation
    PRECONDITIONS: User should not mapped to any segment
    """
    keep_browser_open = True

    def test_001_launch_coral_and_lads_appmobile_web_and_verify_universal_view(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web and verify universal view
        EXPECTED: Home page should load with as per CMS universal config
        """
        pass

    def test_002_login_with_user_as_preconditions(self):
        """
        DESCRIPTION: Login with user as preconditions
        EXPECTED: Universal view should displayed as there is no congifuration for specific segement
        """
        pass
