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
class Test_C3019617_Verify_Registration_of_a_user_from_Roulette_LP_via_Join_now_on_Log_in_pop_up(Common):
    """
    TR_ID: C3019617
    NAME: Verify Registration of a user from Roulette LP via 'Join now' on 'Log in' pop-up
    DESCRIPTION: This test case Registration of a user from came from Roulette LP via 'Join now' on 'Log in' pop-up
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

    def test_001_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log in' button
        EXPECTED: * Sportsbook login pop-up is displayed
        EXPECTED: * On the background the user is automatically navigated to the Sportsbook home page
        EXPECTED: * Any first install tutorial is not displayed
        """
        pass

    def test_002_tap_join_us_here_button_on_the_pop_up(self):
        """
        DESCRIPTION: Tap 'Join us here' button on the pop-up
        EXPECTED: Registration page is displayed on Step 1
        """
        pass

    def test_003__fill_all_required_data_for_step_1_and_2_tap_next_step(self):
        """
        DESCRIPTION: * Fill all required data for Step 1 and 2
        DESCRIPTION: * Tap 'Next Step'
        EXPECTED: * Registration page is displayed on Step 3
        EXPECTED: * 'Optional Promo code' field is present - after the currency and before deposit limits areas
        """
        pass

    def test_004__enter_any_alphanumeric_value_with_char_length_of_1_10_tap_complete_registration(self):
        """
        DESCRIPTION: * Enter any alphanumeric value with char length of 1-10
        DESCRIPTION: * Tap 'Complete Registration'
        EXPECTED: Preference overlay is opened
        """
        pass

    def test_005_tap_save_my_preferences(self):
        """
        DESCRIPTION: Tap 'Save my Preferences'
        EXPECTED: Deposit page is opened
        """
        pass

    def test_006_check_referrer_advertiser_for_the_user_in_ims(self):
        """
        DESCRIPTION: Check 'Referrer advertiser' for the user in IMS
        EXPECTED: Referrer advertiser: {entered promo code value}
        """
        pass
