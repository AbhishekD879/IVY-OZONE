import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C57731998_Verify_the_Pop_up_when_the_iOS_App_toggle_is_Turned_ON_in_the_CMS_for_the_logged_in_User_iOS_native_only(Common):
    """
    TR_ID: C57731998
    NAME: Verify the Pop-up when the iOS App toggle  is Turned 'ON' in the CMS for the logged in User [iOS native only]
    DESCRIPTION: This test case verifies the Pop-up when the iOS App toggle  is Turned 'ON' in the CMS for the logged in User [iOS native only].
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The User is logged in on the iOS app.
    PRECONDITIONS: 2. Open the Oxygen CMS.
    PRECONDITIONS: 3. Navigate to the 1-2-Free section.
    PRECONDITIONS: 4. Select the 'IOS App Toggle' subsection.
    PRECONDITIONS: 5. Check in the 'IOS APP Off' checkbox.
    PRECONDITIONS: 6. Enter "To play 1-2-Free on this device, please visit {{URL}} to play the game!" into the 'Text' row.
    PRECONDITIONS: 7. Enter "https://m.ladbrokes.com" into the 'URL to where user should be directed' row.
    PRECONDITIONS: 8. Enter "ladbrokes.com" into the 'URL Text' row.
    PRECONDITIONS: 9. Enter "OK, thanks" into the 'Close CTA button text' row.
    PRECONDITIONS: 10. Enter "Go to Ladbrokes" into the 'Proceed CTA button text' row.
    PRECONDITIONS: 11. Click on the 'Save Changes' button.
    PRECONDITIONS: 12. Click on the 'Yes' button in the 'Saving of: IOS App Toogle' pop-up.
    PRECONDITIONS: 13. Click on the 'Yes' button in the 'Success' pop-up.
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
        EXPECTED: 3. Amber CTA1: "Go to Ladbrokes".
        EXPECTED: 4. CTA2: "OK, thanks".
        """
        pass

    def test_003_tap_on_the_ok_thanks_button(self):
        """
        DESCRIPTION: Tap on the 'OK, thanks' button.
        EXPECTED: The Pop-up is closed.
        EXPECTED: The User is redirected to the previous page.
        """
        pass

    def test_004_tap_on_the_quick_link_play_1_2_free_on_the_home_page_or_football_sports_page_again(self):
        """
        DESCRIPTION: Tap on the quick link 'Play 1-2-FREE...' on the Home page or Football sports page again.
        EXPECTED: The Pop-up is successfully displayed with next elements:
        EXPECTED: 1. Title: "1-2-Free has moved!".
        EXPECTED: 2. Message: "To play 1-2-free on this device, please visit ladbrokes.com"
        EXPECTED: 3. Amber CTA1: "Go to Ladbrokes".
        EXPECTED: 4. CTA2: "OK, thanks".
        """
        pass

    def test_005_tap_on_the_go_to_ladbrokes_button(self):
        """
        DESCRIPTION: Tap on the 'Go to Ladbrokes' button.
        EXPECTED: The User is redirected to the 1-2-Free web version.
        """
        pass
