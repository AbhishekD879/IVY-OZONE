import pytest
from tests.Common import Common
from tests.base_test import vtest
import voltron.environments.constants as vec


# @pytest.mark.uat
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.p3
@vtest
class Test_C44870161_Verify_the_header_for_a_logged_in_user_Desktop_Mobile(Common):
    """
    TR_ID: C44870161
    NAME: "Verify the header for a logged in user (Desktop/Mobile)
    DESCRIPTION: and once clicked on downward facing chevron next to my avatar My Account overlay is shown (with drop down option available, eg: Banking My Bets, Odds Boosts, FreeBets,Redeem Vouchers, Bet History, Personal Details,
    """
    keep_browser_open = True

    def test_001_verify_the_header_for_a_logged_in_user_mobiletablet(self):
        """
        DESCRIPTION: Verify the header for a logged in user Mobile/Tablet
        EXPECTED: User is displayed with My bets/Balance/Avatar/Betslip
        """
        self.site.login()
        if self.device_type == 'mobile':
            if self.brand == 'bma':
                self.assertTrue(self.site.header.my_bets.is_displayed(),
                                msg='"My bets" not displayed')
            self.assertTrue(self.site.header.right_menu_button.avatar_icon.is_displayed(),
                            msg='"Avatar" icon not found')
            self.assertTrue(self.site.header.user_balance_section.is_displayed(),
                            msg='"User balance section" is not found')
            self.assertTrue(self.site.header.bet_slip_counter.is_displayed(),
                            msg='"Betslip" not displayed')

    def test_002_verify_the_header_for_a_logged_in_user_desktop(self):
        """
        DESCRIPTION: Verify the header for a logged in user Desktop
        EXPECTED: User is displayed with Deposit/Balance/Messages/Avatar/
        """
        if self.device_type == 'desktop':
            self.assertTrue(self.site.header.user_panel.deposit_button.is_displayed(),
                            msg='"Deposit button" not found')
            self.assertTrue(self.site.header.user_panel.my_inbox_button.is_displayed(),
                            msg='"Inbox section" not found')
            self.assertTrue(self.site.header.user_balance_section.is_displayed(),
                            msg='"User balance section" not found')
            self.assertTrue(self.site.header.right_menu_button.avatar_icon.is_displayed(),
                            msg='"Avatar icon" not found')

    def test_003_once_clicked_avatar(self):
        """
        DESCRIPTION: Once clicked Avatar
        EXPECTED: My account Menu with the following elements are shown:
        EXPECTED: Banking, Offers & Free bets, History, Messages, Connect, Settings, Gambling Controls, Help & Contact, Logout, Deposit
        """
        self.site.header.right_menu_button.avatar_icon.click()
        Actual_right_menu_items = self.site.right_menu.items_names
        self.assertTrue((item in vec.bma.EXPECTED_LIST_OF_RIGHT_MENU for item in Actual_right_menu_items),
                        msg=f'Actual items: "{Actual_right_menu_items}" are not equal with the '
                            f'Expected items: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU}"')
        if self.brand == 'ladbrokes':
            self.assertTrue(self.site.right_menu.deposit_button.is_displayed(), msg='"Deposit button" is not displayed in my balance section')
        else:
            actual_deposit_and_log_out = [self.site.right_menu.deposit_button.text, self.site.right_menu.log_out_button.text]
            expected_deposit_and_log_out = [vec.bma.RIGHT_MENU_DEPOSIT, vec.bma.RIGHT_MENU_LOGOUT]
            self.assertEqual(actual_deposit_and_log_out, expected_deposit_and_log_out,
                             msg=f'Actual list: "{actual_deposit_and_log_out}" is not same as expected list"{expected_deposit_and_log_out}"')

    def test_004_on_clicking_my_bets(self):
        """
        DESCRIPTION: On clicking 'My bets,
        EXPECTED: My bets with following elements are shown,
        EXPECTED: Cashout, Open bets, Settle bets, Shop bets
        """
        if self.brand == 'ladbrokes':
            if self.device_type == 'mobile':
                self.site.right_menu.click_item(vec.bet_history.TAB_TITLE)
                actual_my_bets_tabs = self.site.open_bets.tabs_menu.items_names
            else:
                self.navigate_to_page("Homepage")
                self.site.open_my_bets_open_bets()
                actual_my_bets_tabs = list(self.site.betslip.tabs_menu.items_as_ordered_dict.keys())
            for item in actual_my_bets_tabs:
                self.assertIn(item, [vec.bet_history.OPEN_BETS_TAB_NAME, vec.bet_history.SETTLED_BETS_TAB_NAME, vec.bet_history.IN_SHOP_BETS_TAB_NAME, vec.bet_history.CASH_OUT_TAB_NAME],
                              msg=f'Actual items"{actual_my_bets_tabs}"is not same as expected items"{[vec.bet_history.OPEN_BETS_TAB_NAME, vec.bet_history.SETTLED_BETS_TAB_NAME, vec.bet_history.IN_SHOP_BETS_TAB_NAME, vec.bet_history.CASH_OUT_TAB_NAME]}"')
        else:
            self.navigate_to_page("Homepage")
            if self.device_type == 'mobile':
                self.site.header.my_bets.click()
                actual_my_bets_tabs = self.site.open_bets.tabs_menu.items_names
            else:
                self.site.open_my_bets()
                actual_my_bets_tabs = list(self.site.betslip.tabs_menu.items_as_ordered_dict.keys())
            for item in actual_my_bets_tabs:
                self.assertIn(item, [vec.bet_history.OPEN_BETS_TAB_NAME, vec.bet_history.SETTLED_BETS_TAB_NAME, vec.bet_history.IN_SHOP_BETS_TAB_NAME, vec.bet_history.CASH_OUT_TAB_NAME],
                              msg=f'Actual items"{actual_my_bets_tabs}"is not same as expected items"{[vec.bet_history.OPEN_BETS_TAB_NAME, vec.bet_history.SETTLED_BETS_TAB_NAME, vec.bet_history.IN_SHOP_BETS_TAB_NAME, vec.bet_history.CASH_OUT_TAB_NAME]}"')

    def test_005_on_clickingbalance(self):
        """
        DESCRIPTION: On clicking'Balance'
        EXPECTED: Following elements are shown,
        EXPECTED: Withdrawable Online
        EXPECTED: Restricted
        EXPECTED: Available Balance
        EXPECTED: Total Balance
        EXPECTED: Deposit
        EXPECTED: Balance available to user on: Sports/Casino/Poker/Bingo
        """
        self.navigate_to_page("Homepage")
        if self.brand == 'ladbrokes':
            self.site.header.right_menu_button.avatar_icon.click()
            self.site.right_menu.click_item('Banking & Balances')
            self.site.right_menu.click_item('My Balance')
            actual_my_balance_items = list(self.site.right_menu.my_balance.items_as_ordered_dict.keys())
            self.assertEqual(actual_my_balance_items, vec.bma.MY_BALANCE_MENU_ITEMS,
                             msg=f'Actual items"{actual_my_balance_items}"is not same as expected items"{vec.bma.MY_BALANCE_MENU_ITEMS}"')
        else:
            self.site.header.user_balance_section.click()
            actual_my_balance_items = list(self.site.right_menu.my_balance.items_as_ordered_dict.keys())
            self.assertEqual(actual_my_balance_items, vec.bma.MY_BALANCE_MENU_ITEMS,
                             msg=f'Actual items"{actual_my_balance_items}"is not same as expected items"{vec.bma.MY_BALANCE_MENU_ITEMS}"')
        self.assertTrue(self.site.right_menu.deposit_button.is_displayed(), msg='"Deposit button" is not displayed in my balance section')
        my_balance_footer_items = self.site.right_menu.my_balance_footer_items.text
        actual_items_list = my_balance_footer_items.split('\n')
        actual_my_balance_footer_items_list = [i for i in actual_items_list if i in vec.bma.EXPECTED_MY_BALANCE_FOOTER_ITEMS_LIST]
        self.assertEqual(actual_my_balance_footer_items_list, vec.bma.EXPECTED_MY_BALANCE_FOOTER_ITEMS_LIST, msg=f'actual list:"{actual_my_balance_footer_items_list}" is not same as expected list"{vec.bma.EXPECTED_MY_BALANCE_FOOTER_ITEMS_LIST}"')
