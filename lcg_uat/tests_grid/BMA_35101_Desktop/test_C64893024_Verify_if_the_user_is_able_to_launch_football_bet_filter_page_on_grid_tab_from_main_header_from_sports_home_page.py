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
class Test_C64893024_Verify_if_the_user_is_shown_with_a_popup_which_consists_of_the_below_options_I_bet_in_shop_ii_Bet_online_and_with_two_buttons_I_cancel_iigo_betting_on_launching_football_bet_filter(Common):
    """
    TR_ID: C64893024
    NAME: Verify if the user is shown with a popup which consists of the below options. I. "bet in shop", ii. "Bet online"  and with two buttons  I. "cancel", ii."go betting"  on launching football bet filter.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_theexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_successfully_and_able_to_see_popup_with_all_the_options_mentioned_below_1bet_in_shop__2bet_online_radio_buttons_and_with_two_buttons_cancel_and_go_betting(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2.Click on grid tab from main header
        DESCRIPTION: 3.Click on football bet filter from the
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter successfully and able to see popup with all the options mentioned below: 1."Bet in shop" , 2."Bet Online" radio buttons and with two buttons: "Cancel" and "GO betting".
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter successfully and able to see popup with all the options mentioned below: 1."Bet in shop" , 2."Bet Online" radio buttons and with two buttons: "Cancel" and "GO betting".
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
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options, msg='"Bet in shop" is not displayed')
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options, msg='"Bet online" is not displayed')
        self.assertTrue(your_betting_popup.cancel_button, msg="Cancel button is not displayed")
        self.assertTrue(your_betting_popup.go_betting_button, msg="Cancel button is not displayed")
