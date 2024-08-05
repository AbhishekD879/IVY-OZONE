import random
import string
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
class Test_C64893199_Verify_if_the_user_is_able_to_enter_both_Numeric_and_Alphabeticals_to_save_name_and_verify_if_the_user_is_able_to_enter_only_1_25_Characters_in_the_given_space_and_save_the_filter(Common):
    """
    TR_ID: C64893199
    NAME: Verify if the user is able to enter both "Numeric" and "Alphabeticals" to save name and verify if the user is able to enter only 1-25 Characters in the given space and save the filter.
    PRECONDITIONS: 1.User should have valid ladbrokes sports web app.
    PRECONDITIONS: 2.User should have valid Online User Credentials.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_app2click_on_login_button_and_enter_valid_user_details3click_on_grid_tab_from_main_header4click_on_football_bet_filter_from_the_grid_hub5select_bet_in_shop_and_click_on_go_betting_button6select_the_filtering_options_of_coupons_leagues_date7check_whether_the_find_bets_and_save_button_are_active8click_on_save_button9check_whether_the_user_is_able_to_enter_both_numbers_and_alphabets_in_the_given_space_and_check_user_must_be_able_to_enter_between_1_25_characters_only_and_save_the_filterexpected_result1sports_application_should_be_launch_successfully2user_should_be_logged_in_secessfully3user_should_be_able_to_open_grid_tab_from_main_header4user_should_be_able_to_click_on_football_bet_filter_successfully_and_a_popup_is_shown_with1bet_in_shop_and_2bet_online_radio_buttons5user_should_be_navigated_to_football_bet_filter_page6user_must_be_able_to_select_the_filtering_options7user_must_be_able_to_see_both_find_bets_and_save_buttons_in_active_state8user_must_be_able_to_see_a_popup_to_enter_the_name_for_saving_the_filter9user_must_be_able_to_enter_both_numbers_and_alphabets_and_enter_characters_between_1_25_and_save_the_filter(self):
        """
        DESCRIPTION: 1.Launch ladbrokes sports web app.
        DESCRIPTION: 2.Click on login button and enter valid user details.
        DESCRIPTION: 3.Click on grid tab from main header.
        DESCRIPTION: 4.Click on "Football Bet Filter" from the grid hub.
        DESCRIPTION: 5.Select "Bet In Shop" and click on "Go Betting" button.
        DESCRIPTION: 6.Select the filtering options of Coupons, Leagues, Date.
        DESCRIPTION: 7.Check whether the "Find bets" and "Save" button are active.
        DESCRIPTION: 8.Click on "Save" button.
        DESCRIPTION: 9.Check whether the user is able to enter both numbers and alphabets in the given space and
                       check user must be able to enter between 1-25 characters only and save the filter.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be logged in secessfully.
        EXPECTED: 3.User should be able to open grid tab from main header.
        EXPECTED: 4.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        EXPECTED: (1).Bet In Shop and (2).Bet Online Radio buttons.
        EXPECTED: 5.User should be navigated to "Football Bet Filter" page.
        EXPECTED: 6.User must be able to select the Filtering options.
        EXPECTED: 7.User must be able to see both "Find Bets" and "Save" buttons in active state.
        EXPECTED: 8.User must be able to see a popup to enter the name for saving the filter.
        EXPECTED: 9.User must be able to enter both numbers and alphabets and enter characters between 1-25
                    and save the filter.
        """
        self.site.login()
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.open_sport(name=vec.retail.TITLE)
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
        bet_inshop = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop)
        bet_inshop.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.assertFalse(
            self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=15),
            msg='Spinner has not disappeared from Find Bets button')
        self.site.contents.scroll_to_bottom()
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.scroll_to_top()
        content = self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('LEAGUES')
        self.assertTrue(content, msg='"Leagues" not found')
        leagues = list(content.items_as_ordered_dict.items())
        for league_name, league in leagues[:2]:
            league.click()
            self.assertTrue(league.is_selected(),
                            msg=f' Filter "{league_name}" is not selected')
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(expected_result=True),
                        msg='find bets button not enabled')
        self.assertTrue(self.site.football_bet_filter.save_filters_button.is_enabled(expected_result=True),
                        msg='find bets button not enabled')
        self.site.football_bet_filter.save_filters_button.click()
        self.assertTrue(self.site.football_bet_filter.save_filter_popup,
                        msg='"Save filter popup" is not displayed')
        expected_value = 25
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=expected_value + 1))
        self.site.football_bet_filter.save_filter_popup.enter_name(value=name)
        entered_value = self.site.football_bet_filter.save_filter_popup.get_filter_name()
        self.assertEqual(expected_value, len(entered_value),
                         msg=f'Length of Actual Filter entered value "{len(entered_value)}" is not same as'
                             f'Entered value "{name}"')
