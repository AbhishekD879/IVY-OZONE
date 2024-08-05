import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2605942_SSR_Cookie_banner_of_SSR_snapshot(Common):
    """
    TR_ID: C2605942
    NAME: SSR. Cookie banner of SSR snapshot
    DESCRIPTION: Test case verifies user can click on Cookie banner links and Accept button while SSR snapshot is shown. Accepting a cookie banner is recorded in local storage
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turn on in System configuration > Structure
    PRECONDITIONS: To edit Cookie banner links: Static Blocks > Cookie banner >  "<>"in html text editor
    PRECONDITIONS: Clear site data (Dev tools> Application > Clear Storage)
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: Splash screen is shown for a few seconds and then substituted with rendered snapshot
        """
        pass

    def test_002_verify_cookie_banner_is_present_on_ssr_snapshot(self):
        """
        DESCRIPTION: Verify Cookie banner is present on SSR snapshot
        EXPECTED: Cookie banner is present
        """
        pass

    def test_003_click_on_accept(self):
        """
        DESCRIPTION: Click on Accept
        EXPECTED: Cookie banner disappears on SSR snapshot.  Parameter OX.cookieBannerVersion is recorded in local storage
        """
        pass

    def test_004_trigger_ssr_snapshot_empty_cash_and_hard_re_load(self):
        """
        DESCRIPTION: Trigger SSR snapshot (Empty cash and hard re-load)
        EXPECTED: Cookie banner is not shown
        """
        pass

    def test_005_clear_app_data_and_reload_app_verify_cookie_banner_links(self):
        """
        DESCRIPTION: Clear app data and reload app. Verify cookie banner links
        EXPECTED: Cookie banner links are clickable and open in the same or new tab (according to CMS html tag from pre-conditions)
        """
        pass
