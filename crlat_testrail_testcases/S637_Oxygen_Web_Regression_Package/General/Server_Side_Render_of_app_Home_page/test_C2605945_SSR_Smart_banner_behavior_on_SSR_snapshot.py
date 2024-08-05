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
class Test_C2605945_SSR_Smart_banner_behavior_on_SSR_snapshot(Common):
    """
    TR_ID: C2605945
    NAME: SSR. Smart banner behavior on SSR snapshot
    DESCRIPTION: Test case verifies Smart banner display on SSR snapshot, possibility to close it and recording of Smart banner closure in local storage.
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turn on in System configuration > Structure
    PRECONDITIONS: - Enable Smart banner: System configuration > Structure: Smart banners
    PRECONDITIONS: Clear site data (Dev tools> Application > Clear Storage)
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: Splash screen is shown for a few seconds and then substituted with rendered snapshot
        """
        pass

    def test_002_verify_smart_banner_is_shown_on_the_bottom_while_ssr_snapshot_is_on_screen(self):
        """
        DESCRIPTION: Verify Smart banner is shown on the bottom while SSR snapshot is on-screen
        EXPECTED: Smart banner is present
        """
        pass

    def test_003_verify_smart_banner_stays_when_app_is_loaded(self):
        """
        DESCRIPTION: Verify Smart banner stays when app is loaded
        EXPECTED: After app is loaded (main.js) is loaded smart banner stays
        """
        pass

    def test_004_trigger_ssr_screen_empty_cash_and_hard_re_load(self):
        """
        DESCRIPTION: Trigger SSR screen (Empty cash and hard re-load)
        EXPECTED: Smart banner is shown on SSR snapshot
        """
        pass

    def test_005_tap_on_close_button_on_smart_banner_while_ssr_snapshot_is_shown(self):
        """
        DESCRIPTION: Tap on Close button on Smart banner while SSR snapshot is shown
        EXPECTED: Smart banner is closed (OX.smartBannerClosed parameter are recorded in local storage)
        """
        pass

    def test_006_trigger_ssr_screen_empty_cash_and_hard_re_load(self):
        """
        DESCRIPTION: Trigger SSR screen (Empty cash and hard re-load)
        EXPECTED: Smart banner is not shown
        """
        pass
