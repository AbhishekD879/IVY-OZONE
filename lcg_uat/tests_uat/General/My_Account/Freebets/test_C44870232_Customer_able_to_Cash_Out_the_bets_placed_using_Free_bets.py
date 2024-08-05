import tests
import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # grant_freebet method require changes to be done in the ob, so restricted to run this test script only in qa2.
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.p1
@pytest.mark.uat
@vtest
class Test_C44870232_Customer_able_to_Cash_Out_the_bets_placed_using_Free_bets(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C44870232
    NAME: Customer able to Cash Out the bets placed using Free bets
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        PRECONDITIONS: Free bet available
        """
        username = tests.settings.betplacement_user
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
        home_team_selection_id = list(self.event.selection_ids.values())[0]
        self.ob_config.grant_freebet(username=username, level='selection', id=home_team_selection_id)
        self.site.login(username=username, async_close_dialogs=False)

    def test_001_launch_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Launch https://beta-sports.coral.co.uk/
        EXPECTED: HomePage is opened
        """
        # This step is covered in precondition

    def test_002_place_a_bet_on_selection_with_cashout_available_using_free_bet(self):
        """
        DESCRIPTION: Place a bet on selection with cashout available using free bet
        EXPECTED: Bet placed successfully
        """
        self.__class__.free_bet_eventname = '%s v %s' % (self.event.team1, self.event.team2)
        selection = list(self.event.selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=selection)
        self.place_single_bet(freebet=True)
        self.check_bet_receipt_is_displayed(timeout=10)
        self.site.close_betreceipt()

    def test_003_verify_bet_in_my_bets__openbet(self):
        """
        DESCRIPTION: Verify bet in My bets > openbet
        EXPECTED: Bet is displayed in OpenBet
        """
        self.site.open_my_bets_open_bets()
        self.site.wait_splash_to_hide(3)
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.assertEqual(self.bet.event_name, self.free_bet_eventname,
                         msg=f'bet "{self.bet.event_name}" is not equal to "{self.free_bet_eventname}"')

    def test_004_verify_green_cashout_bar_is_available_for_bet(self):
        """
        DESCRIPTION: Verify Green cashout bar is available for bet
        EXPECTED: Cashout is displayed with cash out value
        """
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button,
                        msg=f'"{vec.bet_history.CASH_OUT_TAB_NAME}"is not available for bet')
        self.bet.buttons_panel.full_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.has_cashout_button(),
                        msg=f'"{vec.bet_history.CASHOUT_BUTTON_TEXT}" is not available for bet')
        self.assertTrue(self.bet.buttons_panel.cashout_button.amount.is_displayed(),
                        msg='Cashout is displayed with cash out value')

    def test_005_click_on_cashout_and_verify_user_is__able_to_cash_out_the_bets_placed_using_free_bets(self):
        """
        DESCRIPTION: Click on Cashout and verify user is  able to Cash Out the bets placed using Free bets
        EXPECTED: Free bet, cashed out successfully
        EXPECTED: Header balance is updated with cashout value
        """
        user_balance = self.site.header.user_balance
        self.bet.buttons_panel.cashout_button.click()
        self.site.wait_splash_to_hide(3)
        self.assertTrue(self.bet.wait_for_message(message=vec.bet_history.FULL_CASH_OUT_SUCCESS, timeout=30),
                        msg=f'Message: "{vec.bet_history.FULL_CASH_OUT_SUCCESS}" is not shown')
        actual_message = self.bet.cash_out_error_message
        self.assertEqual(vec.bet_history.CASHOUT_BET.free_bet_notification, actual_message,
                         msg=f'"{vec.bet_history.CASHOUT_BET.free_bet_notification}"and actual message are not same')
        self.device.refresh_page()
        self.site.wait_splash_to_hide(3)
        cashout_balance = self.site.header.user_balance
        self.assertGreater(cashout_balance, user_balance, msg=f'user balance {user_balance} is not updated with cashout value {cashout_balance}')
