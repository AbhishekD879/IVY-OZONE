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
class Test_C2605943_SSR_Google_Tracking_of_Cookie_banner_actions(Common):
    """
    TR_ID: C2605943
    NAME: SSR. Google Tracking of Cookie banner actions
    DESCRIPTION: 
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turn on in System configuration > Structure
    PRECONDITIONS: - Static blocks > Cookie banner set links to be opened in a new tab: add attribute target="_blank" to the link tag
    PRECONDITIONS: Clear site data (Dev tools> Application > Clear Storage)
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: Splash screen is shown for a few seconds and then substituted with rendered snapshot
        """
        pass

    def test_002_tap_accept_on_cookie_banner_while_ssr_snapshot_is_shown(self):
        """
        DESCRIPTION: Tap Accept on Cookie banner while SSR snapshot is shown
        EXPECTED: Cookie banner disappears on SSR snapshot
        """
        pass

    def test_003_when_dynamic_app_is_loaded_open_console_and_perform_datalayer_command(self):
        """
        DESCRIPTION: When dynamic app is loaded open console and perform dataLayer command
        EXPECTED: The following has been recorded in dataLayer: event: "trackEvent"
        EXPECTED: eventAction: "cookie"
        EXPECTED: eventCategory: "policies banner"
        EXPECTED: eventLabel: "accept
        """
        pass

    def test_004_clear_app_data_and_reload_appclick_on_privacy_policy_link(self):
        """
        DESCRIPTION: Clear app data and reload app. Click on Privacy Policy link
        EXPECTED: Link is opened
        """
        pass

    def test_005_when_dynamic_app_is_loaded_open_console_and_perform_datalayer_command(self):
        """
        DESCRIPTION: When dynamic app is loaded open console and perform dataLayer command
        EXPECTED: The following has been recorded in dataLayer: event: "trackEvent"
        EXPECTED: eventAction: event: "trackEvent"
        EXPECTED: eventAction: "cookie"
        EXPECTED: eventCategory: "policies banner"
        EXPECTED: eventLabel: "privacy policy”
        """
        pass

    def test_006_clear_app_data_and_reload_appclick_on_cookie_policy_link(self):
        """
        DESCRIPTION: Clear app data and reload app. Click on Cookie Policy link
        EXPECTED: The following has been recorded in dataLayer: event: "trackEvent"
        EXPECTED: eventAction: event: event: "trackEvent"
        EXPECTED: eventAction: "cookie"
        EXPECTED: eventCategory: "policies banner"
        EXPECTED: eventLabel: "cookie policy"
        """
        pass
