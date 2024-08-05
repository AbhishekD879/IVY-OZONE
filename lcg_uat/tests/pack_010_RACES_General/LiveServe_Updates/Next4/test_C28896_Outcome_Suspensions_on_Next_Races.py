import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


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
@pytest.mark.safari
@vtest
class Test_C28896_Outcome_Suspensions_on_Next_Races(BaseRacing):
    """
    TR_ID: C28896
    NAME: Outcome Suspensions on 'Next Races'
    DESCRIPTION: This test case verifies Suspensions of outcomes on 'Next Races'
    """
    keep_browser_open = True
    price = '1/4'

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
        self.__class__.selection_name, self.__class__.selection_id = list(event_params.selection_ids.items())[0]
        event_off_time = event_params.event_off_time
        self.__class__.created_event_name = f'{event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}' \
            if self.device_type == 'mobile' else f'{event_off_time} {self.horseracing_autotest_uk_name_pattern}'

    def test_001_navigate_to_next_races_module(self):
        """
        DESCRIPTION: Navigate to 'Next Races' module
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_002_suspend_outcome(self):
        """
        DESCRIPTION: Trigger the following situation for event: outcomeStatusCode = 'S' for one of the outcomes of 'Win or Each Way' market
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)

    def test_003_verify_outcomes_for_the_event(self):
        """
        DESCRIPTION: Verify outcomes for the event
        EXPECTED: Price/Odds button for outcome is displayed immediately as greyed out and becomes disabled but still displaying the prices
        """
        autotest_event = self.get_event_from_next_races_module(event_name=self.created_event_name)
        autotest_event.scroll_to()
        outcomes = autotest_event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes were found in {autotest_event} event')
        self.__class__.outcome = outcomes.get(self.selection_name)
        self.assertTrue(self.outcome, msg=f'Outcome "{self.selection_name}" was not found')

        result = self.outcome.bet_button.is_enabled(expected_result=False, timeout=50)  # TODO VOL-1970
        self.assertFalse(result, msg=f'Bet button for {self.selection_name} outcome was not disabled.')
        self.assertEqual(self.outcome.bet_button.name, self.price,
                         msg=f'Outcome price {self.outcome.bet_button.name} is not the same as expected {self.price}')

    def test_004_unsuspend_outcome(self):
        """
        DESCRIPTION: Trigger the following situation for the same outcome: outcomeStatusCode = 'A'
        EXPECTED: Price/Odds button for outcome becomes active again
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=True)

        result = self.outcome.bet_button.is_enabled(timeout=40)
        self.assertTrue(result, msg=f'Bet button for {self.selection_name} outcome was not enabled.')

    def test_005_suspend_outcome(self):
        """
        DESCRIPTION: Trigger the following situation for event: outcomeStatusCode = 'S' for one of the outcomes of 'Win or Each Way' market
        EXPECTED: Price/Odds buttons for outcome are displayed immediately as greyed out and become disabled but still displaying the prices
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)

        result = self.outcome.bet_button.is_enabled(expected_result=False, timeout=40)
        self.assertFalse(result, msg=f'Bet button for {self.selection_name} outcome was not disabled.')
        self.assertEqual(self.outcome.bet_button.name, self.price,
                         msg=f'Outcome price {self.outcome.bet_button.name} is not the same as expected {self.price}')

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Suspended outcome disappears from the 'Next 4 Races' module after page reloading
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Horseracing')

        autotest_event = self.get_event_from_next_races_module(self.created_event_name)
        outcomes = autotest_event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes were found in {autotest_event} event')
        autotest_event.scroll_to()
        self.assertIsNone(outcomes.get(self.selection_name),
                          msg=f'Suspended outcome {self.selection_name} did not disappear after page refresh')
