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
class Test_C64893000_Verify_if_the_user_is_navigated_back_to_the_grid_home_page_from_promotions_page_after_clicking_on_back_button_(Common):
    """
    TR_ID: C64893000
    NAME: Verify if the user is navigated back to the grid home page from promotions page after clicking on back button(<).
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def verify_grid_page(self):
        """"
        To verify grid page
        """

        self.site.wait_content_state(state_name='thegrid')
        self.__class__.grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(self.grid_items, msg='"Grid" page items not loaded')

    def test_001_1_1launch_ladbrokes_sports_url2click_on_grid_tab3click_on_shop_exclusive_promos_from_the_list4click_on_back_button_expected_result1sports_url_should_be_launch_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_shop_exclusive_promos_and_promotions_page_is_opened_successfully4user_should_be_able_to_click_on_back_button__and_user_must_be_navigated_back_to_the_grid_home_page(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on "Shop Exclusive Promos" from the list.
        DESCRIPTION: 4.Click on back button(<) .
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports URL should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        DESCRIPTION: 4.User should be able to click on back button(<)  and user must be navigated back to the grid home page.
        EXPECTED: 1. 1.Sports URL should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        EXPECTED: 4.User should be able to click on back button(<)  and user must be navigated back to the grid home page.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.verify_grid_page()
        result = wait_for_result(lambda: self.grid_items.get(vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()).is_displayed(), timeout=15)
        self.assertTrue(result, msg=f'"{vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()} is not displayed on UI"')
        self.grid_items.get(vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()).click()
        self.site.wait_content_state(state_name='Promotions', timeout=30)
        self.site.back_button.click()
        self.verify_grid_page()
