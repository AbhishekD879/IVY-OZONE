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
class Test_C11783561_Failed_KYC_path_within_login_Roulette_journey(Common):
    """
    TR_ID: C11783561
    NAME: Failed KYC path within login Roulette journey
    DESCRIPTION: This test case verifies Failed KYC flow within Roulette, upgrade to multichannel (login), journey
    PRECONDITIONS: 1. Roulette feature is turned on in CMS: System Configuration -> Structure -> RouletteJourney = 'isRouletteEnabled' checkbox is ticked.
    PRECONDITIONS: 2. Roulette promo code is turned on in CMS: System Configuration -> Structure -> Registration -> 'isPromoCodeFieldEnabled' checkbox is ticked.
    PRECONDITIONS: 3. KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Expected urls for upgrade journey: Login: [Endpoint]/?targetPage=login&referrerPage=https://promotions.coral.co.uk/lp/shop-games/
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: To be able to receive 'ageVerificationStatus' = "review" right after registration > ask a developer to set breakpoint between registration and auto-login and change user status in IMS
    """
    keep_browser_open = True

    def test_001_log_in_with_in_shop_user_with_their_card_number_and_pin(self):
        """
        DESCRIPTION: 'Log in' with in-shop user with their card number and PIN
        EXPECTED: - All on login pop-ups are hidden (IMS or SalesForce)
        EXPECTED: - Upgrade pop-up is not displayed
        EXPECTED: - Relevant GDPR banner is displayed (WS "Get Player Tags" request 35547)
        EXPECTED: - User is automatically navigated to the upgrade page
        """
        pass

    def test_002___fill_out_all_required_data_on_upgrade_page__tap_confirm(self):
        """
        DESCRIPTION: - Fill out all required data on upgrade page
        DESCRIPTION: - Tap 'Confirm'
        EXPECTED: 'Verifying Your Details' pop up appears with a spinner and CMSable text
        """
        pass

    def test_003_before_a_user_is_auto_logged_in_go_to_ims__find_just_updated_user_by_his_username__change_age_verification_result_to_unknown__tap_update_info(self):
        """
        DESCRIPTION: Before a user is auto logged in, go to IMS:
        DESCRIPTION: - Find just updated user by his username
        DESCRIPTION: - Change 'Age verification result' to "unknown"
        DESCRIPTION: - Tap 'Update Info
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_004_in_appverify_that_failed_id_kyc_flow_is_started(self):
        """
        DESCRIPTION: In app:
        DESCRIPTION: Verify that Failed ID KYC flow is started
        EXPECTED: - Failed ID KYC flow is started (with 'Verify Me' button)
        EXPECTED: - User remains in Oxygen app
        EXPECTED: - User will not be redirected back to Gaming
        """
        pass

    def test_005_repeat_steps_1_4changing_age_verification_result_to_active_grace_period_in_step_3(self):
        """
        DESCRIPTION: Repeat steps 1-4,
        DESCRIPTION: changing 'Age verification result' to "active grace period" in Step 3
        EXPECTED: 
        """
        pass
