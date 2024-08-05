import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893020_Verify_inshop_user_is_also_able_to_see_the_pop_up_after_he_logs_in_when_he_clicks_on_FCB_pop_up_clicking_on_cancel_redirects_the_user_to_grid_homepage(Common):
    """
    TR_ID: C64893020
    NAME: Verify inshop user is also able to see the pop up after he logs in when he clicks on FCB pop up, clicking on cancel redirects the user to grid homepage
    PRECONDITIONS: 1.User should have valid ladbrokes sports URL/App URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_urlapp2login_with_valid_grid_card_credentails2click_on_grid_tab_from_sports_main_header3click_on_football_bet_filter__from_the_grid_main_menu4verify_the_fcb_pop_up_is_displayed_with_below_options1bet_inshop2bet_onlineexpected_resultinshop_user_should_also_be_able_to_see_the_fcb_pop_up_with_the_below_options1bet_inshop2bet_online(self):
        """
        DESCRIPTION: 1. 1.Launch ladbrokes sports URL/App.
        DESCRIPTION: 2.Login with valid grid card credentails
        DESCRIPTION: 2.Click on grid tab from sports main header
        DESCRIPTION: 3.Click on Football bet filter  from the grid main menu.
        DESCRIPTION: 4.Verify the FCB pop up is displayed with below options
        DESCRIPTION: 1.Bet inshop
        DESCRIPTION: 2.Bet online
        DESCRIPTION: Expected Result:
        DESCRIPTION: Inshop user should also be able to see the FCB pop up with the below options
        DESCRIPTION: 1.Bet inshop
        DESCRIPTION: 2.Bet online
        EXPECTED: 1.Inshop user should also be able to see the FCB pop up with the below options
        EXPECTED: 1.Bet inshop
        EXPECTED: 2.Bet online
        """
        self.site.wait_content_state("Homepage")
        self.site.grid_connect_login()
        if self.site.upgrade_your_account.is_displayed(timeout=10):
            self.site.upgrade_your_account.no_thanks_button.click()
            self.site.wait_content_state(state_name='Homepage')
        self.assertTrue(self.site.wait_logged_in(timeout=10), msg='User is not logged in')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_menu = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_menu, msg='"Grid" page items not loaded')
        grid_menu.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING, timeout=20)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        bet_in_shop = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop)
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        self.assertTrue(bet_in_shop.is_displayed(), msg='"Bet in shop" is not displayed')
        self.assertTrue(bet_online.is_displayed(), msg='"Bet online" is not displayed')
        your_betting_popup.cancel_button.click()
        self.site.wait_content_state(state_name='thegrid')
