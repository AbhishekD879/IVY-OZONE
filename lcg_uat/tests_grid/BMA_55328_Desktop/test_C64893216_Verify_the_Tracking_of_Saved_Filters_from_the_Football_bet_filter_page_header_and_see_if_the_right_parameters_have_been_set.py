import random
import string
import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893216_Verify_the_Tracking_of_Saved_Filters_from_the_Football_bet_filter_page_header_and_see_if_the_right_parameters_have_been_set(BaseDataLayerTest):
    """
    TR_ID: C64893216
    NAME: Verify  the Tracking of "Saved Filters" from the "Football bet filter" page header and see if the right parameters have been set
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid ladbrokes sports web app.
    PRECONDITIONS: 2.User should have valid Online User Credentials.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_app2click_on_login_button_and_enter_valid_user_details3click_on_grid_tab_from_main_header4click_on_football_bet_filter_from_the_grid_hub5select_bet_online_and_click_on_go_betting_button6click_on_saved_filters_button_from_headerexpected_result1sports_application_should_be_launch_successfully2user_should_be_logged_in_secessfully3user_should_be_able_to_open_grid_tab_from_main_header4user_should_be_able_to_click_on_football_bet_filter_successfully_and_a_popup_is_shown_with1bet_in_shop_and_2bet_online_radio_buttons5user_should_be_navigated_to_football_bet_filter_page6user_should_be_navigated_to_the_saved_filters_page7the_next_push_is_sent_to_gadatalayerpushevent__trackeventeventcategory__football_filtereventaction___apply_filter(self):
        """
        DESCRIPTION: 1. 1.Launch ladbrokes sports web app.
        DESCRIPTION: 2.Click on login button and enter valid user details.
        DESCRIPTION: 3.Click on grid tab from main header.
        DESCRIPTION: 4.Click on "Football Bet Filter" from the grid hub.
        DESCRIPTION: 5.Select "Bet Online" and click on "Go Betting" button.
        DESCRIPTION: 6.Click on "SAVED FILTERS" button from header.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be logged in secessfully.
        DESCRIPTION: 3.User should be able to open grid tab from main header.
        DESCRIPTION: 4.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        DESCRIPTION: (1).Bet In Shop and (2).Bet Online Radio buttons.
        DESCRIPTION: 5.User should be navigated to "Football Bet Filter" page.
        DESCRIPTION: 6.User should be navigated to the "SAVED FILTERS" page.
        DESCRIPTION: 7.The next push is sent to GA:
        DESCRIPTION: dataLayer.push(
        DESCRIPTION: {
        DESCRIPTION: 'event' : 'trackEvent',
        DESCRIPTION: 'eventCategory' : 'football filter',
        DESCRIPTION: 'eventAction' : ' save filters',
        DESCRIPTION: }
        DESCRIPTION: );
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be logged in secessfully.
        EXPECTED: 3.User should be able to open grid tab from main header.
        EXPECTED: 4.User should be able to click on "Football Bet Filter" successfully and a popup is shown with
        EXPECTED: (1).Bet In Shop and (2).Bet Online Radio buttons.
        EXPECTED: 5.User should be navigated to "Football Bet Filter" page.
        EXPECTED: 6.User should be navigated to the "SAVED FILTERS" page.
        EXPECTED: 7.The next push is sent to GA:
        EXPECTED: dataLayer.push(
        EXPECTED: {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'football filter',
        EXPECTED: 'eventAction' : ' save filters',
        EXPECTED: }
        EXPECTED: );
        """
        self.site.wait_content_state(state_name="Homepage")
        self.site.login()
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
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options,
                      msg=f'{vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop} not in {your_betting_options}')
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options,
                      msg=f'{vec.retail.EXPECTED_YOUR_BETTING.bet_online} not in {your_betting_options}')
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        self.assertFalse(
            self.site.football_bet_filter.find_bets_button.has_spinner_icon(expected_result=False, timeout=25),
            msg='Spinner has not disappeared from Find Bets button')
        self.site.contents.scroll_to_bottom()
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.scroll_to_top()
        content = self.site.football_bet_filter.tab_content.items_as_ordered_dict.get('LEAGUES')
        self.assertTrue(content, msg='"Leagues" not found')
        leagues = list(content.items_as_ordered_dict.items())
        for league_name, league in leagues[:2]:
            league.click()
            self.assertTrue(league.is_selected(),
                            msg=f' Filter "{league_name}" is not selected')
        self.assertTrue(self.site.football_bet_filter.save_filters_button.is_enabled(expected_result=True),
                        msg='save filters button not enabled')
        self.site.football_bet_filter.save_filters_button.click()
        self.assertTrue(self.site.football_bet_filter.save_filter_popup,
                        msg='"Save filter popup" is not displayed')
        expected_value = 25
        name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=expected_value))
        self.site.football_bet_filter.save_filter_popup.enter_name(value=name)
        self.site.football_bet_filter.save_filter_popup.save_button.click()
        self.site.football_bet_filter.tab_menu.items_as_ordered_dict.get(vec.retail.SAVED_FILTERS_TAB).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='save filters')
        expected_response = {'event': 'trackEvent', 'eventCategory': 'football filter', 'eventAction': 'save filters', 'eventLabel': '', 'userAction': '', 'betFilterStep': 'Create Your Coupon', 'couponSelection': '|', 'teamSelection': '', 'oppositionSelection': ''}
        self.compare_json_response(actual_response, expected_response)
