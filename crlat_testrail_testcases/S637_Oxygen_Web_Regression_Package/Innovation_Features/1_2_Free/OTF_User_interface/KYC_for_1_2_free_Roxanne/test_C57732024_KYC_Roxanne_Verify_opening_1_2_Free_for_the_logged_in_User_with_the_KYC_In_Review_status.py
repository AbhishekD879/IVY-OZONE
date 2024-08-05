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
class Test_C57732024_KYC_Roxanne_Verify_opening_1_2_Free_for_the_logged_in_User_with_the_KYC_In_Review_status(Common):
    """
    TR_ID: C57732024
    NAME: [KYC] [Roxanne] Verify opening 1-2-Free for the logged in User with the KYC  'In Review' status
    DESCRIPTION: This test case verifies the successful navigation to the 1-2-free game flow for the logged in customer with the KYC 'In Review' status.
    DESCRIPTION: This test case cannot be tested on the dev env. I should be tested on the stage.
    PRECONDITIONS: The User with the KYC 'In Review' status:
    PRECONDITIONS: Login: yester
    PRECONDITIONS: Password: Yester123
    PRECONDITIONS: Or you can change the 'Age verification' status to 'Active grace period' in the IMS:
    PRECONDITIONS: STG: https://admin-stg.ladbrokes.com/backoffice/
    PRECONDITIONS: mykola / Ladcor123!
    """
    keep_browser_open = True

    def test_001_log_in_with_the_credentials_of_the_user_with_the_kyc_in_review_status(self):
        """
        DESCRIPTION: Log in with the credentials of the User with the KYC 'In Review' status.
        EXPECTED: The User is successfully logged in.
        """
        pass

    def test_002_tap_on_the_quick_link_for_any_1_2_free_game(self):
        """
        DESCRIPTION: Tap on the quick link for any 1-2-free game.
        EXPECTED: The User is able to see the 'Account in review' popup as per attached screenshot with the following text:
        EXPECTED: Pop up title: Account in Review
        EXPECTED: Message: Your account is in review. We aim to get back to you within 2 hours. You'll receive an email and onsite message.
        EXPECTED: CTA: OK
        EXPECTED: ![](index.php?/attachments/get/33841)
        """
        pass

    def test_003_tap_on_the_ok_button(self):
        """
        DESCRIPTION: Tap on the 'OK' button.
        EXPECTED: The User will return to the previous page from where the 1-2-free game was launched.
        """
        pass
