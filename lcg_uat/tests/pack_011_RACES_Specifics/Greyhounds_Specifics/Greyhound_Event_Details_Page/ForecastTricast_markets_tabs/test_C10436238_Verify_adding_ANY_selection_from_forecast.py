import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from random import choice
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from selenium.common.exceptions import StaleElementReferenceException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C10436238_Verify_adding_ANY_selection_from_forecast(Common):
    """
    TR_ID: C10436238
    NAME: Verify adding ANY selection from forecast for GH
    DESCRIPTION: This test case verifies functionality of adding ANY selection from forecast
    PRECONDITIONS: 1. GH event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Forecast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User is on EDP on this event in app
    """
    keep_browser_open = True

    def get_runner_bet_button(self):
        sections = self.racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        section_name, section = list(sections.items())[0]
        self.__class__.outcomes = section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'No one outcome was found in section: "{section_name}"')

    def test_000_preconditions(self):
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.greyhound_racing_config.category_id
            class_ids = self.get_class_ids_for_category(category_id=category_id)
            events_filter = self.ss_query_builder \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES,
                                                                      OPERATORS.INTERSECTS, 'SF,CF,RF,'))) \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES,
                                                                      OPERATORS.INTERSECTS, 'CT,TC,'))) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))

            ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_ids, brand=self.brand)
            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
            events = [event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')]

            if not events:
                raise SiteServeException(f'Cannot find active Forecast/Tricast Racing events')
            eventID = choice(events)['event']['id']
        else:
            eventID = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=3,
                                                                   forecast_available=True).event_id

        self.navigate_to_edp(event_id=eventID, sport_name='greyhound-racing')
        self.site.wait_content_state('GreyHoundEventDetails', timeout=20)
        self.__class__.racing_event_tab_content = self.site.greyhound_event_details.tab_content.event_markets_list

    def test_001_select_forecast_tab(self):
        """
        DESCRIPTION: Select Forecast tab
        EXPECTED:
        """
        tab_name = vec.racing.RACING_EDP_FORECAST_MARKET_TAB
        self.racing_event_tab_content.market_tabs_list.open_tab(tab_name)
        sleep(2)
        sections = self.racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        self.assertIn(tab_name, sections,
                      msg=f'"{tab_name}" not found in the list of tabs {list(sections.keys())}')
        self.get_runner_bet_button()
        self.__class__.outcome_name, self.__class__.outcome = list(self.outcomes.items())[0]

    def test_002_click_any_selection_button_on_any_runner(self, add_to_betslip=False):
        """
        DESCRIPTION: Click ANY selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * ALL 1st and 2nd buttons become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * 'Add to Betslip' button remains disabled
        """
        runner_buttons = self.outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{self.outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[2]
        runner_bet_button.click()
        self.assertFalse(self.outcome.has_silks, msg=f'Silk icon is displayed for outcome: "{self.outcome_name}"')
        sleep(2)
        try:
            self.assertTrue(list(self.outcome.items_as_ordered_dict.values())[2].is_selected(),
                            msg=f'Any Button is not selected for "{self.outcome_name}"')
            self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{self.outcome_name}"')
            for outcome_name, outcome in list(self.outcomes.items())[1:]:
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                                 msg=f'1st Button is enabled for all the other runners"{outcome_name}"')
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                                 msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
            if add_to_betslip:
                self.assertTrue(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                                msg='Add To Betslip is not displayed')
            else:
                self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(expected_result=False),
                                 msg='Add To Betslip is displayed')

        except StaleElementReferenceException as e:
            self._logger.debug(f'*** GreyHound sport content refreshed: "{e}"')

    def test_003_click_any_selection_button_on_different_runner(self):
        """
        DESCRIPTION: Click ANY selection button on different runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * ALL 1st and 2nd buttons remain disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * 'Add to Betslip' button becomes enabled
        """
        self.get_runner_bet_button()
        self.outcome_name, self.outcome = list(self.outcomes.items())[1]
        self.test_002_click_any_selection_button_on_any_runner(add_to_betslip=True)
