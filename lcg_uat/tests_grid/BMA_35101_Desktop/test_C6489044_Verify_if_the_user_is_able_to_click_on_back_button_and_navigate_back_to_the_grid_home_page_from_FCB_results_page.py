import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893044_Verify_if_the_user_is_able_to_click_on_back_button_and_navigate_back_to_the_grid_home_page_from_FCB_results_page(Common):
    """
    TR_ID: C64893044
    NAME: Verify if the user is able to click on back button(<)  and navigate back to the grid home page from FCB results page
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2_click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items_and_click_on_bet_online_from_the_fcb_opening_pop_up4_click_on_back_button_on_the_bread_eumnexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_should_be_able_to_select_the_bet_online_and_click_on_go_betting_button_4_user_should_be_able_to_click_the_back_button_and_should_be_navigated_to_the_grid_tab_from_main_header(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2. Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items and click on bet online from the FCB opening pop up.
        DESCRIPTION: 4. Click on back button(<) on the bread eumn
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter and should be able to select the "Bet Online" and click on "Go betting" button .
        DESCRIPTION: 4. User should be able to click the back button and should be navigated to the grid tab from main header.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and should be able to select the "Bet Online" and click on "Go betting" button .
        EXPECTED: 4. User should be able to click the back button and should be navigated to the grid tab from main header.
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
        if self.device_type == 'mobile':
            self.assertTrue(self.site.football_bet_filter.is_back_button_displayed(),
                            msg=f'"Back Button" is not displayed')
            self.site.football_bet_filter.back_button_click()
        else:
            self.assertTrue(self.site.football_bet_filter_results_page.back_button,
                            msg=f'"Back Button" is not displayed')
            self.site.football_bet_filter_results_page.back_button.click()
        self.site.wait_content_state(state_name='thegrid')