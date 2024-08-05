import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C15478415_To_editVanilla_Verify_handling_application_state_correctly_after_sleep_mode(Common):
    """
    TR_ID: C15478415
    NAME: [To edit][Vanilla] Verify handling application state correctly after sleep mode
    DESCRIPTION: This test case verifies that application is handling application state correctly after sleep mode
    PRECONDITIONS: How to reduce the duration of web session: VanillaFramework.Web.Authentication ->  Timeout -> Set on
    PRECONDITIONS: http://qa11.sports.coral.co.uk/mocks/config
    PRECONDITIONS: To find RELOAD_COMPONENT and isAuthenticated requests go to Sourses>webpack>.>Bwin.CoralSports...>app>VanillaAuthVanillaInit>Services>>vanilla-auth.service.ts
    PRECONDITIONS: And put breakpoints on 'this.handleReloadComponentsEvent()' and 'this.vanillaAuth.isAuthenticated().then((isAuthenticated: boolean)' rows
    PRECONDITIONS: ![](index.php?/attachments/get/33981501)
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_lock_the_device_and_wait_until_it_goes_to_the_sleep_mode(self):
        """
        DESCRIPTION: Lock the device and wait until it goes to the sleep mode
        EXPECTED: 
        """
        pass

    def test_003_unlock_the_device_or_trigger_returning_from_sleep_mode(self):
        """
        DESCRIPTION: Unlock the device or trigger returning from sleep mode
        EXPECTED: 
        """
        pass

    def test_004_reload_component_event_is_received_on_transition_from_sleep_modebreakpoint_is_paused__tap_on_step_over_next_function_button_to_proceed_to_next_breakpointindexphpattachmentsget33981500(self):
        """
        DESCRIPTION: RELOAD_COMPONENT event is received on transition from sleep mode
        DESCRIPTION: Breakpoint is paused > tap on 'Step over next function' button to proceed to next breakpoint
        DESCRIPTION: ![](index.php?/attachments/get/33981500)
        EXPECTED: Developer tool -> Sources
        """
        pass

    def test_005_isauthenticated_with_true_value_is_received_from_vanilla(self):
        """
        DESCRIPTION: isAuthenticated with 'true' value is received from Vanilla
        EXPECTED: User stays logged in in application
        """
        pass

    def test_006_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_007_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: 
        """
        pass

    def test_008_lock_the_device_and_wait_until_it_goes_to_the_sleep_mode(self):
        """
        DESCRIPTION: Lock the device and wait until it goes to the sleep mode
        EXPECTED: 
        """
        pass

    def test_009_wait_for_user_login_session_to_timeoutunlock_the_device_or_trigger_returning_from_sleep_mode(self):
        """
        DESCRIPTION: Wait for user login session to timeout
        DESCRIPTION: Unlock the device or trigger returning from sleep mode
        EXPECTED: 
        """
        pass

    def test_010_isauthenticated_with_false_value_is_received_from_vanilla(self):
        """
        DESCRIPTION: isAuthenticated with 'false' value is received from Vanilla
        EXPECTED: Ladbrokes:
        EXPECTED: User is logged out automatically without any pop-up message
        EXPECTED: Coral:
        EXPECTED: User is logged out automatically with corresponding pop-up with the next message:
        EXPECTED: 'Sorry your session appears to have expired. Please login again.
        EXPECTED: If this problem persists, contact our Customer Service Department'
        """
        pass
