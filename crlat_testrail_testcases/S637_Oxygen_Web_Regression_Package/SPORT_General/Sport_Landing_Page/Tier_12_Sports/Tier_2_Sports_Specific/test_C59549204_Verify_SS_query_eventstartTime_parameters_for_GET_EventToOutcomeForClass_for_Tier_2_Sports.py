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
class Test_C59549204_Verify_SS_query_eventstartTime_parameters_for_GET_EventToOutcomeForClass_for_Tier_2_Sports(Common):
    """
    TR_ID: C59549204
    NAME: Verify SS query 'event.startTime' parameters for GET/EventToOutcomeForClass for Tier 2 Sports
    DESCRIPTION: This test case verifies 'event.startTime' parameters for GET/EventToOutcomeForClass for Tier 2 sports on Matches(Mobile) and Today/Tomorrow/Future tabs(Desktop)
    PRECONDITIONS: 1. https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs - list of Tier 1 and Tier 2 sports.
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 2 and Tier 2 sport Outright(Golf, Cycling, Hurling, Motorbikes).
    PRECONDITIONS: 3. Go to Dev Tools > Network > enter 'simpleFilter' in search field > EventToOutcomeForClass.
    """
    keep_browser_open = True

    def test_001_navigate_to_to_matchesmobile_todaytomorrowfuturedesktop_tabs_on_any_sport_landing_page_with_tier_2_sport_configuration(self):
        """
        DESCRIPTION: Navigate to to 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs on any Sport Landing page with Tier 2 Sport configuration
        EXPECTED: 
        """
        pass

    def test_002_open_dev_tools_details_in_preconditions_and_check_eventtomarketforclass_requests(self):
        """
        DESCRIPTION: Open Dev Tools (details in preconditions) and check EventToMarketForClass requests
        EXPECTED: * request to SS /EventToOutcomeForClass on sport landing page has query parameters: simpleFilter=event.event.startTime:greaterThanOrEqual:timeOfDayAfterTomorrowIn00:00:00Z and simpleFilter=event.startTime:lessThan with date, which is Current Time + 48h
        EXPECTED: * request to SS /EventToMarketForClass on sport landing page is NOT received
        """
        pass

    def test_003_repeat_step_2_for_tier_2_sports_outrightgolf_cycling_hurling_motorbikes(self):
        """
        DESCRIPTION: Repeat step 2 for Tier 2 sports Outright(Golf, Cycling, Hurling, Motorbikes)
        EXPECTED: * request to SS /EventToOutcomeForClass on sport landing page has query parameters: simpleFilter=event.event.startTime:greaterThanOrEqual:timeOfDayAfterTomorrowIn00:00:00Z and simpleFilter=event.startTime:lessThan with date, which is Current Time + 48h
        EXPECTED: * request to SS /EventToMarketForClass on sport landing page is NOT received
        """
        pass
