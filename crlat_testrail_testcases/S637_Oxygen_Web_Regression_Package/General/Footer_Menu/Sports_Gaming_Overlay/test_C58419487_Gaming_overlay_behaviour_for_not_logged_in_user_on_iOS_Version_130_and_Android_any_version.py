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
class Test_C58419487_Gaming_overlay_behaviour_for_not_logged_in_user_on_iOS_Version_130_and_Android_any_version(Common):
    """
    TR_ID: C58419487
    NAME: "Gaming" overlay behaviour for not logged in user on iOS Version >= 13.0 and Android (any version)
    DESCRIPTION: This test case verifies "Gaming" overlay behaviour for not logged in user on iOS Version >= 13.0 and all Android versions
    DESCRIPTION: Test case should only be run on mobile/tablet browsers (Safari, Chrome)
    DESCRIPTION: AUTOTEST [C58626054]
    PRECONDITIONS: User is not logged in
    PRECONDITIONS: iOS version is >= 13.0
    PRECONDITIONS: Android - all versions
    PRECONDITIONS: Design: https://app.zeplin.io/project/5c6ac2bc1c25679a7c64f730?seid=5e26bf41f308cd9894fd184e
    PRECONDITIONS: Gaming Overlay Enabled in CMS :
    PRECONDITIONS: System Configuration -> Structure -> GamingEnabled > enabled=true
    PRECONDITIONS: System Configuration -> Structure -> GamingEnabled > overlayUrl > set url
    PRECONDITIONS: ![](index.php?/attachments/get/101693960)
    PRECONDITIONS: overlayUrls:
    PRECONDITIONS: Ladbrokes: https://www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    PRECONDITIONS: Coral:
    PRECONDITIONS: https://qa2.www.coral.co.uk/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    """
    keep_browser_open = True

    def test_001_open_the_application_and_scroll_down_to_the_tab_bar(self):
        """
        DESCRIPTION: Open the application and scroll down to the Tab bar
        EXPECTED: Application is opened and the Tab bar is visible
        """
        pass

    def test_002_tap_on_the_gaming_icon_on_the_tab_bar(self):
        """
        DESCRIPTION: Tap on the "Gaming" icon on the Tab bar
        EXPECTED: - User is taken to the "Casino" landing page
        EXPECTED: - Login overlay or Face/ Touch ID is NOT shown
        """
        pass
