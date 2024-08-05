import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893171_Verify_the_Track_CTA_button_has_been_added_for_GA_tracking_with_right_parameters(BaseDataLayerTest):
    """
    TR_ID: C64893171
    NAME: Verify the "Track" CTA button has been added for GA tracking with right parameters
    PRECONDITIONS: 1.User should have valid Ladbrokes sports web
    PRECONDITIONS: application URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application2click_on_grid_tab_from_main_header3click_on_shop_bet_tracker_from_the_grid_hub4click_on_track_cta_after_entering_the_bet_numberexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_navigated_to_shop_bet_tracker_page4user_should_be_able_to_enter_the_bet_number_and_click_on_track_button5the_next_push_is_sent_to_gadatalayerpush_event__trackeventeventcategory__shop_bet_trackereventaction__scan_your_bet_receipt__track_(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on "Shop Bet Tracker" from the grid hub.
        DESCRIPTION: 4.Click on "Track" CTA after entering the bet number.
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be navigated to "Shop Bet Tracker" page.
        DESCRIPTION: 4.User should be able to enter the bet number and click on Track button.
        DESCRIPTION: 5.The next push is sent to GA:
        DESCRIPTION: dataLayer.push(
        DESCRIPTION: { 'event' : 'trackEvent',
        DESCRIPTION: 'eventCategory' : 'Shop Bet Tracker',
        DESCRIPTION: 'eventAction' : 'Scan your Bet Receipt / Track' }
        DESCRIPTION: );
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be navigated to "Shop Bet Tracker" page.
        EXPECTED: 4.User should be able to enter the bet number and click on Track button.
        EXPECTED: 5.The next push is sent to GA:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Shop Bet Tracker',
        EXPECTED: 'eventAction' : 'Scan your Bet Receipt / Track' }
        EXPECTED: );
        """
        self.site.wait_content_state('Homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items[vec.retail.BET_TRACKER].click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        actual_title = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_title, vec.retail.BET_TRACKER.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.retail.BET_TRACKER.title()}"')
        self.site.bet_tracker.coupon_input = 81030000003247
        self.site.bet_tracker.track_button.click()
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'Bet tracker',
                             'eventAction': 'Track',
                             }
        actual_response = self.get_data_layer_specific_object(object_key='eventAction',
                                                              object_value='Track')
        self.compare_json_response(actual_response, expected_response)
