import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893079_Verify_if_the_user_is_able_to_click_on_Saved_bet_code_icon_and_clicking_on_that_icon_user_should_be_navigated_to_the_Saved_Bet_Code_page(Common):
    """
    TR_ID: C64893079
    NAME: Verify if the user is able to click on Saved bet code icon and clicking on that icon user should be navigated to the "Saved Bet Code" page.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1_launch_ladbrokes_sports2_click_on_grid_tab3click_on_football_bet_filter_from_the_grid_home_page4click_on_the_icon_that_is_present_on_the_header_of_the_pageexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_open_grid_tab3user_should_be_navigated_to_football_bet_filter_page4user_should_be_navigated_to_saved_bet_code_page(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports.
        DESCRIPTION: 2. Click on grid tab.
        DESCRIPTION: 3.Click on "Football Bet Filter" from the Grid home page.
        DESCRIPTION: 4.Click on the icon that is present on the header of the page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be navigated to "Football Bet Filter" page.
        DESCRIPTION: 4.User should be navigated to "Saved Bet Code" page.
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be navigated to "Football Bet Filter" page.
        EXPECTED: 4.User should be navigated to "Saved Bet Code" page.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.open_sport(name=vec.retail.TITLE)
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.assertTrue(self.site.football_bet_filter.saved_bet_codes_icon.is_displayed(),
                        msg='saved bet codes icon is not displayed')
        self.site.football_bet_filter.saved_bet_codes_icon.click()
        wait_for_result(lambda: self.site.saved_bet_codes.title.is_displayed(), timeout=15)
        self.assertEquals(self.site.saved_bet_codes.title.text, vec.retail.SAVED_BET_CODES,
                          msg=f'user is not navigated to "{self.site.saved_bet_codes.title.text}"')
