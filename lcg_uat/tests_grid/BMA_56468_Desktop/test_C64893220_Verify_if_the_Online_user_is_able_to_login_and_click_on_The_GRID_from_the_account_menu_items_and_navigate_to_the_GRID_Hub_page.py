import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893220_Verify_if_the_Online_user_is_able_to_login_and_click_on_The_GRID_from_the_account_menu_items_and_navigate_to_the_GRID_Hub_page(Common):
    """
    TR_ID: C64893220
    NAME: Verify if the Online user is able to login and click on The GRID from the account menu items and navigate to the GRID Hub page.
    DESCRIPTION: 
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid Online user credentials.
    """
    keep_browser_open = True

    def test_001_1_1_launch_ladbrokes_sports_url2_click_on_login_and_login_with_valid_online_user_credentials3_click_on_my_account4_click_on_the_grid_from_the_my_account_menu_items5_click_on_the_grid_home_from_the_grid_menu_itemsexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_click_on_login_and_should_be_able_to_login_as_online_user3user_should_be_able_to_see_my_account_menu_items4user_should_be_able_to_click_on_the_grid_and_able_to_see_the_grid_menu_items5user_should_be_navigated_to_the_grid_hub_page(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports URL.
        DESCRIPTION: 2. Click on login and login with valid Online user credentials.
        DESCRIPTION: 3. Click on My Account.
        DESCRIPTION: 4. Click on "The GRID" from the MY Account menu items.
        DESCRIPTION: 5. Click on "The Grid Home" from "The Grid" menu items.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to click on login and should be able to login as Online user.
        DESCRIPTION: 3.User should be able to see My Account menu items.
        DESCRIPTION: 4.User should be able to click on "The GRID" and able to see the grid menu items.
        DESCRIPTION: 5.User should be navigated to "The GRID Hub" page.
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to click on login and should be able to login as Online user.
        EXPECTED: 3.User should be able to see My Account menu items.
        EXPECTED: 4.User should be able to click on "The GRID" and able to see the grid menu items.
        EXPECTED: 5.User should be navigated to "The GRID Hub" page.
        """
        self.site.wait_content_state(state_name='Homepage', timeout=30)
        self.site.login()
        self.site.header.right_menu_button.avatar_icon.click()
        self.site.right_menu.click_item(vec.retail.TITLE)
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
