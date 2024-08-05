import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893106_Verify_the_coupons_tab_is_displayed_on_the_grid_hub_menu_items(Common):
    """
    TR_ID: C64893106
    NAME: Verify the ' coupons' tab is displayed on the grid hub menu items
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online users.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_headerexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header_and_user_should_see_coupons_tab_on_grid_hub_menu_items(self):
        """
        DESCRIPTION: 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header and user should see coupons tab on grid hub menu items
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header and user should see coupons tab on grid hub menu items
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
