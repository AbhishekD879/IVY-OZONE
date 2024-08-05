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
class Test_C44870316_Verify_Coupon_Detail_Page_and_fixture_on_header(Common):
    """
    TR_ID: C44870316
    NAME: "Verify  Coupon Detail Page and fixture on header"
    DESCRIPTION: -Verify below on the Coupon Detail Page
    DESCRIPTION: -Verifies Fixture Header on Coupon Details page
    PRECONDITIONS: Load Oxygen application - Homepage is opened
    """
    keep_browser_open = True

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        pass

    def test_002_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: 'Coupons' tab is selected and highlighted
        EXPECTED: Coupons Landing page is loaded
        """
        pass

    def test_003_navigate_to_coupon_details_page(self):
        """
        DESCRIPTION: Navigate to Coupon Details page
        EXPECTED: Coupon Details page is loaded
        """
        pass

    def test_004_verify_coupons_header(self):
        """
        DESCRIPTION: Verify Coupons header
        EXPECTED: The following elements are present on Coupons header:
        EXPECTED: * 'Back' button
        EXPECTED: * 'Coupons' inscription
        """
        pass

    def test_005_verify_coupons_sub_header(self):
        """
        DESCRIPTION: Verify Coupons sub-header
        EXPECTED: Coupons sub-header is located below Coupons header
        EXPECTED: "Name of selected coupon" is displayed at the left side of Coupons sub-header
        """
        pass

    def test_006_verify_coupons_page_content(self):
        """
        DESCRIPTION: Verify Coupons page content
        EXPECTED: Events for appropriate coupon are displayed on Coupons Details page
        EXPECTED: First **three** accordions are expanded by default
        EXPECTED: The remaining sections are collapsed by default
        EXPECTED: It is possible to collapse/expand all of the accordions by tapping the accordion's header
        EXPECTED: If no events to show, the message '**No events found**' is displayed
        """
        pass

    def test_007_select_match_results_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Match Results' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Draw
        EXPECTED: -Away
        """
        pass

    def test_008_select_both_teams_to_score_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Both Teams to Score' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Yes
        EXPECTED: -No
        """
        pass

    def test_009_select_total_goals_over_under_152535_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Total Goals Over/ Under 1.5/2.5/3.5' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Over
        EXPECTED: -Under
        """
        pass

    def test_010_select_match_result__both_teams_to_score_in_the_market_selector_drop_down_and_verify_values_on_fixture_headerexpected_result(self):
        """
        DESCRIPTION: Select 'Match Result & Both Teams to Score' in the Market selector drop down and verify values on Fixture header
        DESCRIPTION: Expected Result
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Draw
        EXPECTED: -Away
        """
        pass

    def test_011_select_draw_no_bet_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Draw No Bet' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Away
        """
        pass

    def test_012_select_1st_half_result_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select '1st Half Result' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Draw
        EXPECTED: -Away
        """
        pass

    def test_013_select_to_win_to_nil_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'To Win to Nil' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Away
        """
        pass

    def test_014_select_goal_in_both_halves_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Goal in Both Halves' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Yes
        EXPECTED: -No
        """
        pass

    def test_015_verify_all_the_markets__in_the_event_detail_page(self):
        """
        DESCRIPTION: Verify all the markets  in the event detail page
        EXPECTED: same markets is displayed on EDP
        """
        pass

    def test_016_verify_single_and_multiple_bet_placement_for_coupons(self):
        """
        DESCRIPTION: Verify single and multiple bet placement for coupons
        EXPECTED: single and multiple bets are placed successfully
        """
        pass

    def test_017_on_mobile_close_the_bet_receipt_and_tap_back_button(self):
        """
        DESCRIPTION: On Mobile close the bet receipt and Tap 'Back' button
        EXPECTED: Coupons Landing page is loaded
        EXPECTED: List of coupons is displayed
        """
        pass
