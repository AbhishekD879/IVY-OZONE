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
class Test_C2988627_Homepage_Onboarding_displayed_on_first_app_launch(Common):
    """
    TR_ID: C2988627
    NAME: Homepage Onboarding displayed on first app launch
    DESCRIPTION: This test case verifies that Onboarding overlay is displayed when the app is launched for the 1st time (no cache/cookies)
    PRECONDITIONS: Single onboarding overlay configured in CMS
    PRECONDITIONS: Browser cookies/cache is cleared
    """
    keep_browser_open = True

    def test_001_navigate_to_oxygen_fe(self):
        """
        DESCRIPTION: Navigate to Oxygen FE
        EXPECTED: Onboarding overlay is displayed
        """
        pass

    def test_002_observe_onboarding_overlay(self):
        """
        DESCRIPTION: Observe Onboarding overlay
        EXPECTED: Onboarding overlay contains:
        EXPECTED: * Image set in CMS
        EXPECTED: * Images indicator (dots)
        EXPECTED: * Close button
        """
        pass

    def test_003_tap_on_cta_button_close(self):
        """
        DESCRIPTION: Tap on CTA button (close)
        EXPECTED: Onboarding overlay is closed
        """
        pass

    def test_004_reload_the_page(self):
        """
        DESCRIPTION: Reload the page
        EXPECTED: Onboarding overlay is not displayed
        """
        pass
