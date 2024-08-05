import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared.components.base import ComponentBase


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893117_Verify_three_selections_cant_be_selected_simultaneously_in_the_same_row_at_a_timehome_draw_away(Common, ComponentBase):
    """
    TR_ID: C64893117
    NAME: Verify three selections cant be selected simultaneously in the same row at a time(home, draw, away)
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online users.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_digital_coupons_from_the_grid_hub_menu_items4try_to_select_three_selections_from_same_row_like_homedrawawayexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_digital_coupons_and__open_digital_coupons_page4it_will_not_support_to_select_homedrawaway_from_single_row(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on digital coupons from the Grid hub menu items.
        DESCRIPTION: 4.Try to select three selections from same row like (home,draw,away)
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on digital coupons and  open digital coupons page.
        DESCRIPTION: 4.It will not support to select home,draw,away from single row.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on digital coupons and  open digital coupons page.
        EXPECTED: 4.It will not support to select home,draw,away from single row.
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
        in_shop_coupons.click()
        self.site.wait_content_state(state_name='InShopCoupons')
        sections = self.site.in_shop_coupons.tab_content.accordions_list.items_as_ordered_dict
        section = list(sections.values())[0]
        events = section.items_as_ordered_dict
        event = list(events.values())[0]
        selections = event.selections
        self.scroll_to_we(selections[0])
        selections[0].click()
        self.assertIn("selected", selections[0].get_attribute("class"), msg="selection is not selected")
        selections[1].click()
        self.assertIn("selected", selections[1].get_attribute("class"), msg="selection is not selected")
        self.assertNotIn("selected", selections[0].get_attribute("class"), msg="selection is selected")
