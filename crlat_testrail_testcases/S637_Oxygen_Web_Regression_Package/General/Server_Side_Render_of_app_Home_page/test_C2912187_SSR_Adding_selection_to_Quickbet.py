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
class Test_C2912187_SSR_Adding_selection_to_Quickbet(Common):
    """
    TR_ID: C2912187
    NAME: SSR. Adding selection to Quickbet
    DESCRIPTION: Test case verifies record on SSR snapshot when user adds one selection to quickbet, before the application has finished loading.
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turned on in System configuration > Structure
    PRECONDITIONS: **User is logged in**
    PRECONDITIONS: **OpenBet Systems**
    PRECONDITIONS: - https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=OpenBet+Systems
    PRECONDITIONS: To check request/response to Remote Betslip MS open DevTools -> Network -> WS -> Frames
    """
    keep_browser_open = True

    def test_001_empty_cache_and_hard_reload(self):
        """
        DESCRIPTION: Empty cache and hard reload
        EXPECTED: Splash screen is shown for a few seconds and then substituted with rendered SSR snapshot
        """
        pass

    def test_002_while_ssr_snapshot_is_shown_tap_on_any_price_odds_button_on_it(self):
        """
        DESCRIPTION: While SSR snapshot is shown tap on any Price Odds button on it
        EXPECTED: * Grey overlay is shown
        EXPECTED: * Spinner is displayed within grey overlay
        EXPECTED: * App is not receiving other taps
        EXPECTED: * No request is sent to Remote Betslip MS in WS to get selection data
        """
        pass

    def test_003_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded)
        EXPECTED: * Grey overlay and spinner disappears
        EXPECTED: * 30001 request is sent to Remote Betslip MS in WS to get selection data
        EXPECTED: * Quickbet displays selected outcome
        """
        pass

    def test_004_empty_cache_and_hard_reload_while_ssr_snapshot_is_shown_tap_on_another_odds_button_and_in_backoffice_change_price_for_that_selection(self):
        """
        DESCRIPTION: Empty cache and hard reload. While SSR snapshot is shown tap on another Odds button and in BackOffice change price for that selection
        EXPECTED: * Grey overlay is shown
        EXPECTED: * Spinner is displayed within grey overlay
        EXPECTED: * App is not receiving other taps
        EXPECTED: * No request is sent to Remote Betslip MS in WS to get selection data
        """
        pass

    def test_005_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded)
        EXPECTED: * Grey overlay and spinner disappears
        EXPECTED: * Quickbet displays selected outcome
        EXPECTED: * 30001 request is sent to Remote Betslip MS in WS to get selection data
        EXPECTED: * Message about price change is displayed within Quick Bet
        """
        pass

    def test_006_empty_cache_and_hard_reload_while_ssr_snapshot_is_shown_tap_on_another_odds_button_and_in_backoffice_suspend_selectionmarketevent(self):
        """
        DESCRIPTION: Empty cache and hard reload. While SSR snapshot is shown tap on another Odds button and in BackOffice suspend selection/market/event
        EXPECTED: * Grey overlay is shown
        EXPECTED: * Spinner is displayed within grey overlay
        EXPECTED: * App is not receiving other taps
        EXPECTED: * No request is sent to Remote Betslip MS in WS to get selection data
        """
        pass

    def test_007_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded)
        EXPECTED: * Grey overlay and spinner disappears
        EXPECTED: * Quickbet displays selected and greyed out outcome
        EXPECTED: * 30001 request is sent to Remote Betslip MS in WS to get selection data
        EXPECTED: * Message about suspension selection/market/event is present within Quick Bet
        """
        pass

    def test_008_empty_cache_and_hard_reload_while_ssr_is_shown_tap_on_another_odds_button_and_in_backoffice_undisplay_selectionmarketevent(self):
        """
        DESCRIPTION: Empty cache and hard reload. While SSR is shown tap on another Odds button and in BackOffice undisplay selection/market/event
        EXPECTED: * Grey overlay is shown
        EXPECTED: * Spinner is displayed within grey overlay
        EXPECTED: * App is not receiving other taps
        EXPECTED: * No request is sent to Remote Betslip MS in WS to get selection data
        """
        pass

    def test_009_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded)
        EXPECTED: * Grey overlay and spinner disappears
        EXPECTED: * 30001 request is sent to Remote Betslip MS in WS to get selection data
        EXPECTED: * Quick Bet is displayed
        EXPECTED: * 'Selection is no longer available' error message is displayed
        EXPECTED: **NOTE** to be checked and updated
        """
        pass

    def test_010_empty_cache_and_hard_reload_while_ssr_is_shown_tap_on_another_suspended_price_odds_button(self):
        """
        DESCRIPTION: Empty cache and hard reload. While SSR is shown tap on another suspended Price Odds button
        EXPECTED: * Grey overlay and spinner are NOT shown
        EXPECTED: * App is not receiving other taps
        EXPECTED: * No request is sent to Remote Betslip MS in WS to get selection data
        """
        pass

    def test_011_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded)
        EXPECTED: * App is loaded
        EXPECTED: * Quick Bet is NOT opened
        """
        pass

    def test_012_add_any_selection_s_to_betslip(self):
        """
        DESCRIPTION: Add any selection(-s) to Betslip
        EXPECTED: Selection(-s) is present in Betslip
        """
        pass

    def test_013_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step #2
        EXPECTED: 
        """
        pass

    def test_014_wait_until_app_is_loaded_mainjs_is_loaded(self):
        """
        DESCRIPTION: Wait until app is loaded (main.js is loaded)
        EXPECTED: * App is loaded
        EXPECTED: * Quick Bet is NOT opened
        EXPECTED: * Price Odds button is selected and highlighted in green
        EXPECTED: * Betslip counter increased by 1
        """
        pass

    def test_015_repeat_steps_1_14_but_try_to_open_quick_bet_after__2_seconds__5_seconds__7_secondsof_ssr_snapshot_rendering(self):
        """
        DESCRIPTION: Repeat steps #1-14, but try to open Quick Bet after
        DESCRIPTION: - 2 seconds
        DESCRIPTION: - 5 seconds
        DESCRIPTION: - 7 seconds
        DESCRIPTION: of SSR snapshot rendering
        EXPECTED: 
        """
        pass
