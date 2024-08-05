import pytest
import tests
from tests.base_test import vtest
from time import sleep
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from selenium.common.exceptions import StaleElementReferenceException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C10436237_Adding_1st_2nd_selections_from_Forecast_GH(BaseRacing):
    """
    TR_ID: C10436237
    NAME: Adding 1st, 2nd selections from Forecast GH
    DESCRIPTION: This test case verifies functionality of adding and removing 1st, 2nd selections from Forecast
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
        """
        DESCRIPTION: TST2/STG2: Create racing event with Tricast/Forecast, PROD: Find racing event with Tricast/Forecast
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES,
                                                                          OPERATORS.INTERSECTS, 'CF')), \
                exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE,
                                                          OPERATORS.IS_TRUE)),
            event = \
                self.get_active_events_for_category(category_id=self.ob_config.backend.ti.greyhound_racing.category_id,
                                                    additional_filters=additional_filter)[0]
            outcomes = next((market_info['market']['children'] for market_info in event['event']['children'] if
                             'Win or Each Way' == market_info['market']['name']), None)
            selection_ids = {}
            for outcome in outcomes:
                if 'Unnamed' not in outcome['outcome']['name']:
                    selection_ids[outcome['outcome']['name']] = outcome['outcome']['id']
            self.__class__.eventID = event['event']['id']
            self.__class__.selection_names = selection_ids.keys()
        else:
            event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=3,
                                                                        forecast_available=True,
                                                                        tricast_available=True)
            selection_ids = event_params.selection_ids
            self.__class__.eventID = event_params.event_id
            self.__class__.selection_names = selection_ids.keys()
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')
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

    def test_002_click_1st_selection_button_on_any_runner(self):
        """
        DESCRIPTION: Click 1st selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * 2nd and ANY button for this runner become disabled
        EXPECTED: * All other 1st buttons for all other runners become disabled
        EXPECTED: * Add to Betslip button still disabled
        """
        self.get_runner_bet_button()
        outcome_name, outcome = list(self.outcomes.items())[0]
        runner_buttons = outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[0]
        runner_bet_button.click()
        self.assertFalse(outcome.has_silks, msg=f'Silk icon is displayed for outcome: "{outcome_name}"')
        sleep(2)
        try:
            self.assertTrue(list(outcome.items_as_ordered_dict.values())[0].is_selected(),
                            msg=f'1st Button is not selected for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[2].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{outcome_name}"')
            self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(expected_result=False),
                             msg='Add To Betslip is displayed')
            for outcome_name, outcome in list(self.outcomes.items())[1:]:
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                                 msg=f'1st Button is enabled for all the other runners"{outcome_name}"')
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** GreyHound sport content refreshed: "{e}"')

    def test_003_click_2nd_selection_button_on_a_different_runner(self):
        """
        DESCRIPTION: Click 2nd selection button on a different runner
        EXPECTED: * Selected button is highlighted green. Previously selected button remains green and selected
        EXPECTED: * 1st and ANY button for this runner become disabled
        EXPECTED: * All other 2nd buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button becomes enabled
        """
        self.get_runner_bet_button()
        outcome_name, outcome = list(self.outcomes.items())[1]
        runner_buttons = outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[1]
        runner_bet_button.click()
        sleep(2)
        try:
            self.assertTrue(list(outcome.items_as_ordered_dict.values())[1].is_selected(),
                            msg=f'1st Button is not selected for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[2].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{outcome_name}"')
            for outcome_name, outcome in list(self.outcomes.items())[2:]:
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                                 msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
                self.assertTrue(list(outcome.items_as_ordered_dict.values())[2].is_enabled(),
                                msg=f'Any Button is enabled for all the other runners"{outcome_name}"')
            self.assertTrue(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                            msg='Add To Betslip is not enabled')
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** GreyHound sport content refreshed: "{e}"')
