import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.prod #We can't create promotions under Prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64887507_verify_the_user_is_asked_to_login_when_you_try_to_opt_for_inshop_promotions_without_login(Common):
    """
    TR_ID: C64887507
    NAME: verify the user is asked to login when you try to opt for inshop promotions without login.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True
    button_name = 'Opt In'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Promotion with Opt In button
        """
        opt_in_promo_request_id = self.ob_config.backend.ob.opt_in_offer.default_offer.id
        category_ids = self.cms_config.get_sport_categories()
        connect_promotions = list(filter(lambda param: param['imageTitle'] == 'The Grid', category_ids))
        if not connect_promotions:
            raise CmsClientException('No "Connect Promotions" exist')
        category_id = connect_promotions[0].get('id')
        promotion = self.cms_config.add_promotion(requestId=opt_in_promo_request_id, category_id=[category_id],
                                                  promo_description=[
                                                      {'button_name': f'{self.button_name}',
                                                       'button_link': '',
                                                       'is_it_opt_in_button': True}])

        self.__class__.promotion_title, self.__class__.promo_id, self.__class__.promo_key = \
            promotion.title.upper(), promotion.id, promotion.key
        if self.cms_config.get_promotion(self.promo_id):
            self._logger.debug('*** Promotion with Opt In is configured in CMS successfully')
        else:
            raise CmsClientException('Promotion with Opt In is not configured in CMS')

    def test_001_1_1launch_ladbrokes_sports_url2click_on_grid_tab3click_on_shop_exclusive_promos_from_the_list4click_on_see_more_from_online_promotions_page5click_on_opt_inexpected_result1sports_url_should_be_launched_successfully2user_should_be_able_to_open_grid_tab3user_should_be_able_to_click_on_shop_exclusive_promos_and_promotions_page_is_opened_successfully4user_should_be_able_to_click_on_see_more_from_online_promotions5user_should_be_able_to_click_on_opt_in_and_login_pop_up_triggers(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports URL.
        DESCRIPTION: 2.Click on grid tab.
        DESCRIPTION: 3.Click on "Shop Exclusive Promos" from the list.
        DESCRIPTION: 4.Click on "See more" from online promotions page.
        DESCRIPTION: 5.Click on "Opt-in".
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports URL should be launched successfully.
        DESCRIPTION: 2.User should be able to open grid tab.
        DESCRIPTION: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        DESCRIPTION: 4.User should be able to click on "See more" from online promotions.
        DESCRIPTION: 5.User should be able to click on "Opt-in" and login pop-up triggers.
        EXPECTED: 1. 1.Sports URL should be launched successfully.
        EXPECTED: 2.User should be able to open grid tab.
        EXPECTED: 3.User should be able to click on "Shop Exclusive Promos" and promotions page is opened successfully.
        EXPECTED: 4.User should be able to click on "See more" from online promotions.
        EXPECTED: 5.User should be able to click on "Opt-in" and login pop-up triggers.
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
        self.site.promotions.tabs_menu.open_tab(tab_name=vec.promotions.TABS_RETAIL.upper())
        promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(promotions, vec.promotions.TABS_RETAIL.upper(),
                         msg=f'Current tab "{promotions}" is not equal to expected "{vec.promotions.TABS_RETAIL.upper()}"')
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
        opt_in_button = self.site.promotion_details.tab_content.promotion.detail_description.button
        self.assertTrue(opt_in_button.is_enabled(timeout=20), msg='OptIn button is disabled')
        self.assertEqual(opt_in_button.name, self.button_name,
                         msg=f'Actual button name: "{opt_in_button.name}"'
                             f'is not equal to expected: "{self.button_name}"')
        opt_in_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=5)
        self.assertTrue(dialog, msg='"LOG IN" dialog is not present on page')
