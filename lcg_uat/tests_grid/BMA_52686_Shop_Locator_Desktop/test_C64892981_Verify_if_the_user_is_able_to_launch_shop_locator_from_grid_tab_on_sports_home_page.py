import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64892981_Verify_if_the_user_is_able_to_launch_shop_locator_from_grid_tab_on_sports_home_page(Common):
    """
    TR_ID: C64892981
    NAME: Verify if the user is able to launch shop locator from grid tab on sports home page.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports2click_on_grid_tab3click_on_shop_locator_from_the_listexpected_result1sports_application_should_be_launch_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_shop_locator_and_successfully_open_shop_locator_page(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on shop locator from the list.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on shop locator and successfully open shop locator page.
        EXPECTED: 1. 1.Sports application should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on shop locator and successfully open shop locator page.
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
        self.site.wait_content_state(state_name='ShopLocator', timeout=30)
        actual_title = self.site.shop_locator.page_title.text
        self.assertEqual(actual_title, vec.retail.EXPECTED_GRID_ITEMS.shop_locator.title(),
                         msg=f'Actual Title: "{actual_title}" is not Expected as: "{vec.retail.EXPECTED_GRID_ITEMS.shop_locator.title()}"')
