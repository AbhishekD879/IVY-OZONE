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
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893046_Verify_football_bet_filter_functionality_with_login_for_In_Shop_Online_MC_users(Common):
    """
    TR_ID: C64893046
    NAME: Verify football bet filter functionality with login for In-Shop/Online/MC users.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def verify_football_bet_filter(self):

        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
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
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2_click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items_and_click_on_bet_online_from_the_fcb_opening_pop_up4_click_on_login_button_and_check_the_functionality_for_onlinein_shopmc_customersexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_able_to_select_bet_online_and_click_on_go_betting_button_4_user_should_be_able_to_see_login_overlay_and_able_to_check_the_functionality_with_all_the_type_of_users_(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2. Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items and click on bet online from the FCB opening pop up.
        DESCRIPTION: 4. Click on login button and check the functionality for Online/In-Shop/MC customers.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter and able to select "Bet Online" and click on "Go Betting" button .
        DESCRIPTION: 4. User should be able to see login overlay and able to check the functionality with all the type of users .
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and able to select "Bet Online" and click on "Go Betting" button .
        EXPECTED: 4. User should be able to see login overlay and able to check the functionality with all the type of users .
        """
        self.site.login()
        self.verify_football_bet_filter()
        self.site.logout()
        self.site.login(username=tests.settings.mc_user)
        self.verify_football_bet_filter()
        self.navigate_to_page('homepage')
        self.site.wait_content_state("homepage")
        self.site.logout()
        self.site.grid_connect_login()
        self.verify_football_bet_filter()
