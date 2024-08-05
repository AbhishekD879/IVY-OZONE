import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C1316424_Verify_Scroll_to_top_functionality_for_Desktop(Common):
    """
    TR_ID: C1316424
    NAME: Verify 'Scroll to top' functionality for Desktop
    DESCRIPTION: This test case verifies places/cases where 'Scroll to top' functionality is present/absent.
    DESCRIPTION: Test case to be run on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_navigate_to_any_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to any Sports Landing page
        EXPECTED: Sports Landing page is loaded successfully
        """
        pass

    def test_002_scroll_down_the_page_a_bit_but_making_sure_tabs_below_banner_are_available(self):
        """
        DESCRIPTION: Scroll down the page a bit but making sure tabs below banner are available
        EXPECTED: 
        """
        pass

    def test_003_click_between_tabs(self):
        """
        DESCRIPTION: Click between tabs
        EXPECTED: * Page DOESN'T scroll to top
        EXPECTED: * Respective content is displayed below selected tab
        """
        pass

    def test_004_repeat_steps_2_3_for_tabs_on_the_following_pages_sports_event_details_pages_races_landing_pages_races_event_details_pages_only_market_tabs_virtual_sports_tabs_with_event_time_except_tournaments_deposit_page_bet_slip_international_tote_landing_page_international_tote_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-3 for **tabs** on the following pages:
        DESCRIPTION: * Sports Event Details pages
        DESCRIPTION: * Races Landing pages
        DESCRIPTION: * Races Event Details pages (ONLY Market tabs)
        DESCRIPTION: * Virtual Sports tabs with event time (except 'Tournaments')
        DESCRIPTION: * Deposit page
        DESCRIPTION: * Bet slip
        DESCRIPTION: * International Tote Landing page
        DESCRIPTION: * International Tote Details page
        EXPECTED: * Page DOESN'T scroll to top
        EXPECTED: * Respective content is displayed below selected tab
        """
        pass

    def test_005_repeat_steps_2_3_for_switchers_on_the_following_pages_sports_landing_pages_todaytomorrowfuture_football_competitions_landing_page_populara_z_competitions_details_page_matchesoutrights_races_landing_pages_daily_switchers_lotto_page_virtuals_bet_slip_international_tote_landing_page_international_tote_details_page(self):
        """
        DESCRIPTION: Repeat steps 2-3 for **switchers** on the following pages:
        DESCRIPTION: * Sports Landing pages: Today/Tomorrow/Future;
        DESCRIPTION: * Football Competitions Landing page: Popular/A-Z
        DESCRIPTION: * Competitions Details page: Matches/Outrights
        DESCRIPTION: * Races Landing pages: Daily switchers
        DESCRIPTION: * Lotto page
        DESCRIPTION: * Virtuals
        DESCRIPTION: * Bet slip
        DESCRIPTION: * International Tote Landing page
        DESCRIPTION: * International Tote Details page
        EXPECTED: * Page DOESN'T scroll to top
        EXPECTED: * Respective content is displayed below selected tab
        """
        pass

    def test_006_navigate_to_races_event_details_pages(self):
        """
        DESCRIPTION: Navigate to Races Event Details pages
        EXPECTED: Races Event Details page is loaded successfully
        """
        pass

    def test_007_scroll_down_the_page_a_bit_but_making_sure_tabs_with_time_are_available(self):
        """
        DESCRIPTION: Scroll down the page a bit but making sure tabs with time are available
        EXPECTED: 
        """
        pass

    def test_008_click_between_tabs(self):
        """
        DESCRIPTION: Click between tabs
        EXPECTED: * Page scrolls to the top
        EXPECTED: * Respective content is displayed below selected tab
        """
        pass

    def test_009_repeat_steps_7_8_for_switchers_on_account_history_page_bet_history_transactions_gaming_history(self):
        """
        DESCRIPTION: Repeat steps 7-8 for switchers on Account history page (Bet History, Transactions, Gaming History)
        EXPECTED: * Page scrolls to the top
        EXPECTED: * Respective content is displayed below selected tab
        """
        pass

    def test_010_navigate_to_any_other_page_of_the_application_using_the_left_navigationsports_menuetc(self):
        """
        DESCRIPTION: Navigate to any other page of the application using the left navigation/sports menu/etc.
        EXPECTED: * User is taken to respective page
        EXPECTED: * Reload and scroll to top takes place
        """
        pass
