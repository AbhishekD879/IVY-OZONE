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
class Test_C44870151_User_Account_one_page_for_conditions_under_review(Common):
    """
    TR_ID: C44870151
    NAME: User  Account one page for conditions under review
    DESCRIPTION: User  logged in should be directed to Account one page for Both Conditions
    PRECONDITIONS: " 1. IMS AGE verification status = Unknown/Active grace period
    PRECONDITIONS: player tags POA_required/ AGP_Success_Upload =<5
    PRECONDITIONS: OR
    PRECONDITIONS: 2. IMS AGE verification status = Unknown/Active grace period
    PRECONDITIONS: No Players tags"
    """
    keep_browser_open = True

    def test_001_user_opens_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: User opens https://beta-sports.coral.co.uk/
        EXPECTED: Beta application launched.
        """
        pass

    def test_002_login_in_with_user_(self):
        """
        DESCRIPTION: Login in with user :
        EXPECTED: User is logged in and directed to account one page.
        """
        pass

    def test_003_verify_account_one_page(self):
        """
        DESCRIPTION: Verify account one page
        EXPECTED: User displayed with appropriate information and cannot place bets/deposit/withdraw etc.
        """
        pass
