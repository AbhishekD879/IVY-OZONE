import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod # can't create promotions in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64892999_Verify_if_the_user_is_able_to_click_on_SEE_MORE_after_entering_the_ONLINE_promotions_page(Common):
    """
    TR_ID: C64892999
    NAME: Verify if the user is able to click on "SEE MORE" after entering the "ONLINE" promotions page.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Promotion
        """
        category_ids = self.cms_config.get_sport_categories()
        connect_promotions = list(filter(lambda param: param['imageTitle'] == 'The Grid', category_ids))
        if not connect_promotions:
            raise CmsClientException('No "grid Promotions" exist')
        promotion = self.cms_config.add_promotion()

        self.__class__.promotion_title, self.__class__.promo_id, self.__class__.promo_key = \
            promotion.title.upper(), promotion.id, promotion.key
        if self.cms_config.get_promotion(self.promo_id):
            self._logger.debug('*** Promotion is configured in CMS successfully')
        else:
            raise CmsClientException('Promotion is not configured in CMS')

    def test_001_launch_ladbrokes_sports_url2click_on_grid_tab3click_on_shop_exclusive_promos_from_the_list4click_on_see_more_button_in_online_promotions_pageexpected_result1sports_url_should_be_launch_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_shop_exclusive_promos_and_promotions_page_is_opened_successfully4user_should_be_able_to_click_on_see_more_button_and_navigate_to_see_more_info_page_from_online_promotions_page(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on "Shop Exclusive Promos" from the list.
        DESCRIPTION: 4.Click on "SEE MORE" button in "ONLINE" promotions page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports URL should be launch successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        DESCRIPTION: 4.User should be able to click on "SEE MORE" button and navigate to "SEE MORE INFO" page from "ONLINE" promotions page.
        EXPECTED: 1. 1.Sports URL should be launch successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        EXPECTED: 4.User should be able to click on "SEE MORE" button and navigate to "SEE MORE INFO" page from "ONLINE" promotions page.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items[vec.retail.EXPECTED_GRID_ITEMS.grid_exclusive_promos.title()].click()
        self.site.wait_content_state(state_name='Promotions', timeout=30)

        tabs = self.site.shop_exclusive_promos.promotions_tabs_menu.items_as_ordered_dict
        list(tabs.values())[0].click()
        current_tab = self.site.shop_exclusive_promos.promotions_tabs_menu.current
        self.assertTrue(current_tab, msg=f'"{vec.retail.ONLINE_BUTTON_TITLE.upper()}" tab is not selected by after click')
        self.assertEqual(current_tab, vec.retail.ONLINE_BUTTON_TITLE.upper(),
                         msg=f'Actual tab: "{current_tab}" is not Expected as: '
                             f'"{vec.retail.ONLINE_BUTTON_TITLE.upper()}"')

        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')
        self.assertTrue(self.promotion_title in list(promotions.keys()),
                        msg=f'Test promotion: "{self.promotion_title}" was not found in "{list(promotions.keys())}"')
        promotion = promotions[self.promotion_title]
        promotion.scroll_to()
        name = promotion.name
        self.assertTrue(name, msg='Promo name is empty')
        self.assertTrue(promotion.more_info_button.is_displayed(),
                        msg=f'"More Info" button for Promotion "{name}" is not shown')
        promotion.more_info_button.click()
        self.assertFalse(promotion.has_more_info(expected_result=False, timeout=15), msg='More info still displaying')
        self.site.wait_content_state(state_name='PromotionDetails')
