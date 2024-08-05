import pytest
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
@pytest.mark.retail
@pytest.mark.connect
@pytest.mark.medium
@vtest
@pytest.mark.connect_descoped
class Test_C2377242_Verify_ways_to_get_to_the_Shop_promotions_offers(Common):
    """
    TR_ID: C2377242
    NAME: Verify ways to get to the Shop promotions/offers
    DESCRIPTION: This test case verifies possible ways to get to the Shop promotions/offers
    PRECONDITIONS: **Note that on UI Retail page should be named as 'Connect' for Coral App and 'The Grid' for Ladbrokes**
    PRECONDITIONS: Make sure In-Shop Promotions feature is turned on in CMS: System configuration -> Connect -> promotions
    PRECONDITIONS: Go to CMS and make sure there are some active promotions with Category = 'Connect Promotions', if there are no please create some
    PRECONDITIONS: Load the SB app
    """
    keep_browser_open = True

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
        promotion = self.cms_config.add_promotion(category_id=[category_id])
        self.__class__.promotion_title, self.__class__.promo_id = \
            promotion.title.upper(), promotion.id

    def test_001_tap_promotions_in_the_header_ribbon_menu_on_the_homepage(self):
        """
        DESCRIPTION: Tap 'Promotions' in the header ribbon menu on the homepage
        EXPECTED: * Promotion page with two tabs ('All', 'Shop Exclusive') is opened
        EXPECTED: * Tab 'All' is active
        """
        self.navigate_to_page('promotions')
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(promotions, vec.promotions.TABS_ALL,
                         msg=f'Current tab "{promotions}" is not equal to expected "{vec.promotions.TABS_ALL}"')

    def test_002_tap_the_shop_exclusive_tab(self):
        """
        DESCRIPTION: Tap the 'Shop Exclusive' tab
        EXPECTED: The 'Shop Exclusive' tab with active connect promotions is opened
        """
        self.site.promotions.tabs_menu.open_tab(tab_name=vec.promotions.TABS_RETAIL)
        promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(promotions, vec.promotions.TABS_RETAIL,
                         msg=f'Current tab "{promotions}" is not equal to expected "{vec.promotions.TABS_RETAIL}"')

    def test_003_open_connect_or_the_grid_landing_page_shop_exclusive_promos(self):
        """
        DESCRIPTION: Open 'Connect' OR 'The Grid' landing page -> Shop exclusive promos
        EXPECTED: * Promotion page with two tabs ('All', 'Shop Exclusive') is opened
        EXPECTED: * Tab 'Shop Exclusive' is active
        """
        self.navigate_to_page(name='retail')
        self.site.wait_content_state(state_name='connect')

        connect_menu_options = self.site.connect.menu_items.items_as_ordered_dict
        self.assertTrue(connect_menu_options, msg='There are no menu items on "PROMOTIONS" page')
        shop_exclusive_promos_button = connect_menu_options.get(vec.retail.SHOP_EXCLUSIVE_PROMOS_NAME)
        shop_exclusive_promos_button.click()

        promotions = self.site.promotions.tabs_menu.current
        self.assertEqual(promotions, vec.promotions.TABS_RETAIL,
                         msg=f'Current tab "{promotions}" is not equal to expected "{vec.promotions.TABS_RETAIL}"')

    def test_004_tap_all_tab_and_verify_there_is_no_shop_exclusive_promos_on_it(self):
        """
        DESCRIPTION: Tap 'All' tab
        DESCRIPTION: and verify there is no 'Shop Exclusive' promos on it
        EXPECTED: Promotions with other categories than 'Connect Promotions' category are displayed
        """
        self.site.promotions.tabs_menu.open_tab(tab_name=vec.promotions.TABS_ALL)
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='Can not find any promotions on page')
        self.assertNotIn(self.promotion_title, list(promotions.keys()),
                         msg=f'Promotion: "{self.promotion_title}" found in promotions list: '
                             f'{list(promotions.keys())}')
