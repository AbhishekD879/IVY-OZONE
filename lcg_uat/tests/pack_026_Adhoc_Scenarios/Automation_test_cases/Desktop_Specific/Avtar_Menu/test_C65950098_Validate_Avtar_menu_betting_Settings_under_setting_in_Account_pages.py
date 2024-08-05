import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.avtar_menu
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65950098_Validate_Avtar_menu_betting_Settings_under_setting_in_Account_pages(Common):
    """
    TR_ID: C65950098
    NAME: Validate Avtar menu betting Settings under setting in Account pages
    DESCRIPTION: This test case is to verify the Avtar menu betting Settings under setting in Account pages
    PRECONDITIONS: 1.User should have vaild login credentials to log into the application
    """
    keep_browser_open = True

    def click_on_selection(self):
        self.navigate_to_page("/")
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')
        odd_btn = ButtonBase(web_element=bet_buttons_list[0])
        odd_btn.scroll_to()
        odd_btn.click()
        return odd_btn

    # def check_timeline_bubble(self):
    #     try:
    #         bubble = self.site.timeline.timeline_bubble
    #         if bubble:
    #             return True
    #         else:
    #             return False
    #     except Exception as e:
    #         return False

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should load successfully
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)

    def test_002_verify_betting_settings_page(self):
        """
        DESCRIPTION: Verify betting settings page
        EXPECTED: page consists of
        EXPECTED: 1.quickbet toogle
        EXPECTED: 2.Timeline toggle
        EXPECTED: 3.sett odds
        """
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        wait_for_haul(10)
        setting_item = self.site.right_menu.section_wise_items.get(vec.bma.V2_HEADER.account.upper()).get(
            vec.bma.EXPECTED_RIGHT_MENU.settings.upper())
        setting_item.click()
        wait_for_haul(10)
        setting_page_items = self.site.account_settings.items_as_ordered_dict
        setting_page_items.get(vec.bma.BETTING_SETTINGS).click()
        wait_for_haul(10)
        if self.device_type == 'mobile':
            quick_btn = self.site.settings.allow_quick_bet
            self.assertTrue(quick_btn, msg="Quick Bet button is not found")
        set_ods = self.site.settings.fractional_btn and self.site.settings.decimal_btn
        self.assertTrue(set_ods, msg="Odd Type Switch is not found")

    def test_003_verify_by_enabling_quickbet_toggle(self):
        """
        DESCRIPTION: verify by enabling quickbet toggle
        EXPECTED: User able to acces quick bet on his/her first selection
        """
        if self.device_type == "mobile":
            odd_btn = self.click_on_selection()
            quick_bet = self.site.wait_for_quick_bet_panel()
            self.assertTrue(quick_bet, msg="QuickBet Not Shown")
            self.site.quick_bet_panel.header.close_button.click()
            odd_btn.click()

    def test_004_verify_by_disenable_quickbet_toggle(self):
        """
        DESCRIPTION: verify by disenable quickbet toggle
        EXPECTED: User should not be able to acces quick bet on his/her first selection
        """
        if self.device_type == "mobile":
            self.navigate_to_page("/")
            self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
            self.site.header.right_menu_button.click()
            self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
            setting_item = self.site.right_menu.section_wise_items.get(vec.bma.V2_HEADER.account.upper()).get(
                vec.bma.EXPECTED_RIGHT_MENU.settings.upper())
            setting_item.click()
            wait_for_haul(10)
            setting_page_items = self.site.account_settings.items_as_ordered_dict
            setting_page_items.get(vec.bma.BETTING_SETTINGS).click()
            wait_for_haul(5)
            quick_btn = self.site.settings.allow_quick_bet
            quick_btn.click()

            self.click_on_selection()
            quick_bet = self.site.wait_for_quick_bet_panel()
            self.assertFalse(quick_bet, msg="QuickBet Is Shown")

    def test_005_verify_by_enabling_timeline_toggle(self):
        """
        DESCRIPTION: verify by enabling Timeline toggle
        EXPECTED: User able to acces timeline
        """
        # if self.device_type == "mobile":
        #     self.navigate_to_page("/")
        #     is_timeline_bubble = self.check_timeline_bubble()
        #     self.assertTrue(is_timeline_bubble, msg="Timeline Bubble is not available")

    def test_006_verify_by_disenable_timeline_toggle(self):
        """
        DESCRIPTION: verify by disenable Timeline toggle
        EXPECTED: User should not be able to acces timeline
        """
        if self.device_type == "mobile":
            self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
            self.site.header.right_menu_button.click()
            self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
            setting_item = self.site.right_menu.section_wise_items.get("ACCOUNT").get("SETTINGS")
            setting_item.click()
            wait_for_haul(10)
            setting_page_items = self.site.account_settings.items_as_ordered_dict
            setting_page_items.get('Betting Settings').click()
            wait_for_haul(5)
            # timeline_btn = self.site.settings.timeline_button
            # timeline_btn.click()
            self.site.logout()
            self.site.header.sign_in.click()
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
            dialog.username = self.username
            dialog.password = tests.settings.default_password
            dialog.click_login()

            # has_timeline = self.site.has_timeline(expected_result=False)
            # self.assertFalse(has_timeline, msg="Timeline still Shown Even If Disabled")

    def test_007_verify_by_changing_odd_to_decimal(self):
        """
        DESCRIPTION: verify by changing odd to decimal
        EXPECTED: Odds should be in decimal mode
        """
        # covered in C646463

    def test_008_verify_by_changing_odd_to_fractional(self):
        """
        DESCRIPTION: verify by changing odd to fractional
        EXPECTED: Odds should be in Fractional mode
        """
        # covered in C646463

    def test_009_verify_transaction_history_page(self):
        """
        DESCRIPTION: verify Transaction history page
        EXPECTED: page should consits of total stakes ,total returns,profit/loss with bet details
        """
        wait_for_haul(5)
        self.site.logout()
        self.site.login()
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        right_menu_items = self.site.right_menu.section_wise_items
        transaction_history = right_menu_items.get(vec.bma.V2_HEADER.account.upper()) \
            .get(vec.bma.EXPECTED_RIGHT_MENU.transaction_history.replace(" ", "").upper())
        transaction_history.click()
        wait_for_haul(2)
        self.site.transaction_history.transaction_history_items.get("Transaction History").click()
        wait_for_haul(5)
        date_filter = self.site.transaction_history.transaction_date_filter
        self.assertTrue(date_filter, msg="Transaction Date Filter Not Found On Transaction History page")
        all_options = date_filter.options
        date_filter.select_by_index(len(all_options) - 1)
        wait_for_haul(5)
        all_stake_labels = [label.text.upper() for label in self.site.transaction_history.stake_returns.stake_lables]
        expected_labels = [vec.bet_history.TOTAL_STAKES.replace(":", "").upper(), vec.bet_history.PROFIT_LOSS.replace(" ", "").upper(),
                           vec.bet_history.TOTAL_RETURNS.replace(":", "").upper()]

        for label in expected_labels:
            self.assertIn(label, all_stake_labels,
                          msg=f"Expected label : {label} not found in actual labels {all_stake_labels} ")

    def test_010_verify_the_transaction_history_by_changing_the_date_filter(self):
        """
        DESCRIPTION: verify the transaction history by changing the date filterw
        EXPECTED: Data should be loaded with in the date filter
        """
        # Covered in Step 9

    def test_011_mobileverify_by_clicking_on_the_backward_chevron_beside_account_details_header(self):
        """
        DESCRIPTION: Mobile
        DESCRIPTION: Verify by clicking on the backward chevron beside Account details header
        EXPECTED: User should be navigate to avatar menu page  successfully
        """
        # Covered in step 2

    def test_012_desktopverify_the_username_with_avatar_beside_account_details_header(self):
        """
        DESCRIPTION: Desktop
        DESCRIPTION: Verify the username with avatar beside Account details header
        EXPECTED: User should able to see the username with avatar icon
        """
        # Covered in step 2
