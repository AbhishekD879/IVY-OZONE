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
class Test_C57732040_Verify_the_navigation_to_the_Login_page_from_the_Submit_pop_up_for_logged_out_User(Common):
    """
    TR_ID: C57732040
    NAME: Verify the navigation to the Login page from the 'Submit' pop-up for logged out User
    DESCRIPTION: This test case verifies the navigation to the Login page from the 'Submit' pop-up for logged out User.
    PRECONDITIONS: 1. The CMS has been configured as 'Log in to submit' (the 'SUBMIT' option is selected in the 'Login rule' field).
    PRECONDITIONS: 2. The User is logged out.
    """
    keep_browser_open = True

    def test_001_tap_on_the_submit_cta_log_in_to_submit(self):
        """
        DESCRIPTION: Tap on the submit CTA (Log in to submit).
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
        EXPECTED: The 'Submit quiz' pop-up is displayed.
        """
        pass

    def test_004_tap_on_the_submit_cta_button(self):
        """
        DESCRIPTION: Tap on the 'Submit' CTA button.
        EXPECTED: The quiz is submitted and finished.
        """
        pass
