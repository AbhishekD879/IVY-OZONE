import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C17995881_Vanilla_Verify_Messages_right_menu_option(Common):
    """
    TR_ID: C17995881
    NAME: [Vanilla] Verify Messages right menu option
    DESCRIPTION: This test case is to verify Messages right menu option
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in_to_test_env(self):
        """
        DESCRIPTION: Log in to test env
        EXPECTED: User is logged in, My Account button appears
        """
        pass

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        pass

    def test_003_clicktap_messages_menu_option(self):
        """
        DESCRIPTION: Click/tap Messages menu option
        EXPECTED: My Messages pop-up is displayed with the list of user's messages
        """
        pass
