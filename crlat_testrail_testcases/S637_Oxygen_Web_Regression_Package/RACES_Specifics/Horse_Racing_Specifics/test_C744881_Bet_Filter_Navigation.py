import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C744881_Bet_Filter_Navigation(Common):
    """
    TR_ID: C744881
    NAME: Bet Filter Navigation
    DESCRIPTION: Test case verifies that using 'Bet Filter' link user will be redirected to correct page
    PRECONDITIONS: JIRA tickets:
    PRECONDITIONS: BMA-22884 Horse Racing - Add bet filter to all horse racing pages
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Home Page is opened
        """
        pass

    def test_002_click_on_horse_racing_icon_in_sports_ribbon(self):
        """
        DESCRIPTION: Click on 'Horse Racing' icon in Sports ribbon
        EXPECTED: 'Horse Racing' landing page is opened
        EXPECTED: 'Bet Filter' link with the corresponding icon is displayed in the sub-header
        """
        pass

    def test_003_click_link_bet_filter(self):
        """
        DESCRIPTION: Click link 'Bet Filter'
        EXPECTED: 'Bet Filter page with all data is loaded
        EXPECTED: url(env/bet-finder)
        """
        pass

    def test_004_click_back_navigation_arrow_next_to_bet_filter_in_subheader(self):
        """
        DESCRIPTION: Click 'Back' navigation arrow next to 'Bet Filter in subheader
        EXPECTED: 'Horse Racing' landing page is opened
        EXPECTED: 'Bet Filter' link with the corresponding icon is displayed in the sub-header
        """
        pass

    def test_005_repeat_steps_3_4_with_selected_tabs_featured_antepost_specials_yourcall(self):
        """
        DESCRIPTION: Repeat steps #3-4 with selected Tabs Featured, Antepost, Specials, YourCall
        EXPECTED: 
        """
        pass

    def test_006_open_horse_racing_event_detail_page(self):
        """
        DESCRIPTION: Open Horse Racing event detail page
        EXPECTED: Event Detail Page is opened
        EXPECTED: 'Bet Filter' link with the corresponding icon is displayed in the sub-header
        """
        pass

    def test_007_click_link_bet_filter(self):
        """
        DESCRIPTION: Click link 'Bet Filter'
        EXPECTED: 'Bet Filter page with all data is loaded
        EXPECTED: url(env/bet-finder)
        """
        pass

    def test_008_click_back_navigation_arrow_next_to_bet_filter_in_subheader(self):
        """
        DESCRIPTION: Click 'Back' navigation arrow next to 'Bet Filter in subheader
        EXPECTED: Event Detail Page is opened
        EXPECTED: 'Bet Filter' link with corresponding icon is displayed
        """
        pass

    def test_009_repeat_steps_7_8_with_selected_race_time_meeting_markets(self):
        """
        DESCRIPTION: Repeat steps #7-8 with selected Race Time, Meeting, Markets
        EXPECTED: 
        """
        pass
