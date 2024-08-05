import pytest
import tests
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
class Test_C64893043_Verify_if_the_user_is_able_to_give_the_required_stake_after_selecting_the_required_selections(BaseFootballBetFilter):
    """
    TR_ID: C64893043
    NAME: Verify if the user is able to give the required stake after selecting the required selections.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2_click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items_and_click_on_bet_inshop_from_the_fcb_opening_pop_up4_select_all_required_filters_from_the_three_tabs5_click_on_find_bets_button6_select_the_selections_and_enter_the_required_stakeexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_able_to_select_bet_inshop_and_successfully_click_on_go_betting_button4user_should_be_able_to_select_required_filters_from_three_tabs5user_should_be_able_to_click_on_find_bets_and_able_to_see_all_the_selections_which_are_selected_in_that_filters6user_should_be_able_to_select_from_that_resulted_selections_and_able_to_enter_stake_(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2. Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items and click on bet inshop from the FCB opening pop up.
        DESCRIPTION: 4. Select all required filters from the three tabs.
        DESCRIPTION: 5. Click on "Find bets" button.
        DESCRIPTION: 6. Select the selections and enter the required stake.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter And able to select bet inshop and successfully click on go betting button.
        DESCRIPTION: 4.User should be able to select required filters from three tabs.
        DESCRIPTION: 5.User should be able to click on find bets and able to see all the selections which are selected in that filters.
        DESCRIPTION: 6.User should be able to select from that resulted selections and able to enter stake .
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter And able to select bet inshop and successfully click on go betting button.
        EXPECTED: 4.User should be able to select required filters from three tabs.
        EXPECTED: 5.User should be able to click on find bets and able to see all the selections which are selected in that filters.
        EXPECTED: 6.User should be able to select from that resulted selections and able to enter stake .
        """
        self.site.login(tests.settings.betplacement_user)
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
        _, league = list(content.items_as_ordered_dict.items())[1]
        league.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        self.site.football_bet_filter.find_bets_button.click()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_enabled(expected_result=True),
                        msg=f'"Generate bet code" is disabled')
        generate_bet_code = self.site.football_bet_filter.generate_bet_frame.is_generate_bet_code_active
        self.assertTrue(generate_bet_code, msg='"Generate Bet Code" button is not active after adding selections')
        self.assertTrue(self.site.football_bet_filter.generate_bet_frame.stake_field, msg=f'"Stake value" is not dispalyed entered')
        stake_value = self.site.football_bet_filter.generate_bet_frame.get_stake_value
        expected_stake_value = "10.00"
        self.assertEqual(stake_value, expected_stake_value,
                         msg=f'Actual stake value "{stake_value}" is not same as Expected stake value "{expected_stake_value}"')
