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
class Test_C10940576_Verify_app_recovery_after_Lost_Connection_during_MC_KYC_Success_dialog(Common):
    """
    TR_ID: C10940576
    NAME: Verify app recovery after Lost Connection during MC KYC 'Success' dialog
    DESCRIPTION: This test case verifies that application is recovered after a lost connection which happens during 'Success' dialog with pending verification spinner displaying.
    PRECONDITIONS: * Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: * In-shop user should be logged in and upgraded. [How to create In-Shop user](https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user)
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'
    PRECONDITIONS: * User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: ____________________________________
    PRECONDITIONS: To trigger lost connection/reconnect:
    PRECONDITIONS: * turn the internet off/on
    PRECONDITIONS: * lock/unlock the phone for >5 min
    """
    keep_browser_open = True

    def test_001_upgrade_in_shop_user_to_multichannelopen_connect_from_header_ribbon__tap_use_connect_online__fill_all_required_fields_correctly_use_unique_data_for_mail_and_phone_number__tap_confirm_button(self):
        """
        DESCRIPTION: Upgrade in-shop user to multichannel:
        DESCRIPTION: Open 'Connect' from header ribbon > Tap 'Use Connect Online' > Fill all required fields correctly (use unique data for mail and phone number) > Tap 'Confirm' button
        EXPECTED: 'Success' overlay with pending verification spinner appears
        """
        pass

    def test_002_trigger_lost_connectionreconnectnote_do_not_refresh_the_page(self):
        """
        DESCRIPTION: Trigger lost connection/reconnect
        DESCRIPTION: Note: do not refresh the page
        EXPECTED: The connection was lost and reconnected
        """
        pass

    def test_003_verify_that_user_session_is_reconnected(self):
        """
        DESCRIPTION: Verify that user session is reconnected
        EXPECTED: * User is upgraded and redirected to appropriate KYC flow
        EXPECTED: * If he is logged out, the KYC flow starts after login as MC user
        EXPECTED: * If the user tries to log in with his card and PIN, there is a message "Please use your username and password to log in"
        """
        pass
