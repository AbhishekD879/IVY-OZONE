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
class Test_C63770571_Segmented_super_button_with_show_on_sports_page_config(Common):
    """
    TR_ID: C63770571
    NAME: Segmented super button with show on sports page config
    DESCRIPTION: Ideally while configuring any super button as segmented we should not select anything in show on sports page
    DESCRIPTION: This tc verify what happen if we config segmented super button with show on sports page
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2) Create or Edit super button with segment =  CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 3) Select one or multiple sports pages(Football, Cricket) in show on sports Make sure super button should be in valid date range and all other proper config and save
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

    def test_003_navigate_to_sports_page_which_is_selected_while_creating_super_button_as_in_pre_condition(self):
        """
        DESCRIPTION: Navigate to sports page which is selected while creating super button as in pre condition
        EXPECTED: 1) Segmented super button in pre condition should not display in sports pages(Football, Cricket) as CSP is not applicable to sports pages
        EXPECTED: 2) sports page should display universal super button if it has show in sports = (Football, Cricket)
        EXPECTED: 3) If we don't have any universal super button with show on sports(Football, Cricket), no SB should display
        EXPECTED: 4) Other content in sports pages(Football, Cricket) should display as per config
        """
        pass
