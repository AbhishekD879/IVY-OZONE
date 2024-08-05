import pytest
import tests
from tests.base_test import vtest
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C59491115_Vanilla_Verify_automatic_balance_updating_on_Banking_menu(BaseBetSlipTest):
    """
    TR_ID: C59491115
    NAME: [Vanilla] Verify automatic balance updating on 'Banking' menu
    DESCRIPTION: This test case verifies automatic balance updating in Banking menu
    PRECONDITIONS: User should have at least one payment method registered for his/her account (e.g. credit/debit card with money) to have ability to perform Deposit and Withdraw actions
    PRECONDITIONS: 1. Login into application with user who has positive balance
    PRECONDITIONS: 2. Navigate to My Account > 'Banking'/'Banking & Balances' menu > 'My Balance'
    """
    keep_browser_open = True
    bet_amount = 1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login to the app and navigate to My Balance
        EXPECTED: Logged into the app and navigated to My Balance section from account menu
        """
        self.site.login()
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_id, self.__class__.market_id = event.event_id, event.default_market_id
            self.__class__.selection_id = list(event.selection_ids.values())[0]
        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
            outcomes_resp = market['market']['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                                 for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
            self.__class__.selection_id = list(all_selection_ids.values())[0]
        banking_item = 'BANKING' if self.brand == 'bma' else 'Banking & Balances'
        self.site.header.right_menu_button.avatar_icon.click()
        self.site.right_menu.click_item(banking_item, timeout=10)
        self.site.right_menu.click_item('My Balance', timeout=10)
        self.__class__.user_balance = self.site.header.user_balance

    def test_001_place_a_bet_and_verify_balance_info_displayed_in_banking_menu(self):
        """
        DESCRIPTION: Place a bet and verify balance info displayed in 'Banking' menu
        EXPECTED: Balance is updated automatically after successful bet placement, it is decremented by entered stake
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        section = self.get_betslip_sections().Singles
        _, selection = list(section.items())[0]
        selection.amount_form.input.value = self.bet_amount
        self.__class__.betslip_estimated_returns = selection.est_returns
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()
        updated_balance = self.site.header.user_balance
        expected_updated_balance = self.user_balance - self.bet_amount
        self.assertAlmostEqual(expected_updated_balance, updated_balance,
                               msg=f'Expected balance "{expected_updated_balance}" is not same as Actual balance "{updated_balance}"')

    def test_002_verify_balance_in_case_you_win_a_bet(self):
        """
        DESCRIPTION: Verify Balance in case you win a bet
        EXPECTED: Balance is updated automatically in Banking menu, it is incremented by 'Total Estimated Return'
        """
        current_user_balance = self.site.header.user_balance
        if tests.settings.backend_env != 'prod':
            self.ob_config.update_selection_result(selection_id=self.selection_id, market_id=self.market_id,
                                                   event_id=self.event_id)
            banking_item = 'BANKING' if self.brand == 'bma' else 'Banking & Balances'
            self.site.header.right_menu_button.avatar_icon.click()
            self.site.right_menu.click_item(banking_item)
            self.site.right_menu.click_item('My Balance')
            current_url = self.device.get_current_url()
            sleep(3)
            self.device.refresh_page()
            self.device.navigate_to(url=current_url)
            expected_updated_balance = round(current_user_balance + float(self.betslip_estimated_returns))
            updated_user_balance = round(self.site.header.user_balance)
            self.assertEqual(expected_updated_balance, updated_user_balance,
                             msg=f'Expected balance "{expected_updated_balance}" is not same as "{updated_user_balance}"')
            self.site.right_menu.close_icon.click()

    def test_003_make_a_deposit_to_your_account_and_verify_balance_info_displayed_in_banking_menu(self):
        """
        DESCRIPTION: Make a deposit to your account and verify balance info displayed in Banking menu
        EXPECTED: Balance is updated immediately in Banking menu, it is incremented by entered Deposit amount
        """
        current_balance = self.site.header.user_balance
        self.site.header.right_menu_button.avatar_icon.click()
        self.site.right_menu.deposit_button.click()
        self.site.wait_content_state_changed()
        deposit_amount = 10.00
        self.site.wait_splash_to_hide()
        if self.device_type != 'mobile':
            self.device.driver.set_window_size(width=800, height=1600)
        self.site.deposit.add_new_card_and_deposit(amount=deposit_amount, cvv_2=tests.settings.master_card_cvv)
        self.site.wait_for_deposit_pop_up_closed(timeout=10)
        self.site.deposit.close_button.click()
        if self.device_type == 'mobile':
            self.site.right_menu.close_icon.click()
        self.site.wait_content_state('HomePage', timeout=5)
        actual_balance = self.site.header.user_balance
        expected_balance = current_balance + float(deposit_amount)
        self.assertEqual(actual_balance, expected_balance,
                         msg=f'Actual user balance "{actual_balance}" != Expected "{expected_balance}"')

    def test_004_perform_withdraw_action_from_users_account_and_verify_balance_info_displayed_in_banking_menu(self):
        """
        DESCRIPTION: Perform Withdraw action from user's account and verify balance info displayed in Banking menu
        EXPECTED: Balance is updated immediately in Banking menu, it is incremented by entered Withdrawal amount
        """
        # Cannot be automated
