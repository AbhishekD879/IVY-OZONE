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
class Test_C91136_Tracking_of_success_log_in(Common):
    """
    TR_ID: C91136
    NAME: Tracking of success log in
    DESCRIPTION: This test case verify tracking of success log in
    PRECONDITIONS: 1. User should be logged out
    PRECONDITIONS: 2. Open console
    PRECONDITIONS: 3. Test case should be run on Desktop, Tablet and Mobile devices
    PRECONDITIONS: When a user successfully logs in, then send the following code to the data layer:
    PRECONDITIONS: - 'event' : 'trackPageview'
    PRECONDITIONS: - 'virtualUrl' : '/login/success'
    PRECONDITIONS: - 'location' : '<<location>>'
    PRECONDITIONS: - 'loginOption' : '<<checkbox option>>'
    PRECONDITIONS: - 'loginType' : '<<login type>>'
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

    def test_003_log_in_as_an_online_user_with_valid_credentials_without_enabling_checkboxes_rememer_username_remember_me(self):
        """
        DESCRIPTION: Log in as an online user with valid credentials without enabling checkboxes 'rememer username' /'remember me'
        EXPECTED: User is successfully logged in
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
        EXPECTED: - 'event' : ''trackPageview''
        EXPECTED: - 'virtualUrl' : ''/login/success''
        EXPECTED: - 'location' : ''header''
        EXPECTED: - 'loginOption' : ''none''
        EXPECTED: - 'loginType' : ''online account''
        """
        pass

    def test_006_log_out_from_application(self):
        """
        DESCRIPTION: Log out from application
        EXPECTED: User successfully logged out
        """
        pass

    def test_007_repeat_steps_2_6_from_following_places_enabling_one_or_both_checkboxes_during_login_rememer_username_remember_me__betslip__cashoutwidget__cashout__favouriteswidget__favourites__livestream__mybets___on_mobile_devices_mybets_page__playerbets__lottobet__footballjackpot__optin__minigamesvis__liveracing(self):
        """
        DESCRIPTION: Repeat steps 2-6 from following places enabling one or both checkboxes during login ('rememer username' /'remember me'):
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
        EXPECTED: Following tags are displayed:
        EXPECTED: - 'event' : ''trackPageview''
        EXPECTED: - 'virtualUrl' : ''/login/success''
        EXPECTED: - 'location' : ''<<Tag 'location' is changed and set to one of the place that is listed on the left>>''
        EXPECTED: - 'loginOption' :''<<'remeber me' is set if user enabled only 'remeber me' checkbox, 'remeber username' is set if user enabled only 'remeber username' checkbox, 'both' is set if user enabled both checkboxes>>''
        EXPECTED: - 'loginType' : ''online account''
        """
        pass
