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
class Test_C15478416_Vanilla_Verify_handling_application_state_correctly_after_re_establishing_internet_connection(Common):
    """
    TR_ID: C15478416
    NAME: [Vanilla] Verify handling application state correctly after re-establishing internet connection
    DESCRIPTION: This test case verifies that application is handling application state correctly after re-establishing internet connection
    PRECONDITIONS: To find RELOAD_COMPONENT and isAuthenticated requests go to Sourses>webpack>.>Bwin.CoralSports...>app>VanillaAuthVanillaInit>Services>>vanilla-auth.service.ts
    PRECONDITIONS: And put breakpoints on 'this.handleReloadComponentsEvent()' and 'this.vanillaAuth.isAuthenticated().then((isAuthenticated: boolean)' rows
    """
    keep_browser_open = True

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_trigger_connection_lost(self):
        """
        DESCRIPTION: Trigger connection lost
        EXPECTED: 
        """
        pass

    def test_003_restore_the_connection(self):
        """
        DESCRIPTION: Restore the connection
        EXPECTED: 
        """
        pass

    def test_004_reload_component_event_is_received_after_re_establishment_of_internet_connection(self):
        """
        DESCRIPTION: RELOAD_COMPONENT event is received after re-establishment of internet connection
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

    def test_008_trigger_connection_lost(self):
        """
        DESCRIPTION: Trigger connection lost
        EXPECTED: 
        """
        pass

    def test_009_wait_for_user_session_to_expirerestore_the_connection(self):
        """
        DESCRIPTION: Wait for user session to expire
        DESCRIPTION: Restore the connection
        EXPECTED: 
        """
        pass

    def test_010_restore_the_connection(self):
        """
        DESCRIPTION: Restore the connection
        EXPECTED: 
        """
        pass

    def test_011_isauthenticated_with_false_value_is_received_from_vanilla(self):
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
