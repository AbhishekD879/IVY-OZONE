import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893049_Verify_the_Add_to_bet_slip_button_is_in_disable_state_if_the_user_is_not_selecting_any_selections_(Common):
    """
    TR_ID: C64893049
    NAME: Verify  the "Add to bet slip" button is in disable state if the user  is not selecting any selections .
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items_and_click_on_bet_online_from_the_fcb_opening_pop_up4select_any_filters_from_all_the_three_tabs_and_deselect_all_the_selected_selections_from_result_page5_check_add_to_bet_slip_buttonexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_able_to_select_bet_online_and_successfully_click_on_go_betting_button4_dont_select_any_selections_from_result_page5_add_to_bet_slip_button_should_be_in_disable_state_(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items and click on bet online from the FCB opening pop up.
        DESCRIPTION: 4.select any filters from all the three tabs and deselect all the selected selections from result page
        DESCRIPTION: 5. Check "Add to bet slip" button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter And able to select bet online and successfully click on go betting button.
        DESCRIPTION: 4. don't select any selections from result page.
        DESCRIPTION: 5. "Add to bet slip" button should be in disable state .
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter And able to select bet online and successfully click on go betting button.
        EXPECTED: 4. don't select any selections from result page.
        EXPECTED: 5. "Add to bet slip" button should be in disable state .
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
        _, league = list(content.items_as_ordered_dict.items())[0]
        league.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        self.site.football_bet_filter.find_bets_button.click()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_displayed(),
                        msg='"Add to Betslip Button" is not displayed')
        tabs_menu = self.site.football_bet_filter.tab_menu.items_as_ordered_dict
        for matches_name in tabs_menu:
            tabs_menu[matches_name].click()
            selections = self.site.football_bet_filter_results_page.items
            self.assertTrue(selections, msg='No selections found')
            for selection in selections:
                if selection.checkbox.value:
                    selection.checkbox.click()
        self.assertFalse(self.site.football_bet_filter_results_page.button.is_enabled(expected_result=False),
                         msg=f'"Add to Betslip Button" is enabled')
