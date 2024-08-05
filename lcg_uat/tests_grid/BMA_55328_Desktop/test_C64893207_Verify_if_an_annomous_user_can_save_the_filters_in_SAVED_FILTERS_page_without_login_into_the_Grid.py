import random
import string
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
class Test_C64893207_Verify_if_an_annomous_user_can_save_the_filters_in_SAVED_FILTERS_page_without_login_into_the_Grid(Common):
    """
    TR_ID: C64893207
    NAME: Verify if an annomous user can save the filters in "SAVED FILTERS" page without login into the Grid.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid ladbrokes sports web app.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_app2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub4select_bet_online_and_click_on_go_betting_button5select_the_filtering_options_of_coupons_leagues_date6check_whether_the_find_bets_and_save_button_are_active7click_on_save_button8click_on_saved_filters_button_from_headerexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_successfully_and_a_popup_is_shown_with1bet_in_shop_and_2bet_online_radio_buttons4user_should_be_navigated_to_football_bet_filter_page5user_must_be_able_to_select_the_filtering_options6user_must_be_able_to_see_both_find_bets_and_save_buttons_in_active_state7user_must_be_able_to_see_a_popup_to_enter_the_name_for_saving_the_filter_and_save_it_by_giving_the_name8user_should_be_navigated_to_the_saved_filters_page_and_user_can_see_all_his_saved_filters(self):
        """
        DESCRIPTION: 1. 1.Launch ladbrokes sports web app.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on "Football Bet Filter" from the grid hub.
        DESCRIPTION: 4.Select "Bet Online" and click on "Go Betting" button.
        DESCRIPTION: 5.Select the filtering options of Coupons, Leagues, Date.
        DESCRIPTION: 6.Check whether the "Find bets" and "Save" button are active.
        DESCRIPTION: 7.Click on "Save" button.
        DESCRIPTION: 8.Click on "SAVED FILTERS" button from header.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        DESCRIPTION: (1).Bet In Shop and (2).Bet Online Radio buttons.
        DESCRIPTION: 4.User should be navigated to "Football Bet Filter" page.
        DESCRIPTION: 5.User must be able to select the Filtering options.
        DESCRIPTION: 6.User must be able to see both "Find Bets" and "Save" buttons in active state.
        DESCRIPTION: 7.User must be able to see a popup to enter the name for saving the filter and save it by giving the name.
        DESCRIPTION: 8.User should be navigated to the "SAVED FILTERS" page and user can see all his saved filters.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        EXPECTED: (1).Bet In Shop and (2).Bet Online Radio buttons.
        EXPECTED: 4.User should be navigated to "Football Bet Filter" page.
        EXPECTED: 5.User must be able to select the Filtering options.
        EXPECTED: 6.User must be able to see both "Find Bets" and "Save" buttons in active state.
        EXPECTED: 7.User must be able to see a popup to enter the name for saving the filter and save it by giving the name.
        EXPECTED: 8.User should be navigated to the "SAVED FILTERS" page and user can see all his saved filters.
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
        self.assertFalse(
            self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=25),
            msg='Spinner has not disappeared from Find Bets button')
        self.site.contents.scroll_to_bottom()
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.scroll_to_top()
        content = self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('LEAGUES')
        self.assertTrue(content, msg='"Leagues" not found')
        leagues = list(content.items_as_ordered_dict.items())
        for league_name, league in leagues[:2]:
            league.click()
            self.assertTrue(league.is_selected(),
                            msg=f' Filter "{league_name}" is not selected')
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(expected_result=True),
                        msg='find bets button not enabled')
        self.assertTrue(self.site.football_bet_filter.save_filters_button.is_enabled(expected_result=True),
                        msg='find bets button not enabled')
        self.site.football_bet_filter.save_filters_button.click()
        self.assertTrue(self.site.football_bet_filter.save_filter_popup,
                        msg='"Save filter popup" is not displayed')
        expected_value = 25
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=expected_value))
        self.site.football_bet_filter.save_filter_popup.enter_name(value=name)
        self.site.football_bet_filter.save_filter_popup.save_button.click()
        self.site.football_bet_filter.tab_menu.items_as_ordered_dict.get('SAVED FILTERS').click()
        saved_filters = self.site.football_bet_filter.saved_filters_tab.items_as_ordered_dict
        self.assertTrue(saved_filters, msg=' Saved filters not available')
