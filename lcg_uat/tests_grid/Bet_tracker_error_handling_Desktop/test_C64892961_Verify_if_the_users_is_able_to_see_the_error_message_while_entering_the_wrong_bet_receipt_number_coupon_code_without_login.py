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
class Test_C64892961_Verify_if_the_users_is_able_to_see_the_error_message_while_entering_the_wrong_bet_receipt_number_coupon_code_without_login(Common):
    """
    TR_ID: C64892961
    NAME: Verify if the users is able to see the error message while entering the wrong bet receipt number/coupon code without login.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have invalid bet receipt number.
    """
    keep_browser_open = True
    invalid_betslip_id = 'A1B2C3D4E5'

    def test_001_1_1launch_ladbrokes_sports_application2click_on_grid_tab_from_header_menu3click_on_bet_tracker_from_grid_hub_menu_items_list4enter_invalid_bet_receipt_numberexpected_result1sports_web_application_should_be_launched2user_should_be_able_to_click_on_grid_tab_and_should_be_landed_on_grid_hub_menu3user_should_be_able_to_click_on_bet_tracker_from_grid_hub_menu_items_and_should_be_landed_on_bet_tracker_page4user_should_see_the_following_error_message_after_clicking_on_track_bet_buttonreceipt_code_not_recognized_lorem_ipsum_lorem_ipsum_guiding_text_to_help_users_lorem_ipsum_lorem_ipsum_lorem_ipsum(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports application.
        DESCRIPTION: 2.Click on grid tab from header menu.
        DESCRIPTION: 3.Click on bet tracker from grid hub menu items list.
        DESCRIPTION: 4.Enter invalid bet receipt number.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launched.
        DESCRIPTION: 2.User should be able to click on grid tab and should be landed on grid hub menu.
        DESCRIPTION: 3.User should be able to click on bet tracker from grid hub menu items and should be landed on bet tracker page.
        DESCRIPTION: 4.User should see the following error message after clicking on track bet button.{"Receipt code not recognized. Lorem Ipsum Lorem Ipsum Guiding Text to help users Lorem Ipsum Lorem Ipsum Lorem Ipsum"}
        EXPECTED: 1. 1.Sports web application should be launched.
        EXPECTED: 2.User should be able to click on grid tab and should be landed on grid hub menu.
        EXPECTED: 3.User should be able to click on bet tracker from grid hub menu items and should be landed on bet tracker page.
        EXPECTED: 4.User should see the following error message after clicking on track bet button.{"Receipt code not recognized. Lorem Ipsum Lorem Ipsum Guiding Text to help users Lorem Ipsum Lorem Ipsum Lorem Ipsum"}
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
        coupon_error_msg = wait_for_result(lambda: self.site.bet_tracker.coupon_error_msg.text is not None)
        self.assertTrue(coupon_error_msg, msg='No error message is displayed after tracking invalid coupon')
        self.assertEqual(self.site.bet_tracker.coupon_error_msg.text, vec.retail.BET_RECEIPT_ERROR_MESSAGE,
                         msg=f'Actual error message: "{self.site.bet_tracker.coupon_error_msg.text}" is not same as '
                             f'expected error message: "{vec.retail.BET_RECEIPT_ERROR_MESSAGE}"')
