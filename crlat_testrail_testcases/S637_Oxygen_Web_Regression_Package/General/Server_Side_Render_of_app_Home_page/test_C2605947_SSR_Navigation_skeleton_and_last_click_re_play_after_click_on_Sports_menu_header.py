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
class Test_C2605947_SSR_Navigation_skeleton_and_last_click_re_play_after_click_on_Sports_menu_header(Common):
    """
    TR_ID: C2605947
    NAME: SSR. Navigation skeleton and last click re-play after click on Sports menu header
    DESCRIPTION: Test case verifies record of clicks on SSR navigation skeleton triggered from Sports menu ribbon and replay of the last click after app is loaded
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turned on in System configuration > Structure
    PRECONDITIONS: **App is loaded**
    """
    keep_browser_open = True

    def test_001_empty_cache_and_hard_re_load(self):
        """
        DESCRIPTION: Empty cache and hard re-load
        EXPECTED: SSR is applied (Splash screen is shown for a few seconds and then substituted with rendered snapshot)
        """
        pass

    def test_002_while_ssr_snapshot_is_shown_tap_on_some_item_within_sports_menu_ribbon(self):
        """
        DESCRIPTION: While SSR snapshot is shown tap on some item within Sports menu ribbon
        EXPECTED: Navigation skeleton is shown
        """
        pass

    def test_003_click_on_a_few_menu_items_on_the_footer_menu_and_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Click on a few menu items on the footer menu and wait until app is loaded (main.js is loaded)
        EXPECTED: The last click is replayed after app is loaded
        """
        pass
