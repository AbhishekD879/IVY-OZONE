import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870184_Verify_user_can_open_All_sports_menu_by_clicking_on_All_sports_quick_carousel_on_Home_Page(Common):
    """
    TR_ID: C44870184
    NAME: Verify user can open 'All sports' menu by clicking on 'All sports' quick carousel on Home Page
    PRECONDITIONS: BETA App should be loaded and user is on Home page
    """
    keep_browser_open = True

    def test_001_tap_on_all_sports_icon_on_quick_carousel(self):
        """
        DESCRIPTION: Tap on 'All Sports' icon on Quick Carousel
        EXPECTED: 'All Sports' page opens with 'Top Sports' followed by 'A-Z Betting' Sections. User should be able to tap on any of the menu items and corresponding page should load.
        """
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        all_items.get(vec.SB.ALL_SPORTS).click()
        self.site.wait_content_state(state_name='AllSports')

        top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(top_sports, msg='No sports found in "Top Sports" section')

        az_sports_name = self.site.all_sports.a_z_sports_section.name
        expected_name = vec.SB.AZ_SPORTS.upper()
        self.assertEqual(az_sports_name, expected_name, msg=f'"{expected_name}" section is not displayed')

    def test_002_while_on_all_sports_page_tap_on_back_button(self):
        """
        DESCRIPTION: While on 'All Sports' page tap on 'Back' button
        EXPECTED: User should navigate back to the previous page
        """
        self.site.back_button.click()
        self.site.wait_content_state(state_name='HomePage')
