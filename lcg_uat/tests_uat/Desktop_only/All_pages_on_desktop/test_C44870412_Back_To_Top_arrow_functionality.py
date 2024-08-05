import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.medium
@vtest
class Test_C44870412_Back_To_Top_arrow_functionality(Common):
    """
    TR_ID: C44870412
    NAME: Back To Top arrow functionality
    DESCRIPTION: When user start scrolling down the page and click on Back to Top arrow, is navigated to top of the page
    PRECONDITIONS: User loads the coral desktop web page and log in
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify the Login
        EXPECTED: User should be able to login
        """
        self.site.login()

    def test_001_verify_that_back_to_top_arrow_is_available_in_all_the_pagesverify_that_when_user_start_scrolling_down_the_page_and_click_on_back_to_top_arrow_is_navigated_to_top_of_the_page(self):
        """
        DESCRIPTION: Verify that Back To Top arrow is available in all the pages
        DESCRIPTION: Verify that when user start scrolling down the page and click on Back to Top arrow, is navigated to top of the page
        EXPECTED: Back To Top arrow is available and functionality works fine
        """
        self.site.contents.scroll_to_bottom()
        self.assertTrue(self.site.back_to_top_button.icon.is_displayed(), msg='Back to Top arrow is not available')
        self.site.back_to_top_button.click()
        self.assertTrue(self.site.header.sport_menu.is_displayed(), msg='Sports Header menu is not displayed')
