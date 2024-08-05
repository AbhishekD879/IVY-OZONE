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
class Test_C64893224_Verify_the_items_in_the_GRID_hub_page_after_user_logged_outhttps_zplio_VYEzyMJ(Common):
    """
    TR_ID: C64893224
    NAME: Verify the items in the GRID hub page after user logged out.(https://zpl.io/VYEzyMJ)
    DESCRIPTION: 
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2. User should be logged out.
    """
    keep_browser_open = True

    def test_001_1_1_launch_ladbrokes_sports_url2_click_on_my_account_and_click_on_logout3_click_on_grid_quick_link_on_the_header4verify_the_list_of_items_on_the_grid_hub_page_shop_bet_tracker_grid_exclusive_proms_football_buddy_coupons_saved_bet_code_shop_locator_bet_calculatorexpected_result1sports_application_should_be_launched_successfully2_user_should_be_logged_out_successfully3_user_should_be_able_to_click_on_the_grid_quick_link_and_navigate_to_the_grid_hub__page4user_must_be_able_to_see_the_list_of_items_on_the_grid_hub_page_shop_bet_tracker_grid_exclusive_proms_football_buddy_coupons_saved_bet_code_shop_locator_bet_calculator(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports URL.
        DESCRIPTION: 2. Click on My account and click on logout.
        DESCRIPTION: 3. Click on grid quick link on the header.
        DESCRIPTION: 4.Verify the list of items on the GRID Hub page:
        DESCRIPTION: ->Shop Bet Tracker.
        DESCRIPTION: ->Grid Exclusive Proms.
        DESCRIPTION: ->Football Buddy
        DESCRIPTION: ->Coupons.
        DESCRIPTION: ->Saved Bet Code.
        DESCRIPTION: ->Shop Locator.
        DESCRIPTION: ->Bet Calculator.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2. User should be logged out successfully.
        DESCRIPTION: 3. User should be able to click on the grid quick link and navigate to the GRID HUB  page.
        DESCRIPTION: 4.User must be able to see the list of items on the Grid hub page:
        DESCRIPTION: ->Shop Bet Tracker.
        DESCRIPTION: ->Grid Exclusive Proms.
        DESCRIPTION: ->Football Buddy
        DESCRIPTION: ->Coupons.
        DESCRIPTION: ->Saved Bet Code.
        DESCRIPTION: ->Shop Locator.
        DESCRIPTION: ->Bet Calculator.
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2. User should be logged out successfully.
        EXPECTED: 3. User should be able to click on the grid quick link and navigate to the GRID HUB  page.
        EXPECTED: 4.User must be able to see the list of items on the Grid hub page:
        EXPECTED: ->Shop Bet Tracker.
        EXPECTED: ->Grid Exclusive Proms.
        EXPECTED: ->Football Buddy
        EXPECTED: ->Coupons.
        EXPECTED: ->Saved Bet Code.
        EXPECTED: ->Shop Locator.
        EXPECTED: ->Bet Calculator.
        """
        self.site.wait_content_state(state_name='Homepage', timeout=30)
        self.site.login()
        self.site.logout()
        if self.device_type == 'mobile':
            self.site.open_sport(name=vec.retail.TITLE)
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        self.assertListEqual(list(grid_items), list(vec.retail.EXPECTED_GRID_ITEMS),  msg=f'Actual grid items "{grid_items}" are not equal to expected'f' "{vec.retail.EXPECTED_GRID_ITEMS}"')
