import tests
import pytest
import voltron.environments.constants as vec
from random import choice
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.virtual_sports
@vtest
class Test_C16375058_Verify_highlighting_1st_2nd_ANY_selections_from_Forecast(BaseVirtualsTest):
    """
    TR_ID: C16375058
    NAME: Verify highlighting 1st, 2nd, ANY selections from Forecast
    DESCRIPTION: This test case verifies functionality of adding and removing 1st, 2nd and ANY selections from Forecast tab.
    PRECONDITIONS: 1. Forecast market is configured and shown for Virtual Sports such as: Horse Racing, Horse Racing Jumps, Greyhound, Motor Racing and Cycling.
    PRECONDITIONS: Note: Forecast tab should not be shown for such Virtual Sports as: VGN (Virtual Grand Nationals Races), Football, Tennis, Speedway, Boxing, Darts.
    PRECONDITIONS: 2. User is on Virtual Sports page/Forecast tab (this test case should be run for all sports displayed in the previous step where Forecast tab should be displayed).
    PRECONDITIONS: The rules of displaying Virtuals Forecast and Tricast tabs:
    PRECONDITIONS: 1. Tabs are not shown at all if event does not have ncastTypeCodes attribute. Only WinOrEw Market is displayed in this case (UI looks like on current production).
    PRECONDITIONS: 2. All tabs are shown if event has ncastTypeCodes attribute with set CF and CT.
    PRECONDITIONS: 3. Two tabs: Forecast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CF.
    PRECONDITIONS: 4. Two tabs: Tricast and WinOrEw are shown if event has ncastTypeCodes attribute with set only CT.
    PRECONDITIONS: Also we check if market is WinOrEw: ['To Win', 'To-Win', 'Win/EachWay', 'Win or Each Way']
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
        DESCRIPTION: Create/Get events
        """
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

            event_id = choice(events)['event']['id']
        else:
            event_id = self.ob_config.add_UK_racing_event(forecast_available=True).event_id

        self.navigate_to_page('horse-racing')
        if self.device_type == 'desktop':
            self.site.horse_racing.tab_content.build_card.build_race_card_button.click()
            self.assertTrue(self.site.horse_racing.tab_content.build_card.exit_builder_button.is_enabled(),
                            msg="'Build a Racecard' button is not replaced by 'Exit Builder'")
        self.navigate_to_edp(event_id=event_id, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails', timeout=20)
        self.__class__.racing_event_tab_content = self.site.racing_event_details.tab_content.event_markets_list
        tab_name = vec.racing.RACING_EDP_FORECAST_MARKET_TAB
        self.racing_event_tab_content.market_tabs_list.open_tab(tab_name)
        sleep(2)
        sections = self.racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        self.assertIn(tab_name, sections,
                      msg=f'"{tab_name}" not found in the list of tabs {list(sections.keys())}')

    def test_001_tap_1st_button_for_any_runner(self):
        """
        DESCRIPTION: Tap 1st button for any runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - 2nd and ANY buttons for this runner become disabled;
        EXPECTED: - All other 1st buttons for all other runners become disabled;
        EXPECTED: - Add to Betslip button is still disabled.
        """
        self.get_runner_bet_button()
        outcome_name, outcome = list(self.outcomes.items())[0]
        runner_buttons = outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[0]
        runner_bet_button.click()
        sleep(1)
        try:
            self.assertTrue(list(outcome.items_as_ordered_dict.values())[0].is_selected(),
                            msg=f'1st Button is not selected for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{outcome_name}"')
            self.assertFalse(list(outcome.items_as_ordered_dict.values())[2].is_enabled(expected_result=False),
                             msg=f'Any Button is enabled for "{outcome_name}"')
            for outcome_name, outcome in list(self.outcomes.items())[1:]:
                self.assertFalse(
                    list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                    msg=f'1st Button is enabled for all the other runners"{outcome_name}"')
                self.assertTrue(list(outcome.items_as_ordered_dict.values())[1].is_enabled(),
                                msg=f'2nd Button is not enabled for all the other runners "{outcome_name}"')
                self.assertTrue(list(outcome.items_as_ordered_dict.values())[2].is_enabled(),
                                msg=f'Any Button is not enabled for all the other runners "{outcome_name}"')

            self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(expected_result=False),
                             msg='Add To Betslip is displayed')

        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Horse Racing sport content refreshed: "{e}"')
        self.get_runner_bet_button()
        self.__class__.outcome_name, self.__class__.outcome = list(self.outcomes.items())[1]

    def test_002_tap_2nd_button_for_some_other_runner(self):
        """
        DESCRIPTION: Tap 2nd button for some other runner.
        EXPECTED: - Selected button is highlighted in green. Previously selected button remains green and selected;
        EXPECTED: - 1st and ANY button for this runner become disabled;
        EXPECTED: - All other 2nd buttons for all other runners become disabled;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - Add to Betslip button becomes enabled.
        """
        runner_buttons = self.outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{self.outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[1]
        runner_bet_button.click()
        sleep(2)
        try:
            self.assertTrue(list(self.outcome.items_as_ordered_dict.values())[1].is_selected(),
                            msg=f'Any Button is not selected for "{self.outcome_name}"')
            self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                             msg=f'1st Button is enabled for "{self.outcome_name}"')
            self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[2].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{self.outcome_name}"')

            for outcome_name, outcome in list(self.outcomes.items())[2:]:
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                                 msg=f'1st Button is enabled for all the other runners"{outcome_name}"')
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                                 msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
                self.assertTrue(list(outcome.items_as_ordered_dict.values())[2].is_enabled(),
                                msg=f'Any Button is not selected for "{outcome_name}"')
            self.assertTrue(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                                msg='Add To Betslip is disabled')

        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Horse racing sport content refreshed: "{e}"')
        self.get_runner_bet_button()
        self.__class__.outcome_name, self.__class__.outcome = list(self.outcomes.items())[2]

    def test_003_tap_any_selection_button_for_any_runner(self):
        """
        DESCRIPTION: Tap ANY selection button for any runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - All 1st and 2nd buttons become disabled and unhighlighted;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button becomes disabled.
        """
        runner_buttons = self.outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{self.outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[2]
        runner_bet_button.click()
        sleep(2)
        try:
            self.assertTrue(list(self.outcome.items_as_ordered_dict.values())[2].is_selected(),
                            msg=f'Any Button is not selected for "{self.outcome_name}"')
            self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                             msg=f'1st Button is enabled for "{self.outcome_name}"')
            self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{self.outcome_name}"')

            for outcome_name, outcome in list(self.outcomes.items())[3:]:
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                                 msg=f'1st Button is enabled for all the other runners"{outcome_name}"')
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                                 msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
                self.assertTrue(list(outcome.items_as_ordered_dict.values())[2].is_enabled(),
                                msg=f'Any Button is not selected for "{outcome_name}"')

            self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                                 msg='Add To Betslip is enabled')

        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Horse racing sport content refreshed: "{e}"')
        self.get_runner_bet_button()
        self.__class__.outcome_name, self.__class__.outcome = list(self.outcomes.items())[3]

    def test_004_tap_any_selection_button_for_some_other_runner(self):
        """
        DESCRIPTION: Tap ANY selection button for some other runner.
        EXPECTED: - Selected button is highlighted in green;
        EXPECTED: - All 1st and 2nd buttons remain disabled;
        EXPECTED: - Other ANY buttons remain enabled;
        EXPECTED: - 'Add to Betslip' button becomes enabled.
        """
        runner_buttons = self.outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{self.outcome_name}"')
        runner_bet_button = list(runner_buttons.values())[2]
        runner_bet_button.click()
        sleep(2)
        try:
            self.assertTrue(list(self.outcome.items_as_ordered_dict.values())[2].is_selected(),
                            msg=f'Any Button is not selected for "{self.outcome_name}"')
            self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                             msg=f'1st Button is enabled for "{self.outcome_name}"')
            self.assertFalse(list(self.outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                             msg=f'2nd Button is enabled for "{self.outcome_name}"')

            for outcome_name, outcome in list(self.outcomes.items())[4:]:
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[0].is_enabled(expected_result=False),
                                 msg=f'1st Button is enabled for all the other runners"{outcome_name}"')
                self.assertFalse(list(outcome.items_as_ordered_dict.values())[1].is_enabled(expected_result=False),
                                 msg=f'2nd Button is enabled for all the other runners"{outcome_name}"')
                self.assertTrue(list(outcome.items_as_ordered_dict.values())[2].is_enabled(),
                                msg=f'Any Button is not selected for "{outcome_name}"')
            self.assertTrue(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                            msg='Add To Betslip is disabled')

        except StaleElementReferenceException as e:
            self._logger.debug(f'*** Horse racing sport content refreshed: "{e}"')
