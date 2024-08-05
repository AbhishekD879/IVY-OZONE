import pytest
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
class Test_C64893028_Verify_the_following_tabs_are_displayed_in_football_bet_filter_page_by_clicking_go_betting_buttonby_default_inshop_option_is_selected_on_the_pop_up1_Create_Coupons2_Your_Team3_The_Opposition4_Saved_Filter(Common):
    """
    TR_ID: C64893028
    NAME: Verify the following tabs are displayed in football bet filter page by clicking go betting button(by default inshop option is selected on the pop up)
    1. Create Coupons
    2. Your Team
    3. The Opposition
    4. Saved Filter
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4click_on_bet_inshop_from_the_fcb_opening_pop_up_and__click_on_go_bettingexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_successfully_open_football_bet_filter_page4_user_should_be_able_to_select_bet_inshop_and_click_on_go_betting_button_navigate_to_football_bet_filter_page_and_should_see_all_the_below_tabs1_create_coupons2_your_team3_the_opposition4_saved_filter(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 4.Click on bet inshop from the FCB opening pop up and  click on 'Go betting'
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        DESCRIPTION: 4. User should be able to select "Bet inshop" and click on "Go betting" button ,navigate to football bet filter page and should see all the below tabs:
        DESCRIPTION: 1. Create Coupons.
        DESCRIPTION: 2. Your Team.
        DESCRIPTION: 3. The Opposition.
        DESCRIPTION: 4. Saved Filter.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        EXPECTED: 4. User should be able to select "Bet inshop" and click on "Go betting" button ,navigate to football bet filter page and should see all the below tabs:
        EXPECTED: 1. Create Coupons.
        EXPECTED: 2. Your Team.
        EXPECTED: 3. The Opposition.
        EXPECTED: 4. Saved Filter.
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
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options, msg='"Bet in shop" option is not displayed')
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options, msg='"Bet online" option is not displayed')
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        content = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        self.assertTrue(content, msg="Football bet filter page items not displayed")
