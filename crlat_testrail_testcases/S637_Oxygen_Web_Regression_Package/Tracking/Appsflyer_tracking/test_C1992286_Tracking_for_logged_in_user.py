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
class Test_C1992286_Tracking_for_logged_in_user(Common):
    """
    TR_ID: C1992286
    NAME: Tracking for logged in user
    DESCRIPTION: This test case verifies appsflyer tracking for logged in user
    PRECONDITIONS: 1. iOS smart banner is configured in CMS
    PRECONDITIONS: 2. iOS smart banner is visible for logged in user.
    PRECONDITIONS: 3. Local storage and cookies are cleared.
    """
    keep_browser_open = True

    def test_001_1_load_invictus_app_and_login(self):
        """
        DESCRIPTION: 1. Load invictus app and login
        EXPECTED: iOS smart banner is displayed
        """
        pass

    def test_002_verify_network__httpsappappsflyercomidxxxxxxxxxpidsmartbanner_url(self):
        """
        DESCRIPTION: Verify Network > https://app.appsflyer.com/idXXXXXXXXX?pid=SmartBanner&[...] URL
        EXPECTED: URL should contain c parameter: c=login :
        EXPECTED: https://app.appsflyer.com/idXXXXXXXXX?pid=SmartBanner&c=login
        """
        pass
