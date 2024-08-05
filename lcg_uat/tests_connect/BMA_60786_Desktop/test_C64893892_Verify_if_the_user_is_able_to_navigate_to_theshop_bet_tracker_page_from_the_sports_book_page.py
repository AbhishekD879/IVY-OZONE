import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.connect
@vtest
class Test_C64893892_Verify_if_the_user_is_able_to_navigate_to_theshop_bet_tracker_page_from_the_sports_book_page(Common):
    """
    TR_ID: C64893892
    NAME: Verify if the user is able to navigate to the shop bet tracker page from the sports book page.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Coral sports URL.
    PRECONDITIONS: 2.User Is not logged in with any user.
    """
    keep_browser_open = True

    def test_001_1_1_1_launch_coral_sports_url2_click_on_connect_tab_from_a_z_menu__carousel3click_on_shop_bet_tracker_from_home_page_menu_itemsexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_grid_home_page3user_should_be_navigated_to_the_shop_bet_tracker_pageexpected_result1_1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_grid_home_page3user_should_be_navigated_to_the_shop_bet_tracker_page(self):
        """
        DESCRIPTION: 1. 1. 1. Launch Coral sports URL.
        DESCRIPTION: 2. Click on connect tab from A-Z menu / carousel.
        DESCRIPTION: 3.Click on shop bet tracker from home page menu items.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the grid home page.
        DESCRIPTION: 3.User should be navigated to the Shop bet tracker page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the connect home page.
        DESCRIPTION: 3.User should be navigated to the Shop bet tracker page.
        EXPECTED: 1. 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to navigate to the grid home page.
        EXPECTED: 3.User should be navigated to the Shop bet tracker page.
        """
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='connect')
        connect_items = self.site.connect.menu_items.items_as_ordered_dict
        connect_items[vec.retail.BET_TRACKER].click()
        actual_header = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_header, vec.retail.BET_TRACKER.upper(),
                         msg=f'Actual header "{actual_header}" is not same as Expected header "{vec.retail.BET_TRACKER.upper()}"')
