import pytest
import tests
import datetime
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from time import sleep
from voltron.utils.helpers import switch_to_main_page


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.reg165_fix
@pytest.mark.user_account
@vtest
class Test_C15392887_EDITED_Quick_Deposit_section(BaseBetSlipTest):
    """
    TR_ID: C15392887
    NAME: [EDITED]  Quick Deposit section
    DESCRIPTION: This test case verifies Quick Deposit section within Betslip
    DESCRIPTION: "The Testcase needs to be edited according to Ladbrokes design and QB should be added too (+desktop)" - QB will be described as separate test scenario.
    PRECONDITIONS: 1. Load the app and log in with a user that has at list one credit card added;
    PRECONDITIONS: 2. Add selection to Betslip;
    PRECONDITIONS: 3. Betslip is opened with added selection;
    PRECONDITIONS: 4. User has a positive balance (recommended balance is less than 20 as it MAX amount for a single deposit(GVC Limitation))
    """
    keep_browser_open = True
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'
    deposit_amount = 10
    stake_amount = 1
    higher_stake_amount = 10

    def enter_stake_and_click_on_deposit(self, stake):
        user_balance = self.site.header.user_balance
        stake_value = user_balance + stake
        self.stake.amount_form.input.value = stake_value
        if stake <= 5:
            notification_stake_value = 5
        else:
            notification_stake_value = stake
        self.__class__.expected_message_text = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(notification_stake_value)
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        self.assertEqual(actual_message_text, self.expected_message_text,
                         msg=f'Info panel message: "{actual_message_text}" '
                             f'is not as expected: "{self.expected_message_text}"')
        deposit_button = self.get_betslip_content().make_quick_deposit_button
        self.assertTrue(deposit_button.is_enabled(), msg=f'"{deposit_button.name}" button is not enabled')
        self.assertEqual(deposit_button.name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual button name: "{deposit_button.name}" '
                             f'is not as expected: "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')
        self.get_betslip_content().make_quick_deposit_button.click()
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='"Quick Deposit" section is not displayed')
        sleep(3)
        self.__class__.quick_deposit = self.get_betslip_content().quick_deposit.stick_to_iframe()
        actual_deposit_amount = self.quick_deposit.amount.input.value
        self.__class__.calculated_deposit_amount = stake_value - user_balance
        if self.calculated_deposit_amount <= 5:
            expected_deposit_amount = "{0:.2f}".format(5)
        else:
            expected_deposit_amount = "{0:.2f}".format(self.calculated_deposit_amount)
        self.assertEqual(actual_deposit_amount, expected_deposit_amount,
                         msg=f'Amount field value: "{actual_deposit_amount}"'
                             f'is not as expected: "{expected_deposit_amount}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Add test event, PROD: Find active football event
        """
        if tests.settings.backend_env == 'prod':
            selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'Found Football event with outcomes "{selection_ids}"')
            team2 = list(selection_ids.keys())[-1]
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            team2 = event_params.team2
            selection_ids = event_params.selection_ids
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=user_name, amount=self.deposit_amount,
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
        self.site.login(username=user_name)
        self.open_betslip_with_selections(selection_ids=selection_ids[team2])

    def test_001_enter_value_in_stake_field_that_exceeds_users_balance(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds user's balance
        EXPECTED: * 'Stake' field is pre-populated with value
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(section.items())[0]
        self.enter_stake_and_click_on_deposit(stake=self.stake_amount)
        switch_to_main_page()
        self.assertTrue(self.get_betslip_content().quick_deposit.close_button.is_enabled(),
                        msg='Quick deposit panel close button is not enabled.')
        self.get_betslip_content().quick_deposit.close_button.click()

    def test_002_change_value_in_stake_field_make_sure_that_value_still_exceeds_users_balance(self):
        """
        DESCRIPTION: Change value in 'Stake' field, make sure that value still exceeds user's balance
        EXPECTED: * Difference between entered stake value and users balance is recalculated immediately and displayed on  'Please deposit a min..' error message
        """
        self.enter_stake_and_click_on_deposit(stake=self.higher_stake_amount)

    def test_003_clicktap_make_a_deposit_button(self):
        """
        DESCRIPTION: Click/Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed at the bottom of Betslip
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT AND PLACE BET' immediately and is disabled by default
        """
        # Covered in step 2

    def test_004_verify_quick_deposit_section(self):
        """
        DESCRIPTION: Verify Quick Deposit section
        EXPECTED: Quick Deposit section consists of:
        EXPECTED: * 'Quick Deposit' header and 'X' button
        EXPECTED: * Warning icon and 'Please deposit a min of <currency symbol>XX.XX to continue placing your bet' message
        EXPECTED: * Credit cards drop-down
        EXPECTED: * 'CVV' label and field
        EXPECTED: * 'SET LIMITS' clickable link
        EXPECTED: * Quick stakes buttons are displayed
        EXPECTED: * 'Deposit Amount' label and field and '-' and '+' buttons
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        """
        self.assertTrue(self.quick_deposit.warning_icon,
                        msg='Warning icon is not displayed')
        warning_message = self.quick_deposit.warning_panel
        expected_warning_message = \
            vec.gvc.FUNDS_NEEDED_FOR_BET.format(self.higher_stake_amount)
        self.assertEqual(warning_message, expected_warning_message,
                         msg=f'Incorrect warning message. \nActual:\n[{warning_message}]\nExpected:\n[{expected_warning_message}]')
        self.assertTrue(self.quick_deposit.accounts.is_displayed(),
                        msg='Credit/Debit card Placeholder is not displayed')
        self.assertTrue(self.quick_deposit.accounts.select_button.is_displayed(),
                        msg='Credit/Debit card Drop down arrow is not displayed')
        self.assertTrue(self.quick_deposit.cvv_2, msg='CVV is not displayed')
        self.assertTrue(self.quick_deposit.quick_stake_panel, msg='Quick stakes buttons are not displayed')
        self.assertTrue(self.quick_deposit.minus_button, msg='Minus button is not displayed')
        self.assertTrue(self.quick_deposit.plus_button, msg='Plus button is not displayed')

    def test_005_verify_credit_cards_drop_down(self):
        """
        DESCRIPTION: Verify credit cards drop-down
        EXPECTED: - Credit cards drop-down consists of in case when at list two cards are available:
        EXPECTED: * Card icon
        EXPECTED: * Card number displayed in the next format:
        EXPECTED: ****XXXX
        EXPECTED: where 'XXXX' - the last 4 number of the card
        EXPECTED: - Credit cards drop-down is missing when only one card is available, card is shown without dropdown
        """
        current_card = self.quick_deposit.accounts.existing_account_name
        *first_chars, last_chars = current_card.split(' ')
        self.assertTrue(last_chars.isdigit(), msg='Last characters of card numbers are not displayed')
        actual_first_chars = [*first_chars]
        expected_first_chars = ['xxxx', 'xxxx', 'xxxx']
        self.assertEqual(actual_first_chars, expected_first_chars,
                         msg=f'first characters of card are not in format "{expected_first_chars}" '
                             f'but in "{actual_first_chars}"')

    def test_006_clicktap_card_dropdown(self):
        """
        DESCRIPTION: Click/Tap card dropdown
        EXPECTED: * Credit card is displayed in the next format when only one item is present:
        EXPECTED: ****XXXX
        EXPECTED: * Credit card is displayed in the next format when at list two items are present
        EXPECTED: <payment system> ****XXXX
        EXPECTED: where
        EXPECTED: 'XXXX' - the last 4 number of the card,
        EXPECTED: <payment system>  - may be 'Visa', 'Master Card', 'Maestro'
        """
        # Covered in step 5

    def test_007_verify_card_correctness(self):
        """
        DESCRIPTION: Verify card correctness
        EXPECTED: Last 4 number of card corresponds to **data.payments.methods.[i].account.[j].specificParams** from 33012 response in WS
        EXPECTED: where
        EXPECTED: i - the number of all deposit methods added by user
        EXPECTED: j - the number of all cards added by user within one deposit method
        """
        # Not covered as part of automation

    def test_008_verify_deposit_amount_field(self):
        """
        DESCRIPTION: Verify 'Deposit Amount' field
        EXPECTED: * 'Deposit Amount' field is auto-populated with the difference between entered stake value and users balance if the amount needed for bet >5 or =5 EUR,GBP,USD;
        EXPECTED: * 'Deposit Amount' should be auto-populated with a minimum amount value if the amount needed for bet <5 EUR,GBP,USD;
        """
        # Covered in step 1 and 2

    def test_009_verify___and_plus_buttons(self):
        """
        DESCRIPTION: Verify '-' and '+' buttons
        EXPECTED: * '-' and '+' buttons always erase/add a sum of 5 (user currency)
        """
        self.quick_deposit.plus_button.click()
        actual_plus_deposit_amount = self.quick_deposit.amount.input.value
        plus_deposit_amount = self.calculated_deposit_amount + 5
        expected_plus_deposit_amount = "{0:.2f}".format(plus_deposit_amount)
        self.assertEqual(actual_plus_deposit_amount, expected_plus_deposit_amount,
                         msg=f'Amount field value: "{actual_plus_deposit_amount}"'
                             f'is not as expected: "{expected_plus_deposit_amount}"')

    def test_010_not_present_in_new_versions_of_cashier_app_verify_set_limits_link_navigation(self):
        """
        DESCRIPTION: NOT Present in new versions of Cashier app (Verify 'SET LIMITS' link navigation
        EXPECTED: * Betslip is closed after tapping 'SET LIMITS' link
        EXPECTED: * 'My Limits' page is opened in the same window
        EXPECTED: * URL is: https://xxx.coral.co.uk/limits
        """
        # SET LIMITS is not available on quick deposit

    def test_011_verify_x_button(self):
        """
        DESCRIPTION: Verify 'X' button
        EXPECTED: * 'Quick Deposit' section is closed after clicking/tapping 'X' button
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message stays displayed at the bottom of Betslip
        """
        switch_to_main_page()
        self.assertTrue(self.get_betslip_content().quick_deposit.close_button.is_enabled(),
                        msg='Quick deposit panel close button is not enabled.')
        self.get_betslip_content().quick_deposit.close_button.click()
        actual_message_text = self.get_betslip_content().bet_amount_warning_message
        self.assertEqual(actual_message_text, self.expected_message_text,
                         msg=f'Info panel message: "{actual_message_text}" '
                             f'is not as expected: "{self.expected_message_text}"')
