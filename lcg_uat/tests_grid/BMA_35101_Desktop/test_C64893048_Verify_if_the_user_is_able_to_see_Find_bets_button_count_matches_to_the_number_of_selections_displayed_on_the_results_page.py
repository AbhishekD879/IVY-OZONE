import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893048_Verify_if_the_user_is_able_to_see_Find_bets_button_count_matches_to_the_number_of_selections_displayed_on_the_results_page(Common):
    """
    TR_ID: C64893048
    NAME: Verify if the user is able to see "Find bets" button count matches to the number of selections displayed on the results page
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2_click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items_and_click_on_bet_online_from_the_fcb_opening_pop_up4_select_all_required_filters_from_the_three_tabs5_check_the_count_on_find_bets_button6_click_on_find_bets_buttonexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_able_to_select_bet_online_and_successfully_click_on_go_betting_button4user_should_be_able_to_select_required_filters_from_three_tabs5_user_will_be_shown_resulted_selections_count_on_find_bets_button6_user_should_be_able_to_click_on_find_bets_and_able_to_see_all_selections_which_match_that_selected_filters_and_the_count_should_match_successfully(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2. Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items and click on bet online from the FCB opening pop up.
        DESCRIPTION: 4. Select all required filters from the three tabs.
        DESCRIPTION: 5. Check the count on "find bets" button.
        DESCRIPTION: 6. Click on "find bets" button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter And able to select bet online and successfully click on go betting button.
        DESCRIPTION: 4.User should be able to select required filters from three tabs.
        DESCRIPTION: 5. User will be shown resulted selections count on "find bets" button.
        DESCRIPTION: 6. User should be able to click on find bets and able to see all selections which match that selected filters and the count should match successfully
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter And able to select bet online and successfully click on go betting button.
        EXPECTED: 4.User should be able to select required filters from three tabs.
        EXPECTED: 5. User will be shown resulted selections count on "find bets" button.
        EXPECTED: 6. User should be able to click on find bets and able to see all selections which match that selected filters and the count should match successfully
        """
        global ui_number_of_bets
        self.site.login(tests.settings.betplacement_user)
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items[vec.retail.BET_FILTER.title()].click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options,
                      msg=f' Actual "{vec.retail.EXPECTED_YOUR_BETTING.bet_online}" '
                          f' is not present in Expected "{your_betting_options}"')
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
        leagues = list(self.site.football_bet_filter.tab_content.items_as_ordered_dict.values())[1]
        league = list(leagues.items_as_ordered_dict.values())[0]
        league.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        expected_number_of_bets = self.site.football_bet_filter.read_number_of_bets()
        self.site.football_bet_filter.find_bets_button.click()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_displayed(),
                        msg='"Add to Betslip Button" is not displayed')
        tabs = list(self.site.football_bet_filter.tab_menu.menu_item_names)
        self.assertTrue(tabs, msg=f'No Tabs found')
        numbers = []
        if self.device_type == 'desktop':
            tab_name = list(tabs[len(tabs) - 1])
            for word in tab_name:
                if word.isdigit():
                    numbers.append(word)
                    ui_number_of_bets = ''.join(numbers)
        else:
            tab = tabs[len(tabs) - 1]
            self.site.football_bet_filter.tab_menu.open_tab(tab_name=tab)
            ui_number_of_bets = self.site.football_bet_filter_results_page.number_of_results
        self.assertEqual(int(ui_number_of_bets), expected_number_of_bets,
                         msg=f'Incorrect number of bets filtered. Actual is [{int(ui_number_of_bets)}], Expected [{expected_number_of_bets}]')
