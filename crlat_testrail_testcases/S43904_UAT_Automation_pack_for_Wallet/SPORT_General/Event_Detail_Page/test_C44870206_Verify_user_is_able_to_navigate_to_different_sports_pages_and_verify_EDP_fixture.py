import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870206_Verify_user_is_able_to_navigate_to_different_sports_pages_and_verify_EDP_fixture(Common):
    """
    TR_ID: C44870206
    NAME: "Verify  user is able to navigate to different sports pages and verify EDP fixture
    DESCRIPTION: "Verify that for different sports pages, user is able to navigate to EDP.
    DESCRIPTION: User is displayed with tabs that order markets upon features, depending on sport specific.
    DESCRIPTION: Generally first tabs are All Markets, Main Markets,
    DESCRIPTION: Under each tab, the markets are listed as headers and selection expand on tap, displaying data and odds as per market specific design.
    DESCRIPTION: User is able to switch between markets and navigate forward and backward, in a smooth journey, and pages functionality works fine
    DESCRIPTION: "
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Launch https://beta-sports.coral.co.uk/
        EXPECTED: Home page is opened
        """
        pass

    def test_002_verify_that_for_football_sports_page_user_is_able_to_navigate_to_edp(self):
        """
        DESCRIPTION: Verify that for football sports page, user is able to navigate to EDP.
        EXPECTED: Navigated successfully
        """
        pass

    def test_003_verify_user_is_displayed_with_tabs_that_order_markets_upon_features_depending_on_sport_specificgenerally_first_tabs_are_all_markets_main_markets(self):
        """
        DESCRIPTION: Verify User is displayed with tabs that order markets upon features, depending on sport specific.
        DESCRIPTION: Generally first tabs are All Markets, Main Markets
        EXPECTED: Other markets tabs are displayed
        EXPECTED: All markets tab is highlighted
        """
        pass

    def test_004_under_each_tab_the_markets_are_listed_as_headers_and_selection_expand_on_tap_displaying_data_and_odds_as_per_market_specific_design(self):
        """
        DESCRIPTION: Under each tab, the markets are listed as headers and selection expand on tap, displaying data and odds as per market specific design.
        EXPECTED: Specific markets are displayed for specific market tabs
        """
        pass

    def test_005_user_is_able_to_switch_between_markets_and_navigate_forward_and_backward_in_a_smooth_journey_and_pages_functionality_works_fine(self):
        """
        DESCRIPTION: User is able to switch between markets and navigate forward and backward, in a smooth journey, and pages functionality works fine
        EXPECTED: navigated successfully
        """
        pass

    def test_006_verify_that_for_horse_racing_tennis_user_is_able_to_navigate_to_edp_from_a_z_menu(self):
        """
        DESCRIPTION: Verify that for horse racing/ tennis, user is able to navigate to EDP from A-Z menu
        EXPECTED: Navigated successfully to the respective pages.
        """
        pass
