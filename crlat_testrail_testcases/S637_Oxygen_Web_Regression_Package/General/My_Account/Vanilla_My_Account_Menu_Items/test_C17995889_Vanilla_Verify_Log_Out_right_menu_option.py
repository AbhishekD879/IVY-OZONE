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
class Test_C17995889_Vanilla_Verify_Log_Out_right_menu_option(Common):
    """
    TR_ID: C17995889
    NAME: [Vanilla] Verify Log Out right menu option
    DESCRIPTION: This test case is to verify Log Out right menu option
    DESCRIPTION: [C26346624]
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in_to_test_env_and_navigate_to_the_page_other_than_the_home_page(self):
        """
        DESCRIPTION: Log in to test env and navigate to the page other than the home page
        EXPECTED: User is logged in, My Account button appears
        """
        pass

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        pass

    def test_003_clicktap_log_out_menu_option(self):
        """
        DESCRIPTION: Click/tap Log Out menu option
        EXPECTED: Use is logged out and redirected to the home page
        """
        pass
