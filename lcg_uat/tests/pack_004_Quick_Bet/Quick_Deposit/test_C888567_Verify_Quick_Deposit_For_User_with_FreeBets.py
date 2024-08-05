import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.freebets
@pytest.mark.quick_bet
@pytest.mark.quick_deposit
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C888567_Verify_Quick_Deposit_For_User_with_FreeBets(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C888567
    VOL_ID: C9698097
    NAME: Verify Quick Deposit section for users with free bets
    DESCRIPTION: This test case verifies Quick Deposit section for users with free bets available
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: User is logged in, has 0 balance and free bets and at list one credit card added to his account
    PRECONDITIONS: Users have the cards added to his account
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load Invictus application, create event and login
        """
        self.__class__.username = tests.settings.freebet_user

        self.__class__.eventID = self.ob_config.add_autotest_premier_league_football_event().event_id
        self.ob_config.grant_freebet(username=self.username, level='event', id=self.eventID)

        self.site.login(username=self.username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick bet appears at the bottom of the page
        EXPECTED: 'Use Free bet' link is displayed below event name
        """
        self.navigate_to_edp(event_id=self.eventID)

        self.add_selection_from_event_details_to_quick_bet()
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')

        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content
        self.assertTrue(self.quick_bet.has_use_free_bet_link(), msg='"Use Free Bet" link is not shown')

    def test_002_click_use_free_bet_link_and_select_free_bet_from_the_pop_up(self):
        """
        DESCRIPTION: Click 'Use Free bet' link and select Free bet from the pop-up.
        EXPECTED: Free bet is selected
        EXPECTED: 'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' message is NOT displayed
        EXPECTED: Stake is equal to free bet value
        """
        if self.quick_bet.has_freebet_tooltip():
            self.quick_bet.amount_form.input.click()
        self.quick_bet.use_free_bet_link.click()

        self.__class__.freebet_value = self.select_free_bet()
        total_stake = self.site.quick_bet_panel.selection.bet_summary.combined_total_stake.replace('£', '')
        self.assertEqual(total_stake, self.freebet_value,
                         msg=f'Total stake amount "{total_stake}" '
                             f'is not the same as free bet "{self.freebet_value}"')

    def test_003_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately for Ladbrokes brand
        EXPECTED: The same message(without icon) is displayed below 'QUICK BET' header for Coral brand where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - difference between entered(into a field) stake value and users balance
        EXPECTED: Total Stake is equal to free bet value + stake value
        """
        quick_bet = self.site.quick_bet_panel.selection.content

        quick_bet.amount_form.input.value = self.user_balance + 1
        expected_amount_form = '{0:.2f}'.format(self.user_balance + 1)
        self.assertEqual(quick_bet.amount_form.input.value, expected_amount_form,
                         msg=f'Actual amount "{quick_bet.amount_form.input.value}" '
                             f'does not match expected "{expected_amount_form}"')

        if self.brand == 'ladbrokes':
            result = self.site.quick_bet_panel.wait_for_deposit_info_panel()
            self.assertTrue(result, msg=f'"Min Deposit" message is not shown')
            actual_message = self.site.quick_bet_panel.deposit_info_message.text
        else:
            self.assertTrue(self.site.quick_bet_panel.wait_for_quick_bet_info_panel(),
                            msg='Quick Bet Info Panel is not present')
            actual_message = self.site.quick_bet_panel.info_panels_text[0]

        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(5)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" '
                             f'does not match expected "{expected_message}"')

        expected_total_stake = f'£{self.freebet_value} ' + '+' + f' £{(self.user_balance + 1):,.2f}'
        actual_total_stake = self.site.quick_bet_panel.selection.bet_summary.combined_total_stake
        self.assertEqual(actual_total_stake, expected_total_stake,
                         msg=f'Total stake amount "{actual_total_stake}" '
                             f'is not the same as free bet "{expected_total_stake}"')

    def test_004_log_out_of_app(self):
        """
        DESCRIPTION: Log out of app
        EXPECTED: User is logged out
        """
        self.site.quick_bet_panel.close()
        self.site.logout()

    def test_005_log_in_with_user_that_has_positive_balance_credit_cards_and_free_bets_added_to_his_account(self):
        """
        DESCRIPTION: Log in with user that has positive balance, credit cards and free bets added to his account
        EXPECTED: User is logged in
        """
        self.__class__.username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=self.username, level='event', id=self.eventID)

        self.site.login(username=self.username)
        self.__class__.user_balance = self.site.header.user_balance
        self.site.open_betslip()
        self.clear_betslip()

    def test_006_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps #2-5
        """
        self.test_001_add_selection_to_quick_bet()
        self.test_002_click_use_free_bet_link_and_select_free_bet_from_the_pop_up()
        self.test_003_enter_value_in_stake_field_that_exceeds_users_balance()
