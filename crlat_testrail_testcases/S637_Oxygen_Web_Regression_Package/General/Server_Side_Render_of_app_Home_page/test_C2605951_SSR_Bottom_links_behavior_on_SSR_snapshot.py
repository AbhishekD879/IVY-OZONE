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
class Test_C2605951_SSR_Bottom_links_behavior_on_SSR_snapshot(Common):
    """
    TR_ID: C2605951
    NAME: SSR. Bottom links behavior on SSR snapshot
    DESCRIPTION: Test case verifies user can click on Footer links while SSR snapshot is shown
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Slow 3G (or Fast 3G) mode
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turned on in System configuration > Structure
    """
    keep_browser_open = True

    def test_001_trigger_ssr_snapshot_empty_cash_and_hard_re_load(self):
        """
        DESCRIPTION: Trigger SSR snapshot (Empty cash and hard re-load)
        EXPECTED: Splash screen is shown for a few seconds and then substituted with rendered snapshot
        """
        pass

    def test_002_while_ssr_snapshot_is_shown_scroll_down_and_click_on_the_bottom_links_for_ex_terms__conditions(self):
        """
        DESCRIPTION: While SSR snapshot is shown scroll down and click on the Bottom links (for ex. Terms & Conditions)
        EXPECTED: Click is received while SSR snapshot is shown and link opens
        """
        pass
