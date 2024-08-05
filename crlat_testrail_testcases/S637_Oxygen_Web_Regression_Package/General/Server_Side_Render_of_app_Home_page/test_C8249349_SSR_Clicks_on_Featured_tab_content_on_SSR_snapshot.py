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
class Test_C8249349_SSR_Clicks_on_Featured_tab_content_on_SSR_snapshot(Common):
    """
    TR_ID: C8249349
    NAME: SSR. Clicks on Featured tab content on SSR snapshot
    DESCRIPTION: Test case verifies record of clicks on SSR snapshot and it's replay after app is loaded
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

    def test_002_click_on_odds_button_wait_until_app_is_loaded(self):
        """
        DESCRIPTION: Click on Odds button. Wait until app is loaded
        EXPECTED: Grey overlay on SSR snapshot and Quick Bet dialog is opened after dynamic app is loaded
        """
        pass

    def test_003_trigger_ssr_snapshot_and_perform_click_on_event_card_wait_until_app_is_loaded(self):
        """
        DESCRIPTION: Trigger SSR snapshot and perform click on Event Card. Wait until app is loaded
        EXPECTED: Grey overlay on SSR snapshot and Event Details Page is shown after app is loaded
        """
        pass

    def test_004_trigger_ssr_snapshot_and_perform_click_on_view_all_sport_betting_link_wait_until_app_is_loaded(self):
        """
        DESCRIPTION: Trigger SSR snapshot and perform click on View All (Sport) Betting link. Wait until app is loaded
        EXPECTED: Grey overlay on SSR snapshot and Sport page is opened after dynamic app is loaded
        """
        pass

    def test_005_trigger_ssr_snapshot_and_perform_click_on_plus_markets_link_inside_accordion_wait_until_app_is_loaded(self):
        """
        DESCRIPTION: Trigger SSR snapshot and perform click on "+ markets" link inside accordion. Wait until app is loaded
        EXPECTED: Grey overlay on SSR snapshot and Sport page is opened after dynamic app is loaded
        """
        pass
