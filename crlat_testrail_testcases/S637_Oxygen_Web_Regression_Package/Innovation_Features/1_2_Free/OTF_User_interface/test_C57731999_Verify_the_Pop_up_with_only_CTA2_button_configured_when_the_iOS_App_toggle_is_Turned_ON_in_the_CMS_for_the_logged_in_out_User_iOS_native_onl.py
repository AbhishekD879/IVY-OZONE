import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57731999_Verify_the_Pop_up_with_only_CTA2_button_configured_when_the_iOS_App_toggle_is_Turned_ON_in_the_CMS_for_the_logged_in_out_User_iOS_native_only(Common):
    """
    TR_ID: C57731999
    NAME: Verify the Pop-up with only CTA2 button configured when the iOS App toggle is Turned 'ON' in the CMS for the logged in/out User [iOS native only]
    DESCRIPTION: This test case verifies the Pop-up with only CTA2 button configured when the iOS App toggle is Turned 'ON' in the CMS for the logged in User [iOS native only].
    DESCRIPTION: This case can occur if Apple won't allow to redirect from the native app to the mobile version via URL.
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The User is logged in on the iOS app.
    PRECONDITIONS: 2. Open the Oxygen CMS.
    PRECONDITIONS: 3. Navigate to the 1-2-Free section.
    PRECONDITIONS: 4. Select the 'IOS App Toggle' subsection.
    PRECONDITIONS: 5. Check in the 'IOS APP Off' checkbox.
    PRECONDITIONS: 6. Enter "To play 1-2-Free on this device, please visit {{URL}} to play the game!" into the 'Text' row.
    PRECONDITIONS: 7. Enter "ladbrokes.com" into the 'URL Text' row.
    PRECONDITIONS: 8. Enter "OK, thanks" into the 'Close CTA button text' row.
    PRECONDITIONS: 9. Enter "Go to Ladbrokes" into the 'Proceed CTA button text' row.
    PRECONDITIONS: 10. Click on the 'Save Changes' button.
    PRECONDITIONS: 11. Click on the 'Yes' button in the 'Saving of: IOS App Toogle' pop-up.
    PRECONDITIONS: 12. Click on the 'Yes' button in the 'Success' pop-up.
    """
    keep_browser_open = True

    def test_001_open_the_ios_app(self):
        """
        DESCRIPTION: Open the iOS app.
        EXPECTED: The iOS app is successfully opened.
        """
        pass

    def test_002_tap_on_the_quick_link_play_1_2_free_on_the_home_page__football_sports_page(self):
        """
        DESCRIPTION: Tap on the quick link 'Play 1-2-FREE...' on the Home page / Football sports page.
        EXPECTED: The Pop-up is successfully displayed with next elements:
        EXPECTED: 1. Title: "1-2-Free has moved!".
        EXPECTED: 2. Message: "To play 1-2-free on this device, please visit ladbrokes.com"
        EXPECTED: 3. CTA2: "OK, thanks".
        """
        pass

    def test_003_tap_on_the_ok_thanks_button(self):
        """
        DESCRIPTION: Tap on the 'OK, thanks' button.
        EXPECTED: The User is navigated to the native Home page / previous native page.
        """
        pass
