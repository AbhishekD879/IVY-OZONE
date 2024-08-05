import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_013_Retail_Connect_Features.Football_Bet_Filter.BaseFootballBetFilter import BaseFootballBetFilter


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893034_Verify_few_selections_are_auto_selected_in_the_bet_filter_results_page_on_clicking_find_bets_on_selecting_bet_inshop_on_the_FCB_pop_up(BaseFootballBetFilter):
    """
    TR_ID: C64893034
    NAME: Verify few selections are auto selected in the bet filter results page on clicking find bets on selecting bet inshop on the FCB pop up
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4click_on_bet_in_shop_from_the_fcb_opening_pop_up5select_all_required_filters6click_on_find_bets_buttonexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_successfully_open_football_bet_filter_page4user_should_be_landed_on_football_bet_filter_page_by_clicking_go_betting_page5user_should_be_able_to_select_all_required_filter6some_of_filter_selections_should_be_auto_selected_(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 4.Click on bet in shop from the FCB opening pop up.
        DESCRIPTION: 5.Select all required filters.
        DESCRIPTION: 6.Click on find bets button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        DESCRIPTION: 4.User should be landed on football bet filter page by clicking go betting page.
        DESCRIPTION: 5.User should be able to select all required filter.
        DESCRIPTION: 6.Some of filter selections should be auto selected .
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        EXPECTED: 4.User should be landed on football bet filter page by clicking go betting page.
        EXPECTED: 5.User should be able to select all required filter.
        EXPECTED: 6.Some of filter selections should be auto selected .
        """
        self.site.login()
        self.site.wait_content_state(state_name="Homepage")
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
        for index in content.items_as_ordered_dict.items():
            index[1].click()
            values = int(
                self.site.football_bet_filter.find_bets_button.name.split(" ")[2].split("(")[1].split(")")[0]) <= 20
            if values:
                self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                                msg='Find Bets button is disabled')
                self.site.football_bet_filter.find_bets_button.click()
                break
            else:
                index[1].click()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_enabled(expected_result=True),
                        msg=f'"Generate bet code" is disabled')
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_enabled(expected_result=True),
                        msg=f'"Generate bet code" is disabled')
        generate_bet_code = self.site.football_bet_filter.generate_bet_frame.is_generate_bet_code_active
        self.assertTrue(generate_bet_code, msg='"Generate Bet Code" button is not active after adding selections')
