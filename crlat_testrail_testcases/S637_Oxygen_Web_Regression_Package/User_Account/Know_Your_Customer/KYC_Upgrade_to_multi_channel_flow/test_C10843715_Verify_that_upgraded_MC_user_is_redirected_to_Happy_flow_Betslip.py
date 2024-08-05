import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C10843715_Verify_that_upgraded_MC_user_is_redirected_to_Happy_flow_Betslip(Common):
    """
    TR_ID: C10843715
    NAME: Verify that upgraded MC user is redirected to Happy flow (Betslip)
    DESCRIPTION: This test case verifies that the user who has just finished upgrading process and has 'Age verification result' = "Under Review" in IMS is redirected back to the betslip when the upgrade journey has been started from betslip
    PRECONDITIONS: * Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: * In-shop user should be logged in. [How to create In-Shop user](https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: * User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_upgrade_in_shop_user_to_multichannel_from_betslipadd_several_selections_to_betslip__tap_upgrade_your_account__bet_now_button_at_the_bottom_of_betslip__fill_all_required_fields_correctly__tap_confirm_button(self):
        """
        DESCRIPTION: Upgrade in-shop user to multichannel from betslip:
        DESCRIPTION: Add several selections to betslip > Tap 'UPGRADE YOUR ACCOUNT & BET NOW' button at the bottom of Betslip > Fill all required fields correctly > Tap 'Confirm' button
        EXPECTED: 'Success' overlay with pending verification spinner appears
        """
        pass

    def test_002_before_a_user_is_auto_logged_inin_ims_find_just_updated_user_by_his_username_if_needed_change_age_verification_result_to_under_review_tap_update_info(self):
        """
        DESCRIPTION: Before a user is auto-logged in:
        DESCRIPTION: In IMS:
        DESCRIPTION: * Find just updated user by his username
        DESCRIPTION: * If needed, change 'Age verification result' to "under review"
        DESCRIPTION: * Tap 'Update Info'
        EXPECTED: 'Age verification result' = "under review"
        """
        pass

    def test_003_verify_that_user_is_redirected_to_the_betslip(self):
        """
        DESCRIPTION: Verify that user is redirected to the betslip
        EXPECTED: * In "openapi" websocket:
        EXPECTED: - 'ageVerificationStatus' = "review" is received (in response with "ID":31083)
        EXPECTED: * The user is automatically re-logged with new credentials
        EXPECTED: * The user is redirected to the betslip
        EXPECTED: * Homepage is opened on background
        EXPECTED: * Betslip contains previously added selections
        EXPECTED: * 'Bet now' button is displayed at the bottom
        """
        pass