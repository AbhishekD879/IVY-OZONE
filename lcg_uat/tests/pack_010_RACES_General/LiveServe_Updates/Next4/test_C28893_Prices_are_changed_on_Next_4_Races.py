import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  # we can't trigger live updates on prod and hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.next_races
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C28893_Prices_are_changed_on_Next_4_Races(BaseRacing):
    """
    TR_ID: C28893
    NAME: Prices are changed on 'Next 4 Races'
    DESCRIPTION: This test case verifies prices changes on 'Next 4 Races' module on <Race> Landing page
    """
    keep_browser_open = True
    prices = ['1/4', '1/2', '1/3']

    def test_000_create_next4_racing_event(self):
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
                                                          lp_prices={0: self.prices[0], 1: '1/8'})
        self.__class__.selection_name, self.__class__.selection_id = list(event_params.selection_ids.items())[0]
        event_off_time = event_params.event_off_time
        self.__class__.created_event_name = f'{event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}' \
            if self.device_type == 'mobile' else f'{event_off_time} {self.horseracing_autotest_uk_name_pattern}'

    def test_001_navigate_to_next_4_races_module(self):
        """
        DESCRIPTION: Navigate to 'Next 4 Races' module
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')

    def test_002_trigger_price_change_for_win_or_each_way_market_outcome_for_the_event_from_next_4_races(self):
        """
        DESCRIPTION: Trigger price change for 'Win or Each Way' market outcome for the event from 'Next 4 Races'
        EXPECTED: Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its colour to:
        EXPECTED: blue colour if price has decreased
        EXPECTED: red colour if price has increased
        EXPECTED: Previous Odds under Price/Odds button are updated/added respectively
        """
        autotest_event = self.get_event_from_next_races_module(event_name=self.created_event_name)
        outcomes = autotest_event.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No outcomes were found in {autotest_event} event')
        outcome = outcomes.get(self.selection_name)
        self.assertTrue(outcome, f'Outcome {self.selection_name} was not found')
        outcome.bet_button.scroll_to()
        self.ob_config.change_price(selection_id=self.selection_id, price=self.prices[1])
        result = wait_for_result(lambda: outcome.bet_button.outcome_price_text == self.prices[1],
                                 name=f'New price {self.prices[1]} to appear. '
                                      f'Current is {outcome.bet_button.outcome_price_text}',
                                 timeout=50)
        self.assertTrue(result, msg=f'Price for {self.selection_name} outcome was not changed.')
        self.assertEqual(outcome.previous_price, self.prices[0],
                         msg=f'Previous price {outcome.previous_price} is not the same as expected {self.prices[0]}')

        self.ob_config.change_price(selection_id=self.selection_id, price=self.prices[2])
        result = wait_for_result(lambda: outcome.bet_button.outcome_price_text == self.prices[2],
                                 name=f'New price {self.prices[2]} to appear. '
                                      f'Current is {outcome.bet_button.outcome_price_text}',
                                 timeout=50)
        self.assertTrue(result, msg=f'Price for {self.selection_name} outcome was not changed.')
        expected_previous_price = f'{self.prices[0]} > {self.prices[1]}'
        self.assertEqual(outcome.previous_price, expected_previous_price,
                         msg=f'Previous price {outcome.previous_price} is not the same '
                             f'as expected {expected_previous_price}')
