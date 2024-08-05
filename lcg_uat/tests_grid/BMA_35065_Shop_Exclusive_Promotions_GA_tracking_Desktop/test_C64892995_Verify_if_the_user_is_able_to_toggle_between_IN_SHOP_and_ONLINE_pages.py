import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64892995_Verify_if_the_user_is_able_to_toggle_between_IN_SHOP_and_ONLINE_pages(Common):
    """
    TR_ID: C64892995
    NAME: Verify if the user is able to toggle between "IN-SHOP" and "ONLINE" pages.
    DESCRIPTION: 
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_url2click_on_grid_tab3click_on_shop_exclusive_promos_from_the_listexpected_result1sports_url_should_be_launched_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_shop_exclusive_promos_and_promotions_page_is_opened_successfully4user_should_be_able_to_toggle_between_in_shop_and_online_pages(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on "Shop Exclusive Promos" from the list.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports URL should be launched successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        DESCRIPTION: 4.User should be able to toggle between "IN-SHOP" and "ONLINE" pages.
        EXPECTED: 1. 1.Sports URL should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        EXPECTED: 4.User should be able to toggle between "IN-SHOP" and "ONLINE" pages.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()).click()
        self.site.wait_content_state('promotions')
        actual_title = self.site.promotions.content_title_text
        self.assertEqual(actual_title, vec.retail.PROMOTIONS.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.sb.PROMOTIONS}"')
        promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(promotions.upper(), vec.promotions.TABS_RETAIL.upper(),
                         msg=f'Current tab "{promotions}" is not equal to expected "{vec.promotions.TABS_RETAIL}"')
        self.site.promotions.tabs_menu.open_tab(tab_name=vec.promotions.TABS_ALL.upper())
        promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(promotions.upper(), vec.promotions.TABS_ALL.upper(),
                         msg=f'Current tab "{promotions}" is not equal to expected "{vec.promotions.TABS_ALL}"')