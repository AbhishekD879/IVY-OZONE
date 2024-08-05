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
class Test_C58419488_Enable_Disable_Gaming_overlay_in_CMS(Common):
    """
    TR_ID: C58419488
    NAME: Enable/Disable "Gaming" overlay in CMS
    DESCRIPTION: This test case verifies enabling/disabling "Gaming" overlay in CMS
    DESCRIPTION: Test case should only be run on mobile/tablet browsers (Safari, Chrome)
    PRECONDITIONS: Design: https://app.zeplin.io/project/5c6ac2bc1c25679a7c64f730?seid=5e26bf41f308cd9894fd184e
    PRECONDITIONS: Gaming Overlay Enabled in CMS :
    PRECONDITIONS: System Configuration -> Structure -> GamingEnabled > enabled=true
    PRECONDITIONS: System Configuration -> Structure -> GamingEnabled > overlayUrl > set url
    PRECONDITIONS: ![](index.php?/attachments/get/101693961)
    PRECONDITIONS: overlayUrls:
    PRECONDITIONS: for BETA -  https://beta-www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BINGO
    PRECONDITIONS: For QA -  Coral:
    PRECONDITIONS: https://qa2.www.coral.co.uk/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    PRECONDITIONS: !!! Valid Ladb url: https://www.ladbrokes.com/en/sportsoverlay?.box=1&invokerProduct=BETTING&_disableFeature=GlobalSearch
    """
    keep_browser_open = True

    def test_001_go_to_system_configuration___structure___gamingenabled_in_cms(self):
        """
        DESCRIPTION: Go to System Configuration -> Structure -> GamingEnabled in CMS
        EXPECTED: 
        """
        pass

    def test_002_set_gamingenabled_to_false_and_click_save_changes(self):
        """
        DESCRIPTION: Set "GamingEnabled" to 'false' and click "Save changes"
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_003_open_application_and_scroll_down_to_tab_bar(self):
        """
        DESCRIPTION: Open application and scroll down to Tab bar
        EXPECTED: Application is opened and Tab bar is visible
        """
        pass

    def test_004_tap_on_gaming_button(self):
        """
        DESCRIPTION: Tap on "Gaming" button
        EXPECTED: User is redirected to CMS Configured URL ("Gaming")
        """
        pass

    def test_005_go_to_cms_and_set_gamingenabled_to_true_and_click_save_changes(self):
        """
        DESCRIPTION: Go to CMS and set "GamingEnabled" to 'true' and click "Save changes"
        EXPECTED: Changes are saved in CMS
        """
        pass

    def test_006_open_the_application_and_tap_on_gaming_button(self):
        """
        DESCRIPTION: Open the application and tap on "Gaming" button
        EXPECTED: "Gaming" overlay is opened (note: iOS version should be >= 13.0 for that)
        EXPECTED: ![](index.php?/attachments/get/101694000)
        """
        pass
