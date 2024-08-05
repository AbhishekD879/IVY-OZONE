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
class Test_C44870153_Verify_KYC_behavior_for_blocked_user(Common):
    """
    TR_ID: C44870153
    NAME: Verify KYC behavior for blocked user
    DESCRIPTION: User should be  able to login and redirected to Account one page(Hard redirect with no back URL) .
    PRECONDITIONS: " IMS AGE verification status = Active grace period
    PRECONDITIONS: player tag AGP_Success_Upload >5"
    """
    keep_browser_open = True

    def test_001_open_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Open https://beta-sports.coral.co.uk/
        EXPECTED: BETA application launched.
        """
        pass

    def test_002_login_in_with_user_(self):
        """
        DESCRIPTION: Login in with user :
        EXPECTED: User is logged in and presented with account one page detailing that the user is now blocked and must take appropriate steps to pass kyc process.
        """
        pass
