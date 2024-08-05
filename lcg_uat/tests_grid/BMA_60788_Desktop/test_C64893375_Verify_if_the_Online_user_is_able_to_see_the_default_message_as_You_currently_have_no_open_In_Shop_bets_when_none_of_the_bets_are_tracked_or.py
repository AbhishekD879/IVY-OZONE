import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893375_Verify_if_the_Online_user_is_able_to_see_the_default_message_as_You_currently_have_no_open_In_Shop_bets_when_none_of_the_bets_are_tracked_or_placed_under_that_user(Common):
    """
    TR_ID: C64893375
    NAME: Verify if the Online user is able to see the
    default message as "You currently have no
    open In-Shop bets" when none of the bets are tracked or placed under that user.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid Online user credentials.
    PRECONDITIONS: 3.Bets should not be placed or tracked under that user and local storage is cleared.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_url2login_with_online_user3_click_on_grid_tab_from_a_z_menu__carousel__my_account_menu_items4click_on_shop_bet_tracker_from_home_page_menu_items5check_both_settled_bets_tab_and_open_bets_tabsexpected_result1sports_application_should_be_launched_successfully2logged_in_as_online_user3user_should_be_able_to_navigate_to_the_grid_home_page4user_should_be_navigated_to_the_shop_bet_tracker_page5user_must_be_able_to_see_the_default_message_as_you_currently_have_no_open_in_shop_bets_and_same_for_settled_bets_tab_to_as__you_currently_have_no_settled_in_shop_bets(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Login with Online user.
        DESCRIPTION: 3. Click on grid tab from A-Z menu / carousel / my account menu items.
        DESCRIPTION: 4.Click on shop bet tracker from home page menu items.
        DESCRIPTION: 5.Check both settled bets tab and open bets tabs.
        EXPECTED: 1.Sports application should be launched successfully.
        EXPECTED: 2.Logged in as Online user.
        EXPECTED: 3.User should be able to navigate to the grid home page.
        EXPECTED: 4.User should be navigated to the Shop bet tracker page.
        EXPECTED: 5.User must be able to see the default message as "You currently have no open In-Shop bets" and same for settled bets tab to as  "You currently have no settled In-Shop bets".
        """
        self.site.login()
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.grid.menu_items.items_as_ordered_dict.get(vec.retail.EXPECTED_GRID_ITEMS.shop_bet_tracker).click()
        self.site.wait_content_state(state_name='BetTracker', timeout=20)
        sleep(5)
        self.assertEqual(self.site.bet_tracker.no_event_text.text, vec.retail.OPEN_IN_SHOP_NO_BETS_TEXT,
                         msg=f'Actual message "{self.site.bet_tracker.no_event_text.text}"'
                             f'is not same as expected "{vec.retail.OPEN_IN_SHOP_NO_BETS_TEXT}"')
