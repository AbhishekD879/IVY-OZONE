import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893032_Verify_the_following_when_customer_select_bet_in_shop_option_and_applied_all_required_filters_and_on_clicking_find_bets_button1Coupon_Name2Filtered_Selections3Selection_Name4Event_Name5Event_Date__Time6Price(Common):
    """
    TR_ID: C64893032
    NAME: Verify the following  when customer select bet in shop option and applied all required filters and on clicking find bets button.
    1.Coupon Name,
    2.Filtered Selections,
    3.Selection Name,
    4.Event Name,
    5.Event Date / Time,
    6.Price.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4click_on_bet_in_shop_from_the_fcb_opening_pop_up5select_all_required_filters6click_on_find_bets_buttonexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_successfully_open_football_bet_filter_page4user_should_be_landed_on_football_bet_filter_page_by_clicking_go_betting_page5user_should_be_able_to_select_all_required_filter6on_clicking_find_bets_button_we_should_see_all_the_mentioned_items_for_each_selection_in_the_results_page_successfully1coupon_name2filtered_selections3selection_name4event_name5event_date__time6price(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 4.Click on bet in shop from the FCB opening pop up.
        DESCRIPTION: 5.Select all required filters.
        DESCRIPTION: 6.Click on find bets button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        DESCRIPTION: 4.User should be landed on football bet filter page by clicking go betting page.
        DESCRIPTION: 5.User should be able to select all required filter.
        DESCRIPTION: 6.On clicking find bets button we should see all the mentioned items for each selection in the results page successfully:(1.Coupon Name,
        DESCRIPTION: 2.Filtered Selections,
        DESCRIPTION: 3.Selection Name,
        DESCRIPTION: 4.Event Name,
        DESCRIPTION: 5.Event Date / Time,
        DESCRIPTION: 6.Price.)
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        EXPECTED: 4.User should be landed on football bet filter page by clicking go betting page.
        EXPECTED: 5.User should be able to select all required filter.
        EXPECTED: 6.On clicking find bets button we should see all the mentioned items for each selection in the results page successfully:(1.Coupon Name,
        EXPECTED: 2.Filtered Selections,
        EXPECTED: 3.Selection Name,
        EXPECTED: 4.Event Name,
        EXPECTED: 5.Event Date / Time,
        EXPECTED: 6.Price.)
        """
        self.site.login()
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
        bet_inshop = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop)
        bet_inshop.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.assertFalse(
            self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=15),
            msg='Spinner has not disappeared from Find Bets button')
        self.site.contents.scroll_to_bottom()
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.scroll_to_top()
        coupons_content = self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('COUPONS')
        coupon_name, coupon = list(coupons_content.items_as_ordered_dict.items())[0]
        coupon.click()
        content = self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('LEAGUES')
        _, league = list(content.items_as_ordered_dict.items())[0]
        league.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        filter_bets = self.site.football_bet_filter.read_number_of_bets()
        self.site.football_bet_filter.find_bets_button.click()
        self.assertTrue(self.site.football_bet_filter_results_page.button.is_displayed(),
                        msg='"Add to Betslip Button" is not displayed')
        expected_bets = self.site.football_bet_filter_results_page.number_of_results
        self.assertIn(coupon_name, self.site.football_bet_filter_results_page.coupon_name,
                      msg=f'{coupon_name} is not there in {self.site.football_bet_filter_results_page.coupon_name}')
        self.assertEquals(filter_bets, expected_bets, msg="Filtered Selections are not displayed")
        selections = self.site.football_bet_filter_results_page.items_as_ordered_dict
        self.assertTrue(selections, msg='No selections found')
        for selection_name, selection in selections.items():
            self.assertTrue(selection.checkbox, msg=f'"Checkbox" is not displayed')
            self.assertTrue(selection.name, msg=f'"Selection name" is not displayed')
            self.assertTrue(selection.event_name, msg=f'"Event name" is not displayed')
            self.assertTrue(selection.match_date.text, msg=f'"Event Date" is not displayed')
            self.assertTrue(selection.odds, msg=f'"Odds" is not displayed')
