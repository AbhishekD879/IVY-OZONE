import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # we can't trigger live updates on prod and hl
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.liveserv_updates
@pytest.mark.races
@pytest.mark.low
@vtest
class Test_C141200_Outcome_Becomes_Suspended_Selection_On_Racing_EDP_When_Its_Added_To_Betslip(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C141200
    NAME: Outcome becomes suspended selection on <Race> Event Details page when it is added to the betslip
    """
    keep_browser_open = True
    expected_betslip_counter_value = 2
    lp_prices = {0: '1/2',
                 1: '1/4'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create 'SP', 'LP' and 'SP,LP' racing events
        EXPECTED: Racing event created
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1)
        self.__class__.eventID_sp, self.__class__.event_off_time_sp, self.__class__.selection_ids_sp = \
            event_params.event_id, event_params.event_off_time, event_params.selection_ids

        self._logger.info(f'*** Created SP event id: {self.eventID_sp}, event off time: {self.event_off_time_sp}, '
                          f'selection ids: {list(self.selection_ids_sp.values())}')

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1, lp_prices=self.lp_prices, sp=True)
        self.__class__.eventID_lp_sp, self.__class__.event_off_time_lp_sp, self.__class__.selection_ids_lp_sp = \
            event_params.event_id, event_params.event_off_time, event_params.selection_ids

        self._logger.info(f'*** Created LP-SP event id: {self.eventID_lp_sp}, event off time: {self.event_off_time_lp_sp}, '
                          f'selection ids: {list(self.selection_ids_lp_sp.values())}')

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1, lp_prices=self.lp_prices, sp=False)
        self.__class__.eventID_lp, self.__class__.event_off_time_lp, self.__class__.selection_ids_lp = \
            event_params.event_id, event_params.event_off_time, event_params.selection_ids

        self._logger.info(f'*** Created LP event id: {self.eventID_lp}, event off time: {self.event_off_time_lp}, '
                          f'selection ids: {list(self.selection_ids_lp.values())}')
        self.__class__.eventID = self.eventID_lp
        self.__class__.selection_ids = self.selection_ids_lp

    def test_001_open_racing_edp_page(self):
        """
        DESCRIPTION: Open event details page where event has LP price type
        EXPECTED: Event details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

    def test_002_tap_on_price_button(self):
        """
        DESCRIPTION: Click bet button
        EXPECTED: Selected Price/Odds button is marked as added to Betslip and displayed as green
        EXPECTED: Selection is present in Bet Slip and counter is increased on header (Betslip is closed)
        """
        self.__class__.expected_prices = {}
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, section = list(sections.items())[0]
        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: "{section_name}"')

        for (index, (outcome_name, outcome)) in enumerate(outcomes.items()):
            self.expected_prices.update({outcome_name: outcome.output_price})
            self._logger.debug(f'*** Outcome: {outcome_name}')
            self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Price is suspended for "{outcome_name}"')

            result = wait_for_result(lambda: outcome.bet_button.is_selected(expected_result=False),
                                     name='Wait for Bet button to be enabled',
                                     timeout=3)
            self.assertFalse(result, msg='Quick bet should not be displayed')

            outcome.bet_button.click()

            if index == 0 and self.device_type != 'desktop':
                self.site.add_first_selection_from_quick_bet_to_betslip()
            self.assertTrue(outcome.bet_button.is_selected(timeout=4),
                            msg=f'Bet button is not selected for "{outcome_name}"')

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

    def test_003_suspend_price_and_verify(self):
        """
        DESCRIPTION: Suspend price
        EXPECTED: Price is suspended on 'Event Details' page when it is added to the betslip
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, section = list(sections.items())[0]
        actual_prices = {}

        for selection_name, selection_id in self.selection_ids.items():
            self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=False)

        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: {section_name}')

        for outcome_name, outcome in outcomes.items():
            self.assertFalse(outcome.bet_button.is_enabled(timeout=5, expected_result=False),
                             msg=f'Price is not suspended for {outcome_name}')
            actual_prices.update({outcome_name: outcome.output_price})
        self.assertEqual(actual_prices, self.expected_prices, msg='Prices are not equal')

    def test_004_unsuspend_price_and_verify(self):
        """
        DESCRIPTION: Unsuspend price
        EXPECTED: Price is not suspended on 'Event Details' page when it is added to the betslip
        """
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')

        section_name, section = list(sections.items())[0]
        actual_prices = {}

        for selection_name, selection_id in self.selection_ids.items():
            self.ob_config.change_selection_state(selection_id=selection_id, displayed=True, active=True)

        outcomes = section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section: {section_name}')

        for outcome_name, outcome in outcomes.items():
            self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Price is not active for {outcome_name}')
            actual_prices.update({outcome_name: outcome.output_price})
        self.assertEqual(actual_prices, self.expected_prices, msg='Prices are not equal')

    def test_005_repeat_steps_for_sp_and_lp_sp_events(self):
        """
        DESCRIPTION: Repeat steps # 3-6 for event where price type is 'SP'/'LP,SP'
        EXPECTED: Event details page is opened
        """
        self.site.open_betslip()
        self.clear_betslip()
        self.expected_betslip_counter_value = 2
        self.eventID = self.eventID_sp
        self.selection_ids = self.selection_ids_sp
        self.test_001_open_racing_edp_page()
        self.test_002_tap_on_price_button()
        self.test_003_suspend_price_and_verify()
        self.test_004_unsuspend_price_and_verify()

        self.site.open_betslip()
        self.clear_betslip()
        self.expected_betslip_counter_value = 2
        self.eventID = self.eventID_lp_sp
        self.selection_ids = self.selection_ids_lp_sp
        self.test_001_open_racing_edp_page()
        self.test_002_tap_on_price_button()
        self.test_003_suspend_price_and_verify()
        self.test_004_unsuspend_price_and_verify()
