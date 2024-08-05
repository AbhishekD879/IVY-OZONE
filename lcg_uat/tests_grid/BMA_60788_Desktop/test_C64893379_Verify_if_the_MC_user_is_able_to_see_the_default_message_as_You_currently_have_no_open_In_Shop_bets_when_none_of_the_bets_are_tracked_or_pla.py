import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893379_Verify_if_the_MC_user_is_able_to_see_the_default_message_as_You_currently_have_no_open_In_Shop_bets_when_none_of_the_bets_are_tracked_or_placed_under_that_user(Common):
    """
    TR_ID: C64893379
    NAME: Verify if the MC user is able to see the default message as "You currently have no open In-Shop bets" when none of the bets are tracked or placed under that user.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid In-Shop user credentials.
    PRECONDITIONS: 3.Bets should not be placed or tracked under that user and local storage is cleared.
    """
    keep_browser_open = True

    def test_001_1_1_launch_ladbrokes_sports_url2_login_with_mc_user3_click_on_grid_tab_from_a_z_menu__carousel__my_account_menu_items4click_on_shop_bet_tracker_from_home_page_menu_items5check_both_settled_bets_tab_and_open_bets_tabsexpected_result1sports_application_should_be_launched_successfully2logged_in_as_in_shop_user3user_should_be_able_to_navigate_to_the_grid_home_page4user_should_be_navigated_to_the_shop_bet_tracker_page5user_must_see_the_below_message_if_the_user_has_no_bets_you_currently_have_noopen_in_shop_bets__you_currently_have_nosettled_in_shop_bets(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports URL.
        DESCRIPTION: 2. Login with MC user.
        DESCRIPTION: 3. Click on grid tab from A-Z menu / carousel / my account menu items.
        DESCRIPTION: 4.Click on shop bet tracker from home page menu items.
        DESCRIPTION: 5.Check both settled bets tab and open bets tabs.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.Logged in as In-Shop user.
        DESCRIPTION: 3.User should be able to navigate to the grid home page.
        DESCRIPTION: 4.User should be navigated to the Shop bet tracker page.
        DESCRIPTION: 5.User must see the below message if the user has no bets "You currently have no
        DESCRIPTION: open In-Shop bets" & "You currently have no
        DESCRIPTION: settled In-Shop bets"
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.Logged in as In-Shop user.
        EXPECTED: 3.User should be able to navigate to the grid home page.
        EXPECTED: 4.User should be navigated to the Shop bet tracker page.
        EXPECTED: 5.User must see the below message if the user has no bets "You currently have no
        EXPECTED: open In-Shop bets" & "You currently have no
        EXPECTED: settled In-Shop bets"
        """
        self.site.login(tests.settings.mc_user)
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.grid.menu_items.items_as_ordered_dict.get(vec.retail.BET_TRACKER).click()
        actual_header = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_header, vec.retail.BET_TRACKER,
                         msg=f'Actual header "{actual_header}" is not same as Expected header "{vec.retail.BET_TRACKER.upper()}"')
        wait_for_result(lambda: self.site.bet_tracker.no_event_text.is_displayed(),
                        timeout=30, name='Open In-shop Bets to be displayed.')
        self.assertTrue(self.site.bet_tracker.cash_out_block.open_in_shop_bet_tab.is_displayed(),
                        msg='"Open In Shop Bets" tab not displayed')
        self.assertTrue(self.site.bet_tracker.cash_out_block.settle_in_shop_bet_tab.is_displayed(),
                        msg='"Settled In Shop Bets" tab not displayed')
        self.assertTrue(self.site.bet_tracker.no_event_text.is_displayed(),
                        msg='Default message that "You currently have no open In-Shop bets" not displayed')
        self.assertEqual(self.site.bet_tracker.no_event_text.text, vec.retail.OPEN_IN_SHOP_NO_BETS_TEXT,
                         msg=f'Actual message {self.site.bet_tracker.no_event_text.text}'
                             f'is not same as expected {vec.retail.OPEN_IN_SHOP_NO_BETS_TEXT}')
