import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C11783563_Failed_KYC_path_within_registration_Roulette_journey(Common):
    """
    TR_ID: C11783563
    NAME: Failed KYC path within registration Roulette journey
    DESCRIPTION: This test case verifies Failed KYC flow within Roulette registration journey.
    PRECONDITIONS: 1. Roulette feature is turned on in CMS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is ticked.
    PRECONDITIONS: 2. Roulette promo code is turned on in CMS: System Configuration -> Structure -> Registration -> 'isPromoCodeFieldEnabled' checkbox is ticked.
    PRECONDITIONS: 3. KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Expected urls for upgrade journey: Signup: [Endpoint]/?targetPage=signup&referrerPage=https://promotions.coral.co.uk/lp/shop-games/
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: To be able to receive 'ageVerificationStatus' = "review" right after registration > ask a developer to set breakpoint between registration and auto-login and change user status in IMS
    """
    keep_browser_open = True

    def test_001___fill_out_all_required_fields_on_registration_steps_1_3_mobile_or_steps_1_4_desktop__tap_complete_registration(self):
        """
        DESCRIPTION: - Fill out all required fields on Registration Steps 1-3 (mobile) OR Steps 1-4 (desktop)
        DESCRIPTION: - Tap 'Complete Registration'
        EXPECTED: A user is registered
        """
        pass

    def test_002_before_a_user_is_auto_logged_in_go_to_ims__find_just_updated_user_by_his_username__change_age_verification_result_to_unknown__tap_update_info(self):
        """
        DESCRIPTION: Before a user is auto logged in, go to IMS:
        DESCRIPTION: - Find just updated user by his username
        DESCRIPTION: - Change 'Age verification result' to "unknown"
        DESCRIPTION: - Tap 'Update Info
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_003_in_apptap_save_my_preferences_on_gdpr_screen(self):
        """
        DESCRIPTION: In app:
        DESCRIPTION: Tap 'Save My Preferences' on GDPR screen
        EXPECTED: - Failed ID KYC flow is started (with 'Verify Me' button)
        EXPECTED: - User remains in Oxygen app
        EXPECTED: - User will not be redirected back to Gaming
        """
        pass

    def test_004_repeat_steps_1_3changing_age_verification_result_to_active_grace_period_in_step_2(self):
        """
        DESCRIPTION: Repeat steps 1-3,
        DESCRIPTION: changing 'Age verification result' to "active grace period" in Step 2
        EXPECTED: 
        """
        pass
