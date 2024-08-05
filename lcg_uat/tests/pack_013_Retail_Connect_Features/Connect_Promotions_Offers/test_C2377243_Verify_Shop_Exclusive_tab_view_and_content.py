import pytest
from datetime import datetime
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec


#@pytest.mark.crl_tst2  # Coral only
#@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.desktop
@pytest.mark.promotions
@pytest.mark.connect
@pytest.mark.retail
@pytest.mark.medium
@vtest
@pytest.mark.connect_descoped
class Test_C2377243_Verify_Shop_Exclusive_tab_view_and_content(Common):
    """
    TR_ID: C2377243
    NAME: Verify 'Shop Exclusive' tab view and content
    DESCRIPTION: This test case verifies view of 'Connect Exclusive' tab
    PRECONDITIONS: Make sure In-Shop Promotions feature is turned on in CMS: System configuration -> Connect -> promotions
    PRECONDITIONS: A user is logged in
    PRECONDITIONS: CMS: https://CMS_ENDPOINT/keystone/ -> Pick 'sportsbook' brand from the drop-down -> 'Promotions'  :
    PRECONDITIONS: Active promotions are created with current validity period and Category equal 'Connect Promotions'
    """
    keep_browser_open = True
    promo_titles = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test promotion in CMS
        EXPECTED: Test promotion created
        """
        cms_config = self.get_initial_data_system_configuration().get('Connect', {})
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('Connect')
        if not cms_config.get('promotions'):
            raise CmsClientException('"Connect Promotions" is disabled')
        category_ids = self.cms_config.get_sport_categories()

        connect_promotions = list(filter(lambda param: param['imageTitle'] == 'Connect Promotions', category_ids))
        if not connect_promotions:
            raise CmsClientException('No "Connect Promotions" exist')
        category_id = connect_promotions[0].get('id')

        add_promotion = self.cms_config.add_promotion(category_id=[category_id])
        self.__class__.promotion_title, self.__class__.promo_id = \
            add_promotion.title.upper(), add_promotion.id

        promotions = self.cms_config.get_promotions()
        list_of_connect_promotions = list(filter(lambda param: param['categoryId'] == [category_id], promotions))

        now = datetime.now().isoformat()
        valid_promotions = []
        for promotion in list_of_connect_promotions:
            if promotion['validityPeriodEnd'] >= str(now) and not promotion['disabled']:
                valid_promotions.append(promotion)

        [self.promo_titles.append(promotion.get('title').upper()) for promotion in valid_promotions]

    def test_001_header_ribbon_menu_promotions_shop_exclusive_tab(self):
        """
        DESCRIPTION: Header ribbon menu -> Promotions -> 'Shop Exclusive' tab
        EXPECTED: Tab contains:
        EXPECTED: * List of promotions with category 'Connect Promotions'
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')

        self.site.promotions.tabs_menu.open_tab(tab_name=vec.promotions.TABS_RETAIL)
        promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(promotions, vec.promotions.TABS_RETAIL,
                         msg=f'Current tab "{promotions}" is not equal to expected "{vec.promotions.TABS_RETAIL}"')

        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='Can not find any promotions on page')
        self.assertListEqual(list(promotions.keys()), self.promo_titles,
                             msg=f'Promotion titles in UI: "{list(promotions.keys())}" is not equal in promotions in CMS: '
                             f'"{self.promo_titles}"')

    def test_002_verify_the_list_of_benefits(self):
        """
        DESCRIPTION: Verify the list of benefits
        EXPECTED: * Only benefits with the category 'Connect Promotions' (set in CMS) are displayed
        EXPECTED: * Benefits are sorted accordingly to sort order in CMS
        EXPECTED: * Only banners with current validity time and category equal to 'Connect Promotions' are displayed
        """
        # verified in step 1
        pass
