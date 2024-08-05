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
class Test_C2605941_SSR_snapshot_triggered_when_app_cache_is_empty_and_user_is_logged_in(Common):
    """
    TR_ID: C2605941
    NAME: SSR snapshot triggered when app cache is empty and user is logged in
    DESCRIPTION: Test case verifies that SSR is triggered when user is logged in but app cache is empty
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turn on in System configuration > Structure
    PRECONDITIONS: **User is logged in**
    """
    keep_browser_open = True

    def test_001_empty_cash_and_hard_re_load(self):
        """
        DESCRIPTION: Empty cash and hard re-load
        EXPECTED: SSR is applied (Splash screen is shown for a few seconds and then substituted with rendered snapshot)
        """
        pass

    def test_002_verify_the_spinner_on_the_login_button(self):
        """
        DESCRIPTION: Verify the spinner on the login button
        EXPECTED: The spinner is shown on the login button until dynamic app is loaded (main.js is loaded)
        """
        pass

    def test_003_verify_header_menu_buttons_after_app_is_loaded(self):
        """
        DESCRIPTION: Verify header menu buttons after app is loaded
        EXPECTED: Join button, Login, Betslip buttons are present
        """
        pass

    def test_004_refresh_app(self):
        """
        DESCRIPTION: Refresh app
        EXPECTED: SSR is not applied (app reloaded regularly)
        """
        pass
