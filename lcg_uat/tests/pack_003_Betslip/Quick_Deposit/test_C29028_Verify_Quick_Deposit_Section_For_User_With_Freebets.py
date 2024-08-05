import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Freebets cannot be granted on HL/PROD
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.quick_deposit
@pytest.mark.creditcard
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-54228')
# todo: VOL-5692 [tst] Adapt C29028 Section Open User with Free bets
@vtest
class Test_C29028_Verify_Quick_Deposit_Section_For_User_With_Freebets(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C29028
    NAME: Section Open User with Free bets
    DESCRIPTION: This test case verifies 'Quick Deposit' section for user with free bets available
    PRECONDITIONS: 1.User account with **0 balance,
    PRECONDITIONS: at least one registered Credit Card and Free Bets available**
    PRECONDITIONS: 2.User account with **positive balance,
    PRECONDITIONS: at least one registered Credit Card ****and Free Bets available**
    PRECONDITIONS: Applies for **Mobile** and **Tablet**
    """
    keep_browser_open = True
    stake_input = 5

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Add Football event
        """
        self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids

    def test_001_load_application_and_log_in_with_account_1(self):
        """
        DESCRIPTION: Load application
        DESCRIPTION: Log in with account #1
        EXPECTED: Homepage is shown
        EXPECTED: User is logged in
        """
        username = tests.settings.freebet_user_0_balance
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_add_selection_to_the_bet_slip_via_deeplink(self):
        """
        DESCRIPTION: Add any selection(s) to the Bet Slip and Open the Betslip page/widget
        EXPECTED: - Made selection(s) is displayed within Betslip content area
        EXPECTED: **from OX 99**: Use Freebet Link is displayed for selection
        EXPECTED: **Coral**
        EXPECTED: * 'QUICK DEPOSIT' section is displayed on the bottom of the Bet Slip
        EXPECTED: **Ladbrokes**
        EXPECTED: - There is NO 'Quick Deposit' section or error message displayed on the Bet Slip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])
        self.__class__.section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(self.section.items())[0]
        self.assertTrue(self.stake.has_use_free_bet_link(), msg='Use Free Bet link is not displayed')

        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='Quick Deposit is not displayed')

    def test_003_go_to_free_bet_available_drop_down_and_select_one_of_available_free_bets(self):
        """
        DESCRIPTION: Click on Use Free Bet link and select one of available Free bets
        EXPECTED: Free bet is chosen for selection(s)
        EXPECTED: 'QUICK DEPOSIT' section in NOT shown (as 'Total Stake' = 'Free Bet Stake')
        """
        self.stake.freebet_tooltip.click()
        self.stake.use_free_bet_link.click()
        freebet_value = self.select_free_bet()

        betslip = self.get_betslip_content()
        self.assertEqual(self.get_betslip_content().total_stake, freebet_value,
                         msg=f'Total stake: "{self.get_betslip_content().total_stake}" != Freebet stake: "{freebet_value}"')
        if self.device_type == 'mobile':
            self.assertFalse(betslip.has_deposit_form(expected_result=False), msg='Quick Deposit is displayed')
            self.assertFalse(betslip.keyboard.is_displayed(expected_result=False),
                             msg='Numeric keyboard is unexpectedly shown')

    def test_004_enter_stake_for_the_added_selections(self):
        """
        DESCRIPTION: Enter 'Stake' for the added selection(s) which amount exceeds user balance
        EXPECTED: Value on 'Please deposit a min of <currency>XX.XX to continue placing your bet' default message is changed according to entered stake
        """
        stake_value = self.stake_input + self.user_balance

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        stake_bet_amounts = {
            stake_name: stake_value,
        }
        self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts=stake_bet_amounts)
        info_panel_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(self.stake_input)
        self.assertEqual(info_panel_text, expected_message_text,
                         msg=f'Error message "{info_panel_text}" is not the same as expected "{expected_message_text}"')

    def test_005_clear_bet_slip_and_log_out(self):
        """
        DESCRIPTION: Clear Bet Slip -> Log Out
        EXPECTED: User is logged out
        """
        self.clear_betslip()
        self.site.logout()

    def test_006_log_in_with_account_2(self):
        """
        DESCRIPTION: Log in with account #2
        EXPECTED: User is logged in
        """
        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)
        self.__class__.user_balance = self.site.header.user_balance

    def test_007_add_any_selections_to_the_bet_slip_and_open_the_bet_slip_page_widget(self):
        """
        DESCRIPTION: Add any selection(s) to the Bet Slip and Open the Bet Slip page / widget
        EXPECTED: Made selection(s) is displayed within Bet Slip content area
        EXPECTED: 'Free Bet Available' drop down is present displayed / shown
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])
        self.__class__.section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(self.section.items())[0]
        self.assertTrue(self.stake.has_use_free_bet_link(), msg='Use Free Bet link is not displayed')

    def test_008_select_one_of_available_free_bets_from_free_bet_available_drop_down(self):
        """
        DESCRIPTION: Select one of available Free bets from 'Free Bet Available' drop down
        EXPECTED: Free bet is chosen for selection(s)
        EXPECTED: 'QUICK DEPOSIT' section in NOT displayed (as 'Total Stake' = 'Free Bet Stake')
        EXPECTED: Numeric keyboard is not displayed (if available, mobile only)
        """
        self.test_003_go_to_free_bet_available_drop_down_and_select_one_of_available_free_bets()

    def test_009_enter_stake_for_the_added_selections(self):
        """
        DESCRIPTION: Enter 'Stake' for the added selection(s) which amount exceeds user balance
        EXPECTED: 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where, <currency symbol> - currency that was set during registration 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        stake_value = self.stake_input + self.user_balance

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]

        stake_bet_amounts = {
            stake_name: stake_value,
        }
        self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts=stake_bet_amounts)

        info_panel_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(self.stake_input)
        self.assertEqual(info_panel_text, expected_message_text,
                         msg=f'Error message "{info_panel_text}" is not the same as expected "{expected_message_text}"')

        bet_button_name = self.get_betslip_content().make_quick_deposit_button.name
        self.assertEqual(bet_button_name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Button name "{bet_button_name}" is not '
                             f'the same as expected "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')

    def test_010_tap_make_a_deposit(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: Quick Deposit section is displayed
        """
        self.get_betslip_content().make_quick_deposit_button.click()
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='Quick Deposit is not displayed')
