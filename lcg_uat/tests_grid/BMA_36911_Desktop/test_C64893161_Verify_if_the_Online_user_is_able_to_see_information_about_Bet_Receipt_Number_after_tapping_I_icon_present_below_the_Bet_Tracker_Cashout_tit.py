import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893161_Verify_if_the_Online_user_is_able_to_see_information_about_Bet_Receipt_Number_after_tapping_I_icon_present_below_the_Bet_Tracker_Cashout_title_in_Shop_Bet_Tracker_page(Common):
    """
    TR_ID: C64893161
    NAME: Verify if the Online user is able to see information about Bet Receipt Number after tapping I icon present below the Bet Tracker & Cashout title in Shop Bet Tracker page.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports web
    PRECONDITIONS: application URL.
    PRECONDITIONS: 2.User should have valid Online user credentials.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application2click_on_login_button_and_enter_valid_user_details3click_on_grid_tab_from_main_header4click_on_shop_bet_tracker_from_the_grid_hub5click_on_i_icon_below_the_bet_tracker__cashout_titleexpected_result1sports_application_should_be_launched_successfully2user_should_be_logged_in3user_should_be_able_to_open_grid_tab_from_main_header4user_should_be_navigated_to_shop_bet_tracker_page5user_should_be_able_to_see_the_information_about_your_bet_receipt_number_bet_station_13_digit_bet_number_and_over_the_counter_14_digit_bet_number(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application.
        DESCRIPTION: 2.Click on login button and enter valid user details.
        DESCRIPTION: 3.Click on grid tab from main header.
        DESCRIPTION: 4.Click on "Shop Bet Tracker" from the grid hub.
        DESCRIPTION: 5.Click on (I) icon below the "Bet Tracker & Cashout" title.
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be logged in.
        DESCRIPTION: 3.User should be able to open grid tab from main header.
        DESCRIPTION: 4.User should be navigated to "Shop Bet Tracker" page.
        DESCRIPTION: 5.User should be able to see the information about Your bet receipt number (Bet Station 13 digit bet number) and (Over the counter 14 digit bet number).
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be logged in.
        EXPECTED: 3.User should be able to open grid tab from main header.
        EXPECTED: 4.User should be navigated to "Shop Bet Tracker" page.
        EXPECTED: 5.User should be able to see the information about Your bet receipt number (Bet Station 13 digit bet number) and (Over the counter 14 digit bet number).
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
        grid_items.get(vec.retail.BET_TRACKER.title()).click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        wait_for_result(lambda: self.site.bet_tracker.page_title.is_displayed(),
                        name='In-Shop coupons header is not loaded',
                        timeout=20)
        actual_title = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_title, vec.retail.BET_TRACKER.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.retail.BET_TRACKER.title()}"')
        self.site.bet_tracker.bet_tracker_info_icon.click()
        wait_for_result(lambda: self.site.bet_tracker.receipt_number_info.bet_station_receipt.is_displayed(),
                        name='Bet Tracker Info Icon is not loaded',
                        timeout=20)
        self.assertTrue(self.site.bet_tracker.receipt_number_info.over_the_counter_receipt.is_displayed(),
                        msg='Over the counter receipt info is not displayed')