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
class Test_C64893212_Verify_if_the_inshop_user_is_able_to_see_find_bets_button_getting_active_after_saving_a_filter_and_applying_it(Common):
    """
    TR_ID: C64893212
    NAME: Verify if the inshop user is able to see find bets button getting active after saving a filter and applying it
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid ladbrokes sports web app.
    PRECONDITIONS: 2.User should have valid In-shop User Credentials.
    """
    keep_browser_open = True

    def select_and_save_filters(self, league1, league2):
        content = self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('LEAGUES')
        leagues = list(content.items_as_ordered_dict.items())
        for league_name, league in leagues[league1:league2]:
            league.click()
            self.assertTrue(league.is_selected(),
                            msg=f' Filter "{league_name}" is not selected')
        self.site.football_bet_filter.save_filters_button.click()
        self.assertTrue(self.site.football_bet_filter.save_filter_popup,
                        msg='"Save filter popup" is not displayed')
        expected_value = 25
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=expected_value))
        self.site.football_bet_filter.save_filter_popup.enter_name(value=name)
        self.site.football_bet_filter.save_filter_popup.save_button.click()

    def test_001_launch_ladbrokes_sports_web_app2click_on_login_button_and_enter_valid_user_details3click_on_grid_tab_from_main_header4click_on_football_bet_filter_from_the_grid_hub5select_bet_in_shop_and_click_on_go_betting_button6select_the_filtering_options_of_coupons_leagues_date7check_whether_the_find_bets_and_save_button_are_active8click_on_save_button9click_on_saved_filters_button_from_header10select_the_prefered_filter_from_the_saved_filters_page11click_on_apply_filter_button12check_the_selections_in_filtering_page_and_count_in_find_bets_buttonexpected_result1sports_application_should_be_launch_successfully2user_should_be_logged_in_secessfully3user_should_be_able_to_open_grid_tab_from_main_header4user_should_be_able_to_click_on_football_bet_filter_successfully_and_a_popup_is_shown_with1bet_in_shop_and_2bet_online_radio_buttons5user_should_be_navigated_to_football_bet_filter_page6user_must_be_able_to_select_the_filtering_options7user_must_be_able_to_see_both_find_bets_and_save_buttons_in_active_state8user_must_be_able_to_see_a_popup_to_enter_the_name_for_saving_the_filter_and_save_it_by_giving_the_name9user_should_be_navigated_to_the_saved_filters_page10user_must_be_able_to_select_the_prefered_filter_sucessfully11bet_filter_is_applied_sucessfully_and_removed_from_the_saved_filters12user_must_be_able_to_see_change_in_selections_and_change_in_the_count_in_find_bets_button(self):
        """
        DESCRIPTION: 1. 1.Launch ladbrokes sports web app.
        DESCRIPTION: 2.Click on login button and enter valid user details.
        DESCRIPTION: 3.Click on grid tab from main header.
        DESCRIPTION: 4.Click on "Football Bet Filter" from the grid hub.
        DESCRIPTION: 5.Select "Bet In Shop" and click on "Go Betting" button.
        DESCRIPTION: 6.Select the filtering options of Coupons, Leagues, Date.
        DESCRIPTION: 7.Check whether the "Find bets" and "Save" button are active.
        DESCRIPTION: 8.Click on "Save" button.
        DESCRIPTION: 9.Click on "SAVED FILTERS" button from header.
        DESCRIPTION: 10.Select the prefered filter from the "SAVED FILTERS" page.
        DESCRIPTION: 11.Click on "Apply Filter" button.
        DESCRIPTION: 12.Check the selections in filtering page and count in "FIND BETS" button
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be logged in secessfully.
        DESCRIPTION: 3.User should be able to open grid tab from main header.
        DESCRIPTION: 4.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        DESCRIPTION: (1).Bet In Shop and (2).Bet Online Radio buttons.
        DESCRIPTION: 5.User should be navigated to "Football Bet Filter" page.
        DESCRIPTION: 6.User must be able to select the Filtering options.
        DESCRIPTION: 7.User must be able to see both "Find Bets" and "Save" buttons in active state.
        DESCRIPTION: 8.User must be able to see a popup to enter the name for saving the filter and save it by giving the name.
        DESCRIPTION: 9.User should be navigated to the "SAVED FILTERS" page.
        DESCRIPTION: 10.User must be able to select the prefered filter sucessfully.
        DESCRIPTION: 11.Bet filter is applied sucessfully and removed from the "SAVED FILTERS"
        DESCRIPTION: 12.User must be able to see change in selections and change in the count in "FIND BETS" button.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be logged in secessfully.
        EXPECTED: 3.User should be able to open grid tab from main header.
        EXPECTED: 4.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        EXPECTED: (1).Bet In Shop and (2).Bet Online Radio buttons.
        EXPECTED: 5.User should be navigated to "Football Bet Filter" page.
        EXPECTED: 6.User must be able to select the Filtering options.
        EXPECTED: 7.User must be able to see both "Find Bets" and "Save" buttons in active state.
        EXPECTED: 8.User must be able to see a popup to enter the name for saving the filter and save it by giving the name.
        EXPECTED: 9.User should be navigated to the "SAVED FILTERS" page.
        EXPECTED: 10.User must be able to select the prefered filter sucessfully.
        EXPECTED: 11.Bet filter is applied sucessfully and removed from the "SAVED FILTERS"
        EXPECTED: 12.User must be able to see change in selections and change in the count in "FIND BETS" button.
        """
        self.site.grid_connect_login()
        if self.site.upgrade_your_account.is_displayed(timeout=60):
            self.site.upgrade_your_account.no_thanks_button.click()
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
        bet_in_shop = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop)
        bet_in_shop.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.assertFalse(
            self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=15),
            msg='Spinner has not disappeared from Find Bets button')
        self.site.contents.scroll_to_bottom()
        self.site.wait_content_state_changed(timeout=30)
        self.site.contents.scroll_to_top()
        self.select_and_save_filters(league1=0, league2=2)
        self.select_and_save_filters(league1=3, league2=5)
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(expected_result=True),
                        msg='find bets button not enabled')
        self.assertTrue(self.site.football_bet_filter.save_filters_button.is_enabled(expected_result=True),
                        msg='Save filter button not enabled')

        previous_find_bets_count = self.site.football_bet_filter.read_number_of_bets()
        self.site.football_bet_filter.tab_menu.items_as_ordered_dict.get('SAVED FILTERS').click()
        saved_filters = self.site.football_bet_filter.saved_filters_tab.items_as_ordered_dict
        self.assertTrue(saved_filters, msg=' Saved filters not available')
        preffered_filter = list(saved_filters.values())[1]
        preffered_filter.click()
        self.site.football_bet_filter.tab_menu.items_as_ordered_dict.get(vec.retail.SAVED_FILTERS_TAB).click()
        self.site.football_bet_filter.saved_filters_tab.apply_button.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        current_find_bets_count = self.site.football_bet_filter.read_number_of_bets()
        self.assertNotEqual(previous_find_bets_count, current_find_bets_count,
                            msg='"FIND BETS" count is not changed')
