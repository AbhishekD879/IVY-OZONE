import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64892992_Verify_GA_Tracking_parameters_for_shop_locator(BaseDataLayerTest):
    """
    TR_ID: C64892992
    NAME: Verify GA Tracking parameters for shop locator
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True
    expected_response = {'event': 'trackEvent',
                         'eventAction': 'Menu',
                         'eventCategory': 'Grid',
                         'eventLabel': 'Shop Locator'
                         }

    def test_001_1_1launch_ladbrokes_sports2click_on_grid_tab3click_on_shop_locator_from_the_list4type_in_console_datalayer_tap_enter_and_check_the_responseexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_access_everything_in_shop_locator_page4the_next_push_is_sent_to_gadatalayerpushevent__trackeventeventcategory__quickbeteventaction__place_beteventlabel__successoddsboost__yes(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on shop locator from the list.
        DESCRIPTION: 4.Type in console 'dataLayer', tap 'Enter' and check the response
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to access everything in shop locator page.
        DESCRIPTION: 4.The next push is sent to GA:
        DESCRIPTION: dataLayer.push({
        DESCRIPTION: 'event': 'trackEvent',
        DESCRIPTION: 'eventAction': 'Menu',
        DESCRIPTION: 'eventCategory': 'Grid',
        DESCRIPTION: 'eventLabel': 'Shop Locator'
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to access everything in shop locator page.
        EXPECTED: 4.The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: 'eventAction': 'Menu',
        EXPECTED: 'eventCategory': 'Grid',,
        EXPECTED: 'eventLabel': 'Shop Locator'
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.EXPECTED_GRID_ITEMS.shop_locator.title()).click()
        self.site.wait_content_state(state_name='ShopLocator', timeout=30)

        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Shop Locator')
        self.compare_json_response(actual_response, self.expected_response)
