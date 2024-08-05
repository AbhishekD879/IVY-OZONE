import pytest
import tests
import voltron.environments.constants as vec
import re
from tests.base_test import vtest
from tests.Common import Common
from json import JSONDecodeError
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
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
    enable_bs_performance_log = True
    keep_browser_open = True
    coral_tabs_list = [vec.sb.TABS_NAME_TODAY.upper(), vec.sb.TABS_NAME_TOMORROW.upper(), vec.sb.TABS_NAME_FUTURE.upper()]
    lads_tabs_list = [vec.sb.TABS_NAME_TODAY.title(), vec.sb.TABS_NAME_TOMORROW.title(), vec.sb.TABS_NAME_FUTURE.title()]

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
                if re.search(rf'\b{url}\b', request_url):
                    return request_url
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

    def test_001_navigate_to_to_matchesmobile_todaytomorrowfuturedesktop_tabs_on_any_sport_landing_page_with_tier_2_sport_configuration(self):
        """
        DESCRIPTION: Navigate to to 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs on any Sport Landing page with Tier 2 Sport configuration
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.add_autotest_boxing_event()
            self.ob_config.add_volleyball_event_to_austrian_league()
        self.navigate_to_page('sport/volleyball')
        self.site.wait_content_state_changed()
        if self.device_type != 'mobile':
            date_tabs = self.site.sports_page.date_tab.items_names
            self.assertListEqual(date_tabs, self.coral_tabs_list if self.brand == 'bma' else self.lads_tabs_list,
                                 msg=f'Actaul tabs list: "{date_tabs}" is not same as Expected tabs: "{self.coral_tabs_list if self.brand == "bma" else self.lads_tabs_list}"')
        else:
            default_tab = self.site.sports_page.tabs_menu.current
            self.assertIn(default_tab.upper(), [vec.sb.TABS_NAME_MATCHES.upper(), vec.sb.TABS_NAME_COMPETITIONS.upper()],
                          msg=f'Actual default tab: "{default_tab.upper()}" is not present in Expected tabs list: "{[vec.sb.TABS_NAME_MATCHES.upper(), vec.sb.TABS_NAME_COMPETITIONS.upper()]}"')

    def test_002_open_dev_tools_details_in_preconditions_and_check_eventtomarketforclass_requests(self, sport="Volleyball"):
        """
        DESCRIPTION: Open Dev Tools (details in preconditions) and check EventToMarketForClass requests
        EXPECTED: * request to SS /EventToOutcomeForClass on sport landing page has query parameters: simpleFilter=event.event.startTime:greaterThanOrEqual:timeOfDayAfterTomorrowIn00:00:00Z and simpleFilter=event.startTime:lessThan with date, which is Current Time + 48h
        EXPECTED: * request to SS /EventToMarketForClass on sport landing page is NOT received
        """
        event_to_outcome_response = self.get_response_url('EventToOutcomeForClass')
        if event_to_outcome_response:
            self.assertIn(('simpleFilter=event.startTime:greaterThanOrEqual:' or 'simpleFilter=event.event.startTime:greaterThanOrEqual:'), event_to_outcome_response,
                          msg=f'Expected text: "simpleFilter=event.event.startTime:greaterThanOrEqual:" is not found the response: "{event_to_outcome_response}"')
            self.assertIn(('simpleFilter=event.startTime:lessThan' or 'simpleFilter=event.event.startTime:lessThan'), event_to_outcome_response,
                          msg=f'Expected text: "simpleFilter=event.startTime:lessThan:" is not found the response: "{event_to_outcome_response}"')
        else:
            raise SiteServeException(f'No active events found for the sport "{sport}"')
        event_to_market_response = self.get_response_url('EventToMarketForClass')
        self.assertIsNone(event_to_market_response,
                          msg=f'Response for "EventToMarketForClass" should be None instead of "{event_to_market_response}"')

    def test_003_repeat_step_2_for_tier_2_sports_outrightgolf_cycling_hurling_motorbikes(self):
        """
        DESCRIPTION: Repeat step 2 for Tier 2 sports Outright(Golf, Cycling, Hurling, Motorbikes)
        EXPECTED: * request to SS /EventToOutcomeForClass on sport landing page has query parameters: simpleFilter=event.event.startTime:greaterThanOrEqual:timeOfDayAfterTomorrowIn00:00:00Z and simpleFilter=event.startTime:lessThan with date, which is Current Time + 48h
        EXPECTED: * request to SS /EventToMarketForClass on sport landing page is NOT received
        """
        self.navigate_to_page('sport/darts')
        self.site.wait_content_state_changed()
        self.test_002_open_dev_tools_details_in_preconditions_and_check_eventtomarketforclass_requests(sport='Darts')
