import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893040_Verify_if_the_user_is_able_to_proceed_with_online_MC_login_by_selecting_bet_online_from_the_FCB_opening_pop_up_and_able_to_add_to_bet_lip_and_bet_is_placed(BaseBetSlipTest):
    """
    TR_ID: C64893040
    NAME: Verify if the user is able to proceed with online/MC login by selecting bet online from the FCB opening pop up and able to add to bet lip and bet is placed
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_onlinemc_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4_click_on_bet_online_button_from_that_pop_up5select_few_filters_and_click_on_find_bets_button6click_on_add_to_bet_slip_button7open_bet_slip_and_click_on_place_bet_buttonexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_4user_should_be_able_to__click_on_bet_online_button_from_the_fcb_popup5user_should_be_able_to_select_few_filters_and_able_to_click_on_find_bets_button6user_should_be_able_to_click_on_add_to_bet_slip_button7user_should_see_those_selected_selections_in_bet_slip_and_place_bet_successfully_and_get_a_bet_receipt(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid online/MC user credentials
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 4. Click on bet online button from that pop up.
        DESCRIPTION: 5.Select few filters and click on find bets button.
        DESCRIPTION: 6.Click on add to bet slip button.
        DESCRIPTION: 7.Open bet slip and click on place bet button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter. 4.User should be able to  click on bet "Online button" from the FCB popup.
        DESCRIPTION: 5.User should be able to select few filters and able to click on find bets button.
        DESCRIPTION: 6.User should be able to click on add to bet slip button.
        DESCRIPTION: 7.User should see those selected selections in bet slip and place bet successfully and get a bet receipt.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter. 4.User should be able to  click on bet "Online button" from the FCB popup.
        EXPECTED: 5.User should be able to select few filters and able to click on find bets button.
        EXPECTED: 6.User should be able to click on add to bet slip button.
        EXPECTED: 7.User should see those selected selections in bet slip and place bet successfully and get a bet receipt.
        """
        self.site.login(tests.settings.mc_user)
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
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options,
                      msg=f' Actual "{vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop}" '
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
        self.site.football_bet_filter.find_bets_button.click()
        selections = self.site.football_bet_filter_results_page.items_as_ordered_dict
        self.assertTrue(selections, msg='No selections found')
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_displayed(),
                        msg='"Add to Betslip Button" is not displayed')
        self.site.football_bet_filter_results_page.button.click()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
