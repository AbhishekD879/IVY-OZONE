import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893057_Verify_GA_Tracking_if_the_right_parameters_have_been_added_for_the_below1Saved_Filters(BaseDataLayerTest):
    """
    TR_ID: C64893057
    NAME: Verify GA Tracking if the right parameters have been added for the below
    1.Saved Filters
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_menu_items4type_in_console_data_layer_tap_enter_and_check_the_responseexpected_result1sports_url_should_be_launched_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter4the_next_push_is_sent_to_gadatalayerpushevent__trackeventeventcategory__shop_bet_trackereventaction___saved_filters(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on "football bet filter" from the menu items.
        DESCRIPTION: 4.Select few selections and then click on save filter.
        DESCRIPTION: 5.Type in console 'data Layer', tap 'Enter' and check the response
        EXPECTED: 1.Sports URL should be launched .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on "football bet filter".
        EXPECTED: 4.User should be able to Select few selections and able to click on save filter.
        EXPECTED: 5.The next push is sent to GA:
        EXPECTED: dataLayer.push(
        EXPECTED: {
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'football filter',
        EXPECTED: 'eventAction' : ' Saved Filters',
        EXPECTED: }
        EXPECTED: );
        """
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.grid.menu_items.items_as_ordered_dict.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        bet_online = your_betting_options.get(vec.retail.EXPECTED_YOUR_BETTING.bet_online)
        bet_online.radio_button.click()
        your_betting_popup.go_betting_button.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        sections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        for section in sections.values():
            filters = section.items_as_ordered_dict
            for filter in filters.values():
                filter.click()
                break
        self.site.football_bet_filter.save_filters_button.click()
        result = self.site.football_bet_filter.has_save_filter_popup
        self.assertTrue(result, msg='save filter popup not appeared')
        save_filter_popup = self.site.football_bet_filter.save_filter_popup
        save_filter_popup.enter_name(value='test')
        save_filter_popup.save_button.click()
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='save filters')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'football filter',
                             'eventAction': 'save filters',
                             'eventLabel': '', 'userAction': '',
                             'betFilterStep': 'Create Your Coupon',
                             'couponSelection': '||',
                             'teamSelection': '',
                             'oppositionSelection': ''}
        self.compare_json_response(actual_response, expected_response)
