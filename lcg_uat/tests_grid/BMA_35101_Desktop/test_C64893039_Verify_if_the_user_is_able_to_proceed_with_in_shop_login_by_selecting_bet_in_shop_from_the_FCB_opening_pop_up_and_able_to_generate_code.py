import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_013_Retail_Connect_Features.Football_Bet_Filter.BaseFootballBetFilter import BaseFootballBetFilter


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893039_Verify_if_the_user_is_able_to_proceed_with_in_shop_login_by_selecting_bet_in_shop_from_the_FCB_opening_pop_up_and_able_to_generate_code(BaseFootballBetFilter):
    """
    TR_ID: C64893039
    NAME: Verify if the user is able to proceed with in shop login by selecting bet in shop from the FCB opening pop up and able to generate code
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_login_button_and_enter_valid_in_shop_user_details3click_on_grid_tab_from_main_header4click_on_football_bet_filter_from_the_grid_hub_menu_items5_click_on_bet_in_shop_button_from_that_pop_up6on_the_results_page_select_required_filters_and_click_on_find_bets7select_unselect_few_matches__fill_the_required_stake_and_click_on_generate_code_and_verify_the_code_is_generated_in_saved_bet_codes_pageexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_login_successfully_with_in_shop_user3user_should_be_able_to_open_grid_tab_from_main_header4user_should_be_able_to_click_on_football_bet_filter_5user_should_be_able_to_click_on_in_shop_button_on_that_popup6user_should_be_able_to_click_on_find_bets7user_should_be_able_to_generate_codecan_be_verified_in_saved_bet_codes_page(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2.Click on login button and enter valid in shop user details.
        DESCRIPTION: 3.Click on grid tab from main header.
        DESCRIPTION: 4.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 5. Click on bet in shop button from that pop up.
        DESCRIPTION: 6.On the results page, select required filters and click on find bets
        DESCRIPTION: 7.Select/ unselect few matches , fill the required stake and click on generate code and verify the code is generated in saved bet codes page
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to login successfully with in shop user.
        DESCRIPTION: 3.User should be able to open grid tab from main header.
        DESCRIPTION: 4.User should be able to click on football bet filter. 5.User should be able to click on in-shop button on that popup
        DESCRIPTION: 6.user should be able to click on find bets
        DESCRIPTION: 7.user should be able to generate code(can be verified in saved bet codes page)
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to login successfully with in shop user.
        EXPECTED: 3.User should be able to open grid tab from main header.
        EXPECTED: 4.User should be able to click on football bet filter. 5.User should be able to click on in-shop button on that popup
        EXPECTED: 6.user should be able to click on find bets
        EXPECTED: 7.user should be able to generate code(can be verified in saved bet codes page)
        """
        self.site.wait_content_state('Homepage')
        self.site.grid_connect_login()
        if self.site.upgrade_your_account.is_displayed(timeout=60):
            self.site.upgrade_your_account.no_thanks_button.click()
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
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_enabled(expected_result=True),
                        msg=f'"Generate bet code" is disabled')
