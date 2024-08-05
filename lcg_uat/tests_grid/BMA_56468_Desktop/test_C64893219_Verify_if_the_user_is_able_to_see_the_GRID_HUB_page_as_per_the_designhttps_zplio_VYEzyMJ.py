import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893219_Verify_if_the_user_is_able_to_see_the_GRID_HUB_page_as_per_the_designhttps_zplio_VYEzyMJ(Common):
    """
    TR_ID: C64893219
    NAME: Verify if the user is able to see the "GRID HUB" page as per the design.(https://zpl.io/VYEzyMJ)
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_url2_click_on_grid_quick_link_on_the_header3_verify_the_grid_hub_items_as_per_design_shop_bet_tracker_grid_exclusive_proms_football_buddy_coupons_saved_bet_code_shop_locator_bet_calculatorexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_click_on_the_grid_quick_link_and_navigate_to_the_grid_hub__page3user_should_be_able_to_see_all_the_below_items_in_the_grid_hub_page_as_per_design_shop_bet_tracker_grid_exclusive_proms_football_buddy_coupons_saved_bet_code_shop_locator_bet_calculator(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports URL.
        DESCRIPTION: 2. Click on grid quick link on the header.
        DESCRIPTION: 3. Verify the Grid hub items as per design:
        DESCRIPTION: ->Shop Bet Tracker.
        DESCRIPTION: ->Grid Exclusive Proms.
        DESCRIPTION: ->Football Buddy
        DESCRIPTION: ->Coupons.
        DESCRIPTION: ->Saved Bet Code.
        DESCRIPTION: ->Shop Locator.
        DESCRIPTION: ->Bet Calculator.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to click on the grid quick link and navigate to the GRID HUB  page.
        DESCRIPTION: 3.User should be able to see all the below items in the Grid hub page as per design:
        DESCRIPTION: ->Shop Bet Tracker.
        DESCRIPTION: ->Grid Exclusive Proms.
        DESCRIPTION: ->Football Buddy
        DESCRIPTION: ->Coupons.
        DESCRIPTION: ->Saved Bet Code.
        DESCRIPTION: ->Shop Locator.
        DESCRIPTION: ->Bet Calculator.
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to click on the grid quick link and navigate to the GRID HUB  page.
        EXPECTED: 3.User should be able to see all the below items in the Grid hub page as per design:
        EXPECTED: ->Shop Bet Tracker.
        EXPECTED: ->Grid Exclusive Proms.
        EXPECTED: ->Football Buddy
        EXPECTED: ->Coupons.
        EXPECTED: ->Saved Bet Code.
        EXPECTED: ->Shop Locator.
        EXPECTED: ->Bet Calculator.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertListEqual(list(grid_items), list(vec.retail.EXPECTED_GRID_ITEMS), msg=f'Actual grid items "{grid_items}" are not equal to expected'f' "{vec.retail.EXPECTED_GRID_ITEMS}"')
