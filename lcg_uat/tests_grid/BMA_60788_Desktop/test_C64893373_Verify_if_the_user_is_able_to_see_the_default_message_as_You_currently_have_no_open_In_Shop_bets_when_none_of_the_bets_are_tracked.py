import pytest
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893373_Verify_if_the_user_is_able_to_see_the_default_message_as_You_currently_have_no_open_In_Shop_bets_when_none_of_the_bets_are_tracked(Common):
    """
    TR_ID: C64893373
    NAME: Verify if the user is able to see the default message as "You currently have no open In-Shop bets" when none of the bets are tracked.
    DESCRIPTION: 
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User Is not logged in with any user.
    PRECONDITIONS: 3.Bets should not be tracked and local storage is cleared.
    """
    keep_browser_open = True

    def test_001_1_1_launch_ladbrokes_sports_url2_click_on_grid_tab_from_a_z_menu__carousel3click_on_shop_bet_tracker_from_home_page_menu_items4check_both_settled_bets_tab_and_open_bets_tabsexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_navigate_to_the_grid_home_page3user_should_be_navigated_to_the_shop_bet_tracker_page4user_must_be_able_to_see_thedefault_message_as_you_currently_have_noopen_in_shop_bets_and_same_for_settled_bets_tab_to_as__you_currently_have_nosettled_in_shop_bets(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports URL.
        DESCRIPTION: 2. Click on grid tab from A-Z menu / carousel.
        DESCRIPTION: 3.Click on shop bet tracker from home page menu items.
        DESCRIPTION: 4.Check both settled bets tab and open bets tabs.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to navigate to the grid home page.
        DESCRIPTION: 3.User should be navigated to the Shop bet tracker page.
        DESCRIPTION: 4.User must be able to see the
        DESCRIPTION: default message as "You currently have no
        DESCRIPTION: open In-Shop bets" and same for settled bets tab to as  "You currently have no
        DESCRIPTION: settled In-Shop bets".
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to navigate to the grid home page.
        EXPECTED: 3.User should be navigated to the Shop bet tracker page.
        EXPECTED: 4.User must be able to see the
        EXPECTED: default message as "You currently have no
        EXPECTED: open In-Shop bets" and same for settled bets tab to as  "You currently have no
        EXPECTED: settled In-Shop bets".
        """
        self.site.wait_content_state("Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.BET_TRACKER.title()).click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        actual_title = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_title, vec.retail.BET_TRACKER.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.retail.BET_TRACKER.title()}"')
        wait_for_result(lambda: self.site.bet_tracker.cash_out_block.open_in_shop_bet_tab.is_displayed(),
                        timeout=30, name='Open In-shop Bets to be displayed.')
        self.assertEqual(self.site.bet_tracker.no_event_text.text, vec.retail.OPEN_IN_SHOP_NO_BETS_TEXT,
                         msg=f'Actual message {self.site.bet_tracker.no_event_text.text}'
                             f'is not same as expected {vec.retail.OPEN_IN_SHOP_NO_BETS_TEXT}')
        wait_for_result(lambda: self.site.bet_tracker.cash_out_block.settle_in_shop_bet_tab.is_displayed(),
                        timeout=30, name='Settled In-shop Bets to be displayed.')
        self.site.bet_tracker.cash_out_block.settle_in_shop_bet_tab.click()
        self.assertEqual(self.site.bet_tracker.no_event_text.text, vec.retail.SETTLED_IN_SHOP_NO_BETS_TEXT,
                         msg=f'Actual message "{self.site.bet_tracker.no_event_text.text}"'
                             f'is not same as expected "{vec.retail.SETTLED_IN_SHOP_NO_BETS_TEXT}"')
