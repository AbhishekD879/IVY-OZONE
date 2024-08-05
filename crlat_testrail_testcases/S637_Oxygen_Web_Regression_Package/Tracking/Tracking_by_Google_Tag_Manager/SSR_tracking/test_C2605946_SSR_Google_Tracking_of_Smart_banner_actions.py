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
class Test_C2605946_SSR_Google_Tracking_of_Smart_banner_actions(Common):
    """
    TR_ID: C2605946
    NAME: SSR. Google Tracking of Smart banner actions
    DESCRIPTION: Test case verifies GTM actions on Smart banner are recorded in dataLayer
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turn on in System configuration > Structure
    PRECONDITIONS: - Enable smart banner System configuration > Structure > Smart Banners
    PRECONDITIONS: Clear site data (Dev tools> Application > Clear Storage)
    """
    keep_browser_open = True

    def test_001_load_appwhile_ssr_snapshot_is_shown_tap_download_on_smart_banner_perform_datalayer_command_in_console(self):
        """
        DESCRIPTION: Load app.
        DESCRIPTION: While SSR snapshot is shown tap Download on Smart banner. Perform dataLayer command in Console
        EXPECTED: The following action recorded:
        EXPECTED: event: "trackEvent" eventAction: "click" eventCategory: "ios - smart banner" eventLabel: "Coral Sports Betting & Casino"
        """
        pass

    def test_002_trigger_ssr_snapshot_empty_cash_and_hard_re_load_tap_on_the_close_button_on_smart_bannerperform_datalayer_command_in_console(self):
        """
        DESCRIPTION: Trigger SSR snapshot (Empty cash and hard re-load). Tap on the Close button on Smart banner.
        DESCRIPTION: Perform dataLayer command in Console
        EXPECTED: The following action recorded:
        EXPECTED: event: "trackEvent" eventAction: "close" eventCategory: "ios - smart banner" eventLabel: "Coral Sports Betting & Casino"
        """
        pass
