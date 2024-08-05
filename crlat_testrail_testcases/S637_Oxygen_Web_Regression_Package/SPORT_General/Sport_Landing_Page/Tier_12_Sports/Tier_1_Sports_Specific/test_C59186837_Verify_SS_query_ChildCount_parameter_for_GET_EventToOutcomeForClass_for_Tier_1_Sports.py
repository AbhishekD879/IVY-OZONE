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
class Test_C59186837_Verify_SS_query_ChildCount_parameter_for_GET_EventToOutcomeForClass_for_Tier_1_Sports(Common):
    """
    TR_ID: C59186837
    NAME: Verify SS query 'ChildCount' parameter for GET/EventToOutcomeForClass for Tier 1 Sports
    DESCRIPTION: This test case verifies 'ChildCount' parameter for GET/EventToOutcomeForClass for Tier 1 and Tier 2 sports on Matches(Mobile) and Today/Tomorrow/Future subtabs(Desktop)
    PRECONDITIONS: 1. https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs - list of Tier 1 sports.
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 1 (Tennis, Basketball)
    PRECONDITIONS: 3. Go to Dev Tools > Network > enter 'simpleFilter' in search field > EventToOutcomeForClass.
    """
    keep_browser_open = True

    def test_001_go_to_football_landing_page(self):
        """
        DESCRIPTION: Go to Football landing page
        EXPECTED: The landing page is open
        """
        pass

    def test_002_open_dev_tools_details_in_preconditions_and_check_eventtomarketforclass_requests(self):
        """
        DESCRIPTION: Open Dev Tools (details in preconditions) and check EventToMarketForClass requests
        EXPECTED: request to SS /EventToOutcomeForClass on sport landing page has query parameter:
        EXPECTED: **ChildCount** under 'children'
        EXPECTED: With such attributes:
        EXPECTED: childRecordType: "market"
        EXPECTED: count: 'amount of markets'
        EXPECTED: id: 'child id'
        EXPECTED: refRecordId: 'event id'
        EXPECTED: refRecordType: "event"
        EXPECTED: request to SS /EventToMarketForClass on sport landing page is **NOT** received
        """
        pass

    def test_003_repeat_step_2_for_tier_1_sport_tennis_basketball(self):
        """
        DESCRIPTION: Repeat step 2 for Tier 1 sport (Tennis, Basketball)
        EXPECTED: request to SS /EventToOutcomeForClass on sport landing page has query parameter:
        EXPECTED: **ChildCount** under 'children'
        EXPECTED: With such attributes:
        EXPECTED: childRecordType: "market"
        EXPECTED: count: 'amount of markets'
        EXPECTED: id: 'child id'
        EXPECTED: refRecordId: 'event id'
        EXPECTED: refRecordType: "event"
        EXPECTED: request to SS /EventToMarketForClass on sport landing page is **NOT** received
        """
        pass
