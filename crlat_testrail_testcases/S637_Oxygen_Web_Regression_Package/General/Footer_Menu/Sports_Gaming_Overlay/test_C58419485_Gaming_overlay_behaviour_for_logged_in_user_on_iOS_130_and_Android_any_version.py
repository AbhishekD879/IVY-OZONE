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
class Test_C58419485_Gaming_overlay_behaviour_for_logged_in_user_on_iOS_130_and_Android_any_version(Common):
    """
    TR_ID: C58419485
    NAME: "Gaming" overlay behaviour for logged in user on iOS >= 13.0 and Android  (any version)
    DESCRIPTION: This test case verifies opening and closing "Gaming" overlay.
    DESCRIPTION: Test case should only be run on mobile/tablet browsers (Safari, Chrome)
    PRECONDITIONS: Design: https://app.zeplin.io/project/5c6ac2bc1c25679a7c64f730?seid=5e26bf41f308cd9894fd184e
    PRECONDITIONS: Gaming Overlay Enabled in CMS :
    PRECONDITIONS: System Configuration -> Config -> GamingEnabled > enabled=true
    PRECONDITIONS: System Configuration -> Config -> GamingEnabled > overlayUrl > set url(below).
    PRECONDITIONS: overlayUrls: for BETA -  https://beta-www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BINGO
    PRECONDITIONS: for QA   -  Coral:
    PRECONDITIONS: https://qa2.www.coral.co.uk/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    PRECONDITIONS: !!! Valid Ladb url: https://www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    PRECONDITIONS: The iOS version should be higher than 13.0
    PRECONDITIONS: The user should be logged in.
    """
    keep_browser_open = True

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch Application.
        EXPECTED: Application is launched and user is navigated to the "Home" page.
        """
        pass

    def test_002_tap_on_the_gaming_button_on_the_tap_bar(self):
        """
        DESCRIPTION: Tap on the "Gaming" button on the tap bar.
        EXPECTED: "Gaming" overlay should be shown as per design.
        EXPECTED: ![](index.php?/attachments/get/101705294)
        """
        pass

    def test_003_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on "X" button.
        EXPECTED: "Gaming" overlay should be closed.
        EXPECTED: User should be on the page he was before opening "Gaming" overlay.
        """
        pass

    def test_004_navigate_to_any_sports_page_and_repeat_steps_1_3_above(self):
        """
        DESCRIPTION: Navigate to any Sports page and repeat Steps 1-3 above.
        EXPECTED: 
        """
        pass
