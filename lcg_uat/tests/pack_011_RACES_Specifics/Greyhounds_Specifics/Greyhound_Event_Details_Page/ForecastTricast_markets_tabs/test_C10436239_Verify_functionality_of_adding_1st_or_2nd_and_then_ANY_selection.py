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
class Test_C10436239_Verify_functionality_of_adding_1st_or_2nd_and_then_ANY_selection(Common):
    """
    TR_ID: C10436239
    NAME: Verify functionality of adding 1st or 2nd and then ANY selection
    DESCRIPTION: This test case verifies functionality of adding 1st or 2nd and then ANY selection
    PRECONDITIONS: 1. GH event exists with Win/Each Way market exists.
    PRECONDITIONS: 2. Forecast checkbox is active on Win/Each Way market for this event
    PRECONDITIONS: 3. User is on EDP on this event in app
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get events
        """
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
            event_id = self.ob_config.add_UK_greyhound_racing_event(forecast_available=True).event_id

        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing')

    def test_001_select_forecast_tab(self):
        """
        DESCRIPTION: Select Forecast tab
        """
        self.site.greyhound_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_FORECAST_MARKET_TAB)
        self.__class__.racing_event_tab_content = self.site.greyhound_event_details.tab_content.event_markets_list
        sections = self.racing_event_tab_content.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections was found')
        section_name, section = list(sections.items())[0]
        self.__class__.outcomes = section.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg=f'No one outcome was found in section: "{section_name}"')

    def test_002_click_1st_or_2nd_selection_button_on_any_runner(self):
        """
        DESCRIPTION: Click 1st (or 2nd) selection button on any runner
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * 2nd (or 1st) and ANY button for this runner become disabled
        EXPECTED: * All other 1st buttons for all other runners become disabled
        EXPECTED: * Other ANY buttons remain enabled
        EXPECTED: * Add to Betslip button still disabled
        """
        runner = list(self.outcomes.values())[0]
        runner_buttons = list(runner.items_as_ordered_dict.values())
        runner_buttons[0].click()
        sleep(1)
        self.assertTrue(list(runner.items_as_ordered_dict.values())[0].is_selected(),
                        msg=f'1st Button is not selected')
        for button in runner_buttons[1:]:
            self.assertFalse(button.is_enabled(),
                             msg=f'2nd and ANY Buttons are not disabled')
        for runner in list(self.outcomes.values())[1:]:
            runner_buttons = list(runner.items_as_ordered_dict.values())
            self.assertFalse(runner_buttons[0].is_enabled(),
                             msg=f'1st Button is not disabled')
            self.assertTrue(runner_buttons[1].is_enabled(),
                            msg=f'2nd Button is not enabled')
            self.assertTrue(runner_buttons[-1].is_enabled(),
                            msg=f'Any Button is not enabled')
        self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='Add To Betslip is enabled')

    def test_003_click_any_selection_button_for_any_other_racer(self, runner_number=1):
        """
        DESCRIPTION: Click ANY selection button for any other racer
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * Previously selected button becomes deselected and disabled
        EXPECTED: * ALL 1st and 2nd buttons become disabled
        EXPECTED: * ALL ANY buttons become enabled
        EXPECTED: * Add to Betslip button still disabled
        """
        runner = list(self.outcomes.values())[runner_number]
        runner_buttons = list(runner.items_as_ordered_dict.values())
        runner_buttons[-1].click()
        sleep(1)
        self.assertTrue(list(runner.items_as_ordered_dict.values())[-1].is_selected(),
                        msg=f'ANY Button is not selected')
        runner = list(self.outcomes.values())[0]
        for runner in self.outcomes.values():
            runner_buttons = list(runner.items_as_ordered_dict.values())
            self.assertTrue(runner_buttons[-1].is_enabled(),
                            msg=f'Any Button is not enabled')
            for button in runner_buttons[:-1]:
                self.assertFalse(button.is_enabled(),
                                 msg=f'1st Button is not disabled')
        if runner_number == 1:
            previous_selection = list(runner.items_as_ordered_dict.values())[0]
            self.assertFalse(previous_selection.is_selected(),
                             msg=f'1st Button is selected')
            self.assertFalse(previous_selection.is_enabled(),
                             msg=f'1st Button is enabled')
            self.assertFalse(self.racing_event_tab_content.add_to_betslip_button.is_enabled(expected_result=False),
                             msg='Add to Betslip is not enabled')
        else:
            self.assertTrue(self.racing_event_tab_content.add_to_betslip_button.is_enabled(expected_result=False),
                            msg='Add To Betslip is enabled')

    def test_004_click_another_any_selection_button_for_any_other_racer(self):
        """
        DESCRIPTION: Click another ANY selection button for any other racer
        EXPECTED: * Selected button is highlighted green
        EXPECTED: * All other ANY buttons remain enabled
        EXPECTED: * ALL 1st and 2nd buttons remain disabled
        EXPECTED: * Add to Betslip button becomes enabled
        """
        self.test_003_click_any_selection_button_for_any_other_racer(runner_number=2)
