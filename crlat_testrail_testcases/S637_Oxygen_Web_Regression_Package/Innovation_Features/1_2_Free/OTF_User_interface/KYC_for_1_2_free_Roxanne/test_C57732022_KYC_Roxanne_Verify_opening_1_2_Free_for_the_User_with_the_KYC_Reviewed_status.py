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
class Test_C57732022_KYC_Roxanne_Verify_opening_1_2_Free_for_the_User_with_the_KYC_Reviewed_status(Common):
    """
    TR_ID: C57732022
    NAME: [KYC] [Roxanne] Verify opening 1-2-Free for the User with the KYC 'Reviewed' status
    DESCRIPTION: This test case verifies the successful navigation to the 1-2-free game flow for the logged in customer with the KYC 'Reviewed' status.
    PRECONDITIONS: The User with the KYC 'Reviewed' status:
    PRECONDITIONS: Login: maestro_20190726
    PRECONDITIONS: Password: Password1
    PRECONDITIONS: Or change the 'Age verification' status to 'Passed' in the IMS: https://confluence.egalacoral.com/display/SPI/Unblocking+test+users+after+KYC+feature+release.
    """
    keep_browser_open = True

    def test_001_log_in_with_the_credentials_of_the_user_with_the_kyc_reviewed_status(self):
        """
        DESCRIPTION: Log in with the credentials of the User with the KYC 'Reviewed' status.
        EXPECTED: The User is successfully logged in.
        """
        pass

    def test_002_tap_on_the_quick_link_for_any_1_2_free_game(self):
        """
        DESCRIPTION: Tap on the quick link for any 1-2-free game
        EXPECTED: The User is navigated to the 1-2-free game flow.
        EXPECTED: The User can continue to make a prediction as normal.
        """
        pass
