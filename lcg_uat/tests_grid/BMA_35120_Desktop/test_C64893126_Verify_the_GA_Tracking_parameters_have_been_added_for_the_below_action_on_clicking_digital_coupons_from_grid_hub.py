import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
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
class Test_C64893126_Verify_the_GA_Tracking_parameters_have_been_added_for_the_below_action_on_clicking_digital_coupons_from_grid_hub(BaseDataLayerTest):
    """
    TR_ID: C64893126
    NAME: Verify the GA Tracking parameters have been added for the below action. "on clicking digital coupons from grid hub".
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online users.
    """
    keep_browser_open = True
    expected_response = {'event': 'trackEvent',
                         'eventAction': 'Menu',
                         'eventCategory': 'Grid',
                         'eventLabel': 'In-Shop Coupons'
                         }

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials_url2click_on_grid_tab_from_main_header3click_on_coupons_from_the_menu_items4type_in_console_data_layer_tap_enter_and_check_the_responseexpected_result1sports_url_should_be_launched_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_coupons4the_next_push_is_sent_to_gadatalayerpushevent__trackeventeventcategory__digital_couponeventaction__coupons(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials URL.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on "Coupons" from the menu items.
        DESCRIPTION: 4.Type in console 'data Layer', tap 'Enter' and check the response
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports URL should be launched .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on "Coupons".
        DESCRIPTION: 4.The next push is sent to GA:
        DESCRIPTION: dataLayer.push({
        DESCRIPTION: 'event' : 'trackEvent',
        DESCRIPTION: 'eventCategory' : 'digital coupon',
        DESCRIPTION: 'eventAction' : 'coupons'
        DESCRIPTION: });
        EXPECTED: 1. 1.Sports URL should be launched .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on "Coupons".
        EXPECTED: 4.The next push is sent to GA:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'digital coupon',
        EXPECTED: 'eventAction' : 'coupons'
        EXPECTED: });
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
        self.assertIn(vec.retail.IN_SHOP_COUPONS, grid_items.keys(),
                      msg=f'Expected item "{vec.retail.IN_SHOP_COUPONS}" is not present in Actual items "{grid_items.keys()}"')
        in_shop_coupons = grid_items.get(vec.retail.IN_SHOP_COUPONS)
        self.assertTrue(in_shop_coupons.is_enabled(), msg="Digital(In-Shop) coupons is not clickable")
        in_shop_coupons.click()
        self.site.wait_content_state(state_name='InShopCoupons')
        wait_for_result(lambda: self.site.in_shop_coupons.title.is_displayed(),
                        name='In-Shop coupons header is not loaded',
                        timeout=20)
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='In-Shop Coupons')
        self.compare_json_response(actual_response, self.expected_response)
