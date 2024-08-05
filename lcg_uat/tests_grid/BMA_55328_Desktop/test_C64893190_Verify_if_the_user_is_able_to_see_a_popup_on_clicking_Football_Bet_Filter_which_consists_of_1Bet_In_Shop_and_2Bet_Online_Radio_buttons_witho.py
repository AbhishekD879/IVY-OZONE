import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893190_Verify_if_the_user_is_able_to_see_a_popup_on_clicking_Football_Bet_Filter_which_consists_of_1Bet_In_Shop_and_2Bet_Online_Radio_buttons_without_login(Common):
    """
    TR_ID: C64893190
    NAME: Verify if the user is able to see a popup on clicking "Football Bet Filter" which consists of 1.Bet In Shop and 2.Bet Online Radio buttons without login.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid ladbrokes sports web app.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_app2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hubexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_successfully_and_a_popup_is_shown_with1bet_in_shop_and_2bet_online_radio_buttons(self):
        """
        DESCRIPTION: 1. 1.Launch ladbrokes sports web app.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on "Football Bet Filter" from the grid hub.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        DESCRIPTION: (1).Bet In Shop and (2).Bet Online Radio buttons.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        EXPECTED: (1).Bet In Shop and (2).Bet Online Radio buttons.
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
        your_betting_options = your_betting_popup.items_as_ordered_dict
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options)
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options)
