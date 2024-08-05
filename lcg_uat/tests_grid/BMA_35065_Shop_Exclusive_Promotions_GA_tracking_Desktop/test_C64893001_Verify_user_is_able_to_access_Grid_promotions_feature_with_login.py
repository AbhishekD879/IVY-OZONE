import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893001_Verify_user_is_able_to_access_Grid_promotions_feature_with_login(Common):
    """
    TR_ID: C64893001
    NAME: Verify user is able to access "Grid promotions" feature  with login.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid username and password for login.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_url2click_on_grid_tab3click_on_login_button4click_on_shop_exclusive_promos_from_the_listexpected_result1sports_url_should_be_launched_successfully2user_should_be_able_to_open_grid_tab3user_should_be_logged_in_successfully4user_should_be_able_to_click_on_shop_exclusive_promos_and_promotions_page_is_accessed_successfully(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on login button.
        DESCRIPTION: 4.Click on "Shop Exclusive Promos" from the list.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports URL should be launched successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be logged in successfully.
        DESCRIPTION: 4.User should be able to click on "Shop Exclusive Promos" and promotions page is accessed successfully.
        EXPECTED: 1. 1.Sports URL should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be logged in successfully.
        EXPECTED: 4.User should be able to click on "Shop Exclusive Promos" and promotions page is accessed successfully.
        """
        self.site.login()
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        result = wait_for_result(
            lambda: grid_items.get(vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()).is_displayed(),
            timeout=15)
        self.assertTrue(result,
                        msg=f'"{vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()} is not displayed on UI"')
        grid_items.get(vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()).click()
        self.site.wait_content_state(state_name='Promotions', timeout=30)
