import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17752134_Vanilla_Place_bet_after_account_closure(BaseCashOutTest, BaseUserAccountTest):
    """
    TR_ID: C17752134
    NAME: [Vanilla] Place bet after account closure
    DESCRIPTION: This test case verifies bet placement after Sports product closure
    """
    keep_browser_open = True
    deposit_amount = 20.00

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in and have **Sports** product closed
        PRECONDITIONS: **How to close your account:**
        PRECONDITIONS: Log In -> 'My Account' -> 'Gambling Control'/'Responsible Gambling' -> 'Account Management'/'Account Closure&Reopening' -> click 'Choose' button -> select 'I want to close my account or section of it' -> select 'Sports' category -> set 'Duration' and 'Reason for closure' -> tap 'Close' button
        """
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=user_name, amount=self.deposit_amount, card_number=tests.settings.quick_deposit_card)
        self.site.login(username=user_name)
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=40)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg=f'"Gambling Controls" page is not found. Page url is "{page_url}" instead of "{expected_url}"')
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.assertTrue(self.site.gambling_controls_page.choose_button.is_displayed(),
                        msg=f'"{self.site.gambling_controls.choose_button.name}" button is not displayed')
        self.site.gambling_controls_page.choose_button.click()
        self.assertEqual(self.device.active_tab_title(), vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE,
                         msg=f'"{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION}" page title is incorrect. Page title is "{self.device.active_tab_title()}" instead of "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE}"')
        self.site.wait_splash_to_hide(7)
        self.assertFalse(self.site.account_closure.continue_button.is_enabled(expected_result=False),
                         msg=f'"{vec.account.CONTINUE}" button is not disabled')
        options = self.site.account_closure.items
        self.assertTrue(options, msg=f'"{options}" are not available')
        options[0].click()
        self.assertTrue(self.site.account_closure.continue_button.is_enabled(), msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.account_closure.continue_button.click()
        self.assertEqual(self.device.active_tab_title(), vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE,
                         msg=f'"{vec.account.ACCOUNT_CLOSURE}" page title is incorrect. Page title is "{self.device.active_tab_title()}" instead of "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_PAGE_TITLE}"')
        self.site.service_closure.items_as_ordered_dict[vec.SB.LOBBY].close_button.click()
        self.assertTrue(self.site.service_closure.duration_options.is_displayed(), msg='"Duration" options are not available')
        duration_options = self.site.service_closure.duration_options.items
        self.assertTrue(duration_options, msg=f'"{duration_options}" are not available')
        duration_options[0].click()

        reason_options = self.site.service_closure.reason_options.items
        self.assertTrue(reason_options, msg=f'"{reason_options}" are not available')
        reason_options[0].click()

        self.site.service_closure.continue_button.perform_click()
        self.site.service_closure.close_button.click()
        actual_info_text = self.site.service_closure.info_message.text
        self.assertEqual(actual_info_text, vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_SPORTS_INFO_TEXT,
                         msg=f'Actual text: "{actual_info_text}" is not same as Expected text: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_SPORTS_INFO_TEXT}"')

    def test_001_make_a_bet_selection(self):
        """
        DESCRIPTION: Make a bet selection
        EXPECTED: Selection is added to Bet Slip.
        """
        selection_ids = []
        self.navigate_to_page('Home')
        if tests.settings.backend_env == 'prod':
            selection_ids = self.get_active_event_selections_for_category()
        else:
            selection_ids = self.ob_config.add_autotest_premier_league_football_event(in_play_event=False).selection_ids
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0])

    def test_002_enter_stake(self):
        """
        DESCRIPTION: Enter stake
        EXPECTED: Stake is added
        """
        # Covered in below step

    def test_003_click_the_place_bet_button(self):
        """
        DESCRIPTION: Click the **Place bet** button
        EXPECTED: Bet is not placed.
        """
        self.place_and_validate_single_bet()
        actual_message = self.get_betslip_content().suspended_account_warning_message.text
        self.assertEqual(actual_message, vec.betslip.ACCOUNT_SUSPENDED,
                         msg=f'Actual suspension message: "{actual_message}" is not same as expected suspension message: "{vec.betslip.ACCOUNT_SUSPENDED}"')
        if self.device_type == 'mobile':
            self.site.betslip.close_button.click()

    def test_004_go_to_settled_bets(self):
        """
        DESCRIPTION: Go to **Settled Bets**
        EXPECTED: Bet is not present there
        """
        self.site.open_my_bets_settled_bets()
        no_bet_text = self.site.bet_history.tab_content.accordions_list.no_bets_message
        self.assertEqual(no_bet_text, vec.bet_history.NO_HISTORY_INFO,
                         msg=f'Text "{no_bet_text}" is not the same as expected "{vec.bet_history.NO_HISTORY_INFO}" & bet history is present, which should not present')
        if self.device_type == 'mobile':
            self.assertTrue(self.site.bet_history.tab_content.accordions_list.start_betting_button, msg='"Start beating" button is not displayed, whereas it should display if no bets is present')

    def test_005_go_to_cash_out(self):
        """
        DESCRIPTION: Go to **Cash out**
        EXPECTED: Bet is not present there
        """
        if tests.settings.brand == 'bma':
            self.site.open_my_bets_cashout()
            cashout = self.site.cashout.tab_content.accordions_list
            self.assertTrue(cashout.no_bets_text, msg='You have no Cash Out bets available text is not present')
            self.assertEqual(cashout.no_bets_text, vec.bet_history.NO_CASHOUT_BETS,
                             msg=f'Message "{cashout.no_bets_text}" does not match expected 'f'"{vec.bet_history.NO_CASHOUT_BETS}" & bet history is present, which should not present')
            if self.device_type == 'mobile':
                self.assertTrue(cashout.start_betting_button, msg='"Start beating" button is not displayed')

    def test_006_go_to_open_bets(self):
        """
        DESCRIPTION: Go to **Open bets**
        EXPECTED: Bet is not present there
       """
        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list
        self.assertEqual(open_bets.no_bets_text, vec.bet_history.NO_OPEN_BETS, msg='Message "%s" does not match expected "%s"' % (open_bets.no_bets_text, vec.bet_history.NO_OPEN_BETS))
        if self.device_type == 'mobile':
            self.assertTrue(open_bets.start_betting_button, msg='"Start beating" button is not displayed')
