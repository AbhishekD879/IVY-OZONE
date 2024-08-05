import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893077_Verify_if_the_user_is_able_to_navigate_from_the_Grid_home_page_to_football_bet_filter(Common):
    """
    TR_ID: C64893077
    NAME: Verify if the user is able to navigate from the Grid home page to football bet filter.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports2_click_on_grid_tab3click_on_football_bet_filter_from_the_grid_home_pageexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_open_grid_tab3user_should_be_navigated_to_football_bet_filter_page(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports.
        DESCRIPTION: 2. Click on grid tab.
        DESCRIPTION: 3.Click on "Football Bet Filter" from the Grid home page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be navigated to "Football Bet Filter" page.
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be navigated to "Football Bet Filter" page.
        """
        self.site.wait_content_state('HomePage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_menu_options = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_menu_options, msg='"Grid" page items not loaded')
        grid_menu_options.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_dialog, msg='"Your betting" dialog box not appeared')
        your_betting_dialog.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
