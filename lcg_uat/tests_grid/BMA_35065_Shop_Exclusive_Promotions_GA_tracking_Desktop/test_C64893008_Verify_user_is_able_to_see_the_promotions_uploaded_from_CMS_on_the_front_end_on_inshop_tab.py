import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod # Should not add promo in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893008_Verify_user_is_able_to_see_the_promotions_uploaded_from_CMS_on_the_front_end_on_inshop_tab(Common):
    """
    TR_ID: C64893008
    NAME: Verify user is able to see the promotions uploaded from CMS on the front end on inshop tab
    DESCRIPTION: 
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test promotion in CMS
        EXPECTED: Test promotion created
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

    def test_001_launch_the_cms_tst0prod2click_on_promotions_tab_from_lhm3click_on_create_new_promotion_and_fill_all_the_details_and_save_the_changesselect_category_as_grid_promotions4click_on_shop_exclusive_promos__menu_from_the_list5switch_to_inshop_promotions_tab6verify_if_the_user_is_able_to_see_the_updated_promotions_on_the_front_endexpected_resultthe_uploaded_promotions_from_cms_should_be_reflected_on_the_front_end_in_inshop_tabflow_grid_shop_exclusive_promos_inshop_tab(self):
        """
        DESCRIPTION: 1. 1.Launch the CMS (tst0/Prod)
        DESCRIPTION: 2.Click on promotions tab from LHM
        DESCRIPTION: 3.Click on create new promotion and fill all the details and save the changes(select category as Grid promotions)
        DESCRIPTION: 4.Click on "Shop Exclusive Promos " menu from the list.
        DESCRIPTION: 5Switch to inshop promotions tab
        DESCRIPTION: 6.Verify if the user is able to see the updated promotions on the front end.
        DESCRIPTION: Expected Result:
        DESCRIPTION: The uploaded promotions from CMS should be reflected on the front end in inshop tab
        DESCRIPTION: flow :
        DESCRIPTION: GRID->shop exclusive promos->inshop tab
        EXPECTED: 1. The uploaded promotions from CMS should be reflected on the front end in inshop tab
        EXPECTED: flow :
        EXPECTED: GRID->shop exclusive promos->inshop tab
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
        promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(promotions.upper(), vec.promotions.TABS_RETAIL.upper(),
                         msg=f'Current tab "{promotions}" is not equal to expected "{vec.promotions.TABS_RETAIL}"')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='Can not find any promotions on page')
        self.assertIn(self.promotion_title, list(promotions.keys()),
                     msg=f'Promotion: "{self.promotion_title}" found in promotions list: '
                          f'{list(promotions.keys())}')