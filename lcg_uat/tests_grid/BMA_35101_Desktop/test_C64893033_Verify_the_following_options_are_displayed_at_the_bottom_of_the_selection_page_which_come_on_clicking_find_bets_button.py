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
class Test_C64893033_Verify_the_following_options_are_displayed_at_the_bottom_of_the_selection_page_which_come_on_clicking_find_bets_button(BaseFootballBetFilter):
    """
    TR_ID: C64893033
    NAME: Verify the following options are displayed at the bottom of the selection page which come on clicking find bets button.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4click_on_bet_in_shop_from_the_fcb_opening_pop_up5select_all_required_filters6click_on_find_bets_buttonexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_successfully_open_football_bet_filter_page4user_should_be_landed_on_football_bet_filter_page_by_clicking_go_betting_page5user_should_be_able_to_select_all_required_filter6on_clicking_find_bets_button_user_should_be_able_to_see_all_the_mentioned_items_in_that_result_page_successfully1type_of_bet2cumulative_price3stake_auto_filled_as_104total_stake5total_potential_returns__calculated_value_as_auto_filled_10_stake_and_cumulative_price(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports web application and login with valid user credentials
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
        DESCRIPTION: 6.On clicking find bets button user should be able to see all the mentioned items in that result page successfully:(1.Type of Bet.
        DESCRIPTION: 2.Cumulative Price.
        DESCRIPTION: 3.Stake auto filled as 10Ãƒâ€šÃ‚Â£.
        DESCRIPTION: 4.Total Stake.
        DESCRIPTION: 5.Total Potential Returns. ( Calculated Value as auto filled 10Ãƒâ€šÃ‚Â£ stake and cumulative Price))
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        EXPECTED: 4.User should be landed on football bet filter page by clicking go betting page.
        EXPECTED: 5.User should be able to select all required filter.
        EXPECTED: 6.On clicking find bets button user should be able to see all the mentioned items in that result page successfully:(1.Type of Bet.
        EXPECTED: 2.Cumulative Price.
        EXPECTED: 3.Stake auto filled as 10Ãƒâ€šÃ‚Â£.
        EXPECTED: 4.Total Stake.
        EXPECTED: 5.Total Potential Returns. ( Calculated Value as auto filled 10Ãƒâ€šÃ‚Â£ stake and cumulative Price))
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
            values = int(self.site.football_bet_filter.find_bets_button.name.split(" ")[2].split("(")[1].split(")")[0]) <= 20
            if values:
                self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                                msg='Find Bets button is disabled')
                self.site.football_bet_filter.find_bets_button.click()
                break
            else:
                index[1].click()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_enabled(expected_result=True),
                        msg=f'"Generate bet code" is disabled')
        generate_bet_code = self.site.football_bet_filter.generate_bet_frame.is_generate_bet_code_active
        self.assertTrue(generate_bet_code, msg='"Generate Bet Code" button is not active after adding selections')
        self.assertTrue(self.site.football_bet_filter.generate_bet_frame.stake_field,
                        msg=f'"Stake value" is not dispalyed entered')
        stake_value = self.site.football_bet_filter.generate_bet_frame.get_stake_value
        expected_stake_value = "10.00"
        self.assertEqual(stake_value, expected_stake_value,
                         msg=f'Actual stake value "{stake_value}" is not same as Expected stake value "{expected_stake_value}"')
        generate_bet_frame = self.site.football_bet_filter.generate_bet_frame
        self.assertTrue(generate_bet_frame.cumulative_price.is_displayed(), msg=f'Cumulative price : "{generate_bet_frame.cumulative_price.text} is not displayed')
        self.assertTrue(generate_bet_frame.bet_type.is_displayed(), msg=f'Bet type: "{generate_bet_frame.bet_type.text} is not displayed')
        self.assertTrue(generate_bet_frame.total_stake.is_displayed(), msg=f'Total Stake : "{generate_bet_frame.total_stake.text} is not displayed')
        self.assertTrue(generate_bet_frame.potential_returns.is_displayed(),
                        msg='Potential returns value is not displayed()')
