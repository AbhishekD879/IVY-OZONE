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
class Test_C2605958_SSR_Scroll_position_is_saved_after_dynamic_app_is_loaded(Common):
    """
    TR_ID: C2605958
    NAME: SSR. Scroll position is saved after dynamic app is loaded
    DESCRIPTION: Test case verifies scroll position made on SSR snapshot is saved after app is loaded
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turned on in System configuration > Structure
    PRECONDITIONS: App is loaded
    """
    keep_browser_open = True

    def test_001_trigger_ssr_screen_empty_cash_and_hard_re_load(self):
        """
        DESCRIPTION: Trigger SSR screen (Empty cash and hard re-load)
        EXPECTED: SSR is applied (Splash screen is shown for a few seconds and then substituted with rendered snapshot)
        """
        pass

    def test_002_while_ssr_snapshot_is_shown_scroll_sports_menu_ribbon_wait_until_app_is_loaded(self):
        """
        DESCRIPTION: While SSR snapshot is shown scroll Sports menu ribbon. Wait until app is loaded
        EXPECTED: Scroll position is saved after app is loaded
        """
        pass

    def test_003_while_ssr_snapshot_is_shown_scroll_module_ribbon_tabs_wait_until_app_is_loaded(self):
        """
        DESCRIPTION: While SSR snapshot is shown scroll Module ribbon tabs. Wait until app is loaded
        EXPECTED: Scroll position is saved after app is loaded
        """
        pass

    def test_004_while_ssr_snapshot_is_shown_scroll_down_the_content_of_featured_tab_wait_until_app_is_loaded(self):
        """
        DESCRIPTION: While SSR snapshot is shown scroll down the content of featured tab. Wait until app is loaded
        EXPECTED: Scroll position is saved after app is loaded
        """
        pass
