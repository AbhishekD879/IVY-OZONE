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
class Test_C57731995_Verify_displaying_of_Login_Splash_page(Common):
    """
    TR_ID: C57731995
    NAME: Verify displaying of 'Login Splash page'
    DESCRIPTION: This test case verifies displaying login pop-up
    PRECONDITIONS: Please look for some insights on a pages as follow:
    PRECONDITIONS: Deprecated: https://confluence.egalacoral.com/display/SPI/How+to+run+unpublished+Qubit+variation+on+Ladbrokes
    PRECONDITIONS: Oxygen CMS guide: https://confluence.egalacoral.com/display/SPI/1-2-Free+configurations?preview=/106397589/106397584/1-2-Free%20CMS%20configurations.pdf
    PRECONDITIONS: see section Text Configuration - Splash Page
    PRECONDITIONS: 1. The user is NOT logged in https://m.ladbrokes.com
    PRECONDITIONS: 2. Quick link 'Play 1-2-FREE' is available on Homepage / Football sports page (configure in CMS quick link and set link to 1-2-free as '{evnURL}/1-2-free')
    """
    keep_browser_open = True

    def test_001_tap_on_play_1_2_free_quick_link_on_homepage__football_sports_page(self):
        """
        DESCRIPTION: Tap on 'Play 1-2-FREE' quick link on Homepage / Football sports page
        EXPECTED: User should see Login Splash page, designed:
        EXPECTED: ![](index.php?/attachments/get/30763)
        EXPECTED: - 'Login to Play' button
        EXPECTED: - Cancel button
        """
        pass

    def test_002_tap_on_login_to_play_button(self):
        """
        DESCRIPTION: Tap on 'Login to Play' button
        EXPECTED: Login pop-up should successfully opens
        """
        pass

    def test_003_login_with_valid_user_credentialstap_login_button(self):
        """
        DESCRIPTION: Login with valid user credentials
        DESCRIPTION: Tap 'Login' button
        EXPECTED: - User successfully login
        EXPECTED: - Splash page or Current page should be displayed depending on previous actions
        """
        pass
