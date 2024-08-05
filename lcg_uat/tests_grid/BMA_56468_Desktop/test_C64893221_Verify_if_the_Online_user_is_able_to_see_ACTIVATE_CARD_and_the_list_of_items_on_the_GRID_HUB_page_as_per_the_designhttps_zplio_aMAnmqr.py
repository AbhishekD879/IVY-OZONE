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
class Test_C64893221_Verify_if_the_Online_user_is_able_to_see_ACTIVATE_CARD_and_the_list_of_items_on_the_GRID_HUB_page_as_per_the_designhttps_zplio_aMAnmqr(Common):
    """
    TR_ID: C64893221
    NAME: Verify if the Online user is able to see "ACTIVATE CARD" and the list of items on the GRID HUB page as per the design.(https://zpl.io/aMAnmqr)
    DESCRIPTION: 
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid Online user credentials.
    """
    keep_browser_open = True

    def test_001_1_1_launch_ladbrokes_sports_url2_click_on_login_and_login_with_valid_online_user_credentials3_click_on_my_account4_click_on_the_grid_from_the_my_account_menu_items5_click_on_the_grid_home_from_the_grid_menu_items6verify_the_list_of_items_on_the_grid_hub_page_activate_card_cta_and_shop_bet_tracker_grid_exclusive_proms_football_buddy_coupons_saved_bet_code_shop_locator_bet_calculatorexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_click_on_login_and_should_be_able_to_login_as_online_user3user_should_be_able_to_see_my_account_menu_items4user_should_be_able_to_click_on_the_grid_and_able_to_see_the_grid_menu_items5user_should_be_navigated_to_the_grid_hub_page6user_should_be_able_to_see_all_the_below_items_in_the_grid_hub_page_as_per_design_activate_card_cta_and_shop_bet_tracker_grid_exclusive_proms_football_buddy_coupons_saved_bet_code_shop_locator_bet_calculator(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports URL.
        DESCRIPTION: 2. Click on login and login with valid Online user credentials.
        DESCRIPTION: 3. Click on My Account.
        DESCRIPTION: 4. Click on "The GRID" from the MY Account menu items.
        DESCRIPTION: 5. Click on "The Grid Home" from "The Grid" menu items.
        DESCRIPTION: 6.Verify the list of items on the GRID Hub page:
        DESCRIPTION: ->ACTIVATE CARD (CTA) and
        DESCRIPTION: ->Shop Bet Tracker.
        DESCRIPTION: ->Grid Exclusive Proms.
        DESCRIPTION: ->Football Buddy
        DESCRIPTION: ->Coupons.
        DESCRIPTION: ->Saved Bet Code.
        DESCRIPTION: ->Shop Locator.
        DESCRIPTION: ->Bet Calculator.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to click on login and should be able to login as Online user.
        DESCRIPTION: 3.User should be able to see My Account menu items.
        DESCRIPTION: 4.User should be able to click on "The GRID" and able to see the grid menu items.
        DESCRIPTION: 5.User should be navigated to "The GRID Hub" page.
        DESCRIPTION: 6.User should be able to see all the below items in the Grid hub page as per design:
        DESCRIPTION: ->ACTIVATE CARD (CTA) and
        DESCRIPTION: ->Shop Bet Tracker.
        DESCRIPTION: ->Grid Exclusive Proms.
        DESCRIPTION: ->Football Buddy
        DESCRIPTION: ->Coupons.
        DESCRIPTION: ->Saved Bet Code.
        DESCRIPTION: ->Shop Locator.
        DESCRIPTION: ->Bet Calculator.
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to click on login and should be able to login as Online user.
        EXPECTED: 3.User should be able to see My Account menu items.
        EXPECTED: 4.User should be able to click on "The GRID" and able to see the grid menu items.
        EXPECTED: 5.User should be navigated to "The GRID Hub" page.
        EXPECTED: 6.User should be able to see all the below items in the Grid hub page as per design:
        EXPECTED: ->ACTIVATE CARD (CTA) and
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
        self.site.header.right_menu_button.avatar_icon.click()
        self.site.right_menu.click_item(vec.retail.TITLE)
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        self.assertListEqual(list(grid_items), list(vec.retail.EXPECTED_GRID_ITEMS),
                             msg=f'Actual grid items "{grid_items}" are not equal to expected'f' "{vec.retail.EXPECTED_GRID_ITEMS}"')
        self.assertTrue(self.site.grid.upgrade_account.is_displayed(),
                        msg=f'"{vec.retail.ACTIVATE_CARD_BUTTON}" button is not displayed')
        actual_text = self.site.grid.upgrade_account.text
        self.assertEqual(actual_text, vec.retail.ACTIVATE_CARD_BUTTON,
                         msg=f'Actual text: "{actual_text}" is not same as Expected text: "{vec.retail.ACTIVATE_CARD_BUTTON}"')
