import pytest
import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Offers.BaseOffersTest import BaseOffersTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.offers
@pytest.mark.promotions_banners_offers
@pytest.mark.screen_resolution
@vtest
class Test_C11250796_Verify_redirect_to_absolute_relative_paths_for_Offers(BaseOffersTest):
    """
    TR_ID: C11250796
    VOL_ID: C14790093
    NAME: Verify redirect to absolute/relative paths for Offers
    DESCRIPTION: This test case verifies that redirection to 'target Uri' works fine for absolute and relative paths in Offers
    PRECONDITIONS: 1. Offer module should be created in CMS: Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: 2. Two Offers should be created: Offers -> Offers -> Create Offer
    PRECONDITIONS: * 1st with absolute path in 'target Uri' e.g. https://gaming.coral.co.uk/live-casino
    PRECONDITIONS: * 2nd with relative path in 'target Uri' e.g. /promotions/details/YourCall
    """
    keep_browser_open = True
    ui_urls = None
    offer_widget = None
    device_name = tests.desktop_default
    maximized_browser = False

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create offers for test
        """
        if tests.settings.cms_env != 'prd0':
            all_cms_offer_modules = self.cms_config.get_offer_modules()
            offer_module = next((module for module in all_cms_offer_modules if module.get('name') == f'{self.cms_config.constants.OFFER_MODULE_NAME} C11250796'), None)
            if not offer_module:
                offer_module = self.cms_config.create_offer_module(name=f'{self.cms_config.constants.OFFER_MODULE_NAME} C11250796')
            offer_module_id = offer_module.get('id')
            [self.cms_config.add_offer(showOfferOn='desktop', targetUri=target_uri, offer_module_id=offer_module_id)
             for target_uri in ('/virtual-sports', '/sport/baseball', '/lotto', '/horse-racing')]

        self.__class__.available_cms_modules_and_offers = self.get_available_cms_modules_and_offers()

        if not self.available_cms_modules_and_offers.available_modules:
            raise CmsClientException(f'No offer modules configured in CMS for brand "{self.brand.title()}"')
        if not self.available_cms_modules_and_offers.available_offers:
            raise CmsClientException(f'No offers configured in CMS for brand "{self.brand.title()}"')

        self.site.wait_content_state('Homepage')

    def test_001_load_the_app_on_desktop(self):
        """
        DESCRIPTION: Load the app on Desktop
        EXPECTED: Offers are displayed in Offer widget at the Right column
        """
        if self.device_type == 'desktop':
            self.site.wait_content_state('Homepage')
            self.__class__.offer_widget = self.get_widget(
                cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
            )
            right_column_items = self.site.right_column.items_as_ordered_dict
            self.assertTrue(right_column_items, msg='Right menu items not found')
            self.assertTrue(self.offer_widget,
                            msg=f'Offers module was not found among "{right_column_items.keys()}" widgets')
            offers = self.offer_widget.items_as_ordered_dict
            self.assertTrue(offers, msg='No Offer Modules found')

    def test_002_click_on_1st_offer_with_absolute_path_in_target_uri(self):
        """
        DESCRIPTION: Click on 1st offer with absolute path in 'target Uri'
        EXPECTED: Redirection to 'target Uri' occurs
        """
        if self.device_type == 'desktop':
            offers = self.offer_widget.items_as_ordered_dict
            module_name, module = list(offers.items())[-1]
            offers = module.items_as_ordered_dict
            self.assertTrue(offers, msg=f'No offers found for {module_name}')
            offer_index, offer = list(offers.items())[-1]
            ui_urls = offer.link.get_link()
            try:
                offer.scroll_to()
                offer.link.click()
            except VoltronException:
                offers = self.offer_widget.items_as_ordered_dict
                module_name, module = list(offers.items())[-1]
                offers = module.items_as_ordered_dict
                self.assertTrue(offers, msg=f'No offers found for {module_name}')
                offer_index, offer = list(offers.items())[-1]
                ui_urls = offer.link.get_link()
                offer.scroll_to()
                offer.link.click()
            if ui_urls == '/homepage':
                ui_urls = f'https://{tests.HOSTNAME}'
            wait_for_result(lambda: ui_urls in self.device.get_current_url(),
                            expected_result=True,
                            timeout=3,
                            name='URL to change'
                            )
            expected_url = ui_urls
            self.device.switch_to_new_tab()
            actual_url = self.device.get_current_url().replace('%2F', '/')
            self.softAssert(self.assertIn, expected_url, actual_url,
                            msg=f'Failed to Redirected absolute target Uri {expected_url} actual {actual_url}')

    def test_003_click_on_2nd_offer_with_relative_path_in_target_uri(self):
        """
        DESCRIPTION: Click on 2nd offer with relative path in 'target Uri'
        EXPECTED: Redirection to 'target Uri' occurs
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            self.site.wait_content_state('Homepage')
            offer_widget = self.get_widget(
                cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
            )
            offers = offer_widget.items_as_ordered_dict
            self.assertTrue(offers, msg='No offers shown')
            if len(offers) > 1:
                offers = offer_widget.items_as_ordered_dict
                module_name, module = list(offers.items())[-1]
                offers = module.items_as_ordered_dict
                self.assertTrue(offers, msg=f'No offers found for {module_name}')
                offer_index, offer = list(offers.items())[-2]
                ui_urls = offer.link.get_link()
                try:
                    offer.scroll_to()
                    offer.link.click()
                except VoltronException:
                    offers = self.offer_widget.items_as_ordered_dict
                    module_name, module = list(offers.items())[-1]
                    offers = module.items_as_ordered_dict
                    self.assertTrue(offers, msg=f'No offers found for {module_name}')
                    offer_index, offer = list(offers.items())[-2]
                    ui_urls = offer.link.get_link()
                    offer.scroll_to()
                    offer.link.click()
                if ui_urls == '/homepage':
                    ui_urls = f'https://{tests.HOSTNAME}'
                wait_for_result(lambda: ui_urls in self.device.get_current_url(),
                                expected_result=True,
                                timeout=3,
                                name='URL to change'
                                )
                expected_url = ui_urls
                self.device.switch_to_new_tab()
                actual_url = self.device.get_current_url().replace('%2F', '/')
                self.softAssert(self.assertIn, expected_url, actual_url,
                                msg=f'Failed to Redirected relative target Uri {expected_url} actual {actual_url}')

    def test_004_load_the_app_on_tablet_and_repeat_steps_2_3_for_offers_within_offer_module_below_betslip(self):
        """
        DESCRIPTION: Load the app on Tablet and repeat steps 2-3 for offers within Offer module (below Betslip)
        """
        if self.device_type == 'tablet':

            offer_widget = self.get_widget(
                cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
            )

            offers = offer_widget.items_as_ordered_dict
            self.assertTrue(offers, msg='No offers shown')
            offer_name, offer = list(offers.items())[-1]
            ui_urls = offer.link.get_link()
            try:
                offer.link.click()
            except VoltronException:
                offers = offer_widget.items_as_ordered_dict
                offer_name, offer = list(offers.items())[-1]
                ui_urls = offer.link.get_link()
                offer.link.click()
            if ui_urls == '/homepage':
                ui_urls = f'https://{tests.HOSTNAME}'
            wait_for_result(lambda: ui_urls in self.device.get_current_url(),
                            expected_result=True,
                            timeout=3,
                            name='URL to change'
                            )
            expected_url = ui_urls
            actual_url = self.device.get_current_url().replace('%2F', '/')
            self.softAssert(self.assertIn, expected_url, actual_url,
                            msg=f'Failed to Redirected target Uri {expected_url} actual {actual_url}')

            offers = self.site.home.offers.items_as_ordered_dict
            self.assertTrue(offers, msg='No offers shown')
            if len(offers) > 1:
                offer_widget = self.get_widget(
                    cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
                )
                offers = offer_widget.items_as_ordered_dict
                self.assertTrue(offers, msg='No offers shown')
                offer_name, offer = list(offers.items())[-2]
                ui_urls = offer.link.get_link()
                offer.link.click()
                if ui_urls == '/homepage':
                    ui_urls = f'https://{tests.HOSTNAME}'
                wait_for_result(lambda: ui_urls in self.device.get_current_url(),
                                expected_result=True,
                                timeout=3,
                                name='URL to change'
                                )
                expected_url = ui_urls
                actual_url = self.device.get_current_url().replace('%2F', '/')
                self.softAssert(self.assertIn, expected_url, actual_url,
                                msg=f'Failed to Redirected target Uri {expected_url} actual {actual_url}')
