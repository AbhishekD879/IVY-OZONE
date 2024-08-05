import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732023_KYC_Roxanne_Verify_opening_1_2_Free_for_the_logged_out_User_with_the_KYC_In_Review_status(Common):
    """
    TR_ID: C57732023
    NAME: [KYC] [Roxanne] Verify opening 1-2-Free for the logged out User with the KYC 'In Review' status
    DESCRIPTION: This test case verifies the successful navigation to the 1-2-free game flow for the logged out customer with the KYC 'In Review' status.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_log_out_from_the_system(self):
        """
        DESCRIPTION: Log out from the system.
        EXPECTED: The User is successfully logged out.
        """
        pass

    def test_002_tap_on_the_quick_link_for_any_1_2_free_game(self):
        """
        DESCRIPTION: Tap on the quick link for any 1-2-free game.
        EXPECTED: The User will see the pop up prompting them to log in first.
        """
        pass
