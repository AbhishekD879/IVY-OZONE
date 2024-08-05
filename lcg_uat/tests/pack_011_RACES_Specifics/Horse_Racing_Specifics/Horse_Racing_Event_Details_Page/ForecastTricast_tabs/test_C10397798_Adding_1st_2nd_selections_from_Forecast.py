import pytest
import tests
from tests.base_test import vtest
from random import choice
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from selenium.common.exceptions import StaleElementReferenceException
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C10397798_Adding_1st_2nd_selections_from_Forecast(BaseRacing):
    """
    TR_ID: C10397798
    NAME: Adding 1st, 2nd selections from Forecast
    DESCRIPTION: This test case verifies functionality of adding and removing 1st, 2nd selections from Forecast
    PRECONDITIONS: 1. HR event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Forecast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User should have a Horse Racing event detail page open ("Forecast" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Forecast' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Forecast" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Forecast are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Forecast' tab
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
            category_id = self.ob_config.horseracing_config.category_id
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
            eventID = self.ob_config.add_UK_racing_event(number_of_runners=3,
                                                         forecast_available=True).event_id
        self.navigate_to_page('horse-racing')
        if self.device_type == 'desktop':
            self.site.horse_racing.tab_content.build_card.build_race_card_button.click()
            self.assertTrue(self.site.horse_racing.tab_content.build_card.exit_builder_button.is_enabled(),
                            msg="'Build a Racecard' button is not replaced by 'Exit Builder'")
        self.navigate_to_edp(event_id=eventID, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails', timeout=20)
        self.__class__.racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        tab_name = vec.racing.RACING_EDP_FORECAST_MARKET_TAB
        self.racing_event_tab_content.market_tabs_list.open_tab(tab_name)
        sleep(2)
        sections = self.racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        self.assertIn(tab_name, sections,
                      msg=f'"{tab_name}" not found in the list of tabs {list(sections.keys())}')
        self.get_runner_bet_button()
        self.__class__.outcome_name, self.__class__.outcome = list(self.outcomes.items())[0]

    def test_001_click_1st_selection_button_on_any_runner(self, button_number=0, add_to_betslip=False):
        """
        DESCRIPTION: Click 1st selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * 2nd and ANY button for this runner become disabled
        EXPECTED: * All other 1st buttons for all other runners become disabled
        EXPECTED: * Add to Betslip button still disabled
        """
        runner_buttons = self.outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{self.outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[button_number]
        runner_bet_button.click()
        sleep(1)
        try:
            if button_number == 0:
                self.assertTrue(list(self.outcome.items_as_ordered_dict.values())[0].is_selected(),
                                msg=f'1st Button is not selected for "{self.outcome_name}"')
                self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                                 msg=f'2nd Button is enabled for "{self.outcome_name}"')
                for outcome_name, outcome in list(self.outcomes.items())[1:]:
                    self.assertFalse(
                        list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                        msg=f'1st Button is enabled for all the other runners"{outcome_name}"')
            else:
                for outcome_name, outcome in list(self.outcomes.items())[3:]:
                    self.assertTrue(
                        list(outcome.items_as_ordered_dict.values())[2].is_enabled(),
                        msg=f'Any Button is Disabled for"{outcome_name}"')
                self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                                 msg=f'1st Button is enabled for "{self.outcome_name}"')

            self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[2].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{self.outcome_name}"')

            if add_to_betslip:
                self.assertTrue(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                                msg='Add To Betslip is not displayed')
            else:
                self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(expected_result=False),
                                 msg='Add To Betslip is displayed')

        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Horse Racing sport content refreshed: "{e}"')

    def test_002_click_2nd_selection_button_on_a_different_runner(self):
        """
        DESCRIPTION: Click 2nd selection button on a different runner
        EXPECTED: * Selected button is highlighted green. Previously selected button remains green and selected
        EXPECTED: * 1st and ANY button for this runner become disabled
        EXPECTED: * All other 2nd buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button becomes enabled
        """
        self.get_runner_bet_button()
        self.outcome_name, self.outcome = list(self.outcomes.items())[1]
        self.test_001_click_1st_selection_button_on_any_runner(button_number=1, add_to_betslip=True)