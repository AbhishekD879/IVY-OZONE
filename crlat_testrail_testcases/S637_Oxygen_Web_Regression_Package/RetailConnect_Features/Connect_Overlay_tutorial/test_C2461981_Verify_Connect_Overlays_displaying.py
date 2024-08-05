import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2461981_Verify_Connect_Overlays_displaying(Common):
    """
    TR_ID: C2461981
    NAME: Verify Connect Overlays displaying
    DESCRIPTION: This test case verifies that Connect Overlay will be shown for the user, who had Connect app on his device earlier
    PRECONDITIONS: Make sure Connect Overlay tutorial feature is turned on in CMS: System configuration -> Connect -> overlay
    PRECONDITIONS: * If no overlay appears, ensure that in dev tool -> Application tab -> cookies: field Name 'CONNECT_TRACKER' = 'false' and in Locale storage: OX.connectOverlayRemain is = 4.
    PRECONDITIONS: * Reload the SB app
    PRECONDITIONS: * Connect overlay tutorial is shown
    """
    keep_browser_open = True

    def test_001_close_the_overlay_shown_for_the_first_time_with_a_close_button_x(self):
        """
        DESCRIPTION: Close the overlay (shown for the first time) with a close button (X)
        EXPECTED: * The overlay is closed
        EXPECTED: * Home page is shown
        EXPECTED: * Locale storage: OX.connectOverlayRemain shows value 3
        """
        pass

    def test_002_reload_the_homepage(self):
        """
        DESCRIPTION: Reload the Homepage
        EXPECTED: * A user is left on the Homepage
        EXPECTED: * Connect overlay is displayed for the second time
        EXPECTED: * Locale storage: OX.connectOverlayRemain shows value 2
        """
        pass

    def test_003_tap_an_image_of_the_connect_logo(self):
        """
        DESCRIPTION: Tap an image of the Connect logo
        EXPECTED: Connect landing page is opened
        """
        pass

    def test_004_make_sure_connect_overlay_is_not_shown_on_any_other_page_except_home_page_go_to_any_any_sports_landing_page_reload_the_page(self):
        """
        DESCRIPTION: Make sure Connect Overlay is not shown on any other page except Home page:
        DESCRIPTION: * Go to any (any) Sports landing page
        DESCRIPTION: * Reload the page
        EXPECTED: Connect Overlay does not appear
        """
        pass

    def test_005_tap_homepage_button(self):
        """
        DESCRIPTION: Tap Homepage button
        EXPECTED: Homepage is opened
        """
        pass

    def test_006_verify_log_in_does_not_influence_connect_overlay_displaying_log_in_with_existing_user(self):
        """
        DESCRIPTION: Verify Log in does not influence Connect Overlay displaying:
        DESCRIPTION: * Log in with existing user
        EXPECTED: * User is logged in successfully
        EXPECTED: * default Sportsbook overlay is displayed if user is logged in for the first
        EXPECTED: * Dialogs pop ups are displayed if required
        """
        pass

    def test_007_reload_the_homepage(self):
        """
        DESCRIPTION: Reload the Homepage
        EXPECTED: * A user is left on the Homepage
        EXPECTED: * Connect overlay is displayed for the third time
        EXPECTED: * Locale storage: OX.connectOverlayRemain shows value 1
        """
        pass

    def test_008_tap_take_me_to_the_connect_hub_button(self):
        """
        DESCRIPTION: Tap 'TAKE ME TO THE CONNECT HUB' button
        EXPECTED: Connect landing page is opened
        """
        pass

    def test_009_tap_homepage_button(self):
        """
        DESCRIPTION: Tap Homepage button
        EXPECTED: Homepage is opened
        """
        pass

    def test_010_reload_the_homepage(self):
        """
        DESCRIPTION: Reload the Homepage
        EXPECTED: * A user is left on the Homepage
        EXPECTED: * Connect overlay is displayed for the las time
        EXPECTED: * Locale storage: OX.connectOverlayRemain shows value 0
        """
        pass

    def test_011_reload_the_homepage_again(self):
        """
        DESCRIPTION: Reload the Homepage again
        EXPECTED: * A user is left on the Homepage
        EXPECTED: * Connect overlay is not shown any more
        """
        pass
