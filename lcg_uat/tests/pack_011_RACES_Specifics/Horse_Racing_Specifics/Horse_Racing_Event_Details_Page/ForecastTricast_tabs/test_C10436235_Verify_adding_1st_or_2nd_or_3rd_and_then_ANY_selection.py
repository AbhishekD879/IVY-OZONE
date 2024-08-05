import pytest
from tests.base_test import vtest
from time import sleep
from voltron.environments import constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from selenium.common.exceptions import StaleElementReferenceException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create HR event on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C10436235_Verify_adding_1st_or_2nd_or_3rd_and_then_ANY_selection(BaseRacing):
    """
    TR_ID: C10436235
    NAME: Verify adding 1st or 2nd or 3rd and then ANY selection
    DESCRIPTION: This test case verifies adding 1st or 2nd or 3rd and then ANY selection
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
        DESCRIPTION: TST2/STG2: Create racing event with Tricast/Forecast
        PRECONDITIONS: 1. HR event exists with Win/Each Way market exists.
        PRECONDITIONS: 2. Tricast checkbox is active on Win/Each Way market for this event
        PRECONDITIONS: 3. User should have a Horse Racing event detail page open ("Tricast" tab)
        PRECONDITIONS: * Navigate to HR landing page
        PRECONDITIONS: * Choose the particular event from the 'Race Grid'
        PRECONDITIONS: * Select 'Tricast' tab
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=4,
                                                          forecast_available=True,
                                                          tricast_available=True)
        eventID = event_params.event_id
        self.navigate_to_edp(event_id=eventID, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails', timeout=20)
        self.__class__.racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        tab_name = vec.racing.RACING_EDP_TRICAST_MARKET_TAB
        self.racing_event_tab_content.market_tabs_list.open_tab(tab_name)
        sleep(2)
        sections = self.racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        self.assertIn(tab_name, sections,
                      msg=f'"{tab_name}" not found in the list of tabs {list(sections.keys())}')

    def test_001_click_1st_or_2nd_or_3rd_selection_button_on_any_runner(self):
        """
        DESCRIPTION: Click 1st (or 2nd or 3rd) selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * Not selected buttons for this runner become disabled
        EXPECTED: * All other 1st (or 2nd or 3rd) buttons for all other runners become disabled
        EXPECTED: * ANY buttons for all other runners remain enabled
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
            self._logger.debug(f'*** Horse racing sport content refreshed: "{e}"')

    def test_002_click_any_selection_button_for_any_other_racer(self):
        """
        DESCRIPTION: Click ANY selection button for any other racer
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * Previously selected button becomes deselected and disabled
        EXPECTED: * ALL 1st, 2nd and 3rd buttons become disabled
        EXPECTED: * ALL ANY buttons become enabled
        EXPECTED: * Add to Betslip button still disabled
        """
        self.get_runner_bet_button()
        outcome_name, outcome = list(self.outcomes.items())[1]
        runner_buttons = outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[3]
        runner_bet_button.click()
        sleep(2)
        try:
            self.assertTrue(list(outcome.items_as_ordered_dict.values())[3].is_selected(),
                            msg=f'1st Button is not selected for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[2].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{outcome_name}"')
            for outcome_name, outcome in list(self.outcomes.items())[2:]:
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                                 msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
                self.assertTrue(list(outcome.items_as_ordered_dict.values())[3].is_enabled(),
                                msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
            self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                             msg='Add To Betslip is enabled')
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Horse racing sport content refreshed: "{e}"')

    def test_003_click_any_buttons_for_2_more_runners(self):
        """
        DESCRIPTION: Click ANY buttons for 2 more runners
        EXPECTED: * Selected buttons is highlighted green
        EXPECTED: * ALL other butons become disabled
        EXPECTED: * Add to Betslip button becomes enabled
        """
        self.get_runner_bet_button()
        outcome_name, outcome = list(self.outcomes.items())[2]
        runner_buttons = outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[3]
        runner_bet_button.click()
        sleep(2)
        try:
            self.assertTrue(list(outcome.items_as_ordered_dict.values())[3].is_selected(),
                            msg=f'1st Button is not selected for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[2].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{outcome_name}"')
            for outcome_name, outcome in list(self.outcomes.items())[2:]:
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                                 msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
                self.assertTrue(list(outcome.items_as_ordered_dict.values())[3].is_enabled(),
                                msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
            self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                             msg='Add To Betslip is enabled')
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Horse racing sport content refreshed: "{e}"')

        self.get_runner_bet_button()
        outcome_name, outcome = list(self.outcomes.items())[3]
        runner_buttons = outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[3]
        runner_bet_button.click()
        sleep(2)
        try:
            self.assertTrue(list(outcome.items_as_ordered_dict.values())[3].is_selected(),
                            msg=f'1st Button is not selected for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[2].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{outcome_name}"')
            for outcome_name, outcome in list(self.outcomes.items())[2:]:
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                                 msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
                self.assertTrue(list(outcome.items_as_ordered_dict.values())[3].is_enabled(),
                                msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
            self.assertTrue(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                            msg='Add To Betslip is enabled')
        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Horse racing sport content refreshed: "{e}"')
