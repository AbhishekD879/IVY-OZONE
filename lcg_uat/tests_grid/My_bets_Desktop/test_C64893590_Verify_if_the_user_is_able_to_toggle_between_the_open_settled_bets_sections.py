import pytest
import voltron.environments.constants as vec
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
class Test_C64893590_Verify_if_the_user_is_able_to_toggle_between_the_open_settled_bets_sections(Common):
    """
    TR_ID: C64893590
    NAME: Verify if the user is able to toggle between the open & settled bets sections.
    DESCRIPTION: 
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_url2click_on_grid_tab3click_on_my_bets_at_the_bottom_of_the_page4click_on_open_and_settled_bets_tabsexpected_result1sports_url_should_be_launched_sucessfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_access_my_bets_sucessfully4user_must_be_able_to_toggle_between_the_open_and_settled_bets_sections(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports url.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on "My Bets" at the bottom of the page.
        DESCRIPTION: 4.Click on open and settled bets tabs.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports url should be launched sucessfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to access "My Bets" sucessfully.
        DESCRIPTION: 4.User must be able to toggle between the open and settled bets sections.
        EXPECTED: 1. 1.Sports url should be launched sucessfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to access "My Bets" sucessfully.
        EXPECTED: 4.User must be able to toggle between the open and settled bets sections.
        """
        self.site.login()
        self.site.wait_content_state(state_name="Homepage")
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
        actual_title = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_title, vec.retail.BET_TRACKER.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.retail.BET_TRACKER.title()}"')
        self.assertTrue(self.site.bet_tracker.track_button.is_displayed(),
                        msg='"Track Button" not displayed')
        wait_for_result(lambda: self.site.bet_tracker.cash_out_block.open_in_shop_bet_tab.is_displayed(),
                        timeout=30, name='Open In-shop Bets to be displayed.')
        self.site.bet_tracker.cash_out_block.settle_bet_tab_styles.click()
        result = wait_for_result(lambda: self.site.bet_tracker.cash_out_block.settle_in_shop_bet_tab_active,
                        timeout=30, name='Settle In-shop Bets to be displayed.')
        self.assertTrue(result, msg="Settled in-shop bet is not active")
        self.site.bet_tracker.cash_out_block.open_in_shop_bet_tab.click()
        result = wait_for_result(lambda: self.site.bet_tracker.cash_out_block.open_in_shop_bet_tab_active,
                                 timeout=30, name='Open In-shop Bets to be displayed.')
        self.assertTrue(result, msg="Open in-shop bet is not active")

