import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C1992373_Tracking_for_pre_login_without_cookie(Common):
    """
    TR_ID: C1992373
    NAME: Tracking for pre-login without cookie
    DESCRIPTION: This test case verifies appsflyer tracking for pre-login without cookie banner_domainclick
    PRECONDITIONS: 1. iOS smart banner is configured in CMS
    PRECONDITIONS: 2. iOS smart banner is visible for pre-login user.
    PRECONDITIONS: 3. Local storage and cookies are cleared.
    """
    keep_browser_open = True

    def test_001_load_invictus_app(self):
        """
        DESCRIPTION: Load invictus app
        EXPECTED: - iOS smart banner is displayed
        EXPECTED: - banner_domainclick cookie is not present in Application > Cookies
        """
        pass

    def test_002_verify_network__httpsappappsflyercomidxxxxxxxxxpidsmartbanner_url(self):
        """
        DESCRIPTION: Verify Network > https://app.appsflyer.com/idXXXXXXXXX?pid=SmartBanner&[...] URL
        EXPECTED: URL should contain c parameter: c=NoCookie :
        EXPECTED: https://app.appsflyer.com/idXXXXXXXXX?pid=SmartBanner&c=NoCookie
        """
        pass
