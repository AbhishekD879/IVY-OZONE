import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893281_Verify_if_the_user_is_able_to_navigate_to_the_Shop_Bet_Tracker_Page_from_the_Grid_home_page(Common):
    """
    TR_ID: C64893281
    NAME: Verify if the user is able to navigate to the "Shop Bet Tracker Page" from the Grid home page.
    DESCRIPTION: 
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1_launch_ladbrokes_sports_url2_click_on_the_grid_tab_from_a_z_menu__carousel__my_account_menu_items3click_on_shop_bet_tracker_from_the_grid_home_page_itemsexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_grid_home_page3user_should_be_navigated_to_shop_bet_tracker_page(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports URL.
        DESCRIPTION: 2. Click on The Grid tab from A-Z menu / carousel / my account menu items.
        DESCRIPTION: 3.Click on "Shop Bet Tracker" from the Grid home page items.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the Grid home page.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker Page".
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to navigate to the Grid home page.
        EXPECTED: 3.User should be navigated to "Shop Bet Tracker Page".
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.open_sport(name='ALL SPORTS')
            self.site.wait_content_state(state_name='AllSports')
            self.site.all_sports.a_z_sports_section.items_as_ordered_dict[vec.retail.TITLE.title()].click()
        else:
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertIn(vec.retail.TITLE.title(), sports, msg=f'{vec.retail.TITLE.title()} is present in A-Z Sports')
            sports[vec.retail.TITLE.title()].click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        result = wait_for_result(lambda: grid_items.get(vec.retail.BET_TRACKER.title()).is_displayed(), timeout=15)
        self.assertTrue(result, msg=f'"{vec.retail.BET_TRACKER.title()} is not displayed on UI"')
        grid_items.get(vec.retail.BET_TRACKER.title()).click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        actual_title = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_title, vec.retail.BET_TRACKER.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.retail.BET_TRACKER.title()}"')
