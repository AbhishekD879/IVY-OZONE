import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65950084_Validate_Avtar_menu_immediate_24_hours_break_under_gambling_controls(Common):
    """
    TR_ID: C65950084
    NAME: Validate Avtar menu immediate 24 hours break under gambling controls
    DESCRIPTION: This test case is to verify the Avtar menu immediate 24 hours break gambling controls
    PRECONDITIONS: 1.User should have vaild login credentials to log into the application
    """
    keep_browser_open = True

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded succesfully
        """
        pass

    def test_002_verify_by_clicking_immediate_24_hour_break(self):
        """
        DESCRIPTION: Verify by clicking immediate 24 hour break
        EXPECTED: User should blocked for 24 hours from the application
        """
        pass

    def test_003_verify_the_same_user_by_getting_log_out_and_try_to_login(self):
        """
        DESCRIPTION: Verify the same user by getting log out and try to login
        EXPECTED: User should not be able to login and its should throw error as your account is currently blocked&acirc;&euro;&brvbar;.
        """
        pass

    def test_004_mobileverify_by_clicking_on_the_backward_chevron_beside_gambling_controls_header(self):
        """
        DESCRIPTION: Mobile
        DESCRIPTION: Verify by clicking on the backward chevron beside gambling controls header
        EXPECTED: User should be navigate to avatar menu page  successfully
        """
        pass

    def test_005_desktopverify_the_username_with_avatar_beside_gambling_controls_header(self):
        """
        DESCRIPTION: Desktop
        DESCRIPTION: Verify the username with avatar beside gambling controls header
        EXPECTED: User should able to see the username with avatar icon
        """
        pass
