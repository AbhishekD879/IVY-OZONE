import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result, wait_for_haul

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.avtar_menu
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65950087_Validate_Avtar_menu_Account_closureReopening_gambling_controls(BaseBetSlipTest):
    """
    TR_ID: C65950087
    NAME: Validate Avtar menu Account closure&Reopening gambling controls
    DESCRIPTION: This test case is to verify the Avtar menu Account closure&Reopening gambling controls
    PRECONDITIONS: 1.User should have vaild login credentials to log into the application
    """
    keep_browser_open = True
    account_closure_and_reopening = vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION
    account_closure_and_opening_item_names = ['I want to block certain products on my account','I want to close my account',
                                              'I want to take a break for up to 6 weeks','I want to close my account as I might have a gambling problem']
    sports_book = 'Sportsbook'

    def create_new_user(self):
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='20',
                                                                     card_number='5137651100600001',
                                                                     card_type='mastercard',
                                                                     expiry_month='12',
                                                                     expiry_year='2080',
                                                                     cvv='123'
                                                                     )
        return username

    def validating_bet_placement(self):
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        outcomes = next(((market['market']['children']) for market in events['event']['children'] if
                         market['market'].get('children')), None)
        event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        selection_id = list(event_selection.values())[0]
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.place_single_bet()
        expected_error_message = vec.Quickbet._bet_placement_errors_account_suspended
        actual_error_message = wait_for_result(lambda :self.site.betslip.betslip_sections_list.default_notification, timeout=10)
        self.assertEqual(actual_error_message,expected_error_message, msg=f'actual error message {actual_error_message} is not '
                                                                          f'equal to expected error message {expected_error_message}')
        list(self.get_betslip_sections().Singles.values())[0].remove_button.click()

    def validating_logging_in(self, user_name):
        self.site.logout()
        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        dialog.username = user_name
        dialog.password = tests.settings.default_password
        dialog.click_login()
        wait_for_haul(5)
        not_login = dialog.error_message
        self.assertTrue(not_login, msg=f"Login successful even user {user_name} is blocked for gambling problem")
        dialog.close_dialog()
        dialog.wait_dialog_closed()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=2)
        self.assertFalse(dialog, msg='"Log In" dialog should not be displayed on the screen')

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded succesfully
        """
        username = self.create_new_user()
        self.site.login(username=username)
        self.site.wait_content_state(state_name='HomePage')

    def test_002_verify_by_clicking_account_closureampreopening(self):
        """
        DESCRIPTION: Verify by clicking Account closure&amp;Reopening
        EXPECTED: User should be able to see the data
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(timeout=5),
                        msg='User menu is not opened')
        self.site.right_menu.click_item(item_name=self.site.window_client_config.gambling_controls_title)
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=10),
                        msg=f'"Gambling Controls" page is not opened')
        gambling_controls_items = self.site.gambling_controls.items_as_ordered_dict
        self.assertTrue(gambling_controls_items, msg= 'items in gambling control is available')
        self.assertIn(self.account_closure_and_reopening, gambling_controls_items.keys(), msg=f'item {self.account_closure_and_reopening} '
                                                                                              f'is not present in {gambling_controls_items.keys()}')
        self.__class__.account_closure_and_reopening_value = self.site.gambling_controls.items_as_ordered_dict.get(self.account_closure_and_reopening)
        if self.device_type == 'mobile' and not self.account_closure_and_reopening_value.is_expanded():
            self.account_closure_and_reopening_value.click()

    def test_003_verify_by_clicking_i_want_to_block_certaian_products_on_my_account(self):
        """
        DESCRIPTION: Verify by clicking I want to block certaian products on my account
        EXPECTED: User should able to close the account or certain products by selecting within time dropdown
        """
        account_closure_and_reopening_items = wait_for_result(lambda : self.account_closure_and_reopening_value.items_as_ordered_dict, timeout=10)
        self.assertIn(self.account_closure_and_opening_item_names[0],account_closure_and_reopening_items.keys(), msg=
                      f'{self.account_closure_and_opening_item_names[0]} not present in {account_closure_and_reopening_items.keys()}')
        account_closure_and_reopening_items.get(self.account_closure_and_opening_item_names[0]).click()
        has_close_account_button = self.site.account_closure.has_close_account_button()
        self.assertTrue(has_close_account_button, msg='"CLOSE ACCOUNT" button is not displayed')
        account_closure_items = self.site.account_closure.items_as_ordered_dict
        self.assertTrue(account_closure_items, msg=f'available products {account_closure_items.keys()} is not available')

    def test_004_verify_by_blocking_certain__products(self):
        """
        DESCRIPTION: Verify by blocking certain  products
        EXPECTED: User can  able to login but unabale to place bets
        """
        account_closure_items = self.site.account_closure.items_as_ordered_dict
        self.assertIn(self.sports_book, account_closure_items.keys(), msg=f'{self.sports_book} is not present in {account_closure_items.keys()}')
        account_closure_items.get(self.sports_book).block_button.click()
        self.site.account_closure_overlay.continue_button.click()
        date_filter = self.site.account_closure_overlay.blocking_date_filter
        self.assertTrue(date_filter, msg='date filter is not present')
        if self.device_type=='desktop':
            self.assertFalse(self.site.account_closure.continue_button.is_enabled(), msg='continue button is enable without fill date filter')
            date_filter.select_by_index(1)
            self.assertTrue(self.site.account_closure.continue_button.is_enabled(),
                             msg='continue button is disabled')
            self.site.account_closure.continue_button.click()
            self.site.account_closure.confirm_block_button.click()
        else:
            self.assertFalse(self.site.account_closure_overlay.sports_book_service_closure.continue_button.is_enabled(), msg='continue button is enable')
            date_filter.select_by_index(1)
            self.assertTrue(self.site.account_closure_overlay.sports_book_service_closure.continue_button.is_enabled(),
                            msg='continue button is disabled')
            self.site.account_closure_overlay.sports_book_service_closure.continue_button.click()
            self.site.account_closure_overlay.sports_book_service_closure.confirm_block_button.click()
        self.site.account_closure.account_closure_header.close_button.click()
        self.validating_bet_placement()
        self.site.logout()

    def test_005_verify_by_clicking_i_want_to_close__my_account(self):
        """
        DESCRIPTION: Verify by clicking I want to close  my account
        EXPECTED: User should able to close the account or certain products by selecting within time dropdown
        # """
        username = self.create_new_user()
        self.site.login(username=username)
        self.site.wait_content_state(state_name='HomePage')
        self.test_002_verify_by_clicking_account_closureampreopening()
        account_closure_and_reopening_items = wait_for_result(lambda: self.account_closure_and_reopening_value.items_as_ordered_dict, timeout=10)
        self.assertIn(self.account_closure_and_opening_item_names[1], account_closure_and_reopening_items.keys(), msg=
                      f'{self.account_closure_and_opening_item_names[1]} not present in {account_closure_and_reopening_items.keys()}')
        account_closure_and_reopening_items.get(self.account_closure_and_opening_item_names[1]).click()
        has_close_account_button = self.site.account_closure.has_close_account_button()
        self.assertTrue(has_close_account_button, msg='"CLOSE ACCOUNT" button is not displayed')
        account_closure_items = self.site.account_closure.items_as_ordered_dict
        self.assertTrue(account_closure_items,
                        msg=f'available products {account_closure_items.keys()} is not available')

    def test_006_verify_by_blocking_certain__products(self):
        """
        DESCRIPTION: Verify by blocking certain  products
        EXPECTED: User can able to login but unabale to place bets
        """
        self.test_004_verify_by_blocking_certain__products()

    def test_007_verify_by_clicking_i_want_to_take_break_upto_6_weeks(self):
        """
        DESCRIPTION: Verify by clicking I want to take break upto 6 weeks.
        EXPECTED: User should able to close the account by selecting within time dropdown upto 6 weeks
        """
        username = self.create_new_user()
        self.site.login(username=username)
        self.test_002_verify_by_clicking_account_closureampreopening()
        account_closure_and_reopening_items = wait_for_result(lambda: self.account_closure_and_reopening_value.items_as_ordered_dict, timeout=10)
        self.assertIn(self.account_closure_and_opening_item_names[2], account_closure_and_reopening_items.keys(), msg=
                      f'{self.account_closure_and_opening_item_names[2]} not present in {account_closure_and_reopening_items.keys()}')
        account_closure_and_reopening_items.get(self.account_closure_and_opening_item_names[2]).click()
        date_filter = self.site.account_closure.time_out_layout.blocking_date_filter
        self.assertTrue(date_filter, msg='date filter is not present')
        continue_button = self.site.account_closure.time_out_layout.continue_button
        self.assertFalse(continue_button.is_enabled(), msg='"CONTINUE" button is enable')
        date_filter.select_by_index(1)
        self.assertTrue(continue_button.is_enabled(),
                         msg='"CONTINUE" button is disable')
        continue_button.click()
        self.site.account_closure_overlay.continue_button.click()
        self.site.account_closure_overlay.time_out_wrapper.confirm_time_out_button.click()
        wait_for_haul(5)
        self.site.account_closure.time_out_layout.header.close_button.click()
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='HomePage')
        self.validating_logging_in(user_name=username)

    def test_008_verify_by_clicking_immediate_24_hour_break(self):
        """
        DESCRIPTION: Verify by clicking immediate 24 hour break
        EXPECTED: User should be blocked fro 24 hours from the application .
        """
        # already covered in C65950083

    def test_009_verify_by_clicking_i_want_to_close_my_account_as_i_mighthave_gambling_problem(self):
        """
        DESCRIPTION: verify by clicking I want to close my account as I mighthave gambling problem
        EXPECTED: User should get self exculded unable to login
        """
        username = self.create_new_user()
        self.site.login(username=username)
        self.test_002_verify_by_clicking_account_closureampreopening()
        account_closure_and_reopening_items = wait_for_result(
            lambda: self.account_closure_and_reopening_value.items_as_ordered_dict, timeout=10)
        self.assertIn(self.account_closure_and_opening_item_names[3], account_closure_and_reopening_items.keys(), msg=
        f'{self.account_closure_and_opening_item_names[3]} not present in {account_closure_and_reopening_items.keys()}')
        account_closure_and_reopening_items.get(self.account_closure_and_opening_item_names[3]).click()
        self_exclusion = wait_for_result(lambda : self.site.account_closure.self_exclusion, timeout=5)
        self.assertTrue(self_exclusion, msg='self exclusion page is not present')
        wait_for_haul(5)
        self.site.account_closure.self_exclusion.exclude_me_button.click()
        self.site.account_closure.self_exclusion.continue_process_button.click()
        self.site.account_closure_overlay.self_exclusion_wrapper.continue_button.click()
        if self.device_type=='mobile':

            date_filter = self.site.account_closure_overlay.blocking_date_filter
            self.assertTrue(date_filter,msg='date filter is not present')
            self.assertFalse(self.site.account_closure_overlay.self_exclusion_wrapper.continue_button.is_enabled(),
                             msg='continue button is enable')
            date_filter.select_by_index(1)
            self.assertTrue(self.site.account_closure_overlay.self_exclusion_wrapper.continue_button.is_enabled(),
                             msg='continue button is disable')
            self.site.account_closure_overlay.self_exclusion_wrapper.continue_button.click()
            self.site.account_closure_overlay.self_exclusion_wrapper.password.value=tests.settings.default_password
            self.site.account_closure_overlay.self_exclusion_wrapper.confirm_self_exclusion_button.click()
        else:
            date_filter = self.site.account_closure.blocking_date_filter
            self.assertTrue(date_filter, msg='date filter is not present')
            self.assertFalse(self.site.account_closure.self_exclusion.continue_button.is_enabled(),
                             msg='continue button is enable')
            date_filter.select_by_index(1)
            self.assertTrue(self.site.account_closure.self_exclusion.continue_button.is_enabled(),
                            msg='continue button is disable')
            self.site.account_closure.self_exclusion.continue_button.click()
            self.site.account_closure.self_exclusion.password.value=tests.settings.default_password
            self.site.account_closure.self_exclusion.confirm_self_exclusion_button.click()
        wait_for_haul(5)
        self.site.account_closure.self_exclusion.header.close_button.click()
        self.site.wait_content_state(state_name='HomePage')
        self.validating_logging_in(user_name=username)

    def test_010_mobileverify_by_clicking_on_the_backward_chevron_beside_gambling_controls_header(self):
        """
        DESCRIPTION: Mobile
        DESCRIPTION: verify by clicking on the backward chevron beside gambling controls header
        EXPECTED: User should be navigate to avatar menu page  successfully
        """
        self.site.login()
        self.test_002_verify_by_clicking_account_closureampreopening()
        if self.device_type == 'mobile':
            backward_chevron = self.site.gambling_controls.header_line.back_button
            self.assertTrue(backward_chevron, msg='backward chevron is not available')
            backward_chevron.click()
            self.site.wait_content_state_changed()

    def test_011_desktopverify_the_username_with_avatar_beside_gambling_controls_header(self):
        """
        DESCRIPTION: Desktop
        DESCRIPTION: Verify the username with avatar beside gambling controls header
        EXPECTED: User should able to see the username with avatar icon
        """
        if self.device_type == 'desktop':
            user_name = self.site.gambling_controls.header_line.user_name
            self.assertTrue(user_name, msg='username is not displayed')
            self.assertTrue(self.site.gambling_controls.header_line.avatar.is_displayed(), msg='avatar icon is not displayed')