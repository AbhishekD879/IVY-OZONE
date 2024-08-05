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
class Test_C64881016_All_super_buttons_with_segment_configNo_universal_Superbutton(Common):
    """
    TR_ID: C64881016
    NAME: All super buttons with segment config(No universal Superbutton)
    DESCRIPTION: This test case verifies All super buttons with segment config
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2) Create or Edit super button with segment =Â Â CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 3) Make sure we do not have any super button with universal
    """
    keep_browser_open = True

    def test_001_launch_coral_and_lads_appmobile_web(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web
        EXPECTED: Home page should load  as per CMS config
        """
        pass

    def test_002_verify_universal_view(self):
        """
        DESCRIPTION: verify universal view
        EXPECTED: No super button should display as we don't have super buttons for universal view
        """
        pass

    def test_003_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Home page should load as per CMS segment config.
        """
        pass

    def test_004_verify_home_page(self):
        """
        DESCRIPTION: Verify home page
        EXPECTED: Super button configured in pre conditions should display
        """
        pass
