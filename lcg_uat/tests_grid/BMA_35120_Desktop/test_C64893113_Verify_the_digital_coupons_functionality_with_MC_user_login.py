import pytest
import tests
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
class Test_C64893113_Verify_the_digital_coupons_functionality_with_MC_user_login(Common):
    """
    TR_ID: C64893113
    NAME: Verify the digital coupons functionality with MC user login.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid MC users.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3login_with_valid_user4click_on_digital_coupons_from_the_grid_hub_menu_itemsexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_login__with_valid_user4user_should_be_able_to_click_on_digital_coupons_and__open_digital_coupons_page(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Login with valid user.
        DESCRIPTION: 4.Click on digital coupons from the Grid hub menu items.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should login  with valid user.
        DESCRIPTION: 4.User should be able to click on digital coupons and  open digital coupons page.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should login  with valid user.
        EXPECTED: 4.User should be able to click on digital coupons and  open digital coupons page.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.open_sport(name=vec.retail.TITLE)
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.login(username=tests.settings.mc_user)
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        in_shop_coupons = grid_items.get(vec.retail.IN_SHOP_COUPONS)
        self.assertTrue(in_shop_coupons.is_enabled(), msg="Digital(In-Shop) coupons is not clickable")
        in_shop_coupons.click()
        self.site.wait_content_state(state_name='InShopCoupons')
