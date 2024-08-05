import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from tests.pack_013_Retail_Connect_Features.Football_Bet_Filter.BaseFootballBetFilter import BaseFootballBetFilter


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893030_Verify_the_find_bet_button_is_active_after_selecting_required_filters(BaseCouponsTest, BaseFootballBetFilter):
    """
    TR_ID: C64893030
    NAME: Verify the find bet button is active after selecting required filters.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4click_on_bet_online_from_the_fcb_opening_pop_up5select_all_the_required_filtersexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter_and_successfully_open_football_bet_filter_page4user_should_be_landed_on_football_bet_filter_page_by_clicking_go_betting_page5user_should_be_able_to_select_all_required_filter_and_find_bet_button_should_be_in_active_state_successfullythere_should_be_some_selections_on_find_bet_button(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 4.Click on bet online from the FCB opening pop up.
        DESCRIPTION: 5.Select all the required filters.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        DESCRIPTION: 4.User should be landed on football bet filter page by clicking go betting page.
        DESCRIPTION: 5.User should be able to select all required filter and find bet button should be in active state successfully("There should be some selections on find bet button")
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter and successfully open football bet filter page.
        EXPECTED: 4.User should be landed on football bet filter page by clicking go betting page.
        EXPECTED: 5.User should be able to select all required filter and find bet button should be in active state successfully("There should be some selections on find bet button")
        """
        self.site.login(tests.settings.betplacement_user)
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        bet_filter = 'Football Bet Filter'
        grid_items[bet_filter].click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options)
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options)
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.assertFalse(
            self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=15),
            msg='Spinner has not disappeared from Find Bets button')
        self.site.contents.scroll_to_bottom()
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.scroll_to_top()
        leagues = list(self.site.football_bet_filter.tab_content.items_as_ordered_dict.values())[1]
        league = list(leagues.items_as_ordered_dict.values())[0]
        league.click()
        self.assertTrue(self.site.football_bet_filter.find_bets_button.is_enabled(timeout=2),
                        msg='Find Bets button is disabled')
