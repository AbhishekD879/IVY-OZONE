import pytest
import tests
from random import choice
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter, SiteServeRequests
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C10436241_Verify_adding_1st_2nd_3rd_selections_from_Tricast(Common):
    """
    TR_ID: C10436241
    NAME: Verify adding 1st, 2nd, 3rd selections from Tricast
    DESCRIPTION: This test case verifies adding 1st, 2nd, 3rd selections from Tricast
    PRECONDITIONS: 1. GH event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Tricast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User is on EDP on this event in app
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.greyhound_racing_config.category_id
            class_ids = self.get_class_ids_for_category(category_id=category_id)

            events_filter = self.ss_query_builder \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(
                    LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'SF,CF,RF,'))) \
                .add_filter(exists_filter(LEVELS.EVENT, simple_filter(
                    LEVELS.MARKET, ATTRIBUTES.NCAST_TYPE_CODES, OPERATORS.INTERSECTS, 'CT,TC,'))) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_ACTIVE, OPERATORS.IS_TRUE))

            ss_req = SiteServeRequests(env=tests.settings.backend_env, class_id=class_ids, brand=self.brand)
            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
            events = [event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')]

            if not events:
                raise SiteServeException(f'Cannot find active Forecast/Tricast Racing events')

            event_id = choice(events)['event']['id']
        else:
            event_id = self.ob_config.add_UK_greyhound_racing_event(tricast_available=True).event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')

    def test_001_select_tricast_tab(self):
        """
        DESCRIPTION: Select Tricast tab
        """
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_TRICAST_MARKET_TAB)
        self.__class__.racing_event_tab_content = self.site.greyhound_event_details.tab_content.event_markets_list
        sections = self.racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        section_name, section = list(sections.items())[0]
        self.__class__.outcomes = section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'No one outcome was found in section: "{section_name}"')

    def test_002_click_1st_selection_button_on_any_runner(self, button_number=0, add_to_betslip=False):
        """
        DESCRIPTION: Click 1st selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * 2nd, 3rd and ANY button for this runner become disabled
        EXPECTED: * All other 1st buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button still disabled
        """
        runner = list(self.outcomes.values())[button_number]
        runner_buttons = list(runner.items_as_ordered_dict.values())
        runner_buttons[button_number].click()
        sleep(1)
        self.assertTrue(list(runner.items_as_ordered_dict.values())[button_number].is_selected(),
                        msg=f'1st Button is not selected')
        for button in runner_buttons[button_number + 1:]:
            self.assertFalse(button.is_enabled(),
                             msg=f'2nd, 3rd and ANY Buttons are not disabled')
        for runner in list(self.outcomes.values())[button_number + 1:]:
            runner_buttons = list(runner.items_as_ordered_dict.values())
            self.assertFalse(runner_buttons[button_number].is_enabled(),
                             msg=f'1st Button is not disabled')
            self.assertTrue(runner_buttons[-1].is_enabled(),
                            msg=f'Any Button is not enabled')
        if add_to_betslip:
            self.assertTrue(self.racing_event_tab_content.add_to_betslip_button.is_enabled(),
                            msg='Add To Betslip is displayed')
        else:
            self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(expected_result=False),
                             msg='Add To Betslip is displayed')

    def test_003_click_2nd_selection_button_on_a_different_runner(self):
        """
        DESCRIPTION: Click 2nd selection button on a different runner
        EXPECTED: * Selected button is highlighted green. Previously selected button remains green and selected
        EXPECTED: * 1st, 3rd and ANY button for this runner become disabled
        EXPECTED: * All other 2nd buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button remains disabled
        """
        self.test_002_click_1st_selection_button_on_any_runner(button_number=1)

    def test_004_click_3rd_selection_button_on_a_different_runner(self):
        """
        DESCRIPTION: Click 3rd selection button on a different runner
        EXPECTED: * Selected button is highlighted green. Previously selected button remains green and selected
        EXPECTED: * 2nd, 3rd and ANY button for this runner become disabled
        EXPECTED: * All other 3rd buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button becomes enabled
        """
        self.test_002_click_1st_selection_button_on_any_runner(button_number=2, add_to_betslip=True)
