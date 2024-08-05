import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893051_Verify_the_generate_bar_code_button_is_in_disable_state_if_the_user_is_not_selecting_any_selections_(Common):
    """
    TR_ID: C64893051
    NAME: Verify  the "generate bar code" button is in disable state if the user  is not selecting any selections .
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2_click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items_and_click_on_bet_in_shop_from_the_fcb_opening_pop_up4_select_any_filters_from_the_three_tabs5_click_on_find_bets_button6_dont_select_any_selection7_check_generate_code_buttonexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_able_to_select_bet_in_shop_and_successfully_click_on_go_betting_button4__user_should_select_any_filters_from_three_tabs5_user_should_be_able_to_click_on_find_bets_button6_dont_select_any_selections7_generate_code_button_should_be_in_disable_state(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2. Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items and click on bet in shop from the FCB opening pop up.
        DESCRIPTION: 4. Select any filters from the three tabs.
        DESCRIPTION: 5. Click on find bets button.
        DESCRIPTION: 6. DonÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢t select any selection.
        DESCRIPTION: 7. Check generate code button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter and able to select bet in shop and successfully click on "Go Betting" button.
        DESCRIPTION: 4.  User should select any filters from three tabs.
        DESCRIPTION: 5. User should be able to click on "Find bets" button.
        DESCRIPTION: 6. Don't select any selections.
        DESCRIPTION: 7. "Generate code" button should be in disable state.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and able to select bet in shop and successfully click on "Go Betting" button.
        EXPECTED: 4.  User should select any filters from three tabs.
        EXPECTED: 5. User should be able to click on "Find bets" button.
        EXPECTED: 6. Don't select any selections.
        EXPECTED: 7. "Generate code" button should be in disable state.
        """
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.grid.menu_items.items_as_ordered_dict.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options)
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options)
        bet_in_shop = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop)
        bet_in_shop.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.assertFalse(
            self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=15),
            msg='Spinner has not disappeared from Find Bets button')
        self.site.contents.scroll_to_bottom()
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.scroll_to_top()
        content = self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('LEAGUES')
        _, league = list(content.items_as_ordered_dict.items())[1]
        league.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        self.site.football_bet_filter.find_bets_button.click()
        tabs_menu = self.site.football_bet_filter.tab_menu.items_as_ordered_dict
        for matches_name in tabs_menu:
            tabs_menu[matches_name].click()
            selections = self.site.football_bet_filter_results_page.items
            self.assertTrue(selections, msg='No selections found')
            for selection in selections:
                if selection.checkbox.value:
                    selection.checkbox.click()
        self.assertFalse(self.site.football_bet_filter_results_page.button.is_enabled(expected_result=False),
                         msg=f'"Generate bet code" is enabled')