import pytest
import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Offers.BaseOffersTest import BaseOffersTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Need to create offer module
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.offers
@pytest.mark.promotions_banners_offers
@vtest
class Test_C28047_Offers_displaying_within_the_module_depending_on_Display_From(BaseOffersTest):
    """
    TR_ID: C28047
    NAME: Offers displaying within the module depending on ‘Display From  –  Display to’ date
    DESCRIPTION: This test case verifies Offers displaying depending on ‘Display From  –  Display to’ date selected in CMS for the Offer
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

    def test_000_preconditions(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: Create offers for test
        DESCRIPTION: Check if device size is valid for test execution
        """
        self.__class__.offer_module_name_within_date_range = f'{self.cms_config.constants.OFFER_MODULE_NAME} C28041 with date range'
        self.__class__.offer_module_name_out_of_range = f'{self.cms_config.constants.OFFER_MODULE_NAME} C28041 out of range '

        if tests.settings.cms_env != 'prd0':
            all_cms_offer_modules = self.cms_config.get_offer_modules()
            offer_module_within_date_range = next((module for module in all_cms_offer_modules if module.get('name') == self.offer_module_name_within_date_range), None)
            offer_module_out_of_range = next((module for module in all_cms_offer_modules if module.get('name') == self.offer_module_name_out_of_range), None)

            if not offer_module_within_date_range:
                offer_module_within_date_range = self.cms_config.create_offer_module(name=self.offer_module_name_within_date_range)

            if not offer_module_out_of_range:
                offer_module_out_of_range = self.cms_config.create_offer_module(name=self.offer_module_name_out_of_range)

            offer_module_id_within_range = offer_module_within_date_range.get('id')
            [self.cms_config.add_offer(showOfferOn='desktop', targetUri=target_uri, offer_module_id=offer_module_id_within_range)
             for target_uri in ('/virtual-sports', '/sport/baseball', '/lotto', '/horse-racing')]

            offer_module_id_out_of_range = offer_module_out_of_range.get('id')
            [self.cms_config.add_offer(showOfferOn='desktop', targetUri=target_uri, offer_module_id=offer_module_id_out_of_range,
                                       displayFrom_days=2, displayTo_days=4)
             for target_uri in ('/virtual-sports', '/sport/baseball', '/lotto', '/horse-racing')]

        widgets = self.cms_config.get_widgets()
        self.__class__.available_widget_names = [widget.get('title').upper() for widget in widgets
                                                 if all((widget.get('showOnDesktop'), not widget.get('disabled'),
                                                         widget.get('columns') in ('both', 'rightColumn')))]

        available_cms_modules_and_offers = self.get_available_cms_modules_and_offers()

        if not available_cms_modules_and_offers.available_modules:
            raise CmsClientException(f'No offer modules configured in CMS for brand "{self.brand.title()}"')
        if not available_cms_modules_and_offers.available_offers:
            raise CmsClientException(f'No offers configured in CMS for brand "{self.brand.title()}"')

        self.site.wait_content_state('Homepage')

    def test_001_select_offer_with_date_range_which_includes_current_date_in_cmsload_oxygen_application_and_verify_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with date range which includes current date in CMS.
        DESCRIPTION: Load Oxygen application and verify Offer displaying.
        EXPECTED: Offer is displayed in application
        """
        self.__class__.offer_widget = self.get_widget(
            cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn')
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        self.assertTrue(self.offer_widget,
                        msg=f'Offers module was not found among "{right_column_items.keys()}" widgets')

        self.__class__.offers = self.offer_widget.items_as_ordered_dict
        self.assertTrue(self.offers, msg='No Offer Modules found')

        flag = self.offer_module_name_within_date_range.upper() in list(self.offers.keys())
        self.assertTrue(flag, msg=f'{self.offer_module_name_within_date_range} offer is NOT available in Offers list {self.offers.keys()}')

    def test_002_select_offer_with_date_range_which_does_not_include_current_date_in_cmsload_oxygen_application_and_verify_offer_displaying(self):
        """
        DESCRIPTION: Select Offer with date range which does not include current date in CMS.
        DESCRIPTION: Load Oxygen application and verify offer displaying.
        EXPECTED: Offer is NOT displayed in application
        """
        flag = self.offer_module_name_out_of_range.upper() in list(self.offers.keys())
        self.assertFalse(flag,
                         msg=f'{self.offer_module_name_out_of_range} offer is available in Offers list {self.offers.keys()}')
