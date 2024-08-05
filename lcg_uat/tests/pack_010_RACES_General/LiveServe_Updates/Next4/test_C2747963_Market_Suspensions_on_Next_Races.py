import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  # we can't trigger live updates on prod and hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.next_races
@pytest.mark.races
@vtest
class Test_C2747963_Market_Suspensions_on_Next_Races(BaseRacing):
    """
    TR_ID: C2747963
    NAME: Market Suspensions on 'Next Races'
    DESCRIPTION: This test case verifies Suspensions of market on 'Next Races'
    """
    keep_browser_open = True
    price = '1/4'

    def verify_outcomes_state_for_event(self, expected_result, event_name):
        autotest_event = self.get_event_from_next_races_module(event_name=event_name)
        autotest_event.scroll_to()

        outcomes = autotest_event.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No outcomes found')

        for outcome_name, outcome in outcomes.items():
            try:
                result = outcome.bet_button.is_enabled(expected_result=expected_result, timeout=50,
                                                       bypass_exceptions=(NoSuchElementException,))
            except (StaleElementReferenceException, VoltronException):
                autotest_event = self.get_event_from_next_races_module(event_name=event_name)
                autotest_event.scroll_to()
                outcomes = autotest_event.items_as_ordered_dict
                self.assertTrue(outcomes, msg='No outcomes found')
                result = outcomes.get(outcome_name).bet_button.is_enabled(expected_result=expected_result, timeout=5)

            self.assertEqual(result, expected_result, msg=f'Bet button for "{outcome_name}" enabled state is not "{expected_result}"')
            self.assertEqual(outcomes[outcome_name].bet_button.name, self.price,
                             msg=f'Outcome price {outcomes[outcome_name].bet_button.name} '
                                 f'is not the same as expected {self.price}')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Next4 event
        EXPECTED: Next4 event is created
        """
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesComponentEnabled'):
            self._logger.warning('*** "NextRacesToggle -> nextRacesComponentEnabled" component is disabled. Needs to be enabled')
            self.cms_config.set_next_races_toggle_component_status(next_races_component_status=True)
        self.setup_cms_next_races_number_of_events()

        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=3,
                                                          lp_prices={0: self.price, 1: self.price})
        self.__class__.marketID = event_params.market_id
        self.__class__.eventID = event_params.event_id
        event_off_time = event_params.event_off_time
        self.__class__.created_event_name = f'{event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}' \
            if self.device_type == 'mobile' else f'{event_off_time} {self.horseracing_autotest_uk_name_pattern}'

    def test_001_navigate_to_next_races_module(self):
        """
        DESCRIPTION: Navigate to 'Next Races' module
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_002_suspend_market(self):
        """
        DESCRIPTION: Trigger the following situation for event: marketStatusCode = 'S' for one of the outcomes of 'Win or Each Way' market
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True,
                                           active=False)

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: All Price/Odds buttons of this event on Next Races are displayed immediately as greyed out and become disabled but still displaying the prices
        """
        self.verify_outcomes_state_for_event(event_name=self.created_event_name, expected_result=False)

    def test_004_unsuspend_market(self):
        """
        DESCRIPTION: Trigger the following situation for the same market: marketStatusCode = 'A'
        EXPECTED: Price/Odds buttons for outcomes of the event become active again
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True,
                                           active=True)

        self.verify_outcomes_state_for_event(event_name=self.created_event_name, expected_result=True)

    def test_005_suspend_market(self):
        """
        DESCRIPTION: Trigger the following situation for event: marketStatusCode = 'S'
        EXPECTED: All Price/Odds buttons of this event on Next Races are displayed immediately as greyed out and become disabled but still displaying the prices
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True,
                                           active=False)
        self.verify_outcomes_state_for_event(event_name=self.created_event_name, expected_result=False)

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Event with suspended 'Win or Each Way' market disappear from the 'Next 4 Races' module after page reloading
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Horseracing')

        event = self.get_event_from_next_races_module(event_name=self.created_event_name, raise_exceptions=False)
        self.assertFalse(event, msg=f'Event "{self.created_event_name}" is still displayed')
