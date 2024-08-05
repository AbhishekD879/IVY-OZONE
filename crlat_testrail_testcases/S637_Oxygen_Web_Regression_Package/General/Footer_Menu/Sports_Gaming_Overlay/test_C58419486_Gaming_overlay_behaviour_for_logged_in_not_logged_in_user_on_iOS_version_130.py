import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C58419486_Gaming_overlay_behaviour_for_logged_in_not_logged_in_user_on_iOS_version_130(Common):
    """
    TR_ID: C58419486
    NAME: "Gaming" overlay behaviour for logged in/not logged in user on iOS version < 13.0
    DESCRIPTION: This test case verifies "Gaming Overlay" behaviour for logged in user on iOS version < 13.0
    DESCRIPTION: Test case should only be run on mobile/tablet browsers (Safari, Chrome)
    DESCRIPTION: AUTOTEST [C58626827]
    PRECONDITIONS: Design: https://app.zeplin.io/project/5c6ac2bc1c25679a7c64f730?seid=5e26bf41f308cd9894fd184e
    PRECONDITIONS: Gaming Overlay Enabled in CMS :
    PRECONDITIONS: System Configuration -> Config -> GamingEnabled > enabled=true
    PRECONDITIONS: System Configuration -> Config -> GamingEnabled > overlayUrl > set url(below).
    PRECONDITIONS: overlayUrls: for BETA -  https://beta-www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BINGO
    PRECONDITIONS: for QA - Coral:
    PRECONDITIONS: https://qa2.www.coral.co.uk/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    PRECONDITIONS: !!! Valid Ladb url: https://www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    PRECONDITIONS: The iOS version should be lower 13.0
    PRECONDITIONS: User is not logged in
    """
    keep_browser_open = True

    def test_001_launch_the_application_and_scroll_down_to_tab_bar(self):
        """
        DESCRIPTION: Launch the application and scroll down to Tab bar.
        EXPECTED: Application is opened and Tab bar is visible.
        """
        pass

    def test_002_tap_on_the_gaming_button_on_the_tap_bar(self):
        """
        DESCRIPTION: Tap on the "Gaming" button on the tap bar.
        EXPECTED: User is redirected to the "Casino" landing page.
        """
        pass

    def test_003_launch_the_application_and_log_in_with_correct_credentials(self):
        """
        DESCRIPTION: Launch the application and log in with correct credentials.
        EXPECTED: User is logged in and sees the "Home" page.
        """
        pass

    def test_004_tap_on_the_gaming_button_on_the_tab_bar(self):
        """
        DESCRIPTION: Tap on the "Gaming" button on the Tab bar.
        EXPECTED: User is redirected to the "Casino" landing page.
        """
        pass
