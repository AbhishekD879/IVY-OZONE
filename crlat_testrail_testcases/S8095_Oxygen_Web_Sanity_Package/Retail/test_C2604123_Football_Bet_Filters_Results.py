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
class Test_C2604123_Football_Bet_Filters_Results(Common):
    """
    TR_ID: C2604123
    NAME: Football Bet Filters Results
    DESCRIPTION: This test case verifies saving filter results from Football Filter
    PRECONDITIONS: following API returns events for applying Football filters on (After navigating to Football Filter search in console: retailCoupon):
    PRECONDITIONS: **Important. This Api can return prod events only, so test case need to be tested on env. with prod endpoints**
    PRECONDITIONS: Online betting:
    PRECONDITIONS: https://api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LAD0cc93c420eeb433aaf57a1ca299ed93c
    PRECONDITIONS: In-Shop betting:
    PRECONDITIONS: https://api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADe196db0611e240d7a8ea3fc67135c37c
    PRECONDITIONS: for old test environment:
    PRECONDITIONS: Online betting:
    PRECONDITIONS: https://sandbox-api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADb3b4313883004240a754070676e25258
    PRECONDITIONS: In-Shop betting:
    PRECONDITIONS: https://sandbox-api.ladbrokes.com/v2/sportsbook-api/retailCoupon?locale=en-GB&api-key=LADee73ca08b7e84aad8954e5c955e1dba8
    PRECONDITIONS: 1. Load SportBook App
    """
    keep_browser_open = True

    def test_001_select_connect_from_header_sports_ribbon_coral_only(self):
        """
        DESCRIPTION: Select 'Connect' from header sports ribbon (Coral Only)
        EXPECTED: Coupon landing page is opened
        """
        pass

    def test_002_tap_football_bet_filter_coral_only(self):
        """
        DESCRIPTION: Tap Football Bet Filter (Coral Only)
        EXPECTED: * No pop-up appears
        EXPECTED: * A user is on bet filter page for in-shop betting
        """
        pass

    def test_003_apply_several_filters_and_tap_find_bets_button_coral_only(self):
        """
        DESCRIPTION: Apply several filters and tap 'Find Bets' button (Coral Only)
        EXPECTED: * The results page is opened
        EXPECTED: * Selections that corresponds to selected filters are shown
        """
        pass

    def test_004_check_off_a_few_selections_and_tap_shop_locator_button_coral_only(self):
        """
        DESCRIPTION: Check off a few selections and tap 'SHOP LOCATOR' button (Coral Only)
        EXPECTED: Shops map is loaded
        """
        pass

    def test_005_go_football_page___select_coupons_tab_accumulatorsaccas___select_specific_match_betting_market_couponcontains_events_with_match_result_market_that_means_that_couponsortcod_mr_is_retrieved_from_backoffice_the_way_to_check_it_open_dev_tool___network___link_on_the_coupon___preview__ssresponce___children___coupon___couponsortcodemr(self):
        """
        DESCRIPTION: Go Football page -> select Coupons tab (Accumulators/ACCAS) -> select specific match betting market Coupon
        DESCRIPTION: (contains events with 'Match result' market, that means that couponSortCod: 'MR' is retrieved from backoffice. The way to check it: open dev tool -> Network -> link on the coupon -> Preview ->SSResponce -> Children -> Coupon -> couponSortCode:"MR")
        EXPECTED: * A user is on coupon details page
        EXPECTED: * There is 'Bet Filter' link opposite to 'Coupons' back button
        """
        pass

    def test_006_tap_on_bet_filter_link(self):
        """
        DESCRIPTION: Tap on 'Bet Filter' link
        EXPECTED: * No pop-up appears
        EXPECTED: * A user is on bet filter page for online betting
        """
        pass

    def test_007_tap_find_bets_button_and_verify_filter_is_applied_only_on_the_events_of_selected_coupon(self):
        """
        DESCRIPTION: Tap 'Find bets' button and verify filter is applied only on the events of selected coupon
        EXPECTED: * Evens results list is displayed
        EXPECTED: * All events belong to the selected coupon
        """
        pass

    def test_008_get_back_to_coupons_tab___select_specific_not_match_betting_market_coupondoes_not_contains_events_with_match_result_market_that_means_that_couponsortcod____is_retrieved_from_backoffice(self):
        """
        DESCRIPTION: Get back to Coupons tab -> select specific, NOT match betting market, Coupon
        DESCRIPTION: (does not contains events with 'Match result' market, that means that couponSortCod: '--' is retrieved from backoffice)
        EXPECTED: * A user is on coupon details page
        EXPECTED: * 'Bet Filter' link is absent
        """
        pass
