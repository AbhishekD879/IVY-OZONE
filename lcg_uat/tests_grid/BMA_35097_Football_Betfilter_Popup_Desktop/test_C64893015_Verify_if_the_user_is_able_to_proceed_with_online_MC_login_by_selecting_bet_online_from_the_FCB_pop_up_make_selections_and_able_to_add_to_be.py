import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893015_Verify_if_the_user_is_able_to_proceed_with_online_MC_login_by_selecting_bet_online_from_the_FCB_pop_up_make_selections_and_able_to_add_to_betslip(BaseBetSlipTest):
    """
    TR_ID: C64893015
    NAME: Verify if the user is able to proceed with online/MC login by selecting bet online from the FCB pop up ,make selections and able to add to betslip
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid ladbrokes sports URL/App URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_urlapp2click_on_login_button_and_login_with_onlinemc_user3click_on_grid_tab_from_sports_main_header4click_on_football_bet_filter__from_the_grid_main_menu5_click_on_bet_online_button_from_that_pop_up6click_on_go_betting7select_the_required_filters_and_click_on_find_bets8select_the_required_matches_from_the_results_enter_the_stake_and_click_on_add_to_betslip9verify_the_betslips_has_all_the__details_provided_by_usermatches_stakeexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_login_with_onlinemc_customer_successfully3user_should_be_able_to_open_grid_tab4user_should_be_able_to_click_on_football_bet_filter_5user_should_be_able_to__click_on_bet_online_button_from_that_popup678_user_should_be_able_to_make_required_selections_and_click_on_find_bets_make_the_required_selectionsstakematches_and_click_on_add_to_betslip9betslip_should_contain_all_the_matches_added_by_the_user(
            self):
        """
        DESCRIPTION: 1. 1.Launch ladbrokes sports URL/App.
        DESCRIPTION: 2.Click on login button and login with online/MC user.
        DESCRIPTION: 3.Click on grid tab from sports main header
        DESCRIPTION: 4.Click on Football bet filter  from the grid main menu.
        DESCRIPTION: 5. Click on bet online button from that pop up.
        DESCRIPTION: 6.Click on Go betting
        DESCRIPTION: 7.Select the required filters and click on find bets
        DESCRIPTION: 8.select the required matches from the results, enter the stake and click on add to betslip
        DESCRIPTION: 9.Verify the betslips has all the  details provided by user(matches, stake)
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to login with online/MC customer successfully.
        DESCRIPTION: 3.User should be able to open grid tab.
        DESCRIPTION: 4.User should be able to click on Football bet filter .
        DESCRIPTION: 5.User should be able to  click on bet "Online button" from that popup
        DESCRIPTION: 6,7,8,: User should be able to make required selections and click on find bets, make the required selections(stake,matches) and click on add to betslip
        DESCRIPTION: 9.Betslip should contain all the matches added by the user
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to login with online/MC customer successfully.
        EXPECTED: 3.User should be able to open grid tab.
        EXPECTED: 4.User should be able to click on Football bet filter .
        EXPECTED: 5.User should be able to  click on bet "Online button" from that popup
        EXPECTED: 6,7,8,: User should be able to make required selections and click on find bets, make the required selections(stake,matches) and click on add to betslip
        EXPECTED: 9.Betslip should contain all the matches added by the user
        """
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

        results_selections = []
        results_name = []
        tabs_menu = self.site.football_bet_filter.tab_menu.items_as_ordered_dict
        for matches_name in tabs_menu:
            tabs_menu[matches_name].click()
            selections = self.site.football_bet_filter_results_page.items_as_ordered_dict
            for selection in selections.values():
                if selection.checkbox.value:
                    if not(selection.name in results_name):
                        results_name.append(selection.name)
                        results_selections.append(selection.odds.text.split('@')[1].strip())
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_displayed(),
                        msg='"Add to Betslip Button" is not displayed')
        self.site.football_bet_filter_results_page.button.click()
        self.assertTrue(self.site.has_betslip_opened(timeout=10), msg='Betslip is not opened')
        singles_section = self.get_betslip_sections().Singles
        self.assertEqual(len(singles_section), len(results_selections),
                         msg=f'Singles selection count "{len(results_selections)}" is not the same as expected {len(singles_section)}')
        for stake_name, stake in singles_section.items():
            self.assertIn(str(stake.odds).strip(), results_selections,
                          msg=f'{str(stake.odds)} odd is not in betslip {results_selections}')
