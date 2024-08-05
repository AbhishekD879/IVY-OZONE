import pytest
import tests
from json import JSONDecodeError
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@vtest
class Test_C26832986_Verify_SS_query_eventstartTime_parameters_for_GET_EventToOutcomeForClass_for_Tier_1_Sports(Common):
    """
    TR_ID: C26832986
    NAME: Verify SS query 'event.startTime' parameters for GET/EventToOutcomeForClass for Tier 1 Sports
    DESCRIPTION: This test case verifies 'event.startTime' parameters for GET/EventToOutcomeForClass for Tier 1 sports on Matches(Mobile) and Today/Tomorrow/Future tabs(Desktop)
    PRECONDITIONS: 1. https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs - list of Tier 1 and Tier 2 sports.
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 1 (Tennis, Basketball)
    PRECONDITIONS: 3. Go to Dev Tools > Network > enter 'simpleFilter' in search field > EventToOutcomeForClass.
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def test_000_preconditions(self):
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_premier_league_football_event()
            self.ob_config.add_tennis_event_to_autotest_trophy()

    def get_response_url(self, url):
        """
        :param url: Required URl
        :return: Complete url
        """
        perflog = self.device.get_performance_log()
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_001_go_to_football_landing_page(self):
        """
        DESCRIPTION: Go to Football landing page
        EXPECTED: The landing page is open
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='football')

    def test_002_open_dev_tools_details_in_preconditions_and_check_eventtomarketforclass_requests(self, sport='football'):
        """
        DESCRIPTION: Open Dev Tools (details in preconditions) and check EventToMarketForClass requests
        EXPECTED: * request to SS /EventToOutcomeForClass on sport landing page has query parameters: simpleFilter=event.event.startTime:greaterThanOrEqual:timeOfDayAfterTomorrowIn00:00:00Z and simpleFilter=event.startTime:lessThan with date, which is Current Time + 48h
        EXPECTED: * request to SS /EventToMarketForClass on sport landing page is NOT received
        """
        event_to_outcome_response = self.get_response_url('/EventToOutcomeForClass')
        if not event_to_outcome_response:
            raise SiteServeException(f'No event data available for sport "{sport}"')
        else:
            self.assertIn('simpleFilter=event.startTime:greaterThanOrEqual:', event_to_outcome_response,
                          msg=f'Expected: "simpleFilter=event.startTime:greaterThanOrEqual" is not present in Actual: "{event_to_outcome_response}"')
            self.assertIn('simpleFilter=event.startTime:lessThan', event_to_outcome_response,
                          msg=f'Expected: "simpleFilter=event.startTime:lessThan" is not present in Actual: "{event_to_outcome_response}"')
        event_to_market_response = self.get_response_url('EventToMarketForClass')
        self.assertIsNone(event_to_market_response)

    def test_003_repeat_step_2_for_tier_1_sport(self):
        """
        DESCRIPTION: Repeat step 2 for Tier 1 sport
        EXPECTED: * request to SS /EventToOutcomeForClass on sport landing page has query parameters: simpleFilter=event.event.startTime:greaterThanOrEqual:timeOfDayAfterTomorrowIn00:00:00Z and simpleFilter=event.startTime:lessThan with date, which is Current Time + 48h
        EXPECTED: * request to SS /EventToMarketForClass on sport landing page is NOT received
        """
        self.navigate_to_page('sport/tennis')
        self.site.wait_content_state(state_name='tennis')
        self.test_002_open_dev_tools_details_in_preconditions_and_check_eventtomarketforclass_requests(sport='tennis')
