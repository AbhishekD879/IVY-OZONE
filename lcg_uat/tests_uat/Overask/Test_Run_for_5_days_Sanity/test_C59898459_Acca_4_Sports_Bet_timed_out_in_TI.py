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
@pytest.mark.acca
@vtest
class Test_C59898459_Acca_4_Sports_Bet_timed_out_in_TI(BaseBetSlipTest):
    """
    TR_ID: C59898459
    NAME: Acca 4 Sports Bet timed out in TI
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1.21
    max_mult_bet = 1.21
    prices = [{'odds_home': '1/5', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/10', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/15', 'odds_draw': '1/4', 'odds_away': '1/6'},
              {'odds_home': '1/20', 'odds_draw': '1/4', 'odds_away': '1/6'}]
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        for i in range(4):
            event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices[i], max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            self.__class__.eventID = event_params.event_id
            self.selection_ids.append(list(event_params.selection_ids.values())[0])
        self.site.login()
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'
        self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, trader_timeout=3)

    def test_001_add_four_selections_from_any_sport_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add four selections from any sport to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        try:
            self.open_betslip_with_selections(selection_ids=self.selection_ids)
            self.__class__.bet_amount = self.max_bet + 1.1
            self.place_multiple_bet(number_of_stakes=1)
            overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
            self.assertTrue(overask, msg='Overask is not triggered for the User')
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_002_time_out_in_ti(self):
        """
        DESCRIPTION: Time out in TI
        EXPECTED: After the Counter Offer has expired in TI, the customer will see the bet slip with the message that "this bet has not been accepted by traders!" and we should not see a bet in My Bets and Account History.
        """
        self.site.wait_splash_to_hide(5)
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        multiple_section = self.get_betslip_sections(multiples=True).Multiples
        stake = multiple_section.overask_trader_offer.stake_content.stake_value.value.strip('£')
        self.assertEqual(float(stake), self.max_bet,
                         msg=f'Actual Stake: "{stake}" is not same as '
                             f'Expected stake: "{self.max_bet}"')
