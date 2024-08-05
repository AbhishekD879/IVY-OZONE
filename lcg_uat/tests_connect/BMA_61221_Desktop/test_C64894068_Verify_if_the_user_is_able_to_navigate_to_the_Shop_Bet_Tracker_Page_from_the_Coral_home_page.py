import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.connect
@vtest
class Test_C64894068_Verify_if_the_user_is_able_to_navigate_to_the_Shop_Bet_Tracker_Page_from_the_Coral_home_page(Common):
    """
    TR_ID: C64894068
    NAME: Verify if the user is able to navigate to the "Shop Bet Tracker Page" from the Coral home page.
    PRECONDITIONS: 1.User should have valid Coral sports URL.
    """
    keep_browser_open = True

    def test_001_1_1_1_launch_coral_sports_url2_click_on_coral_tab_from_a_z_menu__carousel__my_account_menu_items3click_on_shop_bet_tracker_from_the_coral_home_page_itemsexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_coral_home_page3user_should_be_navigated_to_shop_bet_tracker_pageexpected_result1_1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_coral_home_page3user_should_be_navigated_to_shop_bet_tracker_page(self):
        """
        DESCRIPTION: 1. 1. 1. Launch Coral sports URL.
        DESCRIPTION: 2. Click on coral tab from A-Z menu / carousel / my account menu items.
        DESCRIPTION: 3.Click on "Shop Bet Tracker" from the coral home page items.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the coral home page.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker Page".
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the coral home page.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker Page".
        EXPECTED: 1. 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to navigate to the coral home page.
        EXPECTED: 3.User should be navigated to "Shop Bet Tracker Page".
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='connect')
        menu_items = self.site.connect.menu_items.items_as_ordered_dict
        menu_items[vec.retail.BET_TRACKER].click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        actual_header = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_header, vec.retail.BET_TRACKER.upper(),
                         msg=f'Actual header "{actual_header}" is not same as Expected header "{vec.retail.BET_TRACKER.upper()}"')
