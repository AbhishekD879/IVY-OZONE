import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.connect
@vtest
class Test_C64893953_Verify_if_the_user_is_able_to_tap_on_the_bettracker_input_field_and_enter_10_digit_alpha_numeric_GBS_bet_slip_number(Common):
    """
    TR_ID: C64893953
    NAME: Verify if the user is able to tap on the bettracker input field and enter 10 digit alpha numeric GBS bet slip number.
    DESCRIPTION: 
    PRECONDITIONS: 1.User should have valid Coral sports URL.
    PRECONDITIONS: 2.User should have valid GBS bet slip number.
    """
    keep_browser_open = True

    def test_001_1_1_1_launch_coral_sports_url2_click_on_connect_tab_from_a_z_menu__carousel__my_account_menu_items3click_on_shop_bet_tracker_from_the_connect_home_page_items4tap_on_bet_tracker_input_fieldexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_connect_home_page3user_should_be_navigated_to_shop_bet_tracker_page4user_should_be_able_to_tap_on_bet_tracker_input_field_and_enter_10_digit_alpha_numeric_gbs_bet_slip_numberexpected_result1_1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_connect_home_page3user_should_be_navigated_to_shop_bet_tracker_page4user_should_be_able_to_tap_on_bet_tracker_input_field_and_enter_10_digit_alpha_numeric_gbs_bet_slip_number(self):
        """
        DESCRIPTION: 1. 1. 1. Launch Coral sports URL.
        DESCRIPTION: 2. Click on Connect tab from A-Z menu / carousel / my account menu items.
        DESCRIPTION: 3.Click on "Shop Bet Tracker" from the Connect home page items.
        DESCRIPTION: 4.Tap on bet tracker input field.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the Connect home page.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker Page".
        DESCRIPTION: 4.User should be able to tap on bet tracker input field and enter 10 digit alpha numeric GBS bet slip number.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the Connect home page.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker Page".
        DESCRIPTION: 4.User should be able to tap on bet tracker input field and enter 10 digit alpha numeric GBS bet slip number.
        EXPECTED: 1. 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to navigate to the Connect home page.
        EXPECTED: 3.User should be navigated to "Shop Bet Tracker Page".
        EXPECTED: 4.User should be able to tap on bet tracker input field and enter 10 digit alpha numeric GBS bet slip number.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='connect')
        connect_items = self.site.connect.menu_items.items_as_ordered_dict
        self.assertTrue(connect_items, msg='"Connect" page items not loaded')
        connect_items.get(vec.retail.BET_TRACKER.title()).click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        bet_slip = "1YDWLHPMSM"
        self.site.bet_tracker.coupon_input = bet_slip
        text = self.site.bet_tracker.coupon_input.get_attribute('value')
        self.assertEqual(text, bet_slip, msg="Unable to enter betlslip number")
