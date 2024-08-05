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
class Test_C64893135_Verify_if_the_user_is_able_to_click_on_back_button_on_the_header_of_Shop_bet_tracker_page_and_navigate_back_to_the_Grid_home_page(Common):
    """
    TR_ID: C64893135
    NAME: Verify if the user is able to click on (<) back button on the header of  Shop bet tracker page and navigate back to the Grid home page.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports web
    PRECONDITIONS: application URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application2click_on_grid_tab_from_main_header3click_on_shop_bet_tracker_from_the_grid_hub4click_on__back_buttonexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_navigated_to_shop_bet_tracker_page4user_should_come_back_to_the_grid_home_page(
            self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports web application.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on "Shop Bet Tracker" from the grid hub.
        DESCRIPTION: 4.Click on (<) back button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker" page.
        DESCRIPTION: 4.User should come back to the Grid home page.
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be navigated to "Shop Bet Tracker" page.
        EXPECTED: 4.User should come back to the Grid home page.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.BET_TRACKER.title()).click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        actual_title = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_title, vec.retail.BET_TRACKER.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.retail.BET_TRACKER.title()}"')
        if self.device_type == 'mobile':
            self.site.header.back_button.click()
        else:
            self.site.bet_tracker.back_button.click()
        self.site.wait_content_state(state_name='thegrid')
