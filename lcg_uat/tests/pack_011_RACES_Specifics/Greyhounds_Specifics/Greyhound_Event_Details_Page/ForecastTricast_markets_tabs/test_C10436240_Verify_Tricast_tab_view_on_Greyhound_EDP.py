import pytest
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lad_beta2
@pytest.mark.high
@pytest.mark.races
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.forecast_tricast
@pytest.mark.desktop
@vtest
class Test_C10436240_Verify_Tricast_tab_view_on_Greyhound_EDP(BaseRacing):
    """
    TR_ID: C10436240
    NAME: Verify Tricast tab view on Greyhound EDP
    DESCRIPTION: This test case verifies Tricast tab view on Greyhound EDP
    PRECONDITIONS: 1. GH event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Tricast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User is on EDP on this event in app
    """
    keep_browser_open = True

    def get_runner_bet_button(self):
        sections = self.racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
        outcome_name, outcome = list(outcomes.items())[0]
        runner_buttons = outcome.items_as_ordered_dict
        self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
        return list(runner_buttons.items())[0]

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create racing event with Tricast/Forecast, PROD: Find racing event with Tricast/Forecast
        """
        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'TC')), \
                exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.IS_EACH_WAY_AVAILABLE, OPERATORS.IS_TRUE))

            event = self.get_active_events_for_category(category_id=self.ob_config.backend.ti.greyhound_racing.category_id,
                                                        additional_filters=additional_filter)[0]
            outcomes = next((market_info['market']['children'] for market_info in event['event']['children'] if 'Win or Each Way' == market_info['market']['name']), None)
            selection_ids = {}
            for outcome in outcomes:
                if 'Unnamed' not in outcome['outcome']['name']:
                    selection_ids[outcome['outcome']['name']] = outcome['outcome']['id']
            self.__class__.eventID = event['event']['id']
            self.__class__.selection_names = selection_ids.keys()

            self._logger.info(f'*** Found event "{self.eventID}" with selections {self.selection_names}')
        else:
            event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=3,
                                                                        forecast_available=True, tricast_available=True)
            selection_ids = event_params.selection_ids
            self.__class__.eventID = event_params.event_id
            self.__class__.selection_names = selection_ids.keys()

    def test_001_navigate_to_edp_of_event_from_preconditions(self):
        """
        DESCRIPTION: Navigate to EDP of event from preconditions
        EXPECTED: * Separate Tricast tab displayed after Win/Each way market tab
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='greyhound-racing')
        self.__class__.racing_event_tab_content = self.site.greyhound_event_details.tab_content.event_markets_list
        if tests.settings.backend_env != 'prod':
            actual_tabs_names = self.racing_event_tab_content.market_tabs_list.items_names
            expected_tab_names = vec.racing.RACING_EDP_MARKET_TABS_NAMES
            self.assertEqual(actual_tabs_names, expected_tab_names,
                             msg=f'Actual tab order "{actual_tabs_names}" '
                                 f'does not match expected "{expected_tab_names}"')

    def test_002_select_tricast_tabverify_its_layout(self):
        """
        DESCRIPTION: Select Tricast tab
        DESCRIPTION: Verify it's layout
        EXPECTED: * List of selections with:
        EXPECTED: - runner number
        EXPECTED: - runner name
        EXPECTED: - no silks
        EXPECTED: - no race form info
        EXPECTED: * Unnamed favourites and Non Runners are NOT displayed
        EXPECTED: * Runners ordered by runner number
        EXPECTED: * 4 grey tappable buttons displayed at the right side of each runner:
        EXPECTED: - 1st
        EXPECTED: - 2nd
        EXPECTED: - 3rd
        EXPECTED: - ANY
        EXPECTED: * Green 'Add To Betslip' button displayed at the bottom of the list, disabled by default
        """
        tab_name = vec.racing.RACING_EDP_TRICAST_MARKET_TAB
        self.racing_event_tab_content.market_tabs_list.open_tab(tab_name)
        self.__class__.racing_event_tab_content = self.site.greyhound_event_details.tab_content.event_markets_list
        sections = self.racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')
        runners_names = list(outcomes.keys())
        self.assertEqual(sorted(runners_names), sorted(list(self.selection_names)),
                         msg=f'Actual Runner names "{sorted(runners_names)}" '
                         f'does not match expected "{sorted(list(self.selection_names))}"')

        self.assertFalse(vec.racing.UNNAMED_FAVORITE in outcomes,
                         msg=f'"{vec.racing.UNNAMED_FAVORITE}" selection is shown on the Tricast tab')

        for outcome_name, outcome in outcomes.items():
            runner_buttons = outcome.items_as_ordered_dict
            self.assertTrue(runner_buttons, msg=f'No runner buttons found for "{outcome_name}"')
            runner_bet_button_names = list(runner_buttons.keys())
            self.assertEqual(runner_bet_button_names, vec.racing.RACING_EDP_TRICAST_RACING_BUTTONS,
                             msg=f'Actual racing button names "{runner_bet_button_names}" '
                             f'does not match expected "{vec.racing.RACING_EDP_TRICAST_RACING_BUTTONS}"')
        self.assertTrue(self.racing_event_tab_content.add_to_betslip_button.is_displayed(),
                        msg='Add To Betslip is not displayed')

    def test_003_tap_any_1st_2nd_3rd_or_any_button(self):
        """
        DESCRIPTION: Tap any 1st, 2nd, 3rd or ANY button
        EXPECTED: Button is selected and highlighted green
        """
        runner_name, runner_bet_button = self.get_runner_bet_button()
        runner_bet_button.click()
        runner_name, runner_bet_button = self.get_runner_bet_button()
        self.assertTrue(runner_bet_button.is_selected(), msg=f'Button is not selected for "{runner_name} runner')

    def test_004_tap_same_button_again(self):
        """
        DESCRIPTION: Tap same button again
        EXPECTED: Button is deselected and not highlighted
        """
        runner_name, runner_bet_button = self.get_runner_bet_button()
        runner_bet_button.click()
        runner_name, runner_bet_button = self.get_runner_bet_button()
        self.assertFalse(runner_bet_button.is_selected(expected_result=False),
                         msg=f'Button is not selected for "{runner_name} runner')
