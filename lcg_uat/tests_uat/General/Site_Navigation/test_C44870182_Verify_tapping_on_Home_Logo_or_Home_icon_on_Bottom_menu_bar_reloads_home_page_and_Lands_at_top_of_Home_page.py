import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.prod
@pytest.mark.p2
@pytest.mark.uat
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870182_Verify_tapping_on_Home_Logo_or_Home_icon_on_Bottom_menu_bar_reloads_home_page_and_Lands_at_top_of_Home_page(Common):
    """
    TR_ID: C44870182
    NAME: Verify tapping on Home Logo or 'Home' icon on Bottom menu bar reloads home page and Lands at top of Home page
    DESCRIPTION: "Verify user can navigate homepage by clicking 'Home' tab verify user can scroll up from bottom of page on click of Home tab"
    PRECONDITIONS: Coral app should be open and user is on Home page
    """
    keep_browser_open = True

    def test_001_scroll_down_on_home_page_and_tap_on_home_logo_on_the_header_bar(self):
        """
        DESCRIPTION: Scroll down on home page and Tap on Home Logo on the Header bar
        EXPECTED: Home Page should reload and user lands at the top of the home page.
        """
        self.site.wait_content_state('HomePage')
        self.site.contents.scroll_to_bottom()
        self.site.header.brand_logo.click()
        self.site.wait_content_state('HomePage')
        self.assertTrue(self.site.home.menu_carousel.is_displayed(), msg='Not scrolled to top of the homepage')

    def test_002_scroll_down_on_home_page_and_tap_on_the_home_icon_on_bottom_menu_bar(self):
        """
        DESCRIPTION: Scroll down on Home page and tap on the 'Home' icon on bottom menu bar
        EXPECTED: Home Page should reload and user lands at the top of the home page.
        """
        self.site.contents.scroll_to_bottom()
        self.site.navigation_menu.get_footer_menu_item(vec.sb.HOME_FOOTER_ITEM).click()
        self.assertTrue(self.site.home.menu_carousel.is_displayed(), msg='Not scrolled to top of the homepage')

    def test_003_navigate_to_any_other_page_of_the_app_and_tap_on_home_icon_on_bottom_menu_bar(self):
        """
        DESCRIPTION: Navigate to any other page of the app and tap on 'Home' icon on bottom menu bar
        EXPECTED: Home Page should reload and user lands at the top of the home page.
        """
        self.site.home.menu_carousel.click_item(vec.siteserve.FOOTBALL_TAB)
        self.test_002_scroll_down_on_home_page_and_tap_on_the_home_icon_on_bottom_menu_bar()
