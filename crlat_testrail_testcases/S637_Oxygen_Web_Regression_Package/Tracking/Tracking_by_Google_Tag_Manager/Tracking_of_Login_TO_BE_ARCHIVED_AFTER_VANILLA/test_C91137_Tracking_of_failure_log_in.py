import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C91137_Tracking_of_failure_log_in(Common):
    """
    TR_ID: C91137
    NAME: Tracking of failure log in
    DESCRIPTION: This test case verify tracking of unsuccess log in
    PRECONDITIONS: User should be logged out
    PRECONDITIONS: Open console
    PRECONDITIONS: Test case should be run on Desktop, Tablet and Mobile devices
    PRECONDITIONS: When a user successfully logs in, then send the following code to the data layer:
    PRECONDITIONS: - 'event' : 'trackEvent'
    PRECONDITIONS: - 'eventCategory': 'login'
    PRECONDITIONS: - 'eventAction': 'attempt'
    PRECONDITIONS: - 'eventLabel': 'failure'
    PRECONDITIONS: - 'location' : '<<location>>'
    PRECONDITIONS: - 'errorMessage': '<<error message>>'
    PRECONDITIONS: - 'errorCode': 'error code'
    PRECONDITIONS: LOGIN LOCATION should equal place where login pop up was triggered and user was logged in.
    PRECONDITIONS: Notice: minigamesvis can be disabled, need to clarify.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_tap_on_log_in_button_from_header(self):
        """
        DESCRIPTION: Tap on 'Log in' button from header
        EXPECTED: Pop up login appears
        """
        pass

    def test_003_trigger_any_error_during_logging_infor_example_incorrect_password_username_log_in_with_frozen_account(self):
        """
        DESCRIPTION: Trigger any error during logging in
        DESCRIPTION: For example: incorrect password/ username/ log in with frozen account
        EXPECTED: - User is not logged in
        EXPECTED: - Error message is displayed on log in pop up
        """
        pass

    def test_004_in_console_window_type_datalayer_and_press_enter_button(self):
        """
        DESCRIPTION: In Console window type 'dataLayer' and press Enter button
        EXPECTED: Objects are displayed within Console window.
        """
        pass

    def test_005_expand_the_last_object(self):
        """
        DESCRIPTION: Expand the last Object
        EXPECTED: Following tags are displayed:
        EXPECTED: - 'event' : 'trackEvent'
        EXPECTED: - 'eventCategory': 'login'
        EXPECTED: - 'eventAction': 'attempt'
        EXPECTED: - 'eventLabel': 'failure'
        EXPECTED: - 'location' : 'header'
        EXPECTED: - 'errorMessage': '<<error message>>'
        EXPECTED: - 'errorCode': 'error code'
        """
        pass

    def test_006_verify_errormessage_tag(self):
        """
        DESCRIPTION: Verify 'errorMessage' tag
        EXPECTED: - 'errorMessage' should equal the front end error message that a customer sees
        EXPECTED: - The whole text of the message is present
        EXPECTED: - Text should be in lowercase without underscore
        """
        pass

    def test_007_verify_errorcode_tag(self):
        """
        DESCRIPTION: Verify 'errorCode' tag
        EXPECTED: - 'errorCode' should be equal the back end error code (Network-> Request 'LoginAndGetTempToken.php?casinoname=coraltst..'-> Response -> 'errorCode')
        EXPECTED: - If any of the error codes contains upper case then this should be changed to lower case without underscore
        """
        pass

    def test_008_repeat_steps_2_8_from_following_places__betslip__cashoutwidget__cashout__favouriteswidget__favourites__livestream__mybets___on_mobile_devices_mybets_page__playerbets__lottobet__footballjackpot__optin__minigamesvis__liveracing__bet_history__registration__log_out_pop_up(self):
        """
        DESCRIPTION: Repeat steps 2-8 from following places:
        DESCRIPTION: - betslip
        DESCRIPTION: - cashoutwidget
        DESCRIPTION: - cashout
        DESCRIPTION: - favouriteswidget
        DESCRIPTION: - favourites
        DESCRIPTION: - livestream
        DESCRIPTION: - mybets - on mobile devices mybets page
        DESCRIPTION: - playerbets
        DESCRIPTION: - lottobet
        DESCRIPTION: - footballjackpot
        DESCRIPTION: - optin
        DESCRIPTION: - minigamesvis
        DESCRIPTION: - liveracing
        DESCRIPTION: - bet-history
        DESCRIPTION: - registration
        DESCRIPTION: - Log out pop-up
        EXPECTED: 
        """
        pass
