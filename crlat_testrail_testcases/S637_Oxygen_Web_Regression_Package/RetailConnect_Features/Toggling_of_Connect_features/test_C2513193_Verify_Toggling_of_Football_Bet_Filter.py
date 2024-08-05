import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2513193_Verify_Toggling_of_Football_Bet_Filter(Common):
    """
    TR_ID: C2513193
    NAME: Verify Toggling of Football Bet Filter
    DESCRIPTION: This test case verify that Football Bet Filter feature can be switched on/off in CMS
    DESCRIPTION: CMS -> System configuration -> Connect -> football Filter
    PRECONDITIONS: 1. Load CMS and make sure Football Bet Filter feature is turned off: System configuration -> Connect -> football Filter = false (the rest of Connect features are turned on)
    PRECONDITIONS: 2. Load SportBook App
    PRECONDITIONS: 3. Log in
    """
    keep_browser_open = True

    def test_001__go_to_football__coupons_tab(self):
        """
        DESCRIPTION: * Go to Football > 'Coupons' tab
        EXPECTED: 'Coupons' tab is loaded
        """
        pass

    def test_002__select_any_coupon_that_contains_events_with_match_result_market_in_console_search_coupon___find_coupons_with_couponsortcode_mr_verify_the_presence_of_bet_filter_link(self):
        """
        DESCRIPTION: * Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR">)
        DESCRIPTION: * Verify the presence of 'Bet Filter' link
        EXPECTED: * Coupons details page is opened
        EXPECTED: * 'Bet filter' link is absent
        """
        pass

    def test_003_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_004__from_the_header_ribbon_select_all_sports_verify_connect_section_at_the_bottom(self):
        """
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * 'Football Bet Filter' item is absent  in 'Connect' section
        """
        pass

    def test_005_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_006__from_the_header_ribbon_select_connect_verify_the_list_of_connect_features(self):
        """
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify the list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * 'Football Bet Filter' item is absent
        """
        pass

    def test_007_verify_navigation_to_football_bet_filter_by_direct_linkhttpscoralcoukbet_filterfiltersyourteams(self):
        """
        DESCRIPTION: Verify navigation to Football Bet Filter by direct link
        DESCRIPTION: https://****.coral.co.uk/bet-filter/filters/yourTeams
        EXPECTED: Home page is loaded instead
        """
        pass

    def test_008__load_cms_turn_football_filter_feature_on_reload_sportbook_app(self):
        """
        DESCRIPTION: * Load CMS
        DESCRIPTION: * Turn 'football Filter' feature on
        DESCRIPTION: * Reload SportBook App
        EXPECTED: 
        """
        pass

    def test_009_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_010__go_to_football__coupons_tab(self):
        """
        DESCRIPTION: * Go to Football > 'Coupons' tab
        EXPECTED: 'Coupons' tab is loaded
        """
        pass

    def test_011__select_any_coupon_that_contains_events_with_match_result_market_in_console_search_coupon___find_coupons_with_couponsortcode_mr_verify_presence_of_bet_filter_link(self):
        """
        DESCRIPTION: * Select any coupon that contains events with 'Match result' market (In Console: search 'coupon' - find coupons with couponSortCode: "MR">)
        DESCRIPTION: * Verify presence of 'Bet Filter' link
        EXPECTED: 'Bet Filter' link is present
        """
        pass

    def test_012_tap_bet_filter_link(self):
        """
        DESCRIPTION: Tap 'Bet Filter' link
        EXPECTED: Football Bet Filter page is opened
        """
        pass

    def test_013_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_014__from_the_header_ribbon_select_all_sports_verify_connect_section_at_the_bottom(self):
        """
        DESCRIPTION: * From the header ribbon select 'All sports'
        DESCRIPTION: * Verify 'Connect' section at the bottom
        EXPECTED: * 'All sports' page is loaded
        EXPECTED: * 'Football Bet Filter' item is present  in 'Connect' section
        """
        pass

    def test_015_tap_football_bet_filter_item(self):
        """
        DESCRIPTION: Tap 'Football Bet Filter' item
        EXPECTED: * Football Bet Filter page is opened
        """
        pass

    def test_016_tap_football_bet_filter_item(self):
        """
        DESCRIPTION: Tap 'Football Bet Filter' item
        EXPECTED: * Football Bet Filter page is opened
        """
        pass

    def test_017_navigate_to_the_homepage(self):
        """
        DESCRIPTION: Navigate to the homepage
        EXPECTED: Home page is opened
        """
        pass

    def test_018__from_the_header_ribbon_select_connect_verify_the_list_of_connect_features(self):
        """
        DESCRIPTION: * From the header ribbon select 'Connect'
        DESCRIPTION: * Verify the list of Connect features
        EXPECTED: * Connect Landing page is opened
        EXPECTED: * 'Football Bet Filter' item is present
        """
        pass

    def test_019_only_for_coral_for_nowtap_football_bet_filter_item(self):
        """
        DESCRIPTION: **only for Coral for now**
        DESCRIPTION: Tap 'Football Bet Filter' item
        EXPECTED: * Football Bet Filter page is opened
        """
        pass
