import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893023_Verify_if_the_user_is_able_to_launch_football_bet_filter_page_on_grid_tab_from_main_header_from_sports_home_page(Common):
    """
    TR_ID: C64893023
    NAME: Verify if the user is able to launch football bet filter page on grid tab from main header from sports home page.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4click_on_any_option_bet_onlinein_shopexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_successfully_open_football_bet_filter_page4_user_should_be_able_to_click_on_go_betting_button_and_should_be_landed_on_football_bet_filter_page_(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2.Click on grid tab from main header
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 4.Click on any option bet online/in shop.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        DESCRIPTION: 4. User should be able to click on go betting button and should be landed on football bet filter page .
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        EXPECTED: 4. User should be able to click on go betting button and should be landed on football bet filter page .
        """
        self.site.login()
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
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
