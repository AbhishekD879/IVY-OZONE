import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_prod
@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893215_Verify_if_the_user_is_able_to_see_Save_filter_in_inactive_state_and_Find_bets_in_active_state_when_user_navigates_to_the_football_bet_filter_page_from_the_grid_home_page(Common):
    """
    TR_ID: C64893215
    NAME: Verify if the user is able to see "Save filter" in inactive state and "Find bets" in active state when user navigates to the football bet filter page from the grid home page.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid ladbrokes sports web app.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_app2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub4select_bet_online_and_click_on_go_betting_buttonexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_successfully_and_a_popup_is_shown_with1bet_in_shop_and_2bet_online_radio_buttons4user_should_be_navigated_to_football_bet_filter_page_and_should_see_save_filter_button_in_inactive_state_and_find_bets_in_active_state(self):
        """
        DESCRIPTION: 1. 1.Launch ladbrokes sports web app.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on "Football Bet Filter" from the grid hub.
        DESCRIPTION: 4.Select "Bet Online" and click on "Go Betting" button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        DESCRIPTION: (1).Bet In Shop and (2).Bet Online Radio buttons.
        DESCRIPTION: 4.User should be navigated to "Football Bet Filter" page and should see "Save filter" button in inactive state and "Find bets" in active state.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        EXPECTED: (1).Bet In Shop and (2).Bet Online Radio buttons.
        EXPECTED: 4.User should be navigated to "Football Bet Filter" page and should see "Save filter" button in inactive state and "Find bets" in active state.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options,
                      msg=f'{vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop} not in {your_betting_options}')
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options,
                      msg=f'{vec.retail.EXPECTED_YOUR_BETTING.bet_online} not in {your_betting_options}')
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.assertFalse(
            self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=15),
            msg='Spinner has not disappeared from Find Bets button')
        self.site.contents.scroll_to_bottom()
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.scroll_to_top()
        self.assertFalse(self.site.football_bet_filter.save_filters_button.is_enabled(expected_result=False),
                         msg='Save filter button enabled')
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(expected_result=True),
                        msg='find bets button not enabled')
