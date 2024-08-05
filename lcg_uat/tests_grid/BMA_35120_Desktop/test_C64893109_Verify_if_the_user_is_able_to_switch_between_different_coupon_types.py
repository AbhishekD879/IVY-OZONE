import pytest
import random
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893109_Verify_if_the_user_is_able_to_switch_between_different_coupon_types(Common):
    """
    TR_ID: C64893109
    NAME: Verify if the user is able to switch between different coupon types
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online users.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_digital_coupons_from_the_grid_hub_menu_items4switch_between_one_coupon_type_to_another_coupon_typeexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_see_different_digital_coupons_like_midweekweekendacca_insurance_etc4user_should_be_able_to_switch_between_different_coupon_types(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on digital coupons from the Grid hub menu items.
        DESCRIPTION: 4.switch between one coupon type to another coupon type
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should see different digital coupons like midweek,weekend,acca insurance etc.,
        DESCRIPTION: 4.user should be able to switch between different coupon types.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should see different digital coupons like midweek,weekend,acca insurance etc.,
        EXPECTED: 4.user should be able to switch between different coupon types.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.open_sport(name=vec.retail.TITLE)
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.login()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        in_shop_coupons = grid_items.get(vec.retail.IN_SHOP_COUPONS)
        self.assertTrue(in_shop_coupons.is_enabled(), msg="Digital(In-Shop) coupons is not clickable")
        in_shop_coupons.click()
        self.site.wait_content_state(state_name='InShopCoupons')
        in_shop_coupons = self.site.in_shop_coupons.coupons_tabs_menu
        current_tab = in_shop_coupons.current
        in_shop_coupons_tabs = in_shop_coupons.items_as_ordered_dict
        del in_shop_coupons_tabs[current_tab]
        try:
            tab = random.choice(list(in_shop_coupons_tabs.keys()))
            in_shop_coupons.items_as_ordered_dict[tab].click()
        except IndexError:
            self._logger.info("**** More than one coupon tabs are not found")
        self.site.wait_content_state_changed(timeout=5)
        in_shop_coupons.items_as_ordered_dict[current_tab].click()
        self.site.wait_content_state_changed(timeout=5)
