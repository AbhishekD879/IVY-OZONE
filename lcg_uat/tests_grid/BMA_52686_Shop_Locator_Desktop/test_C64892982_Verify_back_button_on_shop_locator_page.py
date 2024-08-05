import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64892982_Verify_back_button_on_shop_locator_page(Common):
    """
    TR_ID: C64892982
    NAME: Verify back button(<) on shop locator page.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports2click_on_grid_tab3click_on_shop_locator_from_the_list4click_on_back_button_on_top_left_corner_from_shop_locator_pageexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_shop_locator_and_successfully_open_shop_locator_page4user_should_go_back_successfully_to_the_gird_menu(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on shop locator from the list.
        DESCRIPTION: 4.Click on back button on top left corner from shop locator page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on shop locator and successfully open shop locator page.
        DESCRIPTION: 4.User should go back successfully to the gird menu.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on shop locator and successfully open shop locator page.
        EXPECTED: 4.User should go back successfully to the gird menu.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.EXPECTED_GRID_ITEMS.shop_locator.title()).click()
        self.site.wait_content_state(state_name='ShopLocator', timeout=60)
        actual_title = self.site.shop_locator.page_title.text
        self.assertEqual(actual_title, vec.retail.EXPECTED_GRID_ITEMS.shop_locator.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.retail.EXPECTED_GRID_ITEMS.shop_locator.title()}"')
        if self.device_type == 'mobile':
            self.assertTrue(self.site.header.back_button.is_displayed(),
                            msg=f'"Back button" is not displayed on shoplocator page.', )
            self.site.header.back_button.click()
        else:
            self.assertTrue(self.site.shop_locator.back_button.is_displayed(),
                            msg=f'"Back button" is not displayed on shoplocator page.', )
            self.site.shop_locator.back_button.click()
        self.site.wait_content_state(state_name='thegrid')
