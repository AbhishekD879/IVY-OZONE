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
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893104_Verify_the_generate_bar_code_button_is_active_when_we_click_on_any_selection(Common, ComponentBase):
    """
    TR_ID: C64893104
    NAME: Verify the  generate bar code button is active when we click on any selection.
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

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_digital_coupons_from_the_grid_hub_menu_items4randomly_select_few_selections_from_all_coupon_typesexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_digital_coupons_and__open_digital_coupons_page4user_should_see_that_generate_bar_code_button_will_be_in_active_state_(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on digital coupons from the Grid hub menu items.
        DESCRIPTION: 4.Randomly select few selections from all coupon types
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on digital coupons and  open digital coupons page.
        DESCRIPTION: 4.User should see that generate bar code button will be in active state .
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on digital coupons and  open digital coupons page.
        EXPECTED: 4.User should see that generate bar code button will be in active state .
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
            generate_bet_code = self.site.in_shop_coupons.tab_content.generate_bet_frame.is_generate_bet_code_active
            self.assertFalse(generate_bet_code, msg='"Generate Bet Code" button is in active state when no selections are added')
            self.choose_selection()
            generate_bet_code = self.site.in_shop_coupons.tab_content.generate_bet_frame.is_generate_bet_code_active
            self.assertTrue(generate_bet_code, msg='"Generate Bet Code" button is not active after adding selections')
