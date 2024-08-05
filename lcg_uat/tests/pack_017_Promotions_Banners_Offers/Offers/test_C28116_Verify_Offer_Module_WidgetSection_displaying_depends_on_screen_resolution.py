from time import sleep

import pytest

import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Offers.BaseOffersTest import BaseOffersTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


#@pytest.mark.prod
@pytest.mark.hl
#@pytest.mark.tst2
#@pytest.mark.stg2
@pytest.mark.offers
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.high
@pytest.mark.offers
@pytest.mark.promotions_banners_offers
@pytest.mark.quarantine
@pytest.mark.na
@vtest
class Test_C28116_Verify_Offer_Module_WidgetSection_displaying_depends_on_screen_resolution(BaseOffersTest):
    """
    TR_ID: C28116
    VOL_ID: C10806953
    NAME: Verify Offer Module Widget/Section displaying depends on screen resolution
    DESCRIPTION: This test case verifies Offer Module Widget/Section displaying for Desktop depends on screen resolution
    PRECONDITIONS: 1) To load CMS use the next links:
    PRECONDITIONS: DEV -  https://coral-cms-dev0.symphony-solutions.eu/login
    PRECONDITIONS: TST2 -  https://coral-cms-tst2.symphony-solutions.eu/login
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/login
    PRECONDITIONS: HL -  https://coral-cms-hl.symphony-solutions.eu/login
    PRECONDITIONS: PROD -  https://coral-cms.symphony-solutions.eu/login
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2) Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    available_cms_modules_and_offers = None
    available_widget_names = None
    width_less_than_1100 = 1099
    width_equal_to_1100 = 1100
    maximized_browser = False

    def set_windows_width(self, width):
        window_size = self.device.driver.get_window_size()
        self.device.set_viewport_size(width, window_size.get('height'))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: Create offers for test
        DESCRIPTION: Check if device size is valid for test execution
        """
        cms_banners = self.get_initial_data_system_configuration().get('DynamicBanners', {})
        if not cms_banners:
            cms_banners = self.cms_config.get_system_configuration_item('DynamicBanners')
        use_aem_offer_modules_banners = cms_banners.get('useAemOfferModulesBanners', False)
        if use_aem_offer_modules_banners:
            raise CmsClientException('CMS offers won\'t be shown as AEM offers are enabled')
        if tests.settings.cms_env != 'prd0':
            all_cms_offer_modules = self.cms_config.get_offer_modules()
            offer_module = next((module for module in all_cms_offer_modules if module.get('name') == f'{self.cms_config.constants.OFFER_MODULE_NAME} C28116'), None)
            if not offer_module:
                offer_module = self.cms_config.create_offer_module(name=f'{self.cms_config.constants.OFFER_MODULE_NAME} C28116')
            offer_module_id = offer_module.get('id')
            [self.cms_config.add_offer(showOfferOn='desktop', targetUri=target_uri, offer_module_id=offer_module_id)
             for target_uri in ('/virtual-sports', '/sport/baseball', '/lotto', '/horse-racing')]

        widgets = self.cms_config.get_widgets()
        self.__class__.available_widget_names = [widget.get('title').upper() for widget in widgets
                                                 if all((widget.get('showOnDesktop'),
                                                         not widget.get('disabled'),
                                                         widget.get('columns') in ('both', 'rightColumn')))]

        self.__class__.available_cms_modules_and_offers = self.get_available_cms_modules_and_offers()
        if not self.available_cms_modules_and_offers.available_modules:
            raise CmsClientException(f'No offer modules configured in CMS for brand "{self.brand.title()}"')
        if not self.available_cms_modules_and_offers.available_offers:
            raise CmsClientException(f'No offers configured in CMS for brand "{self.brand.title()}"')

        self.site.wait_content_state('Homepage')
        self._logger.info(f'Current window size: {self.device.driver.get_window_size()}')

    def test_001_resize_the_page_to_less_1100px_width_and_verify_Offer_Modules_location(self):
        """
        DESCRIPTION: Resize the page to < 1100px width and verify Offer Modules location
        EXPECTED: Offer widget is present at the Right column
        EXPECTED: Every Offer Module is displayed in separate section
        """
        self.set_windows_width(self.width_less_than_1100)
        self._logger.info(f'Current window size: {self.device.driver.get_window_size()}')
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')

        offer_widget = self.get_widget(
            cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
        )
        self.assertTrue(offer_widget, msg=f'Offers module was not found among "{right_column_items.keys()}" widgets')

        offers = offer_widget.items_as_ordered_dict
        self.assertTrue(offers, msg='No Offer Modules found')
        offer_names = offers.keys()
        for offer_name in offer_names:
            offers = offer_widget.items_as_ordered_dict
            offer = offers[offer_name]
            offer.collapse()
            self.assertFalse(offer.is_expanded(expected_result=False),
                             msg=f'Offer {offer_name} is not collapsed after click')

            offer.expand()
            self.assertTrue(offer.is_expanded(), msg=f'Offer {offer_name} is not expanded after click')
            sleep(0.5)

    def test_002_resize_the_page_equal_to_1100px_width_and_verify_Offer_Modules_location(self):
        """
        DESCRIPTION: Verify Offer Modules presence
        EXPECTED: * Offers are present at the Content Area next to AEM Banners
        EXPECTED: * Offer widget is NOT present at the Right column anymore
        """
        self.set_windows_width(self.width_equal_to_1100)
        self._logger.info(f'Current window size: {self.device.driver.get_window_size()}')
        self.assertTrue(self.site.home.offers.is_displayed(), msg='Offers section is not shown')
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        self.assertNotIn(self.cms_config.constants.OFFERS_WIDGET_NAME, right_column_items.keys(),
                         msg=f'"{self.cms_config.constants.OFFERS_WIDGET_NAME}" is present among "{right_column_items.keys()}"')
