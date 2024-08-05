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
class Test_C2605940_SSR_snapshot_is_triggered_on_3G_speed_when_app_is_loaded_for_the_first_time(Common):
    """
    TR_ID: C2605940
    NAME: SSR snapshot is triggered on 3G speed when app is loaded for the first time
    DESCRIPTION: Test case verifies that Site Server Render is applied when app is loaded with empty cache
    PRECONDITIONS: **Requirements to testing:**
    PRECONDITIONS: To be tested on the environment with Akamai, in Fast 3G mode (also applied to slow 3G and Online, but fast 3G is optimal)
    PRECONDITIONS: **CMS configuration:**
    PRECONDITIONS: - Featured module ribbon tab is set as the first module
    PRECONDITIONS: - SSR is turned on in System configuration > Structure
    PRECONDITIONS: Clear site data (Dev tools> Application > Clear Storage)
    """
    keep_browser_open = True

    def test_001_load_app_when_app_storage_is_cleared(self):
        """
        DESCRIPTION: Load app when app storage is cleared
        EXPECTED: SSR is triggered (splash screen is shown for a few seconds and then substituted with rendered snapshot)
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

    def test_004_perform_regular_refresh(self):
        """
        DESCRIPTION: Perform regular refresh
        EXPECTED: App is loaded without SSR
        """
        pass

    def test_005_perform_empty_cache_and_hard_re_load(self):
        """
        DESCRIPTION: Perform Empty cache and hard re-load
        EXPECTED: SSR is triggered (Splash screen is shown for a few seconds and then substituted with rendered snapshot)
        """
        pass

    def test_006_verify_user_can_navigate_after_app_is_loaded(self):
        """
        DESCRIPTION: Verify user can navigate after app is loaded
        EXPECTED: User can navigate across app
        """
        pass

    def test_007_verify_user_can_login_after_app_is_loaded(self):
        """
        DESCRIPTION: Verify user can login after app is loaded
        EXPECTED: User logs in
        """
        pass
