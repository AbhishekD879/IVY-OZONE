import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C761771_Displaying_numeric_keyboard_with_Quick_Deposit_section_mobile_only(Common):
    """
    TR_ID: C761771
    NAME: Displaying numeric keyboard with 'Quick Deposit' section (mobile only)
    DESCRIPTION: This test case verifies numeric keyboard displaying prior to, after and within Quick Deposit section
    DESCRIPTION: ***Jira tickets***:
    DESCRIPTION: BMA-20463: New betslip - Nummeric keyboard (mobile only)
    DESCRIPTION: BMA-21999: Numeric keyboard - quick stake buttons
    DESCRIPTION: STEPS 1-24, 26-29 are the same for both brands; STEP 25 and its expected result is unique and applicable only for CORAL brand.
    PRECONDITIONS: Oxygen application is loaded
    PRECONDITIONS: User account with Zero balance and tied/added credit/debit card is present
    PRECONDITIONS: User account with positive balance and tied/added credit/debit card is present
    """
    keep_browser_open = True

    def test_001_log_in_with_account_with_zero_balance(self):
        """
        DESCRIPTION: Log in with **account with Zero balance**
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_one_selection_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add one selection to the Betslip > Open Betslip
        EXPECTED: - Selection is available within Betslip
        EXPECTED: - 'Quick Deposit' section is shown
        EXPECTED: -  Numeric keyboard is shown within 'Quick Deposit' section
        EXPECTED: From OX 100:
        EXPECTED: Numeric keyboard is not shown within 'Quick Deposit' section
        """
        pass

    def test_003_tap_on_quick_deposit_section_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header
        EXPECTED: - Numeric keyboard disappears
        EXPECTED: - 'Quick Stake' buttons are shown below 'Deposit Amount' and 'CVV' fields
        """
        pass

    def test_004_set_focus_over_stake_field_in_betslip__deposit_amount_or_cvv_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Stake' field in Betslip / 'Deposit Amount' or 'CVV' in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard is shown within 'Quick Deposit' section
        EXPECTED: - 'Quick Stake' buttons disappear
        """
        pass

    def test_005_tap_on_quick_deposit_section_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header
        EXPECTED: - Numeric keyboard disappears
        EXPECTED: - 'Quick Stake' buttons are shown below 'Deposit Amount' and 'CVV' fields
        """
        pass

    def test_006_x_button_in_quick_deposit_section(self):
        """
        DESCRIPTION: 'X' button in 'Quick Deposit' section
        EXPECTED: - 'Quick Deposit' section is closed
        """
        pass

    def test_007_enter_value_that_is_lower_than_minimum_required_deposit_value_into_stake_fieldminimum_deposit_value_is_5_gbp_usd_eur_50_kr(self):
        """
        DESCRIPTION: Enter value that is *lower than* minimum required deposit value into 'Stake' field
        DESCRIPTION: (Minimum deposit value is 5 GBP, USD, EUR/ 50 KR)
        EXPECTED: - Message 'Please deposit a min of #CURRENCY_VALUE.VALUE' to continue placing your bet' is shown above 'MAKE A DEPOSIT' button, where
        EXPECTED: * (VALUE.VALUE is the minimum deposit value, depending on user's currency setting)
        """
        pass

    def test_008_tap_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'MAKE A DEPOSIT' button
        EXPECTED: - Numeric keyboard disappears
        EXPECTED: - 'Quick Deposit' section is opened
        EXPECTED: - 'Quick Stake' buttons are shown below 'Deposit Amount' and 'CVV' fields
        """
        pass

    def test_009_set_focus_over_stake_field_in_betslip__deposit_amount_or_cvv_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Stake' field in Betslip / 'Deposit Amount' or 'CVV' in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard is shown within 'Quick Deposit' section
        EXPECTED: - 'Quick Stake' buttons disappear
        """
        pass

    def test_010_tap_on_x_button_in_quick_deposit_section(self):
        """
        DESCRIPTION: Tap on 'X' button in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard disappears
        EXPECTED: - 'Quick Deposit' section is collapsed
        """
        pass

    def test_011_close_betslip___add_2_more_selections_to_the_betslip___open_betslip(self):
        """
        DESCRIPTION: Close Betslip -> Add 2 more selections to the Betslip -> Open Betslip
        EXPECTED: - Selections are available within Betslip
        EXPECTED: - 'Quick Deposit' section is not shown
        EXPECTED: - Numeric keyboard is not shown
        """
        pass

    def test_012_set_focus_over_any_stake_field_in_betslip(self):
        """
        DESCRIPTION: Set focus over any 'Stake' field in Betslip
        EXPECTED: - Numeric keyboard is shown above 'MAKE A DEPOSIT' button
        """
        pass

    def test_013_repeat_steps_8_10(self):
        """
        DESCRIPTION: Repeat steps 8-10
        EXPECTED: Results are the same
        """
        pass

    def test_014_clear_betslip_and_log_out(self):
        """
        DESCRIPTION: Clear Betslip and Log out
        EXPECTED: Betslip is empty
        EXPECTED: User is logged out
        """
        pass

    def test_015_log_in_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Log in with **user account with positive balance**
        EXPECTED: 
        """
        pass

    def test_016_add_one_selection_to_the_betslip___open_betslip(self):
        """
        DESCRIPTION: Add one selection to the Betslip -> Open Betslip
        EXPECTED: - Selection is available within Betslip
        EXPECTED: - No 'Quick Deposit' section is shown
        EXPECTED: - Numeric keyboard is shown
        EXPECTED: From OX 100:
        EXPECTED: - Numeric keyboard is not shown
        """
        pass

    def test_017_tap_on_balance___deposit_button_in_the_betslip_header(self):
        """
        DESCRIPTION: Tap on Balance -> 'Deposit' button in the Betslip header
        EXPECTED: - 'Quick Deposit' section is shown
        EXPECTED: - Numeric keyboard is not shown
        """
        pass

    def test_018_set_focus_over_stake_field_in_betslip__deposit_amount_or_cvv_in_quick_deposit_section(self):
        """
        DESCRIPTION: Set focus over 'Stake' field in Betslip / 'Deposit Amount' or 'CVV' in 'Quick Deposit' section
        EXPECTED: - Numeric keyboard is shown within 'Quick Deposit' section
        """
        pass

    def test_019_tap_on_quick_deposit_section_header(self):
        """
        DESCRIPTION: Tap on 'Quick Deposit' section header
        EXPECTED: - Numeric keyboard disappears
        """
        pass

    def test_020_tap_on_balance___deposit_button_in_the_betslip_header(self):
        """
        DESCRIPTION: Tap on Balance -> 'Deposit' button in the Betslip header
        EXPECTED: - 'Quick Deposit' section is closed
        """
        pass

    def test_021_enter_value_into_stake_field_that_exceeds_users_balance_by_a_value_that_is_higher_than_minimum_required_deposit_valueminimum_deposit_value_is_5_gbp_usd_eur_50_kr_(self):
        """
        DESCRIPTION: Enter value into 'Stake' field that exceeds user's balance by a value, that is *higher than* minimum required deposit value
        DESCRIPTION: (Minimum deposit value is 5 GBP, USD, EUR/ 50 KR )
        EXPECTED: - Message 'Please deposit a min of #CURRENCY_VALUE.VALUE' to continue placing your bet' is shown above 'MAKE A DEPOSIT' button, where
        EXPECTED: * (VALUE.VALUE = ENTERED STAKE - USER'S CURRENT BALANCE, depending on user's currency setting)
        EXPECTED: - Numeric keyboard is shown
        """
        pass

    def test_022_remove_entered_value_from_stake_field_without_losing_focus_from_stake_field(self):
        """
        DESCRIPTION: Remove entered value from 'Stake' field (without losing focus from 'Stake' field)
        EXPECTED: - Message 'Please deposit a min of #CURRENCY_VALUE.VALUE' disappears
        EXPECTED: - Numeric keyboard remains being shown
        """
        pass

    def test_023_close_betslip___add_2_more_selections_to_the_betslip___open_betslip(self):
        """
        DESCRIPTION: Close Betslip -> Add 2 more selections to the Betslip -> Open Betslip
        EXPECTED: - Selections are available within Betslip
        EXPECTED: - 'Quick Deposit' section is not shown
        EXPECTED: - Numeric keyboard is not shown
        """
        pass

    def test_024_set_focus_over_any_stake_field(self):
        """
        DESCRIPTION: Set focus over any 'Stake' field
        EXPECTED: [Coral]
        EXPECTED: - Numeric Keyboard with 'Quick Stake' buttons is shown.
        EXPECTED: Keyboard contains:
        EXPECTED: * +<currency symbol>5
        EXPECTED: * +<currency symbol>10
        EXPECTED: * +<currency symbol>50
        EXPECTED: * +<currency symbol>100
        EXPECTED: where <currency symbol> may be :
        EXPECTED: * 'GBP': symbol = £;
        EXPECTED: * 'USD': symbol = $;
        EXPECTED: * 'EUR': symbol = €;
        EXPECTED: * 'SEK': symbol = Kr'
        EXPECTED: **NOTE** that for SEK currency the values of quick stakes are: 50, 100, 500, 1000
        EXPECTED: [Ladbrokes]
        EXPECTED: 'Quick Stake' buttons are removed from numeric keyboard
        """
        pass

    def test_025_coral_onlyadd_value_into_stake_field_by_tapping_on_any_quick_stake_button(self):
        """
        DESCRIPTION: [Coral ONLY]
        DESCRIPTION: Add value into 'Stake' field by tapping on any 'Quick Stake' button
        EXPECTED: - Amount from the tapped 'Quick Stake' button is shown in the 'Stake' field
        """
        pass

    def test_026_coralladbrokesedit_the_value_in_stake_field_so_it_would_exceed_users_current_balance_and_click_make_a_deposit_button(self):
        """
        DESCRIPTION: [CORAL/LADBROKES]
        DESCRIPTION: Edit the value in 'Stake' field so it would exceed user's current balance and click ''MAKE A DEPOSIT' button'
        EXPECTED: [CORAL/LADBROKES]
        EXPECTED: - Numeric keyboard disappears
        EXPECTED: - 'Quick Deposit' section is opened
        EXPECTED: - 'Quick Stake' buttons are shown below 'Deposit Amount' and 'CVV' fields
        """
        pass

    def test_027_coralladbrokestap_on_any_quick_stake_button_shown_within_the_quick_deposit_section(self):
        """
        DESCRIPTION: [CORAL/LADBROKES]
        DESCRIPTION: Tap on any 'Quick Stake' button shown within the 'Quick Deposit' section
        EXPECTED: [CORAL/LADBROKES]
        EXPECTED: 'Amount' from tapped button is summed with previously shown value in 'Deposit Amount' field.
        """
        pass

    def test_028_coralladbrokesset_focus_over_cvv__deposit_amount_field(self):
        """
        DESCRIPTION: [CORAL/LADBROKES]
        DESCRIPTION: Set focus over 'CVV' / 'Deposit Amount' field
        EXPECTED: [CORAL/LADBROKES]
        EXPECTED: Numeric Keyboard *without* 'Quick Stake' buttons is shown
        """
        pass

    def test_029_coralladbrokeswhile_deposit_amount_field_is_in_focus_click_on_any_numeric_button_shown_in_numeric_keyboard(self):
        """
        DESCRIPTION: [CORAL/LADBROKES]
        DESCRIPTION: While 'Deposit Amount' field is in focus, click on any 'numeric' button shown in Numeric keyboard
        EXPECTED: [CORAL/LADBROKES]
        EXPECTED: Manually entered value overrides previously entered/shown one
        """
        pass
