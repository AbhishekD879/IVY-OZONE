import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.issue('https://jira.openbet.com/browse/LCRCORE-16654')  # Issue in ladbrokes only. todo : Need to remove this marker after given epic was closed
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.overask
@pytest.mark.trader_timeout
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C59898463_2_singles_1_with_OA_and_another_without_OA_and_trader_times_out(BaseBetSlipTest):
    """
    TR_ID: C59898463
    NAME: 2 singles: 1 with OA and another without OA and trader times out
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1.20
    max_mult_bet = 1.21
    bet_amount = 0.11
    bet_amount1 = 1.3
    prices = [{'odds_home': '1/5', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/10', 'odds_draw': '1/4', 'odds_away': '1/6'}]
    selection_ids = []

    def test_001_add_two_selections_from_any_sport_to_betslip_one_with_overask_and_another_without_overasktrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two selections from any sport to Betslip (one with overask and another without overask)
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        for i in range(2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices[i], max_bet=self.max_bet,
                                                                                     max_mult_bet=self.max_mult_bet)
            self.__class__.event_name = event_params.ss_response['event']['name']
            self.selection_ids.append(list(event_params.selection_ids.values())[0])
        self.site.login()
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'
        self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, trader_timeout=3)
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

    def test_002_time_out_in_ti(self):
        """
        DESCRIPTION: Time out in TI
        EXPECTED: After the Counter Offer has expired in TI, the customer should see an automated offer at max stake in bet slip
        """
        self.site.wait_content_state_changed()
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        single_section = list(self.get_betslip_sections().Singles.values())[1]
        stake = single_section.offered_stake.text.strip('£')
        self.assertEqual(float(stake), self.max_bet,
                         msg=f'Actual Stake: "{stake}" is not same as '
                             f'Expected stake: "{self.max_bet}"')
