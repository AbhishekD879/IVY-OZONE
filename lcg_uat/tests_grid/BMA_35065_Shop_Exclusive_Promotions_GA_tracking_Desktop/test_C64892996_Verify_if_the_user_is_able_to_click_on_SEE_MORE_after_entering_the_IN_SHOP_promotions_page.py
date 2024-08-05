import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod  # can't create promotions in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64892996_Verify_if_the_user_is_able_to_click_on_SEE_MORE_after_entering_the_IN_SHOP_promotions_page(Common):
    """
    TR_ID: C64892996
    NAME: Verify if the user is able to click on "SEE MORE" after entering the "IN-SHOP" promotions page.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Promotion with stream button
        """
        category_ids = self.cms_config.get_sport_categories()
        connect_promotions = list(filter(lambda param: param['imageTitle'] == 'The Grid', category_ids))
        if not connect_promotions:
            raise CmsClientException('No "Connect Promotions" exist')
        category_id = connect_promotions[0].get('id')
        promotion = self.cms_config.add_promotion(category_id=[category_id])

        self.__class__.promotion_title, promo_id = promotion.title.upper(), promotion.id
        if self.cms_config.get_promotion(promo_id):
            self._logger.debug('*** Promotion is configured in CMS successfully')
        else:
            raise CmsClientException('Promotion is not configured in CMS')

    def test_001_launch_ladbrokes_sports_url2click_on_grid_tab3click_on_shop_exclusive_promos_from_the_list4click_on_see_more_button_in_in_shop_promotions_pageexpected_result1sports_url_should_be_launch_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_shop_exclusive_promos_and_promotions_page_is_opened_successfully4user_should_be_able_to_click_on_see_more_button_and_navigate_to_see_more_info_page_from_in_shop_promotions_page(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on "Shop Exclusive Promos" from the list.
        DESCRIPTION: 4.Click on "SEE MORE" button in "IN-SHOP" promotions page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports URL should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        DESCRIPTION: 4.User should be able to click on "SEE MORE" button and navigate to "SEE MORE INFO" page from "IN-SHOP" promotions page.
        EXPECTED: 1. 1.Sports URL should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        EXPECTED: 4.User should be able to click on "SEE MORE" button and navigate to "SEE MORE INFO" page from "IN-SHOP" promotions page.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()).click()
        self.site.wait_content_state(state_name='promotions', timeout=30)
        self.site.promotions.tabs_menu.open_tab(tab_name=vec.promotions.TABS_RETAIL.upper())
        inshop_promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(inshop_promotions, vec.promotions.TABS_RETAIL.upper(),
                         msg=f'Current tab "{inshop_promotions}" is not equal to expected "{vec.promotions.TABS_RETAIL.upper()}"')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        promotion = promotions.get(self.promotion_title)
        self.assertTrue(promotion, msg=f'"{self.promotion_title}" promotion not found on page')
        self.assertTrue(promotion.more_info_button.is_displayed(),
                        msg=f'"See More" button for Promotion "{self.promotion_title}" is not shown')
        promotion.more_info_button.click()
        self.site.wait_content_state(state_name='PromotionDetails')
