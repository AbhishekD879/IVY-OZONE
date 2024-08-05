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
class Test_C1490801_Verify_Desktop_Quick_Links(Common):
    """
    TR_ID: C1490801
    NAME: Verify Desktop Quick Links
    DESCRIPTION: This test case verifies Desktop Quick Links.
    DESCRIPTION: To be run on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * Desktop Quick Links should be configured and enabled in CMS (Menus>Desktop Quick Links) (refer to TC: https://ladbrokescoral.testrail.com/index.php?/cases/view/1489871 )
    PRECONDITIONS: * Text above Quick Links should be configured and enabled in CMS (Static Blocks) (refer to TC: https://ladbrokescoral.testrail.com/index.php?/cases/view/1474001 )
    PRECONDITIONS: * Desktop Quick Links are NOT displayed on mobile and tablet devices
    """
    keep_browser_open = True

    def test_001_scroll_down_the_page(self):
        """
        DESCRIPTION: Scroll down the page
        EXPECTED: * Desktop Quick Links are displayed at the bottom of main content area
        EXPECTED: * CMS configured text is displayed above Quick Links
        """
        pass

    def test_002_verify_order_of_desktop_quick_links(self):
        """
        DESCRIPTION: Verify order of Desktop Quick Links
        EXPECTED: Desktop Quick Links are ordered as in CMS
        """
        pass

    def test_003_navigate_to_other_pages_within_the_app(self):
        """
        DESCRIPTION: Navigate to other pages within the app
        EXPECTED: * Desktop Quick Links are displayed at the bottom of main content area on ALL pages, except for 'My account' related pages; Registration form; AZ-sports page; Connect pages, Horse Racing Bet Filter(Finder)
        """
        pass

    def test_004_verify_quick_links_for_different_resolutions(self):
        """
        DESCRIPTION: Verify Quick Links for different resolutions
        EXPECTED: * Desktop Quick Links are displayed at the bottom of main content area
        EXPECTED: * Desktop Quick Links are displayed below widgets (In-play/Live Stream/League Table, Results, etc) at 1279 px and smaller resolutions
        """
        pass

    def test_005_hover_over_any_desktop_quick_link(self):
        """
        DESCRIPTION: Hover over any Desktop Quick Link
        EXPECTED: * Hover state is activated
        EXPECTED: * Pointer changes the view from 'Normal select' to 'Link select' for realizing the possibility to click on the particular area
        """
        pass

    def test_006_click_on_any_desktop_quick_link(self):
        """
        DESCRIPTION: Click on any Desktop Quick Link
        EXPECTED: User is redirected to URL set in selected Quick Link
        """
        pass

    def test_007_in_cms_disable_all_quick_links_but_leave_text_above_them_enabled(self):
        """
        DESCRIPTION: In CMS disable all Quick Links but leave text above them enabled
        EXPECTED: 
        """
        pass

    def test_008_back_to_oxygen_app_and_scroll_down_the_page(self):
        """
        DESCRIPTION: Back to Oxygen app and scroll down the page
        EXPECTED: Quick Links AND text above them are NOT displayed at the bottom of the main content area on all pages
        """
        pass
