import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Can't create events, can't trigger ob on prod
@pytest.mark.uat
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.open_bets
@pytest.mark.other
@vtest
class Test_C44870294_2_singles_1_with_OA_and_another_without_OA_and_trader_times_out(BaseBetSlipTest):
    """
    TR_ID: C44870294
    NAME: 2 singles : 1 with OA and another without OA and trader times out
    """
    keep_browser_open = True
    max_bet = 1.2
    prices = {'odds_home': '1/12', 'odds_draw': '1/11', 'odds_away': '1/9'}
    selection_ids = []
    bet_amount = 0.11
    bet_amount1 = 1.3

    def test_001_place_one_oa_bet_and_one_non_oa_bet(self):
        """
        DESCRIPTION: Place one OA bet and one non-OA bet
        EXPECTED: The bets should have gone through to the OA flow
        """
        for i in range(2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet)
            selection_ids = event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
        self.site.login()
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'
        self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, trader_timeout=3)

    def test_002_in_the_ti_allow_the_oa_bet_to_time_out(self):
        """
        DESCRIPTION: In the TI, allow the OA bet to time out
        EXPECTED: The bet should have timed out
        """
        try:
            self.open_betslip_with_selections(selection_ids=self.selection_ids)
            self.singles_section = self.get_betslip_sections().Singles
            stake_name, stake = list(self.singles_section.items())[0]
            stake_bet_amounts = {
                stake_name: self.bet_amount,
            }
            self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts=stake_bet_amounts)
            stake_name, stake = list(self.singles_section.items())[1]
            stake_bet_amounts = {
                stake_name: self.bet_amount1,
            }
            self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts=stake_bet_amounts)
            betnow_btn = self.get_betslip_content().bet_now_button
            betnow_btn.click()
            overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
            self.assertTrue(overask, msg='Overask is not triggered for the User')
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_003_check_that_you_see_the_message_that_the_bets_have_not_been_accepted_by_traders(self):
        """
        DESCRIPTION: Check that you see the message that the bets have not been accepted by Traders
        EXPECTED: You should see the message and the bets should not have been placed
        """
        self.device.driver.implicitly_wait(10)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')
