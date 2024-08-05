import datetime
import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.js_functions import click
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.uat
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.p2
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870133_Verify_deposit_instructions_for_each_deposit_methods(Common):
    """
    TR_ID: C44870133
    NAME: Verify deposit instructions for each deposit methods.
    """
    keep_browser_open = True
    deposit_amount = 20.00

    def navigating_to_deposit(self):
        self.site.wait_content_state_changed()
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')
        right_menu = self.site.right_menu
        right_menu.click_item(item_name=vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0])
        banking_menu_title = right_menu.header.title
        self.assertEqual(banking_menu_title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0],
                         msg=f'Actual text: "{banking_menu_title}" '
                             f'is not same as Expected text: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0]}"')
        banking_menu_items = list(right_menu.get_items().keys())
        self.assertEqual(banking_menu_items, vec.bma.BANKING_MENU_ITEMS,
                         msg=f'Actual items: "{banking_menu_items}"'
                             f'is not same as Expected items: "{vec.bma.BANKING_MENU_ITEMS}"')
        right_menu.click_item(vec.bma.BANKING_MENU_ITEMS[1])
        self.site.wait_content_state_changed()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User has attached credit//debit cards to his account
        PRECONDITIONS: Tap My Account - Click on Banking -> Click on Deposit
        """
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username)
        self.site.wait_content_state("HomePage")
        status = self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=self.deposit_amount,
                                                                          card_number='5137651100600001',
                                                                          card_type='mastercard',
                                                                          expiry_month=f'{now.month:02d}',
                                                                          expiry_year=shifted_year,
                                                                          cvv=tests.settings.master_card_cvv)
        self.assertTrue(status, msg='The card is not added successfully')
        self.navigate_to_page('Home')
        self.site.wait_content_state('HOMEPAGE', timeout=20)
        self.navigating_to_deposit()

    def test_001_user_is_on_deposit_page(self):
        """
        DESCRIPTION: User is on Deposit page
        EXPECTED: Validate following  fields on Deposit page
        EXPECTED: 'Deposit' header and 'X' button (Note: This step is applicable for mobile only)
        EXPECTED: On desktop there is no 'X' button. The deposit window closes, when the user clicks anywhere outside the box.
        EXPECTED: Currency
        EXPECTED: Amount edit field
        EXPECTED: 'X' button inside the Amount field box
        EXPECTED: Quick deposit of £20, £50, £100
        EXPECTED: Credi/Debit card section consists of:
        EXPECTED: Credit/Debit card Dropdown and Placeholder
        EXPECTED: Card number displayed in the next format: XXXX **** **** XXXX
        EXPECTED: (where 'XXXX' - the first and last 4 number of the card)
        EXPECTED: 'Other payment options' under Dropdown.
        EXPECTED: CVV2 field
        EXPECTED: Transaction currency
        EXPECTED: 'i' information tool tip
        EXPECTED: Optional Bonus code
        EXPECTED: Option to enter Bonus code when clicked on the arrow next to it
        EXPECTED: Deposit button
        """
        if self.device_type == 'mobile':
            self.assertTrue(wait_for_result(lambda: self.site.deposit.deposit_title.is_displayed(), timeout=15),
                            msg='Deposit Header is not displayed')
            self.assertTrue(wait_for_result(lambda: self.site.deposit.close_button.is_displayed(), timeout=15),
                            msg='Deposit close button is not displayed')
        else:
            self.device.driver.set_window_size(width=1600, height=1600)
            try:
                self.assertFalse(self.site.deposit.close_button, msg='Deposit close button is displayed')
            except VoltronException:
                self._logger.info("The close button is not displayed in Deposit")
        self.site.wait_content_state_changed()
        # Cannot validate The deposit window closes, when the user clicks anywhere outside the box in automation
        self.quick_deposit_menu = self.site.deposit.stick_to_iframe()
        self.assertTrue(self.quick_deposit_menu.amount.is_displayed(),
                        msg='The Amount text field is not displayed')
        self.assertTrue(self.quick_deposit_menu.amount_clear.is_displayed(),
                        msg='The amount text clear "X" is not displayed')
        quick_deposit_options = self.quick_deposit_menu.quick_stake_panel.items_as_ordered_dict
        actual_options = list(quick_deposit_options.keys())
        expected_options = [vec.gvc.EXPECTED_DEPOSIT_LIMIT_OPTIONS[1].replace("£ ", "+"),
                            vec.gvc.EXPECTED_DEPOSIT_LIMIT_OPTIONS[2].replace("£ ", "+"),
                            vec.gvc.EXPECTED_DEPOSIT_LIMIT_OPTIONS[3].replace("£ ", "+")]
        self.assertEqual(actual_options, expected_options,
                         msg=f'The quick deposit option "{expected_options}" is not displayed'
                             f' instead displayed "{actual_options}"')
        self.assertTrue(self.quick_deposit_menu.accounts.is_displayed(),
                        msg='Credit/Debit card Placeholder is not displayed')
        self.assertTrue(self.quick_deposit_menu.accounts.select_button.is_displayed(),
                        msg='Credit/Debit card Drop down arrow is not displayed')
        current_card = self.quick_deposit_menu.accounts.existing_account_name
        first_chars, *middle_chars1, last_chars = current_card.split(' ')
        self.assertTrue(first_chars.isdigit(), msg='First characters of card numbers are not displayed')
        self.assertTrue(last_chars.isdigit(), msg='Last characters of card numbers are not displayed')
        actual_middle_chard = [*middle_chars1]
        expected_middle_chars = ['xxxx', 'xxxx']
        self.assertEqual(actual_middle_chard, expected_middle_chars,
                         msg=f'Middle characters of card are not in format "{expected_middle_chars}" '
                             f'but in "{actual_middle_chard}"')
        self.assertTrue(self.quick_deposit_menu.cvv_2.is_displayed(), msg='CVV2 field is not displayed')
        self.quick_deposit_menu.accounts.click()
        select_menu_list = self.quick_deposit_menu.accounts.select_menu.items_names
        self.assertIn(vec.bma.OTHER_PAYMENT_OPTIONS, select_menu_list,
                      msg=f'"{vec.bma.OTHER_PAYMENT_OPTIONS}" option is not available')
        self.assertTrue(self.quick_deposit_menu.transaction_currency.is_displayed(),
                        msg='Transaction currency dropdown field is not displayed')
        self.assertTrue(self.quick_deposit_menu.transaction_tooltip.is_displayed(),
                        msg='The tooltip "i" information is not displayed')
        self.assertTrue(self.quick_deposit_menu.optional_bonus_code.is_displayed(),
                        msg='The optional bonus code along with dropdown is not displayed')
        click(self.quick_deposit_menu.optional_bonus_code)
        self.assertTrue(self.quick_deposit_menu.bonus_code.is_displayed(),
                        msg='The bonus code field is not displayed')
        self.assertTrue(self.quick_deposit_menu.deposit_button.is_displayed(),
                        msg='The deposit button is not displayed')
