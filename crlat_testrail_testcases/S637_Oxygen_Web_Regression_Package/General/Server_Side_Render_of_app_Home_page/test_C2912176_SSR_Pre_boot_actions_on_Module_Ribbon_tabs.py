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
class Test_C2912176_SSR_Pre_boot_actions_on_Module_Ribbon_tabs(Common):
    """
    TR_ID: C2912176
    NAME: SSR. Pre-boot actions on Module Ribbon tabs
    DESCRIPTION: Test case verifies record on SSR snapshot when user navigates within Module Ribbon tabs and it's re-play when app is loaded
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turned on in System configuration > Structure
    PRECONDITIONS: **User is logged in**
    """
    keep_browser_open = True

    def test_001_empty_cache_and_hard_reload(self):
        """
        DESCRIPTION: Empty cache and hard reload
        EXPECTED: Splash screen is shown for a few seconds and then substituted with rendered SSR snapshot
        """
        pass

    def test_002_while_ssr_screen_is_shown_select_in_play_option_on_module_ribbon_tabs(self):
        """
        DESCRIPTION: While SSR screen is shown, select 'In Play' option on Module Ribbon tabs
        EXPECTED: * Grey overlay is shown
        EXPECTED: * Spinner is displayed within grey overlay
        EXPECTED: * App is not receiving other taps
        EXPECTED: * No requests are sent to receive tab data
        """
        pass

    def test_003_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded)
        EXPECTED: * Grey overlay and spinner disappears
        EXPECTED: * 'In Play' tab is opened
        EXPECTED: * Content of 'In Play' tab is loaded
        """
        pass

    def test_004_repeat_steps_1_3_for_next_races_build_your_bet_enhanced_live_streammodule_ribbon_tab(self):
        """
        DESCRIPTION: Repeat steps #1-3 for
        DESCRIPTION: * Next Races
        DESCRIPTION: * Build Your Bet
        DESCRIPTION: * Enhanced
        DESCRIPTION: * Live stream
        DESCRIPTION: Module Ribbon tab
        EXPECTED: 
        """
        pass
