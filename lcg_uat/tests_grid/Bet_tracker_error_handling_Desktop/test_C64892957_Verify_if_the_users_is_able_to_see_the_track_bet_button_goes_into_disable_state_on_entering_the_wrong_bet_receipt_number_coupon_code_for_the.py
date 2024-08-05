import pytest
from tests.base_test import vtest
from voltron.environments import constants as vec
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
class Test_C64892957_Verify_if_the_users_is_able_to_see_the_track_bet_button_goes_into_disable_state_on_entering_the_wrong_bet_receipt_number_coupon_code_for_the_3rd_time(Common):
    """
    TR_ID: C64892957
    NAME: Verify if the users is able to see the track bet button goes into disable state on entering the wrong bet receipt number/coupon code for the 3rd time.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have invalid bet receipt number.
    PRECONDITIONS: 3.User should have valid online/in shop user login Credentials.
    """
    keep_browser_open = True
    invalid_betslip_id = 'A1B2C3D4E5'

    def test_001_launch_ladbrokes_sports_application_and_login_with_valid_onlinein_shop_user2click_on_grid_tab_from_header_menu3click_on_bet_tracker_from_grid_hub_menu_items_list4try_to_enter_wrong_bet_receipt_numbercoupon_code_3_times_in_a_rowexpected_result1sports_web_application_should_be_launched2user_should_be_able_to_click_on_grid_tab_and_should_be_landed_on_grid_hub_menu3user_should_be_able_to_click_on_bet_tracker_from_grid_hub_menu_items_and_should_be_landed_on_bet_tracker_page4on_the_3rd_time_track_bet_button_should_be_in_disable_state_for_30_seconds_and_a_valid_message_should_be_shownreceipt_code_not_recognized_verify_it_is_still_valid_and_try_again_in_30_seconds_if_the_problem_persist_please_contact_xxxxxlorem_ipsum(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports application and login with valid online/in shop user.
        DESCRIPTION: 2.Click on grid tab from header menu.
        DESCRIPTION: 3.Click on bet tracker from grid hub menu items list.
        DESCRIPTION: 4.Try to enter wrong bet receipt number/coupon code 3 times in a row.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launched.
        DESCRIPTION: 2.User should be able to click on grid tab and should be landed on grid hub menu.
        DESCRIPTION: 3.User should be able to click on bet tracker from grid hub menu items and should be landed on bet tracker page.
        DESCRIPTION: 4.On the 3rd time track bet button should be in disable state for 30 seconds and a valid message should be shown.{"Receipt code not recognized. Verify it is still valid and try again in 30 seconds. If the problem persist please contact XXXXXLorem Ipsum"}
        EXPECTED: 1. 1.Sports web application should be launched.
        EXPECTED: 2.User should be able to click on grid tab and should be landed on grid hub menu.
        EXPECTED: 3.User should be able to click on bet tracker from grid hub menu items and should be landed on bet tracker page.
        EXPECTED: 4.On the 3rd time track bet button should be in disable state for 30 seconds and a valid message should be shown.{"Receipt code not recognized. Verify it is still valid and try again in 30 seconds. If the problem persist please contact XXXXXLorem Ipsum"}
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items[vec.retail.BET_TRACKER].click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        self.site.bet_tracker.coupon_input = self.invalid_betslip_id
        self.assertTrue(self.site.bet_tracker.track_button.is_displayed(), msg='"Track button" is not displayed')
        self.site.bet_tracker.track_button.click()
        self.site.wait_content_state_changed(timeout=15)
        coupon_error_msg = wait_for_result(lambda: self.site.bet_tracker.coupon_error_msg.text is not None)
        self.assertTrue(coupon_error_msg, msg='No error message is displayed after tracking invalid coupon')
        self.assertEqual(self.site.bet_tracker.coupon_error_msg.text, vec.retail.BET_RECEIPT_ERROR_MESSAGE,
                         msg=f'Actual error message: "{self.site.bet_tracker.coupon_error_msg.text}" is not same as '
                             f'expected error message: "{vec.retail.BET_RECEIPT_ERROR_MESSAGE}"')
        self.site.bet_tracker.track_button.click()
        self.site.wait_content_state_changed(timeout=15)
        self.site.bet_tracker.track_button.click()
        self.site.wait_content_state_changed(timeout=15)
        self.assertFalse(self.site.bet_tracker.track_button.is_enabled(), msg=f'"Track Bet Button is Enabled"')
        self.assertEqual(self.site.bet_tracker.coupon_error_msg.text, vec.retail.BET_RECEIPT_ERROR_MESSAGE_3RD_TIME_Track,
                         msg=f'Actual error message: "{self.site.bet_tracker.coupon_error_msg.text}" is not same as '
                             f'expected error message: "{vec.retail.BET_RECEIPT_ERROR_MESSAGE_3RD_TIME_Track}"')
