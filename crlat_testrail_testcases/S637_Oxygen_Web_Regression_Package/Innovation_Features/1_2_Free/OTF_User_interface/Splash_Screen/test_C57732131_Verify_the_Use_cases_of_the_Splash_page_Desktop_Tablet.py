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
class Test_C57732131_Verify_the_Use_cases_of_the_Splash_page_Desktop_Tablet(Common):
    """
    TR_ID: C57732131
    NAME: Verify the Use cases of the Splash page [Desktop/Tablet]
    DESCRIPTION: This test case verifies the Use cases of the Splash page on the Desktop.
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The User is not logged in https://m.ladbrokes.com.
    PRECONDITIONS: 2. The Quick link 'Play 1-2-FREE' is available on Homepage / Football sports page.
    PRECONDITIONS: 3. The User does not have any prediction.
    """
    keep_browser_open = True

    def test_001_tap_on_the_play_1_2_free_quick_link_on_homepage__football_sports_page(self):
        """
        DESCRIPTION: Tap on the 'Play 1-2-FREE' quick link on Homepage / Football sports page.
        EXPECTED: User should see the Splash page with the Ladbrokes 1-2-free desktop logo.
        EXPECTED: The 'Login/register' pop-up is opened.
        """
        pass

    def test_002_tap_on_the_x_icon(self):
        """
        DESCRIPTION: Tap on the 'X' icon.
        EXPECTED: The 'Login/register' pop-up is closed.
        """
        pass

    def test_003_tap_on_the_cancel_button(self):
        """
        DESCRIPTION: Tap on the 'Cancel' button.
        EXPECTED: The User is redirected to the Home page / Football sports page.
        """
        pass

    def test_004_tap_on_the_play_1_2_free_quick_link_on_homepage__football_sports_page_again(self):
        """
        DESCRIPTION: Tap on the 'Play 1-2-FREE' quick link on Homepage / Football sports page again.
        EXPECTED: User should see the Splash page with the Ladbrokes 1-2-free desktop logo.
        EXPECTED: The 'Login/register' pop-up is opened.
        """
        pass

    def test_005_tap_on_the_x_icon(self):
        """
        DESCRIPTION: Tap on the 'X' icon.
        EXPECTED: The 'Login/register' pop-up is closed.
        """
        pass

    def test_006_tap_on_the_login_to_play_button(self):
        """
        DESCRIPTION: Tap on the 'Login to play' button.
        EXPECTED: The 'Login/register' pop-up is opened.
        """
        pass

    def test_007_enter_valid_credentials_and_click_on_the_login_button(self):
        """
        DESCRIPTION: Enter valid credentials and click on the 'Login' button.
        EXPECTED: The User is successfully logged in.
        EXPECTED: The 'Current' tab is opened.
        """
        pass
