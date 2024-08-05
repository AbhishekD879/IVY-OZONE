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
class Test_C64893010_Verify_if_the_user_is_able_to_launch_Football_bet_filter_page_on_grid_tab_from_sports_home_page(Common):
    """
    TR_ID: C64893010
    NAME: Verify if the user is able to launch Football bet filter page on grid tab from sports home page.
    PRECONDITIONS: 1.User should have valid ladbrokes sports URL/App URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_urlapp2click_on_grid_tab_for_desktop_from_the_header3click_on_football_bet_filter__from_the_grid_main_menu4click_on_any_option_bet_onlinein_shopexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_football_bet_filter__and_successfully_open_football_bet_filter__page4_user_should_be_able_to_click_on_go_betting_button_and_landed_on_football_bet_filter_page_successfully(self):
        """
        DESCRIPTION: 1. 1.Launch ladbrokes sports URL/App
        DESCRIPTION: 2.Click on grid tab for desktop from the header
        DESCRIPTION: 3.Click on Football bet filter  from the grid main menu.
        DESCRIPTION: 4.Click on any option bet online/in shop.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on Football bet filter  and successfully open Football bet filter  page.
        DESCRIPTION: 4. User should be able to click on go betting button and landed on Football bet filter page successfully.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on Football bet filter  and successfully open Football bet filter  page.
        EXPECTED: 4. User should be able to click on go betting button and landed on Football bet filter page successfully.
        """
        self.site.wait_content_state("Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_menu = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_menu, msg='"Grid" page items not loaded')
        grid_menu.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options,
                      msg='"Bet in shop" is not displayed')
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options,
                      msg='"Bet online" is not displayed')
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
