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
class Test_C64881013_User_with_segmentation_but_no_config_in_CMS_universal_view(Common):
    """
    TR_ID: C64881013
    NAME: User with segmentation, but no config in CMS â€“ universal view
    DESCRIPTION: This test case verifies user with segmentation, but no config in CMS
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: Â 2) No configuration in CMS for CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True

    def test_001_launch_coral_and_lads_appmobile_web_and_verify_universal_view(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web and verify universal view
        EXPECTED: Home page should load with as per CMS universal config
        """
        pass

    def test_002_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Universal view should displayed as there is no congifuration for specific segement
        """
        pass
