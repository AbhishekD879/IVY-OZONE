import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed now, can't create OB event on prod
# @pytest.mark.hl - Can't be executed now, can't create OB event on prod
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.critical
@pytest.mark.betslip
@pytest.mark.mobile_only
@vtest
class Test_C28865_C28866_C28870_C28871_Making_One_Single_Racing_Selection(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C28865
    TR_ID: C28866
    TR_ID: C28870
    TR_ID: C28871
    VOL_ID: C9697954
    NAME: Making One Single Racing Selection
    """
    keep_browser_open = True
    prices = {0: '1/5'}

    def add_selection(self):
        """
        DESCRIPTION: Add single 'SP' selection to bet slip
        EXPECTED: 1.  Single bet is added to bet slip.
        EXPECTED: 2.  Bet slip counter is increased to 1.
        """
        event_name = self.site.racing_event_details.tab_content.race_details.event_title
        self._logger.debug(f'*** Race event name: "{event_name}"')
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='*** No one section was found')
        first_section_name, first_section = list(sections.items())[0]
        outcomes = first_section.items_as_ordered_dict
        self.assertTrue(len(outcomes) == 1, msg=f'Found "{len(outcomes)}" racing outcomes but expected 1')
        self._logger.debug(f'*** Outcomes {list(outcomes.keys())}')
        self.__class__.outcome_name, outcome = list(outcomes.items())[0]
        self.assertTrue(outcome.bet_button.is_enabled(), msg=f'Racing outcome "{self.outcome_name}" is disabled')
        outcome.bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.__class__.expected_betslip_counter_value += 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create 2 test events: one with SP, another with LP prices
        """
        event_params_SP = self.ob_config.add_UK_racing_event(number_of_runners=1, time_to_start=2)
        event_params_LP = self.ob_config.add_UK_racing_event(number_of_runners=1, time_to_start=20, lp_prices=self.prices)
        self.__class__.event_off_time_SP = event_params_SP.event_off_time
        self.__class__.event_off_time_LP = event_params_LP.event_off_time
        self.__class__.event_name_SP = f'{self.event_off_time_SP} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.event_name_LP = f'{self.event_off_time_LP} {self.horseracing_autotest_uk_name_pattern}'
        self.__class__.meeting_name = self.horseracing_autotest_uk_name_pattern if self.brand == 'ladbrokes' \
            else self.horseracing_autotest_uk_name_pattern.upper()

    def test_001_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='Horseracing')

    def test_002_go_to_the_event_details_page_of_event_with_SP_price(self):
        """
        DESCRIPTION: Go to the event details page of the event with SP price
        EXPECTED: Event details page is opened
        """
        self.open_racing_event_details(section_name=self.uk_and_ire_type_name,
                                       meeting_name=self.meeting_name,
                                       event_off_time=self.event_off_time_SP)

    def test_003_add_single_sp_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single 'SP' selection to bet slip
        EXPECTED: 1.  Single bet is added to bet slip.
        EXPECTED: 2.  Bet slip counter is increased to 1.
        """
        self.add_selection()

    def test_004_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: Bet Slip with bet details is opened
        """
        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

        self.site.header.bet_slip_counter.click()
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip has not opened')

    def test_005_enter_stake_for_sp_selection(self):
        """
        DESCRIPTION: Enter stake for 'SP' selection
        EXPECTED: 1.  The total wager for the bet is entered.
        EXPECTED: 2.  Amounts of **'Est. Returns'**, **'Total Est. Returns'** are equal to 'N/A' value
        EXPECTED: 3.  **'Total Stake'** is changed due to selected stake.
        """
        section = self.get_betslip_sections().Singles
        self.assertTrue(len(section.items()) == 1, msg='More than 1 stake found in Betslip')
        stake_name, stake = list(section.items())[0]
        self._logger.info(f'*** Verifying stake "{stake_name}"')
        stake.amount_form.input.value = self.bet_amount
        est_returns = stake.est_returns
        betslip = self.get_betslip_content()
        total_est_returns, self.__class__.total_stake = betslip.total_estimate_returns, float(betslip.total_stake)
        self.assertEqual(est_returns, 'N/A', msg=f'Stake estimate returns "{est_returns}" is not N/A')
        self.assertEqual(total_est_returns, 'N/A', msg=f'Total estimate returns {total_est_returns} is not N/A')
        self.assertEqual(float(self.total_stake), self.bet_amount,
                         msg=f'Total stake "{self.total_stake}" is not "{self.bet_amount}"')

    def test_006_close_betslip(self):
        """
        DESCRIPTION: Close betslip
        EXPECTED: Page from which navigation was is shown
        """
        self.site.close_betslip()
        self.site.wait_content_state(state_name='RacingEventDetails')

    def test_007_go_to_bet_slip_again(self):
        """
        DESCRIPTION: Go to Bet Slip  again
        EXPECTED: Selection and entered stake are remembered
        """
        self.test_004_go_to_the_bet_slip()
        section = self.get_betslip_sections().Singles
        self.assertTrue(len(section.items()) == 1, msg='More than 1 stake found in Betslip')

    def test_008_add_lp_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 'LP' selection to the bet Slip
        EXPECTED: 1.  Single bet is added to the Bet Slip
        EXPECTED: 2.  Bet slip indicator is increased
        """
        self.site.close_betslip()
        self.site.back_button_click()
        self.site.wait_content_state(state_name='Horseracing')
        self.open_racing_event_details(section_name=self.uk_and_ire_type_name,
                                       meeting_name=self.meeting_name,
                                       event_off_time=self.event_off_time_LP)
        self.add_selection()

    def test_009_enter_a_stake_for_lp_selection(self):
        """
        DESCRIPTION: Enter a stake for 'LP' selection
        EXPECTED: 1.  The total wager for the bet is entered.
        EXPECTED: 2.  Amounts of **'Estimated Returns'**,** 'Total Est. Returns'** are calculated according to the predefined formula
        EXPECTED: 3.  **'Total Stake' **is changed due to selected stake
        """
        self.test_004_go_to_the_bet_slip()
        section = self.get_betslip_sections().Singles
        self.assertEqual(len(section.items()), 2, msg=f'Found "{len(section.items())}" but expected 2 stakes in Betslip')
        stake_name, stake = list(section.items())[1]
        self._logger.info(f'*** Verifying stake "{stake_name}"')
        self.assertEqual(self.outcome_name, stake_name,
                         msg=f'LP selection name "{self.outcome_name}" is not the same as expected "{stake_name}"')
        stake.amount_form.input.value = self.bet_amount
        est_returns = stake.est_returns
        betslip = self.get_betslip_content()
        total_est_returns, total_stake = betslip.total_estimate_returns, float(betslip.total_stake)
        self.assertNotEqual(est_returns, 'N/A', msg=f'Stake estimate returns "{est_returns}" is N/A')
        self.assertEqual(total_est_returns, 'N/A', msg=f'Total estimate returns "{total_est_returns}" is not N/A')
        self.assertEqual(total_stake, self.total_stake + self.bet_amount,
                         msg=f'Total stake "{total_stake}" is not "{self.total_stake + self.bet_amount}"')
