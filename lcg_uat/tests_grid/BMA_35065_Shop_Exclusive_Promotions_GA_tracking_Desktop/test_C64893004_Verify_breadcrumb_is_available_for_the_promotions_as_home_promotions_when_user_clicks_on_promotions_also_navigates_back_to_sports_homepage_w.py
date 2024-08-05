import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893004_Verify_breadcrumb_is_available_for_the_promotions_as_home_promotions_when_user_clicks_on_promotions_also_navigates_back_to_sports_homepage_when_he_clicks_on_home(Common):
    """
    TR_ID: C64893004
    NAME: Verify breadcrumb is available for the promotions as 'home->promotions' when user clicks on promotions , also navigates back to sports homepage when he clicks on home
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    EXPECTED_PROMOTION_BREADCRUMS = ['Home', 'promotions']

    def test_001_1_1launch_ladbrokes_sports_url2click_on_grid_tab3click_on_shop_exclusive_promos_from_the_listexpected_result1sports_url_should_be_launched_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_shop_exclusive_promos_and_promotions_page_is_opened_successfully4user_should_be_able_to_view_home__promotions_on_breadcrumb5user_should_be_able_to_click_on_home_and_navigate_back_to_the_sports_homepage(
            self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on "Shop Exclusive Promos" from the list.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports URL should be launched successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        DESCRIPTION: 4.User should be able to view "Home ->promotions" on breadcrumb.
        DESCRIPTION: 5.User should be able to click on home and navigate back to the sports homepage.
        EXPECTED: 1. 1.Sports URL should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        EXPECTED: 4.User should be able to view "Home ->promotions" on breadcrumb.
        EXPECTED: 5.User should be able to click on home and navigate back to the sports homepage.
        """
        self.site.wait_content_state("Homepage")
        self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_menu = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_menu, msg='"Grid" page items not loaded')
        grid_menu.get(vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()).click()
        breadcrumb = self.site.promotions.breadcrumbs.items_as_ordered_dict
        self.assertTrue(breadcrumb, msg='No breadcrumbs found')
        actual_breadcrumbs = list(breadcrumb.keys())
        self.assertEqual(self.EXPECTED_PROMOTION_BREADCRUMS, actual_breadcrumbs,
                         msg=f'Breadcrumbs {actual_breadcrumbs} are not the same '
                             f'as expected {self.EXPECTED_PROMOTION_BREADCRUMS}')
        breadcrumb[self.EXPECTED_PROMOTION_BREADCRUMS[0]].link.click()
        self.site.wait_content_state("Homepage")
