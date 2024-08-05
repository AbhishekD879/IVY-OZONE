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
class Test_C10841457_Verify_verification_overlay_after_upgrade(Common):
    """
    TR_ID: C10841457
    NAME: Verify verification overlay after upgrade
    DESCRIPTION: 
    PRECONDITIONS: * Make sure Upgrade feature is turned on in CMS: System configuration -> Connect -> upgrade
    PRECONDITIONS: * In-shop user should be logged in. [How to create In-Shop user](https://confluence.egalacoral.com/display/SPI/Create+In-Shop+user)
    PRECONDITIONS: * In-shop user should go through the upgrading process. The way to upgrade In-Shop user:
    PRECONDITIONS: * Load SportBook
    PRECONDITIONS: * Log in as In-Shop user
    PRECONDITIONS: * Open 'Connect' from header ribbon
    PRECONDITIONS: * Tap 'Use Connect Online'
    PRECONDITIONS: * Enter Card number and pin (if it is needed)
    PRECONDITIONS: * Fill all required fields correctly (use unique data for mail and phone number)
    PRECONDITIONS: * Tap 'Confirm' button
    PRECONDITIONS: NOTE:
    PRECONDITIONS: - Link to access IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - To find & edit user details in IMS go to: 'Player Management' tab > Player Search > Enter 'Username' & press 'Enter'paceKey=SPI&title=Playtech+IMS)
    PRECONDITIONS: * User Age Verification Result status is received in wss://openapi-{env}.egalacoral.com web socket call within response frame ID: 31083 (can be found in browser Dev Tools on Network tab)
    PRECONDITIONS: _____________________
    PRECONDITIONS: The text for 'Success' overlay is configurable in CMS:  Static Blocks >  KYC - PENDING VERIFICATION DIALOG AFTER UPGRADE > Html Markup
    PRECONDITIONS: Time of the overlay displaying is responded to the settings in CMS:  System Configuration > Structure > KYC > pendingDialogTimeout
    """
    keep_browser_open = True

    def test_001_verify_success_overlay_with_pending_verification_spinner(self):
        """
        DESCRIPTION: Verify 'Success' overlay with pending verification spinner
        EXPECTED: *  'Success' overlay with pending verification spinner appears
        EXPECTED: *  Time for the spinner is responded to settings in CMS
        EXPECTED: *  It overlays the previous upgrade page
        """
        pass

    def test_002_verify_success_overlay_with_pending_verification_spinner_structure(self):
        """
        DESCRIPTION: Verify 'Success' overlay with pending verification spinner structure
        EXPECTED: * 'VERIFYING YOUR DETAILS' header
        EXPECTED: * CMS configurable text, e.g 'Your account upgrade has been successful. Just a few more seconds, please wait…'
        EXPECTED: * Spinner
        EXPECTED: * there is NO close button on the overlay
        """
        pass

    def test_003_verify_that_time_of_displaying_success_overlay_with_pending_verification_spinner_is_responded_to_settings_in_cms(self):
        """
        DESCRIPTION: Verify that time of displaying 'Success' overlay with pending verification spinner is responded to settings in CMS
        EXPECTED: The time of displaying 'Success' overlay with pending verification spinner is equal to the value of "pendingDialogTimeout"
        """
        pass
