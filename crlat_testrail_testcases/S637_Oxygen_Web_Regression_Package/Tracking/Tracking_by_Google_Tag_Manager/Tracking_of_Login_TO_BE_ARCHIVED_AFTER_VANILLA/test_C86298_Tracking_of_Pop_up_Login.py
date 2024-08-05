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
class Test_C86298_Tracking_of_Pop_up_Login(Common):
    """
    TR_ID: C86298
    NAME: Tracking of Pop up Login
    DESCRIPTION: This test case verifies tracking of Pop up Login
    PRECONDITIONS: 1. User should be logged out
    PRECONDITIONS: 2. Open console
    PRECONDITIONS: 3. Test case should be run on Desktop, Tablet and Mobile devices
    PRECONDITIONS: When a user clicks on the login button, then send the following code to the data layer:
    PRECONDITIONS: - 'event' : 'trackPageview'
    PRECONDITIONS: - 'virtualUrl' : '/login'
    PRECONDITIONS: - 'location' : '<< LOGIN LOCATION >>'
    PRECONDITIONS: LOGIN LOCATION should equal place where login pop up was triggered
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

    def test_003_in_console_window_type_datalayer_and_press_enter_button(self):
        """
        DESCRIPTION: In Console window type 'dataLayer' and press Enter button
        EXPECTED: Objects are displayed within Console window.
        """
        pass

    def test_004_expand_the_last_object(self):
        """
        DESCRIPTION: Expand the last Object
        EXPECTED: Following tags are displayed:
        EXPECTED: - 'event' : ''trackPageview''
        EXPECTED: - 'virtualUrl' : ''/login''
        EXPECTED: - 'location' : ''header''
        """
        pass

    def test_005_repeat_steps_2_4_from_following_places__betslip__cashoutwidget__cashout__favouriteswidget__favourites__livestream__mybets___mubets_page_on_mobile_devices__playerbets__lottobet__footballjackpot__optin__minigamesvis__liveracing(self):
        """
        DESCRIPTION: Repeat steps 2-4 from following places:
        DESCRIPTION: - betslip
        DESCRIPTION: - cashoutwidget
        DESCRIPTION: - cashout
        DESCRIPTION: - favouriteswidget
        DESCRIPTION: - favourites
        DESCRIPTION: - livestream
        DESCRIPTION: - mybets - mubets page on mobile devices
        DESCRIPTION: - playerbets
        DESCRIPTION: - lottobet
        DESCRIPTION: - footballjackpot
        DESCRIPTION: - optin
        DESCRIPTION: - minigamesvis
        DESCRIPTION: - liveracing
        EXPECTED: Tag 'location' is changed and set to one of the place that is listed on the left
        """
        pass
