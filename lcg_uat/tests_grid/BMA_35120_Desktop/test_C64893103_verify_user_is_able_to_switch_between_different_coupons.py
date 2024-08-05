import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.pages.shared.components.base import ComponentBase


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893103_verify_user_is_able_to_switch_between_different_coupons(Common, ComponentBase):
    """
    TR_ID: C64893103
    NAME: verify user is able to switch between different coupons
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online users.
    """
    keep_browser_open = True

    def choose_selection(self):
        sections = self.site.in_shop_coupons.tab_content.accordions_list.items_as_ordered_dict
        section = list(sections.values())[0]
        events = section.items_as_ordered_dict
        event = list(events.values())[0]
        selections = event.selections
        self.scroll_to_we(selections[0])
        selections[0].click()

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_digital_coupons_from_the_grid_hub_menu_items4select_at_least_one_selection_from_each_coupons_and_switch_from_one_coupon_to_anotherexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_digital_coupons_and__open_digital_coupons_page4user_should_be_able_to_navigate_easily_and_able_to_select_any_selections_from_all_the_available_pages(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on digital coupons from the Grid hub menu items.
        DESCRIPTION: 4.Select at least one selection from each coupons and switch from one coupon to another.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on digital coupons and  open digital coupons page.
        DESCRIPTION: 4.User should be able to navigate easily and able to select any selections from all the available pages.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on digital coupons and  open digital coupons page.
        EXPECTED: 4.User should be able to navigate easily and able to select any selections from all the available pages.
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
        tabs = self.site.in_shop_coupons.coupons_tabs_menu.items_as_ordered_dict
        for tab_name, tab in tabs.items():
            tab.click()
            self.choose_selection()