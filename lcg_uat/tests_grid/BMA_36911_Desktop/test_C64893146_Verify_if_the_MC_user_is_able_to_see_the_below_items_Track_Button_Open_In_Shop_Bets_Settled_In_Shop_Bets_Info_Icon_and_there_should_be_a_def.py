import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893146_Verify_if_the_MC_user_is_able_to_see_the_below_items_Track_Button_Open_In_Shop_Bets_Settled_In_Shop_Bets_Info_Icon_and_there_should_be_a_default_message_that_You_currently_have_no_open_In_Shop_betsafter_navigating_to_Shop_Bet_Tracker_page(Common):
    """
    TR_ID: C64893146
    NAME: Verify if the MC user is able to see the below items (Track Button, Open In Shop Bets, Settled In Shop Bets, Info Icon and there should be a default message that You currently have no open In-Shop bets)after navigating to "Shop Bet Tracker" page.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports web
    PRECONDITIONS: application URL.
    PRECONDITIONS: 2.User should have valid MC user credentials.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application2click_on_login_button_and_enter_valid_user_details3click_on_grid_tab_from_main_header4click_on_shop_bet_tracker_from_the_grid_hubexpected_result1sports_application_should_be_launched_successfully2user_should_be_logged_in3user_should_be_able_to_open_grid_tab_from_main_header4user_should_be_navigated_to_shop_bet_tracker_page5user_should_be_able_to_see_all_the_below_items__track_button_open_in_shop_bets_settled_in_shop_bets_info_icon_and_there_should_be_a_default_message_that_you_currently_have_no_open_in_shop_bets(
            self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application.
        DESCRIPTION: 2.Click on login button and enter valid user details.
        DESCRIPTION: 3.Click on grid tab from main header.
        DESCRIPTION: 4.Click on "Shop Bet Tracker" from the grid hub.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be logged in.
        DESCRIPTION: 3.User should be able to open grid tab from main header.
        DESCRIPTION: 4.User should be navigated to "Shop Bet Tracker" page.
        DESCRIPTION: 5.User should be able to see all the below items:-
        DESCRIPTION: ->Track Button,
        DESCRIPTION: ->Open In Shop Bets,
        DESCRIPTION: ->Settled In Shop Bets,
        DESCRIPTION: ->Info Icon and
        DESCRIPTION: ->There should be a default message that You currently have no open In-Shop bets
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be logged in.
        EXPECTED: 3.User should be able to open grid tab from main header.
        EXPECTED: 4.User should be navigated to "Shop Bet Tracker" page.
        EXPECTED: 5.User should be able to see all the below items:-
        EXPECTED: ->Track Button,
        EXPECTED: ->Open In Shop Bets,
        EXPECTED: ->Settled In Shop Bets,
        EXPECTED: ->Info Icon and
        EXPECTED: ->There should be a default message that You currently have no open In-Shop bets
        """
        self.site.login(username=tests.settings.mc_user)
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
        self.assertTrue(self.site.bet_tracker.track_button.is_displayed(),
                        msg='betracker track button is not displayed')
        self.assertTrue(self.site.bet_tracker.bet_tracker_info_icon.is_displayed(),
                        msg='betracker info icon is not displayed')
        wait_for_result(lambda: self.site.bet_tracker.cash_out_block.open_in_shop_bet_tab.is_displayed(),
                        timeout=30, name='Open In-shop Bets to be displayed.')
        self.assertTrue(self.site.bet_tracker.cash_out_block.settle_in_shop_bet_tab.is_displayed(),
                        msg='"Settled In Shop Bets" tab not displayed')
        self.assertEqual(self.site.bet_tracker.no_event_text.text, vec.retail.OPEN_IN_SHOP_NO_BETS_TEXT,
                         msg=f'Actual message {self.site.bet_tracker.no_event_text.text}'
                             f'is not same as expected {vec.retail.OPEN_IN_SHOP_NO_BETS_TEXT}')
