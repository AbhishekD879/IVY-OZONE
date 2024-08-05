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
class Test_C64893042_Verify_if_the_filtered_selections_are_added_to_bet_slip_after_clicking_on_add_to_betslip_for_online_customer(Common):
    """
    TR_ID: C64893042
    NAME: Verify if the filtered selections are added to bet slip after clicking on add to betslip  for online customer.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2_login_with_online_customer3click_on_grid_tab_from_main_header4click_on_football_bet_filter_from_the_grid_hub_menu_items5_click_on_bet_online_button_from_that_pop_up6_select_required_filters_and_click_on_find_bets_button7_select_required_selections_and_click_on_add_to_bet_slip_button8_open_bet_slip_which_is_there_on_top_rightexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_login_online_customer_3user_should_be_able_to_open_grid_tab_from_main_header4user_should_be_able_to_click_on_football_bet_filter_5user_should_be_click_on_bet_online_button_successfully_from_the_fcb_opening_pop_up6_user_should_be_able_to_select_required_filters_and_able_to_click_on_find_bets_button7_user_should_be_able_to_select_required_selections_and_able_to_click_on_add_to_bet_slip_button_8_user_should_be_able_to_open_the_bet_slips_page_and_should_be_able_to_see_all_the_selections_which_are_selected_in_step_6(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2. Login with online customer.
        DESCRIPTION: 3.Click on grid tab from main header.
        DESCRIPTION: 4.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 5. Click on "Bet Online" button from that pop up.
        DESCRIPTION: 6. Select required filters and click on "Find Bets" button.
        DESCRIPTION: 7. Select required selections and Click on "Add to Bet slip" button.
        DESCRIPTION: 8. Open bet slip which is there on top right
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to login online customer .
        DESCRIPTION: 3.User should be able to open grid tab from main header.
        DESCRIPTION: 4.User should be able to click on football bet filter. 5.User should be click on "Bet Online" button successfully from the FCB opening pop up.
        DESCRIPTION: 6. User should be able to select required filters and able to click on "Find Bets" button.
        DESCRIPTION: 7. User should be able to select required selections and able to click on "Add to bet slip" button .
        DESCRIPTION: 8. User should be able to open the bet slips page and should be able to see all the selections which are selected in step 6.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to login online customer .
        EXPECTED: 3.User should be able to open grid tab from main header.
        EXPECTED: 4.User should be able to click on football bet filter. 5.User should be click on "Bet Online" button successfully from the FCB opening pop up.
        EXPECTED: 6. User should be able to select required filters and able to click on "Find Bets" button.
        EXPECTED: 7. User should be able to select required selections and able to click on "Add to bet slip" button .
        EXPECTED: 8. User should be able to open the bet slips page and should be able to see all the selections which are selected in step 6.
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
        leagues = list(self.site.football_bet_filter.tab_content.items_as_ordered_dict.values())[1]
        league = list(leagues.items_as_ordered_dict.values())[0]
        league.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        self.site.football_bet_filter.find_bets_button.click()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_displayed(),
                        msg='"Add to Betslip Button" is not displayed')
        selections = self.site.football_bet_filter_results_page.items_as_ordered_dict
        self.assertTrue(selections, msg='No selections found')