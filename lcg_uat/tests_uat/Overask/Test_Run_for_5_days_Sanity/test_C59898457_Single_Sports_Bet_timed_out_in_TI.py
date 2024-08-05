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
class Test_C59898457_Single_Sports_Bet_timed_out_in_TI(BaseBetSlipTest):
    """
    TR_ID: C59898457
    NAME: Single Sports Bet timed out in TI
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1.22
    prices = {'odds_home': '1/12', 'odds_draw': '1/13', 'odds_away': '1/14'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.site.login()
        if self.device_type == 'mobile':
            self.__class__.channel = 'M'
        else:
            self.__class__.channel = 'I'
        self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel, trader_timeout=3)

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        try:
            self.open_betslip_with_selections(selection_ids=self.selection_id)
            self.__class__.bet_amount = self.max_bet + 1.1
            self.place_single_bet(number_of_stakes=1)
            overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
            self.assertTrue(overask, msg='Overask is not triggered for the User')
        finally:
            self.bet_intercept.change_trader_and_offer_timeout(channel_id=self.channel)

    def test_002_time_out_in_ti(self):
        """
        DESCRIPTION: Time out in TI
        EXPECTED: After the Counter Offer has expired in TI, the customer should see an offer at max stake
        """
        self.site.wait_splash_to_hide(5)
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        single_section = self.get_betslip_sections().Singles
        stake = single_section.overask_trader_offer.stake_content.stake_value.value.strip('£')
        self.assertEqual(float(stake), self.max_bet,
                         msg=f'Actual Stake: "{stake}" is not same as '
                             f'Expected stake: "{self.max_bet}"')
