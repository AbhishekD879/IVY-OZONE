import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64887531_Verify_the_following_categories_are_displayed_in_create_coupon_page_from_football_bet_filterSelect_Betinshop_betonline_from_the_FCB_pop_up1_Create_your_Coupon_section_with_show_more_drop_down2_Show_more_info_should_be_in_line_with_Prod_functio(Common):
    """
    TR_ID: C64887531
    NAME: Verify the following categories are displayed in create coupon page from football bet filter(Select Betinshop/betonline from the FCB pop up)
    1. Create your Coupon section with show more drop down.
    2. Show more info should be in line with Prod functio
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4click_on_bet_onlinebet_inshop__from_the_fcb_opening_pop_up_and__click_on_go_bettingexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_successfully_open_football_bet_filter_page4user_should_be_landed_on_create_coupon_page_and_it_should_contain_all_the_mentioned_items_in_that_page_successfully1_create_your_coupon_section_with_show_more_drop_down2_show_more_info_should_be_in_line_with_prod_functionality3coupon_tabs4leagues_tabs5date(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 4.Click on bet online/Bet inshop  from the FCB opening pop up and  click on 'Go betting'
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        DESCRIPTION: 4.User should be landed on create coupon page and it should contain all the mentioned items in that page successfully:(1. Create your Coupon section with show more drop down.
        DESCRIPTION: 2. Show more info should be in line with Prod functionality.
        DESCRIPTION: 3.Coupon Tabs.
        DESCRIPTION: 4.Leagues Tabs.
        DESCRIPTION: 5.Date.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        EXPECTED: 4.User should be landed on create coupon page and it should contain all the mentioned items in that page successfully:(1. Create your Coupon section with show more drop down.
        EXPECTED: 2. Show more info should be in line with Prod functionality.
        EXPECTED: 3.Coupon Tabs.
        EXPECTED: 4.Leagues Tabs.
        EXPECTED: 5.Date.
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
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        content = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        self.assertTrue(content, msg="Football bet filter page items not displayed")
