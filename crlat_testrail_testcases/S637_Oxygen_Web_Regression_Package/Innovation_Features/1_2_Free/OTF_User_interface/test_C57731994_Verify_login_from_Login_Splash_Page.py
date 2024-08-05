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
class Test_C57731994_Verify_login_from_Login_Splash_Page(Common):
    """
    TR_ID: C57731994
    NAME: Verify login from 'Login Splash Page'
    DESCRIPTION: This test case verifies displaying login pop-up
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: 1. The user is NOT logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE' is available on Homepage / Football sports page
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_quick_link_on_homepage__football_sports_page(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE' quick link on Homepage / Football sports page.
        EXPECTED: The 'Login/Register' pop-up is displayed over the Login Splash page.
        """
        pass

    def test_002_enter_the_valid_credentialstap_on_the_login_button(self):
        """
        DESCRIPTION: Enter the valid credentials.
        DESCRIPTION: Tap on the 'Login' button.
        EXPECTED: The User is successfully logged in.
        """
        pass

    def test_003_tap_on_the_play_now_button(self):
        """
        DESCRIPTION: Tap on the 'Play now' button.
        EXPECTED: The Current tab is displayed.
        """
        pass
