import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C493191_Verify_Fixture_Header_on_Coupon_Details_page(Common):
    """
    TR_ID: C493191
    NAME: Verify Fixture Header on Coupon Details page
    DESCRIPTION: This test case verifies Fixture Header on Coupon Details page
    PRECONDITIONS: **CMS Configuration:**
    PRECONDITIONS: Football Coupon ->Coupon Segments -> Create New Segment -> Featured coupon section
    PRECONDITIONS: NOTE:  **Popular coupon** section contains all the rest of available coupons EXCEPT coupons are present in *Featured section*
    PRECONDITIONS: 1) In order to get a list of coupons use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon?existsFilter=coupon:simpleFilter:event.startTime:greaterThanOrEqual:2017-07-04T21:00:00.000Z&existsFilter=coupon:simpleFilter:event.suspendAtTime:greaterThan:2017-07-05T13:09:30.000Z&existsFilter=coupon:simpleFilter:event.isStarted:isFalse&simpleFilter=coupon.siteChannels:contains:M&existsFilter=coupon:simpleFilter:event.categoryId:intersects:16&existsFilter=coupon:simpleFilter:event.cashoutAvail:equals:Y&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: Load Oxygen application - Homepage is opened
    PRECONDITIONS: **COUPONS** for Coral (CMS configurable)
    PRECONDITIONS: **ACCAS** for Ladbrokes (CMS configurable)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_and_navigate_to_football_coupon_details_page(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Football Coupon Details page
        EXPECTED: * Coupon Details page is loaded
        EXPECTED: * Events for appropriate coupon are displayed on Coupons Details page
        """
        pass

    def test_002_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the 'Market selector' drop down
        EXPECTED: * The ‘Market Selector’ displayed below the Coupon sub-header and above the First accordion on the page
        EXPECTED: * 'Match Result' is selected by default in 'Market selector' drop down
        EXPECTED: * "Market:" is shown in front of <market name> ( **CORAL** ) / <Market name> and 'Change' text with arrow ( **LADBROKES** )
        EXPECTED: *  Market selector is not shown on Goalscorer details page
        """
        pass

    def test_003_select_match_results_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Match Results' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Draw
        EXPECTED: -Away
        """
        pass

    def test_004_select_both_teams_to_score_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Both Teams to Score' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Yes
        EXPECTED: -No
        """
        pass

    def test_005_select_total_goals_over_under_152535_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Total Goals Over/ Under 1.5/2.5/3.5' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Over
        EXPECTED: -Under
        """
        pass

    def test_006_select_match_result_and_both_teams_to_score_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Match Result and Both Teams To Score' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Draw
        EXPECTED: -Away
        """
        pass

    def test_007_select_draw_no_bet_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Draw No Bet' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Away
        """
        pass

    def test_008_select_1st_half_result_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select '1st Half Result' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Draw
        EXPECTED: -Away
        """
        pass

    def test_009_select_to_win_to_nil_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'To Win to Nil' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Away
        """
        pass

    def test_010_select_goal_in_both_halves_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Goal in Both Halves' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Yes
        EXPECTED: -No
        """
        pass
