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
class Test_C64892963_Verify_if_the_user_is_able_to_see_the_bet_tracker_error_message_while_he_tries_to_enter_the_Alphanumeric_characters(Common):
    """
    TR_ID: C64892963
    NAME: Verify if the user is able to see the bet tracker error message while he tries to enter the Alphanumeric characters
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should be on shop bet tracker
    """
    keep_browser_open = True
    alphanumeric_chars = 'DCN478358D'

    def test_001_1_1launch_ladbrokes_sports_application2click_on_grid_tab_from_header_menu3click_on_bet_tracker_from_grid_hub_menu_items_list4try_to_enter_alphanumeric_charactersexpected_result1sports_web_application_should_be_launched2user_should_be_able_to_click_on_grid_tab_and_should_be_landed_on_grid_hub_menu3user_should_be_able_to_click_on_bet_tracker_from_grid_hub_menu_items_and_should_be_landed_on_bet_tracker_page4user_should_be_able_to_enter_the_alphanumeric_as_gbs_bets_are_tracked(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports application.
        DESCRIPTION: 2.Click on grid tab from header menu.
        DESCRIPTION: 3.Click on bet tracker from grid hub menu items list.
        DESCRIPTION: 4.try to enter alphanumeric characters
        DESCRIPTION: 1.Sports web application should be launched.
        DESCRIPTION: 2.User should be able to click on grid tab and should be landed on grid hub menu.
        DESCRIPTION: 3.User should be able to click on bet tracker from grid hub menu items and should be landed on bet tracker page.
        DESCRIPTION: 4.User should be able to enter the alphanumeric as GBS bets are tracked
        EXPECTED: 1. 1.Sports web application should be launched.
        EXPECTED: 2.User should be able to click on grid tab and should be landed on grid hub menu.
        EXPECTED: 3.User should be able to click on bet tracker from grid hub menu items and should be landed on bet tracker page.
        EXPECTED: 4.User should be able to enter the alphanumeric as GBS bets are tracked
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
        actual_header = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_header, vec.retail.BET_TRACKER.title(),
                         msg=f'Actual header "{actual_header}" is not same as Expected header "{vec.retail.BET_TRACKER.title()}"')
        self.site.bet_tracker.coupon_input = self.alphanumeric_chars
        self.assertTrue(self.site.bet_tracker.track_button.is_displayed(), msg='"Track button" is not displayed')
        self.site.bet_tracker.track_button.click()
        coupon_error_msg = wait_for_result(lambda: self.site.bet_tracker.coupon_error_msg.text is not None)
        self.assertTrue(coupon_error_msg, msg='No error message is displayed after tracking invalid coupon')
