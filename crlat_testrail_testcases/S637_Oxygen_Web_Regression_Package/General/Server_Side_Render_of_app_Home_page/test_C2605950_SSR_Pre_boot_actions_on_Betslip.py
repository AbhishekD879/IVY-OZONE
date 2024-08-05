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
class Test_C2605950_SSR_Pre_boot_actions_on_Betslip(Common):
    """
    TR_ID: C2605950
    NAME: SSR. Pre-boot actions on Betslip
    DESCRIPTION: Test case verifies Betslip action record on SSR snapshot and it's re-play when app is loaded
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turned on in System configuration > Structure
    PRECONDITIONS: **User is logged in and selection is added to Betslip**
    """
    keep_browser_open = True

    def test_001_empty_cache_and_hard_reload(self):
        """
        DESCRIPTION: Empty cache and hard reload
        EXPECTED: Splash screen is shown for a few seconds and then substituted with rendered snapshot
        """
        pass

    def test_002_while_ssr_screen_is_shown_tap_on_betslip_icon(self):
        """
        DESCRIPTION: While SSR screen is shown tap on Betslip icon
        EXPECTED: Grey overlay is shown, app is not receiving other taps.
        """
        pass

    def test_003_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded)
        EXPECTED: Betslip is opened and selection is shown
        """
        pass

    def test_004_empty_cache_and_hard_reload_while_ssr_is_shown_tap_on_another_odds_button(self):
        """
        DESCRIPTION: Empty cache and hard reload. While SSR is shown tap on another Odds button
        EXPECTED: Grey overlay is shown, app is not receiving other taps.
        """
        pass

    def test_005_wait_until_app_is_loaded_mainjs_is_loaded_open_betslip(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded). Open Betslip
        EXPECTED: One more selection has been added to Betslip
        """
        pass

    def test_006_clear_site_data_application__clear_storage_and_re_load_app(self):
        """
        DESCRIPTION: Clear site data (Application > Clear Storage) and re-load app
        EXPECTED: Splash screen is shown for a few seconds and then substituted with rendered snapshot
        """
        pass

    def test_007_while_ssr_screen_is_shown_tap_on_betslip_icon(self):
        """
        DESCRIPTION: While SSR screen is shown tap on Betslip icon
        EXPECTED: Grey overlay is shown, app is not receiving other taps.
        """
        pass

    def test_008_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded)
        EXPECTED: Betslip is opened with “You have no selections in the slip” message
        """
        pass
