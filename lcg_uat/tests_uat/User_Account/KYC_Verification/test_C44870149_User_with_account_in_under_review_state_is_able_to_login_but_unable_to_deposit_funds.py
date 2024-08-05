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
class Test_C44870149_User_with_account_in_under_review_state_is_able_to_login_but_unable_to_deposit_funds(Common):
    """
    TR_ID: C44870149
    NAME: User with account in 'under review' state is able to login but unable to deposit funds.
    DESCRIPTION: 
    PRECONDITIONS: 1. User's account should be having status as 'Under review', i.e. user has registered in the application but has not uploaded KYC documents (for age and address proof).
    PRECONDITIONS: 2. User should not be logged in the application.
    PRECONDITIONS: Note:- In IMS database, status should be IMS AGE verification status = Under review
    PRECONDITIONS: Ref: https://app.zeplin.io/project/5c935fb0320dd2055d273d96/screen/5c99eafa66d66477525a2b2a,
    """
    keep_browser_open = True

    def test_001_login_with_either_one_of_the_following_users_in_the_application_and_verify_1_testgvccl_euro6coral1232_testgvccl_euro8coral123(self):
        """
        DESCRIPTION: Login with either one of the following users in the application and verify:-
        DESCRIPTION: 1. testgvccl-euro6/Coral123
        DESCRIPTION: 2. testgvccl-euro8/Coral123
        EXPECTED: Message shown on the top of the Home page stating
        EXPECTED: 'You can only deposit & play once your account has been verified. Please verify it here (hyper link)'
        """
        pass

    def test_002_click_on_hyperlink_please_verify_it_here(self):
        """
        DESCRIPTION: Click on hyperlink 'Please verify it here'
        EXPECTED: 1. The user is prompted to upload documents for age and address proof.
        EXPECTED: 2. There is no option for the user to deposit funds.
        """
        pass

    def test_003_click_on_logout(self):
        """
        DESCRIPTION: Click on Logout.
        EXPECTED: User logs out from the application successfully.
        """
        pass
