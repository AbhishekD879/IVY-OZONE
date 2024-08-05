import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.navigation
@vtest
class Test_C17723913_Vanilla_Verify_top_menu_when_not_logged_in(Common):
    """
    TR_ID: C17723913
    NAME: [Vanilla] Verify top menu when not logged in
    DESCRIPTION: This test case is to verify top menu options when user is not logged in
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - C48716305
    DESCRIPTION: Desktop - C48716307
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_verify_the_top_menu_when_user_is_not_logged_in(self):
        """
        DESCRIPTION: Verify the top menu when user is not logged in:
        EXPECTED: Top menu contains following menu options:
        EXPECTED: - Join
        EXPECTED: - Login
        EXPECTED: For **Mobile**:
        EXPECTED: - Ladbrokes has 1 button Log in/Join
        EXPECTED: - Coral has 2 buttons Log in and Join
        EXPECTED: For **Desktop**:
        EXPECTED: - Ladbrokes and Coral has 2 buttons Log in and Join
        """
        pass

    def test_002_coral_clicktap_join_button(self):
        """
        DESCRIPTION: Coral: Click/Tap Join button
        EXPECTED: Registration form is displayed on the first step.
        """
        pass

    def test_003_coral_close_join_form(self):
        """
        DESCRIPTION: Coral: Close Join form
        EXPECTED: Join form is closed
        """
        pass

    def test_004_coral_clicktap_login_buttonladbrokes_clicktap_log_injoin_in_button(self):
        """
        DESCRIPTION: Coral: Click/tap Login button
        DESCRIPTION: Ladbrokes: Click/tap Log in/Join in button
        EXPECTED: Login form is opened
        """
        pass
