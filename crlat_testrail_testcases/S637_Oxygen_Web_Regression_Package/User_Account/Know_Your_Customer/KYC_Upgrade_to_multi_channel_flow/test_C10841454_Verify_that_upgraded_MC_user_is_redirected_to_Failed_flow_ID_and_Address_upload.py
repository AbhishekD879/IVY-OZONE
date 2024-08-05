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
class Test_C10841454_Verify_that_upgraded_MC_user_is_redirected_to_Failed_flow_ID_and_Address_upload(Common):
    """
    TR_ID: C10841454
    NAME: Verify that upgraded MC user is redirected to Failed flow (ID and Address upload)
    DESCRIPTION: This test case verifies that the user who has just finished upgrading process and has 'Age verification result' = "Active Grace Period" with 'AGP_Success_Upload - 5' in IMS is redirected to failed flow (User failed initial details match (age & address))
    PRECONDITIONS: * Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: * In-shop user should be logged in. [How to create In-Shop user](https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: * User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    """
    keep_browser_open = True

    def test_001_upgrade_in_shop_user_to_multichannelopen_connect_from_header_ribbon__tap_use_connect_online__fill_all_required_fields_correctly_use_unique_data_for_mail_and_phone_number__tap_confirm_button(self):
        """
        DESCRIPTION: Upgrade in-shop user to multichannel:
        DESCRIPTION: Open 'Connect' from header ribbon > Tap 'Use Connect Online' > Fill all required fields correctly (use unique data for mail and phone number) > Tap 'Confirm' button
        EXPECTED: 'Success Upgrade' pop up with pending verification spinner appears
        """
        pass

    def test_002_before_a_user_is_auto_logged_inin_ims_find_just_updated_user_by_his_username_if_needed_change_age_verification_result_to_active_grace_period_tap_update_info_add_player_tag_agp_success_upload___5_or_less(self):
        """
        DESCRIPTION: Before a user is auto-logged in:
        DESCRIPTION: In IMS:
        DESCRIPTION: * Find just updated user by his username
        DESCRIPTION: * If needed, change 'Age verification result' to "Active grace period"
        DESCRIPTION: * Tap 'Update Info'
        DESCRIPTION: * Add Player Tag 'AGP_Success_Upload - 5 or less'
        EXPECTED: Changes are saved in IMS
        """
        pass

    def test_003_in_app_verify_that_verification_failed_page_is_shown(self):
        """
        DESCRIPTION: In app: Verify that 'Verification Failed' page is shown
        EXPECTED: 'Verification Failed' page is shown with 'Verify Me' button
        """
        pass
