import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod //cant create events
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.desktop
@vtest
class Test_C9752213_Verify_that_Partial_Cash_Out_button_is_not_shown_in_case_bet_is_placed_with_free_bet(BaseCashOutTest):
    """
    TR_ID: C9752213
    NAME: Verify that 'Partial Cash Out' button is not shown in case bet is placed with free bet
    DESCRIPTION: This test case verifies that partial cash out is unavailable for bets which were placed with Free Bet Offer
    PRECONDITIONS: 1. Login and place bet with cash out available using Free Bet Offer
    PRECONDITIONS: 2. Navigate to My Bets page
    PRECONDITIONS: NOTE: Test case should be run on Cash Out and on Open Bets tab
    PRECONDITIONS: You can check the appropriate attribute in Web Developer Tool>Network tab>https://cashout-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/bet-details?token=94223d7220a6bd2a12b2217979bede17a3d7674a72a0dbe01727a22d8a940697  - "partialCashoutAvailable" should be 'N'
    PRECONDITIONS: **From release XXX.XX (according to BMA-50940/BMA-50937/BMA-50936):**
    PRECONDITIONS: - Open Dev Tools -> Network tab -> WS filter (cashout request)
    PRECONDITIONS: - WebSocket connection to Cashout MS is created when user lands on myBets/Cashout page
    PRECONDITIONS: You can check the appropriate attribute in Dev Tools -> Network tab -> WS filter (cashout request) - in initial bets response "partialCashoutAvailable" should be 'N'
    """
    keep_browser_open = True

    def verify_cashout_tab(self, bet):
        if bet == vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE:
            bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event1_name, number_of_bets=1)
        else:
            bet_name, bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event_names, number_of_bets=1)
        self.assertTrue(bet, msg=f'Bet "{bet_name}" is not displayed')
        self.assertFalse(bet.buttons_panel.has_partial_cashout_button(expected_result=False),
                         msg='"PARTIAL CASHOUT" button is present')
        self.assertTrue(bet.buttons_panel.has_full_cashout_button(), msg='"FULL CASHOUT" button is not present')

    def verify_openbet_tab(self, bet):
        if bet == vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE:
            bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event1_name, number_of_bets=1)
        else:
            bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event_names, number_of_bets=1)
        self.assertTrue(bet, msg=f'Bet "{bet_name}" is not displayed')
        self.assertFalse(bet.buttons_panel.has_partial_cashout_button(expected_result=False),
                         msg='"PARTIAL CASHOUT" button is present')
        self.assertTrue(bet.buttons_panel.has_full_cashout_button(), msg='"FULL CASHOUT" button is not present')

    def test_000_preconditions(self):
        self.__class__.events = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.__class__.event1_name = f'{self.events[0].event_name} {self.events[0].local_start_time}'
        event2_name = f'{self.events[1].event_name} {self.events[1].local_start_time}'
        self.__class__.event_names = f'{self.event1_name}, {event2_name}'
        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)
        self.assertTrue(self.site.header.has_freebets(), msg='User does not have Free bets')
        self.open_betslip_with_selections(selection_ids=self.events[0].selection_ids['Draw'])
        self.place_single_bet(number_of_stakes=1, freebet=True)
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()

    def test_001_verify_that_patrial_cash_out_button_is_not_shown_for_the_bet_on_cash_out_and_on_open_bets_tabs(self):
        """
        DESCRIPTION: Verify that 'Patrial Cash Out' button is not shown for the bet on Cash Out and on Open bets tabs
        EXPECTED: Patrial Cash Out' button is not shown
        """
        self.site.open_my_bets_open_bets()
        self.verify_openbet_tab(bet=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            self.verify_cashout_tab(bet=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)

    def test_002_provide_the_same_verification_for_multiple_betverify_that_patrial_cash_out_button_is_not_shown_multiple_bet_placed_with_free_bet_offer(self):
        """
        DESCRIPTION: Provide the same verification for MULTIPLE bet
        DESCRIPTION: Verify that 'Patrial Cash Out' button is not shown multiple bet placed with Free Bet Offer
        EXPECTED: 'Patrial Cash Out' button is not shown
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(
            selection_ids=(self.events[0].selection_ids['Draw'], self.events[1].selection_ids['Draw']))
        self.place_multiple_bet(number_of_stakes=1, freebet=True)
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_open_bets()
        self.verify_openbet_tab(bet=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            self.verify_cashout_tab(bet=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
