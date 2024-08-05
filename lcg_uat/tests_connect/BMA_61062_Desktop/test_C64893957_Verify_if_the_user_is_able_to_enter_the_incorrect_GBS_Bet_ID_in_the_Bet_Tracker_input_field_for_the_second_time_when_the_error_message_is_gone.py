import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.conect
@vtest
class Test_C64893957_Verify_if_the_user_is_able_to_enter_the_incorrect_GBS_Bet_ID_in_the_Bet_Tracker_input_field_for_the_second_time_when_the_error_message_is_gone(Common):
    """
    TR_ID: C64893957
    NAME: Verify if the user is able to enter the incorrect "GBS" Bet ID in the Bet Tracker input field for the second time when the error message is gone.
    PRECONDITIONS: 1.User should have valid Coral sports URL.
    PRECONDITIONS: 2.User should have invalid "GBS" bet receipt number.
    """
    keep_browser_open = True
    invalid_coupon = 'DCN478358D'

    def track_invali_coupon_and_verify_message(self):
        self.site.bet_tracker.coupon_input = self.invalid_coupon
        self.assertTrue(self.site.bet_tracker.track_button.is_displayed(), msg='"Track button" is not displayed')
        self.site.bet_tracker.track_button.click()
        coupon_error_msg = wait_for_result(lambda: self.site.bet_tracker.coupon_error_msg.text is not None)
        self.assertTrue(coupon_error_msg, msg='No error message is displayed after tracking invalid coupon')

    def test_001_launch_coral_sports_url2_click_on_connect_tab_from_a_z_menu__carousel__my_account_menu_items3click_on_shop_bet_tracker_from_the_connect_home_page_items4tap_on_bet_tracker_input_field_and_enter_the_10_digit__alpha_numeric_gbs_bet_receipt_number5click_on_track_button6check_if_the_user_is_able_to_see_the_respective_error_message_after_tracking_for_the_2nd_timeexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_navigate_to_the_connect_home_page3user_should_be_navigated_to_shop_bet_tracker_page4user_should_be_able_to_tap_on_bet_tracker_input_field_and_enter_the_invalid_gbs_bet_receipt_number5user_should_be_able_to_click_on_track_button6user_should_be_able_to_see_the_respective_error_message_as__expected_result1_1sports_application_should_be_launch_successfully2user_should_be_able_to_navigate_to_the_connect_home_page3user_should_be_navigated_to_shop_bet_tracker_page4user_should_be_able_to_tap_on_bet_tracker_input_field_and_enter_the_invalid_gbs_bet_receipt_number5user_should_be_able_to_click_on_track_button6user_should_be_able_to_see_the_respective_error_message_as__(self):
        """
        DESCRIPTION: 1.Launch Coral sports URL.
        DESCRIPTION: 2.Click on Connect tab from A-Z menu / carousel / my account menu items.
        DESCRIPTION: 3.Click on "Shop Bet Tracker" from the Connect home page items.
        DESCRIPTION: 4.Tap on bet tracker input field and enter the 10 digit  alpha numeric "GBS" bet receipt number.
        DESCRIPTION: 5.Click on track button.
        DESCRIPTION: 6.Check if the user is able to see the respective Error Message after tracking for the 2nd time.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to navigate to the Connect home page.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker Page".
        DESCRIPTION: 4.User should be able to tap on bet tracker input field and enter the invalid "GBS" bet receipt number.
        DESCRIPTION: 5.User should be able to click on track button.
        DESCRIPTION: 6.User should be able to see the Respective error message as " "
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='connect')
        menu_items = self.site.connect.menu_items.items_as_ordered_dict
        menu_items[vec.retail.BET_TRACKER].click()
        actual_header = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_header, vec.retail.BET_TRACKER.upper(),
                         msg=f'Actual header "{actual_header}" is not same as Expected header "{vec.retail.BET_TRACKER.upper()}"')
        self.track_invali_coupon_and_verify_message()
        sleep(30)  # track button will be disabled till the next 30 sec
        self.track_invali_coupon_and_verify_message()
