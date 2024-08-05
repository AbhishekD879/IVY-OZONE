import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C29061_Bet_Placement_after_Logout(Common):
    """
    TR_ID: C29061
    NAME: Bet Placement after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: **Jira tickets:** BMA-5678 (Handle HTTP Error 401)
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Invictus in one browser tab -> add selections to the Bet Slip, go to the 'Bet Slip' page and enter stake for selection
    PRECONDITIONS: *   Duplicate browser tab, log out from this tab -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_make_steps_from_preconditions_with_opened_bet_slip_with_selections_on_the_first_tab__observe_the_betslip_and_try_to_tap_bet_now_button(self):
        """
        DESCRIPTION: Make steps from Preconditions with opened bet slip with selections (on the first tab)
        DESCRIPTION: - Observe the BetSlip and try to tap 'Bet Now' button
        EXPECTED: Popup message about logging out automatically appears.
        EXPECTED: User is logged out from the application
        EXPECTED: User is not able to perform **'Bet Now'** action as button changes to 'Login and place bet' button
        """
        pass

    def test_002_to_editclose_you_are_logged_out_pop_up_dialogclick_login_and_place_bet_button(self):
        """
        DESCRIPTION: **TO EDIT**
        DESCRIPTION: Close 'You are logged out pop up' dialog
        DESCRIPTION: Click 'Login and place bet' button
        EXPECTED: - Log in pop up appears
        EXPECTED: - Bet is not placed until the user confirms the login
        """
        pass

    def test_003_log_in_to_the_appobserve_the_bet_and_user_balance(self):
        """
        DESCRIPTION: Log in to the app
        DESCRIPTION: Observe the bet and user balance
        EXPECTED: User is logged in and the bet is placed without additional confirmation
        EXPECTED: User's balance is decreased accordingly to the initial stake set
        """
        pass

    def test_004_repeat_steps_1_2__close_log_in_dialog_invoked_by_login_and_place_bet_button__log_in_to_the_application_via_log_in_button_on_the_header_not_via_login_and_place_bet_button(self):
        """
        DESCRIPTION: Repeat steps 1-2
        DESCRIPTION: - Close 'Log in' dialog invoked by 'Login and place bet' button
        DESCRIPTION: - Log in to the application via 'Log in' button on the header (not via 'Login and place bet' button)
        EXPECTED: User balance is NOT changed after the re-login
        EXPECTED: User is able to place a bet after successful login
        """
        pass

    def test_005_repeat_steps_from_preconditions(self):
        """
        DESCRIPTION: Repeat steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_006_observe_the_bet_slip_page_for_tablet_and_desktop_only(self):
        """
        DESCRIPTION: Observe the 'Bet Slip' page (**for tablet and desktop only**)
        EXPECTED: User is logged out from the application
        EXPECTED: 'Join Us' and 'Log In' buttons are visible
        EXPECTED: User is not able to perform **'Bet Now'** action
        EXPECTED: User stays on 'Bet Slip' page
        """
        pass
