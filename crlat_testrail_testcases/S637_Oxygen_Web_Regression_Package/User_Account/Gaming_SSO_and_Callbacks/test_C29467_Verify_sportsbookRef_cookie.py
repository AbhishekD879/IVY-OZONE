import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C29467_Verify_sportsbookRef_cookie(Common):
    """
    TR_ID: C29467
    NAME: Verify sportsbookRef cookie
    DESCRIPTION: This test case verifies presence of **sportsbookRef** cookie.
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-5731 (As a Games PO I want the BMA to create a cookie on the coral.co.uk domain to determine which sports book is referencing casino games)
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Application is loaded
        """
        pass

    def test_002_verify_created_cookie(self):
        """
        DESCRIPTION: Verify created cookie
        EXPECTED: sportsbookRef cookie was created on the Invictus application loading
        """
        pass

    def test_003_verify_cookie_name(self):
        """
        DESCRIPTION: Verify cookie Name
        EXPECTED: cookie Name: **sportsbookRef**
        """
        pass

    def test_004_verify_cookie_value(self):
        """
        DESCRIPTION: Verify cookie Value
        EXPECTED: cookie Value: **bma**
        """
        pass

    def test_005_verify_cookie_domain(self):
        """
        DESCRIPTION: Verify cookie Domain
        EXPECTED: cookie Domain: **.coral.co.uk**
        """
        pass

    def test_006_verify_cookie_expiresmax_age(self):
        """
        DESCRIPTION: Verify cookie Expires/Max-Age
        EXPECTED: cookie Expires/Max-Age:
        EXPECTED: **created time + 3 days**
        """
        pass
