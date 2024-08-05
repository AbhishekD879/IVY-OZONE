import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893016_Verify_if_the_user_is_able_to_see_all_the_selections_by_clicking_find_bets_button_after_selecting_all_the_required_filters(Common):
    """
    TR_ID: C64893016
    NAME: Verify if the user is able to see all the selections by clicking find bets button after selecting all the required filters.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid ladbrokes sports URL/App URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_urlapp2_click_on_grid_tab_from_sports_main_header3click_on_football_bet_filter__from_the_grid_main_menu_and_click_on_bet_online_from_that_popup4_select_all_the_required_filters_from_the_three_tabs5_click_on_find_bets_buttonexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_football_bet_filter__and_able_to_select_bet_online_and_successfully_click_on_go_betting_button4user_should_be_able_to_select_required_filters_from_the_three_tabs5user_should_be_able_to_click_on_find_bets_button_and_able_to_see_all_selections_which_match_that_selected_filters(self):
        """
        DESCRIPTION: 1. 1. Launch ladbrokes sports URL/App.
        DESCRIPTION: 2. Click on grid tab from sports main header
        DESCRIPTION: 3.Click on Football bet filter  from the grid main menu and click on bet online from that popup.
        DESCRIPTION: 4. Select all the required filters from the three tabs.
        DESCRIPTION: 5. Click on "find bets" button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on Football bet filter  And able to select bet online and successfully click on go betting button.
        DESCRIPTION: 4.User should be able to select required filters from the three tabs.
        DESCRIPTION: 5.User should be able to click on "Find bets" button and able to see all selections which match that selected filters.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on Football bet filter  And able to select bet online and successfully click on go betting button.
        EXPECTED: 4.User should be able to select required filters from the three tabs.
        EXPECTED: 5.User should be able to click on "Find bets" button and able to see all selections which match that selected filters.
        """
        self.site.wait_content_state(state_name="Homepage")
        self.site.login()
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
        content = self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('LEAGUES')
        league = list(content.items_as_ordered_dict.values())[0]
        league.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        self.site.football_bet_filter.find_bets_button.click()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_displayed(),
                        msg='"Add to Betslip Button" is not displayed')
        selections = self.site.football_bet_filter_results_page.items_as_ordered_dict
        self.assertTrue(selections, msg='No selections found')