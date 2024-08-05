import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893017_Verify_user_is_able_to_See_FCB_opening_pop_up_everytime_he_clicks_on_Football_bet_filter(Common):
    """
    TR_ID: C64893017
    NAME: Verify user is able to See FCB opening pop up everytime he clicks on Football bet filter
    PRECONDITIONS: 1.User should have valid ladbrokes sports URL/App URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_urlapp2_click_on_grid_tab_from_sports_main_header3click_on_football_bet_filter__from_the_grid_main_menu_and_click_on_bet_online_from_that_popup4_select_all_the_required_filters_from_the_three_tabs5_click_on_find_bets_button6come_back_to_grid_homepage_and_click_on_foot_bet_filter_and_verify_user_is_able_to_see_the_fcb_pop_up_againexpected_resultuser_should_be_able_to_see_the_fcb_pop_up_whenever_he_clicks_on_fcb_pop_up_any_number_of_times(self):
        """
        DESCRIPTION: 1. 1. Launch ladbrokes sports URL/App.
        DESCRIPTION: 2. Click on grid tab from sports main header
        DESCRIPTION: 3.Click on Football bet filter  from the grid main menu and click on bet online from that popup.
        DESCRIPTION: 4. Select all the required filters from the three tabs.
        DESCRIPTION: 5. Click on "find bets" button.
        DESCRIPTION: 6.come back to grid homepage and click on foot bet filter and verify user is able to see the FCB pop up again
        EXPECTED: 1. User should be able to see the FCB pop up whenever he clicks on FCB pop up any number of times
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        wait_for_result(lambda: self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('LEAGUES') is not None,
                        timeout=20)
        section = self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('LEAGUES')
        league = list(section.items_as_ordered_dict.values())[0]
        league.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
        self.site.football_bet_filter.find_bets_button.click()
        self.device.go_back()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.device.go_back()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
