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
class Test_C59539231_Verify_SS_query_ChildCount_parameter_for_GET_CouponToOutcomeForCoupon(Common):
    """
    TR_ID: C59539231
    NAME: Verify SS query 'ChildCount' parameter for GET/CouponToOutcomeForCoupon
    DESCRIPTION: This test case verifies the 'ChildCount' parameter for GET/CouponToOutcomeForCoupon and the correct amount of markets displayed for each event on the coupon details page in the '+<number of available markets> Market' link.
    PRECONDITIONS: 1. Go to the sports landing page
    PRECONDITIONS: 2. Open Coupon tab (ACCA)
    """
    keep_browser_open = True

    def test_001_open_any_coupon_details_page(self):
        """
        DESCRIPTION: Open any coupon details page
        EXPECTED: Events are displayed
        """
        pass

    def test_002_open_dev_tools_details_in_preconditions_and_check_coupontooutcomeforcoupon_requests(self):
        """
        DESCRIPTION: Open Dev Tools (details in preconditions) and check CouponToOutcomeForCoupon requests
        EXPECTED: request to SS /CouponToOutcomeForCoupon has query parameter:
        EXPECTED: ChildCount
        EXPECTED: With such attributes:
        EXPECTED: childRecordType: "market"
        EXPECTED: count: 'amount of markets'
        EXPECTED: id: 'child id'
        EXPECTED: refRecordId: 'event id'
        EXPECTED: refRecordType: "event"
        EXPECTED: request to SS /EventToMarketForEvent is NOT received
        """
        pass

    def test_003_compare_the_number_of_markets_in_the_childcount_parameter_and_the_number_of_markets_in_the_link_for_each_event(self):
        """
        DESCRIPTION: Compare the number of markets in the ChildCount parameter and the number of markets in the link for each event
        EXPECTED: The number of markets - 1 is displayed for each event in the '+<number of available markets> Market' link
        """
        pass

    def test_004_tapclick_plusnumber_of_available_markets_markets_link(self):
        """
        DESCRIPTION: Tap/click '+<number of available markets>' Markets link
        EXPECTED: '+<number of available markets> Market' link leads to the Event Details page
        """
        pass

    def test_005_verify_plusnumber_of_available_markets_market_link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Verify '+<number of available markets> Market' link for event with ONLY one market
        EXPECTED: '+<number of available markets> Market' link is not shown on the Event section
        """
        pass
