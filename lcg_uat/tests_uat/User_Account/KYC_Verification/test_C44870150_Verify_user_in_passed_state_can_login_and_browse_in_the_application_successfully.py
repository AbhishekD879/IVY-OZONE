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
class Test_C44870150_Verify_user_in_passed_state_can_login_and_browse_in_the_application_successfully(Common):
    """
    TR_ID: C44870150
    NAME: Verify user in passed state can login and browse in the application successfully.
    DESCRIPTION: Ref : https://app.zeplin.io/project/5c935fb0320dd2055d273d96/screen/5c9a0d1ac54bff583f05ecd8
    PRECONDITIONS: 1. User's account should be having status as 'passed', i.e. user's KYC documents have been accepted.
    PRECONDITIONS: 2. User should not be logged in the application.
    PRECONDITIONS: 3. Note:- In IMS database - IMS AGE verification status = Passed
    """
    keep_browser_open = True

    def test_001_log_in_the_application_with_the_user_and_verify(self):
        """
        DESCRIPTION: Log in the application with the user and verify.
        EXPECTED: The user is logged in.
        """
        pass

    def test_002_navigate_to_2_3_pages_in_the_application_verify(self):
        """
        DESCRIPTION: Navigate to 2-3 pages in the application. Verify.
        EXPECTED: The user is able to navigate in the application.
        """
        pass

    def test_003_navigate_to_the_deposit_page_and_verify(self):
        """
        DESCRIPTION: Navigate to the Deposit page and verify.
        EXPECTED: The user is able to navigate to the deposit page.
        """
        pass
