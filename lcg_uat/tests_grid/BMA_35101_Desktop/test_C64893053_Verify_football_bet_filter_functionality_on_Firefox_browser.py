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
class Test_C64893053_Verify_football_bet_filter_functionality_on_Firefox_browser(Common):
    """
    TR_ID: C64893053
    NAME: Verify football bet filter functionality on Firefox browser
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def click_and_verify_bet_filter(self):
        self.site.wait_content_state(state_name='thegrid')
        self.site.grid.menu_items.items_as_ordered_dict.get(vec.retail.FB_BET_FILTER_NAME).click()
        self.__class__.your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(self.your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = self.your_betting_popup.items_as_ordered_dict
        return your_betting_options

    def test_001_launch_ladbrokes_sports_web_application_in_firefox_browser2_click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items_and_click_on_bet_online_from_the_fcb_opening_pop_up4_click_on_bet_in_shop_button_from_that_pop_upexpected_result1_launch_ladbrokes_sports_web_application_in_firefox_browser2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_able_to_select_bet_online_and_successfully_click_on_go_betting_button4user_should_be_to_click_on_bet_in_shop_button_from_the_popup(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports web application in Firefox browser.
        DESCRIPTION: 2. Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items and click on bet online from the FCB opening pop up.
        DESCRIPTION: 4. Click on bet in shop button from that pop up.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. Launch Ladbrokes sports web application in Firefox browser.
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter And able to select bet online and successfully click on go betting button.
        DESCRIPTION: 4.User should be to click on "Bet in shop" button from the popup.
        EXPECTED: 1. 1. Launch Ladbrokes sports web application in Firefox browser.
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter And able to select bet online and successfully click on go betting button.
        EXPECTED: 4.User should be to click on "Bet in shop" button from the popup.
        """
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        your_betting_options = self.click_and_verify_bet_filter()
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options)
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options)
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        self.your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        if self.device_type == 'mobile':
            self.site.back_button.click()
        else:
            self.site.football_bet_filter_results_page.back_button.click()
        self.site.wait_content_state(state_name='thegrid')
        your_betting_options = self.click_and_verify_bet_filter()
        bet_in_shop = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop)
        bet_in_shop.radio_button.click()
        self.your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
