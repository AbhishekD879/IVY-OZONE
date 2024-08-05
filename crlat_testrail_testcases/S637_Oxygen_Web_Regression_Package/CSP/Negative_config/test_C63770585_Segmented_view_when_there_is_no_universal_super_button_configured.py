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
class Test_C63770585_Segmented_view_when_there_is_no_universal_super_button_configured(Common):
    """
    TR_ID: C63770585
    NAME: Segmented view when there is no universal super button configured
    DESCRIPTION: This testcase verifies segmented view when there is no universal super button configured
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2) Create or Edit super button with segment =  CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 3) Make sure we do not have any super button with universal
    """
    keep_browser_open = True

    def test_001_launch_coral_and_lads_appmobile_web_and_verify_universal_view(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web and verify universal view
        EXPECTED: Home - featured or highlights tab should load with as per CMS universal config
        EXPECTED: No super button should display as we don't have super buttons for universal view
        """
        pass

    def test_002_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Home - featured or highlights tab should load with as per CMS segment config
        EXPECTED: Super button configured in pre conditions should display
        """
        pass
