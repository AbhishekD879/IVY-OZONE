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
class Test_C64893125_Verify_the_font_sizes_and_font_types_of_all_the_content_present_through_the_coupon_buddy_pages_from_this_following_zeppelin_linkDesign_https_zplio_boQmKpE(Common):
    """
    TR_ID: C64893125
    NAME: Verify the font sizes and font types of all the content present through the coupon buddy pages from this following zeppelin link Design : https://zpl.io/boQmKpE
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online users.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_digital_coupons_from_the_grid_hub_menu_items4verify_the_font_size_and_font_type_for_all_the_text_present_in_the_ui_screenexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_digital_coupons_and__open_digital_coupons_page4it_should_be_same_as_zeppelin_screens(
            self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on digital coupons from the Grid hub menu items.
        DESCRIPTION: 4.Verify the font size and font type for all the text present in the UI screen.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on digital coupons and  open digital coupons page.
        DESCRIPTION: 4.It should be same as zeppelin screens.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on digital coupons and  open digital coupons page.
        EXPECTED: 4.It should be same as zeppelin screens.
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
        header_font_size = self.site.in_shop_coupons.title_styles.css_property_value('font-size')
        self.assertEqual(header_font_size, '14px',
                         msg=f'In Shop Coupon font size is not equal to Zepplin Font Size 14px'
                             f'actual result "{header_font_size}"')
        header_font_type = self.site.in_shop_coupons.title_styles.css_property_value('font-family')
        self.assertIn('Helvetica Neue', header_font_type,
                      msg=f'In Shop Coupon font family is not equal to Zepplin Font Family'
                          f' actual result "{header_font_type}"')
        tab_font_size = self.site.in_shop_coupons.coupons_tabs_menu.tab_styles.css_property_value('font-size')
        self.assertEqual(tab_font_size, '12px',
                         msg=f'In Shop Coupon tab menu font size is not equal to Zepplin Font Size 14px'
                             f'actual result "{tab_font_size}"')
        tab_font_type = self.site.in_shop_coupons.coupons_tabs_menu.tab_styles.css_property_value('font-family')
        self.assertIn('Roboto Condensed', tab_font_type,
                      msg=f'In Shop Coupon tab menu font type is not equal to Zepplin Font family'
                          f'actual result "{tab_font_type}"')
        team_font_size = self.site.in_shop_coupons.tab_content.team_styles.css_property_value('font-size')
        self.assertEqual(team_font_size, '13px',
                         msg=f'In Shop Coupon team font size is not equal to Zepplin Font Size 13px'
                             f'actual result "{team_font_size}"')
        team_font_type = self.site.in_shop_coupons.tab_content.team_styles.css_property_value('font-family')
        self.assertIn('Helvetica Neue', team_font_type,
                      msg=f'In Shop Coupon font family is not equal to Zepplin Font Family'
                          f' actual result "{team_font_type}"')
