import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.connect
@vtest
class Test_C64893959_Verify_if_the_user_is_able_to_click_on_TRACK_button_when_user_gets_error_message_for_the_third_time(Common):
    """
    TR_ID: C64893959
    NAME: Verify if the user is able to click on "TRACK" button when user gets error message for the third time.
    PRECONDITIONS: 1.User should have valid Coral sports URL.
    PRECONDITIONS: 2.User should have invalid "GBS" bet receipt number.
    """
    keep_browser_open = True
    invalid_GBS_bet_receipt_number = 'A1B2C3D4E5'

    def test_001_1_1_1_launch_coral_sports_url2_click_on_connect_tab_from_a_z_menu__carousel__my_account_menu_items3click_on_shop_bet_tracker_from_the_connect_home_page_items4tap_on_bet_tracker_input_field_and_enter_the_10_digit__alpha_numeric_gbs_bet_receipt_number5click_on_track_buttonexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_connect_home_page3user_should_be_navigated_to_shop_bet_tracker_page4user_should_be_able_to_tap_on_bet_tracker_input_field_and_enter_the_invalid_gbs_bet_receipt_number5user_should_not_be_able_to_click_on_track_button_as_it_is_disabled_for_30secexpected_result1_1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_connect_home_page3user_should_be_navigated_to_shop_bet_tracker_page4user_should_be_able_to_tap_on_bet_tracker_input_field_and_enter_the_invalid_gbs_bet_receipt_number5user_should_not_be_able_to_click_on_track_button_as_it_is_disabled_for_30sec(self):
        """
        DESCRIPTION: 1. 1. 1. Launch Coral sports URL.
        DESCRIPTION: 2. Click on Connect tab from A-Z menu / carousel / my account menu items.
        DESCRIPTION: 3.Click on "Shop Bet Tracker" from the Connect home page items.
        DESCRIPTION: 4.Tap on bet tracker input field and enter the 10 digit  alpha numeric "GBS" bet receipt number.
        DESCRIPTION: 5.Click on track button.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the Connect home page.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker Page".
        DESCRIPTION: 4.User should be able to tap on bet tracker input field and enter the invalid "GBS" bet receipt number.
        DESCRIPTION: 5.User should not be able to click on track button as it is disabled for 30sec.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the Connect home page.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker Page".
        DESCRIPTION: 4.User should be able to tap on bet tracker input field and enter the invalid "GBS" bet receipt number.
        DESCRIPTION: 5.User should not be able to click on track button as it is disabled for 30sec.
        EXPECTED: 1. 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to navigate to the Connect home page.
        EXPECTED: 3.User should be navigated to "Shop Bet Tracker Page".
        EXPECTED: 4.User should be able to tap on bet tracker input field and enter the invalid "GBS" bet receipt number.
        EXPECTED: 5.User should not be able to click on track button as it is disabled for 30sec.
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
        self.site.bet_tracker.coupon_input = self.invalid_GBS_bet_receipt_number
        self.assertTrue(self.site.bet_tracker.track_button.is_displayed(), msg='"Track button" is not displayed')
        self.site.bet_tracker.track_button.click()
        coupon_error_msg = wait_for_result(lambda: self.site.bet_tracker.coupon_error_msg.text is not None)
        self.assertTrue(coupon_error_msg, msg='No error message is displayed after tracking invalid coupon')
        self.assertFalse(self.site.bet_tracker.track_button.is_enabled(),
                         msg='Track bet button is enabled which should be disabled for 30sec')
