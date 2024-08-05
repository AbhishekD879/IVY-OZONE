import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C3233902_Verify_optional_Promo_code_field(Common):
    """
    TR_ID: C3233902
    NAME: Verify optional Promo code field
    DESCRIPTION: This test case verifies optional Promo code field
    PRECONDITIONS: * KYC is OFF in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is NOT selected)
    PRECONDITIONS: OR
    PRECONDITIONS: * KYC is ON is CMS, but user IMS status 'Age Verification Result' = 'under review' or 'passed'
    PRECONDITIONS: * Roulette feature is turned on in CMS:
    PRECONDITIONS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is ticked
    PRECONDITIONS: System Configuration -> Structure -> Registration = 'isPromoCodeFieldEnabled' checkbox is ticked
    PRECONDITIONS: * SB app is loaded
    PRECONDITIONS: * Roulette landing page is displayed
    PRECONDITIONS: * Roulette journey can be verified within Local storage and -> attribute for Roulette users = 'OX.rouletteJourney'
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user
    PRECONDITIONS: NOTE: The users will be able to see the dedicated landing page ONCE in a lifetime; upon first app launch - http://promotions.coral.co.uk/lp/shop-games/
    """
    keep_browser_open = True

    def test_001_tap_register_online_button(self):
        """
        DESCRIPTION: Tap 'Register online' button
        EXPECTED: Registration page is displayed on Step 1
        """
        pass

    def test_002__fill_all_required_data_for_step_1_and_2_tap_next_step(self):
        """
        DESCRIPTION: * Fill all required data for Step 1 and 2
        DESCRIPTION: * Tap 'Next Step'
        EXPECTED: * Registration page is displayed on Step 3
        EXPECTED: * Optional 'Promo code' field is present - after the currency and before deposit limits areas
        EXPECTED: * 'Promo code' title is displayed above
        EXPECTED: * ‘Retail Promotional Code (Optional)’ black colored placeholder is displayed inside the field
        EXPECTED: * 'Complete Registration' button is enabled
        """
        pass

    def test_003_enter_any_invalid_data_symbols_or_more_than_10_alphanumeric_values(self):
        """
        DESCRIPTION: Enter any invalid data (symbols or more than 10 alphanumeric values)
        EXPECTED: * 'Please enter a valid promo code (only alphanumeric values are accepted and 1-10 characters long).' red colored message appears under the field
        EXPECTED: * 'Complete Registration' button is disabled
        """
        pass

    def test_004_remove_all_the_data_from_the_field(self):
        """
        DESCRIPTION: Remove all the data from the field
        EXPECTED: * 'Please enter a valid promo code (only alphanumeric values are accepted and 1-10 characters long).' message disappears
        EXPECTED: * 'Complete Registration' button is enabled
        """
        pass

    def test_005_tap_complete_registration(self):
        """
        DESCRIPTION: Tap 'Complete Registration'
        EXPECTED: Preference overlay is opened
        """
        pass

    def test_006_tap_save_my_preferences(self):
        """
        DESCRIPTION: Tap 'Save my Preferences'
        EXPECTED: Deposit page is opened
        """
        pass

    def test_007_check_referrer_advertiser_for_the_user_in_ims(self):
        """
        DESCRIPTION: Check 'Referrer advertiser' for the user in IMS
        EXPECTED: Referrer advertiser: {default value}
        """
        pass

    def test_008_tap_register_online_button(self):
        """
        DESCRIPTION: Tap 'Register online' button
        EXPECTED: Registration page is displayed on Step 1
        """
        pass

    def test_009__fill_all_required_data_for_step_1_and_2_tap_next_step(self):
        """
        DESCRIPTION: * Fill all required data for Step 1 and 2
        DESCRIPTION: * Tap 'Next Step'
        EXPECTED: * Registration page is displayed on Step 3
        EXPECTED: * Optional 'Promo code' field is present - after the currency and before deposit limits areas
        EXPECTED: * 'Promo code' title is displayed above
        EXPECTED: * ‘Retail Promotional Code (Optional)’ black colored placeholder is displayed inside the field
        EXPECTED: * 'Complete Registration' button is enabled
        """
        pass

    def test_010_enter_any_invalid_data_symbols_or_more_than_10_alphanumeric_values(self):
        """
        DESCRIPTION: Enter any invalid data (symbols or more than 10 alphanumeric values)
        EXPECTED: * 'Please enter a valid promo code (only alphanumeric values are accepted and 1-10 characters long).' red colored message appears under the field
        EXPECTED: * 'Complete Registration' button is disabled
        """
        pass

    def test_011__remove_the_invalid_data_enter_any_valid_data(self):
        """
        DESCRIPTION: * Remove the invalid data
        DESCRIPTION: * Enter any valid data
        EXPECTED: 'Complete Registration' button is enabled
        """
        pass

    def test_012_tap_complete_registration(self):
        """
        DESCRIPTION: Tap 'Complete Registration'
        EXPECTED: Preference overlay is opened
        """
        pass

    def test_013_tap_save_my_preferences(self):
        """
        DESCRIPTION: Tap 'Save my Preferences'
        EXPECTED: Deposit page is opened
        """
        pass

    def test_014_check_referrer_advertiser_for_the_user_in_ims(self):
        """
        DESCRIPTION: Check 'Referrer advertiser' for the user in IMS
        EXPECTED: Referrer advertiser: {entered promo code value}
        """
        pass

    def test_015__repeat_steps_1_and_2_tap_on_promo_code_field_leave_it_empty_other_fields_are_filled_out_with_valid_data_tap_on_complete_registration(self):
        """
        DESCRIPTION: * Repeat Steps 1 and 2
        DESCRIPTION: * Tap on Promo code field (leave it empty)
        DESCRIPTION: * Other fields are filled out with valid data
        DESCRIPTION: * Tap on 'Complete Registration'
        EXPECTED: Registration complete
        EXPECTED: Promo code field isn't required
        """
        pass
