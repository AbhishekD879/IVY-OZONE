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
class Test_C57732039_Verify_the_navigation_to_the_Login_page_from_the_Splash_page_for_logged_out_User(Common):
    """
    TR_ID: C57732039
    NAME: Verify the navigation to the Login page from the Splash page for logged out User
    DESCRIPTION: This test case verifies the navigation to the Login page from the Splash page for logged out User.
    PRECONDITIONS: 1. The CMS has been configured as 'Log in to view' (the 'START' option is selected in the 'Login rule' field).
    PRECONDITIONS: 2. The User is logged out.
    """
    keep_browser_open = True

    def test_001_tap_on_the_cta_to_start_the_quiz_log_in_to_play_for_free(self):
        """
        DESCRIPTION: Tap on the CTA to start the quiz (Log in to Play for free).
        EXPECTED: The Login pop-up is opened.
        """
        pass

    def test_002_enter_valid_credentials(self):
        """
        DESCRIPTION: Enter valid credentials.
        EXPECTED: The existing 'After log in' pop-ups are displayed (Odds Boost/Quick Deposit).
        """
        pass

    def test_003_tap_on_the_x__okthanks_buttons(self):
        """
        DESCRIPTION: Tap on the 'X' / 'OK,Thanks' buttons.
        EXPECTED: The starting Splash page is displayed.
        """
        pass
