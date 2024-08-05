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
class Test_C64893136_Verify_if_the_user_is_able_to_navigate_to_Shop_Bet_Tracker_page_by_clicking_on_Shop_Bet_Tracker_button_under_the_Grid_title_from_A_Z_menu(Common):
    """
    TR_ID: C64893136
    NAME: Verify if the user is able to navigate to "Shop Bet Tracker" page by clicking on "Shop Bet Tracker" button under the Grid title from A-Z menu.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports application.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_application2click_on_a_z_menu3click_on_shop_bet_tracker_from_the_a_z_menu_under_the_gridexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_open_a_z_menu3user_should_be_navigated_to_shop_bet_tracker_page(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports application.
        DESCRIPTION: 2.Click on A-Z menu.
        DESCRIPTION: 3.Click on "Shop Bet Tracker" from the A-Z menu under the Grid.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to open A-Z menu.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker page."
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to open A-Z menu.
        EXPECTED: 3.User should be navigated to "Shop Bet Tracker page."
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
        grid_items.get(vec.retail.BET_TRACKER.title()).click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        actual_title = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_title, vec.retail.BET_TRACKER.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.retail.BET_TRACKER.title()}"')
