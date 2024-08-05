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
class Test_C60004593_Verify_ChildCount_parameter_for_GET_EventToOutcomeForEvent_on_Football_Coupon_Details_page_when_FeatureToggle_FootballCoupons_is_enabled_in_CMS(Common):
    """
    TR_ID: C60004593
    NAME: Verify  'ChildCount' parameter for GET/EventToOutcomeForEvent on Football Coupon Details page when FeatureToggle->FootballCoupons is enabled in CMS
    DESCRIPTION: This test case verifies the 'ChildCount' parameter for GET/EventToOutcomeForEvent and the correct amount of markets displayed for each event on the coupon details page in the '+<number of available markets> Market' link in case FeatureToggle->FootballCoupons is enabled in CMS.
    PRECONDITIONS: 1. In CMS go to System Config and enable FeatureToggle->FootballCoupons
    PRECONDITIONS: 2. Go to the Football landing page
    PRECONDITIONS: 3. Open Coupon tab (ACCA)
    """
    keep_browser_open = True

    def test_001_open_any_coupon_details_page(self):
        """
        DESCRIPTION: Open any coupon details page
        EXPECTED: Events are displayed
        """
        pass

    def test_002_open_dev_tools_details_in_preconditions_and_check_eventtooutcomeforevent_requests(self):
        """
        DESCRIPTION: Open Dev Tools (details in preconditions) and check /EventToOutcomeForEvent requests
        EXPECTED: request to SS /EventToOutcomeForEvent has query parameter:
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
