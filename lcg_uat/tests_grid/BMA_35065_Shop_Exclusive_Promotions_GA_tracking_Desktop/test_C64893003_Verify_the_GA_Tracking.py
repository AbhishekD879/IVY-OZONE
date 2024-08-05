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
class Test_C64887505_Verify_the_GA_Tracking(BaseDataLayerTest):
    """
    TR_ID: C64887505
    NAME: Verify the "GA Tracking"
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_url2click_on_grid_tab3click_on_shop_exclusive_promos_from_the_list4type_in_console_datalayer_tap_enter_and_check_the_responseexpected_result1sports_url_should_be_launched_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_shop_exclusive_promos_and_promotions_page_is_accessed_successfully4the_next_push_is_sent_to_gadatalayerpushevent__trackeventeventcategory__quick_betevent_action__place_betevent_label__successodds_boost__yes(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on "Shop Exclusive Promos" from the list.
        DESCRIPTION: 4.Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: 1.Sports URL should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is accessed successfully.
        EXPECTED: 4.The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Grid',
        EXPECTED: 'event Action' : 'Menu',
        EXPECTED: 'event Label' : 'Grid Exclusive Promos'
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()).click()
        self.site.wait_content_state(state_name='promotions', timeout=30)
        actual_response = self.get_data_layer_specific_object(object_key='eventAction', object_value='Menu')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'Grid',
                             'eventAction': 'Menu',
                             'eventLabel': 'Grid Exclusive Promos'}
        self.compare_json_response(actual_response, expected_response)
