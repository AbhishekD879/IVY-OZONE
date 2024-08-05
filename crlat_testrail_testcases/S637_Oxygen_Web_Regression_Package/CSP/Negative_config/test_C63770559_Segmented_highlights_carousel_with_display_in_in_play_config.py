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
class Test_C63770559_Segmented_highlights_carousel_with_display_in_in_play_config(Common):
    """
    TR_ID: C63770559
    NAME: Segmented highlights carousel with display in in-play config
    DESCRIPTION: Ideally while configuring any highlights carousel as segmented we should not select display in-play check box
    DESCRIPTION: This tc verify what happen if we config segmented HC with display in-play checkbox
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2) Create or Edit highlights carousel with segment =  CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 3) Check display in in-play check box Make sure HC should be in valid date range and all other proper config and save highlights carousel
    """
    keep_browser_open = True

    def test_001_launch_coral_and_lads_appmobile_web_and_verify_universal_view(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web and verify universal view
        EXPECTED: Home - featured or highlights tab should load with as per CMS universal config
        """
        pass

    def test_002_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Home - featured or highlights tab should load with as per CMS segment config
        """
        pass

    def test_003_navigate_to_in_play_and_verify_highlights_carousel(self):
        """
        DESCRIPTION: Navigate to in-play and verify highlights carousel
        EXPECTED: 1) Segmented HC in pre condition should not display in in-play as CSP is not applicable to in-play
        EXPECTED: 2) In play page should display universal HCS if it has display in-play checked
        EXPECTED: 3) If we don't have any universal HC with display in in-play, no HCs should display
        EXPECTED: 4) Other content in in-play should display as per config
        """
        pass
