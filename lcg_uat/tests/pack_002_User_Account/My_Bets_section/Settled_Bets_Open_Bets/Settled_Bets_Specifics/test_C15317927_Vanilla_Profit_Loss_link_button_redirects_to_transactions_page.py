import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.bet_history_open_bets
@vtest
class Test_C15317927_Vanilla_Profit_Loss_link_button_redirects_to_transactions_page(Common):
    """
    TR_ID: C15317927
    NAME: [Vanilla] Profit/Loss link button redirects to transactions page
    DESCRIPTION:
    PRECONDITIONS: User logged in to the application and is on Home page.
    """
    keep_browser_open = True

    def test_001_open_my_account___history___betting_history(self):
        """
        DESCRIPTION: Open My Account -> History -> Betting History
        EXPECTED: My Bets / Settled Bets tab section is opened
        """
        self.site.login()
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2])
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[6])
        self.site.wait_content_state_changed()
        actual_history_menu = list(self.site.right_menu.items_as_ordered_dict)
        self.assertEqual(actual_history_menu, vec.bma.HISTORY_MENU_ITEMS,
                         msg=f'Actual items: "{actual_history_menu}" are not equal with the'
                             f'Expected items: "{vec.bma.HISTORY_MENU_ITEMS}"')
        self.site.right_menu.click_item(vec.bma.HISTORY_MENU_ITEMS[0])
        self.site.wait_content_state('bet-history')
        self.site.wait_content_state_changed()

    def test_002_click_on_profitloss_button(self):
        """
        DESCRIPTION: Click on Profit/Loss button
        EXPECTED: /mobileportal/transactions page is opened
        """
        profit_loss = self.site.bet_history.tab_content.accordions_list.settled_bets
        self.assertTrue(profit_loss, msg='Profit / Loss information not shown')
        profit_loss.click()
        expected_url = "/mobileportal/transactions"
        actual_url = self.device.get_current_url()
        self.assertIn(expected_url, actual_url,
                      msg=f'Expected url: "{expected_url}" is not in actual url: "{actual_url}"')

    def test_003_desktop_mode_go_to_home_page_check_if_see_profit__loss_button_is_displayed_in_my_bets___settled_bets_tab_on_the_right(
            self):
        """
        DESCRIPTION: [Desktop mode] Go to Home page, check if "See Profit / Loss" button is displayed in 'My Bets' -> 'Settled Bets' tab on the right
        EXPECTED: "See Profit / Loss" button is visible
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='Home')
            self.site.wait_content_state('HomePage')
            self.site.open_my_bets_settled_bets()

    def test_004_desktop_mode_click_on_profitloss_button(self):
        """
        DESCRIPTION: [Desktop mode] Click on Profit/Loss button
        EXPECTED: /mobileportal/transactions page is opened
        """
        if self.device_type == 'desktop':
            profit_loss = self.site.bet_history.tab_content.accordions_list.settled_bets
            self.assertTrue(profit_loss, msg='Profit / Loss information not shown')
            profit_loss.click()
            expected_url = "/mobileportal/transactions"
            actual_url = self.device.get_current_url()
            self.assertIn(expected_url, actual_url,
                          msg=f'Expected url: "{expected_url}" is not in actual url: "{actual_url}"')
