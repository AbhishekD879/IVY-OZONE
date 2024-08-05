import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893596_Verify_if_the_Online_user_is_able_to_navigate_to_the_bet_tracker_page_from_the_grid_hub_menu_items(Common):
    """
    TR_ID: C64893596
    NAME: Verify if the Online user is able to navigate to the bet tracker page from the grid hub menu items.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_url2click_on_the_grid_tab_from_the_top_header3click_on_the_shop_bet_tracker_on_the_grid_hub_menu_itemexpected_result1user_must_be_able_to_access_the_ladbrokes_sports2user_must_be_able_to_click_on_the_grid_tab_and_enter_the_grid_hub_menu_items_page3user_must_be_able_to_click_on_the_shop_bet_tracker_and_navigate_to_the_shop_bet_tracker_page(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports url.
        DESCRIPTION: 2.Click on the grid tab from the top header.
        DESCRIPTION: 3.Click on the shop bet tracker on the grid hub menu item.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.User must be able to access the ladbrokes sports.
        DESCRIPTION: 2.User must be able to click on the grid tab and enter the grid hub menu items page.
        DESCRIPTION: 3.User must be able to click on the shop bet tracker and navigate to the shop bet tracker page.
        EXPECTED: 1. 1.User must be able to access the ladbrokes sports.
        EXPECTED: 2.User must be able to click on the grid tab and enter the grid hub menu items page.
        EXPECTED: 3.User must be able to click on the shop bet tracker and navigate to the shop bet tracker page.
        """
        self.site.wait_content_state(state_name="Homepage")
        self.site.login()
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items are not loaded')
        grid_items[vec.retail.BET_TRACKER].click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
