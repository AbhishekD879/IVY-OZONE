import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C34298265_Register_and_Add_Credit_Card(Common):
    """
    TR_ID: C34298265
    NAME: Register and Add Credit Card
    DESCRIPTION: Verify that the user can Register and add a Credit Card as payment method
    DESCRIPTION: AUTOMATED [C45158733]
    DESCRIPTION: Note: need to update for Ladbrokes brand.
    PRECONDITIONS: Note: Registration and Payment methods are handled on GVC side.
    PRECONDITIONS: * Documentation for user registration and payment methods:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+create+test+user+for+GVC+Vanilla+automatically+by-passing+KYC
    """
    keep_browser_open = True

    def test_001_open_oxygen_app(self):
        """
        DESCRIPTION: Open Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_click_on_join_button(self):
        """
        DESCRIPTION: Click on 'JOIN' button
        EXPECTED: Registration Overlay is opened
        EXPECTED: ![](index.php?/attachments/get/11306801)
        """
        pass

    def test_003_fill_in_the_required_data1_country_residence__use_united_kingdomand_currency2_email_for_internal_accounts_use_usernameinternalgvccom3_username_for_internal_accounts_use_testgvccl_username4_password(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Country residence ( use 'United Kingdom')and currency
        DESCRIPTION: 2. Email (for internal accounts use *username*@internalgvc.com)
        DESCRIPTION: 3. Username (for internal accounts use testgvccl-*username*)
        DESCRIPTION: 4. Password
        EXPECTED: 
        """
        pass

    def test_004_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button
        EXPECTED: Registration Step 2 is opened
        EXPECTED: ![](index.php?/attachments/get/11306802)
        """
        pass

    def test_005_fill_in_the_required_data1_title_mrms2_first_name3_last_name4_date_of_birth_random_daymonthyear_18_years_plus(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Title: Mr/Ms
        DESCRIPTION: 2. First name
        DESCRIPTION: 3. Last name
        DESCRIPTION: 4. Date of birth (random day/month/year, 18 years plus)
        EXPECTED: 
        """
        pass

    def test_006_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button
        EXPECTED: Registration Step 3 is opened
        EXPECTED: ![](index.php?/attachments/get/11306803)
        """
        pass

    def test_007_fill_in_the_required_data1_postcode_use_postcode_12345_and_select_suggested_address2_phone_number_use_079111234563_checkboxes_to_receive_freebets_bonuses_and_offers_from_coral_via__choose_any(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Postcode (use postcode 12345 and select suggested address)
        DESCRIPTION: 2. Phone number( use 07911123456)
        DESCRIPTION: 3. Checkboxes to receive FreeBets, bonuses and offers from Coral via ( choose any)
        EXPECTED: 
        """
        pass

    def test_008_click_on_create_my_account_button(self):
        """
        DESCRIPTION: Click on 'CREATE MY ACCOUNT' button
        EXPECTED: Desktop: 'SET YOUR DEPOSIT LIMITS' pop-up appears with option to close (x)
        EXPECTED: Mobile/Tablet:'SET YOUR DEPOSIT LIMITS' overlay appears with option to close (x)
        EXPECTED: ![](index.php?/attachments/get/11306804)
        """
        pass

    def test_009__choose_any_deposit_limit_select_checkbox_for_privacy_policy_click_submit_button(self):
        """
        DESCRIPTION: * Choose any deposit limit
        DESCRIPTION: * Select checkbox for privacy policy
        DESCRIPTION: * Click 'SUBMIT' button
        EXPECTED: Deposit page is opened with message on green panel:
        EXPECTED: 'You are registered!
        EXPECTED: Almost there, make a deposit and get your welcome bonus.'and payment methods available ( e.g. Visa, Mastercard, Maestro)
        EXPECTED: ![](index.php?/attachments/get/11306805)
        """
        pass

    def test_010_choose_any_payment_method__one_from_visa_mastercard_maestro_and_fill_in_the_required_data__amount__choose_20__credit_card_number___use_credit_card_added_in_documentation_in_preconditions__expiration_date___any_valid_date_in_the_future_eg_122018__cvv2__eg_123(self):
        """
        DESCRIPTION: Choose any payment method ( one from Visa, Mastercard, Maestro) and fill in the required data:
        DESCRIPTION: - Amount ( choose 20)
        DESCRIPTION: - Credit card number - (Use credit card added in documentation in Preconditions)
        DESCRIPTION: - Expiration date - any valid date in the future (e.g. 12.2018)
        DESCRIPTION: - CVV2 ( e.g. 123)
        EXPECTED: 
        """
        pass

    def test_011_click_on_deposit_amountcurrency_buttonwhere_amount__deposit_amount_enteredcurrency__currency_selected_during_registration(self):
        """
        DESCRIPTION: Click on 'DEPOSIT [amount][currency]' button
        DESCRIPTION: where [amount] = deposit amount entered
        DESCRIPTION: [currency] = currency selected during registration.
        EXPECTED: * Message 'Your deposit of [amount][currency] has been successful
        EXPECTED: An email has been sent to your registered email address.' is displayed on green panel
        EXPECTED: * TRANSACTION DETAILS
        EXPECTED: * 'OK' button
        EXPECTED: * 'MAKE ANOTHER DEPOSIT' button
        EXPECTED: ![](index.php?/attachments/get/11306799)
        """
        pass

    def test_012_click_ok_button(self):
        """
        DESCRIPTION: Click 'OK' button
        EXPECTED: Coral Home Page is opened.
        EXPECTED: User is logged in and balance is displayed on header with amount deposited on previous step.
        EXPECTED: ![](index.php?/attachments/get/11306800)
        """
        pass
