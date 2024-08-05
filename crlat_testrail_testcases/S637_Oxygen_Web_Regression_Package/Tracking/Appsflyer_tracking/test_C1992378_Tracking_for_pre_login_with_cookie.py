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
class Test_C1992378_Tracking_for_pre_login_with_cookie(Common):
    """
    TR_ID: C1992378
    NAME: Tracking for pre-login with cookie
    DESCRIPTION: This test case verifies appsflyer tracking for pre-login with cookie banner_domainclick
    PRECONDITIONS: 1. iOS smart banner is configured in CMS
    PRECONDITIONS: 2. iOS smart banner is visible for pre-login user.
    PRECONDITIONS: 3. Local storage and cookies are cleared.
    PRECONDITIONS: 4. **Testing links:**
    PRECONDITIONS: Coral link with C parameter for testing
    PRECONDITIONS: http://wlcoral.iaofr.com/wl/clk/?btag=a_1b_17000&c=test
    PRECONDITIONS: Coral link without C parameter for testing
    PRECONDITIONS: http://wlcoral.iaofr.com/wl/clk/?btag=a_1b_17000
    PRECONDITIONS: **NOTE:** We can receive banner_domainclick cookie only via production right now. How to do this:
    PRECONDITIONS: - click one of the testing links above (with or wothout C parameter)
    PRECONDITIONS: - from promo page navigate to prod env via clicking "Play Now"
    PRECONDITIONS: - verify banner_domainclick cookie is present in Application > Cookies.
    PRECONDITIONS: - then open testing env in different tab (local storage and cookies should be cleared)
    PRECONDITIONS: - verify banner_domainclick cookie is avaiable in Application > Cookies with or without c param correspondingly.
    """
    keep_browser_open = True

    def test_001_perform_steps_from_preconditions_to_receive_banner_domainclick_cookie_without_c_parameter(self):
        """
        DESCRIPTION: Perform steps from preconditions to receive banner_domainclick cookie WITHOUT c parameter
        EXPECTED: 
        """
        pass

    def test_002_load_invictus_app(self):
        """
        DESCRIPTION: Load invictus app
        EXPECTED: - iOS smart banner is displayed
        EXPECTED: - banner_domainclick cookie is present in Application > Cookies without c parameter
        """
        pass

    def test_003_verify_network__httpsappappsflyercomidxxxxxxxxxpidsmartbanner_url(self):
        """
        DESCRIPTION: Verify Network > https://app.appsflyer.com/idXXXXXXXXX?pid=SmartBanner&[...] URL
        EXPECTED: URL should not contain c parameter:
        EXPECTED: Request URL: https://app.appsflyer.com/idXXXXXXXXX?pid=SmartBanner&c=affiliate&af_sub1=3calp100dt&af_sub2=a_1b_17000&af_sub3=
        """
        pass

    def test_004_clear_local_storage_and_cookies_and_perform_steps_from_preconditions_to_receive_banner_domainclick_cookie_with_c_parameter(self):
        """
        DESCRIPTION: Clear local storage and cookies and perform steps from preconditions to receive banner_domainclick cookie WITH c parameter
        EXPECTED: 
        """
        pass

    def test_005_load_invictus_app(self):
        """
        DESCRIPTION: Load invictus app
        EXPECTED: - iOS smart banner is displayed
        EXPECTED: - banner_domainclick cookie is present in Application > Cookies with c parameter
        """
        pass

    def test_006_verify_network__httpsappappsflyercomidxxxxxxxxxpidsmartbanner_url(self):
        """
        DESCRIPTION: Verify Network > https://app.appsflyer.com/idXXXXXXXXX?pid=SmartBanner&[...] URL
        EXPECTED: URL should contain c parameter:
        EXPECTED: Request URL: https://app.appsflyer.com/id553287152?pid=SmartBanner&c=affiliate&af_sub1=3calp100dt&af_sub2=a_1b_17000&af_sub3=c_test
        """
        pass
