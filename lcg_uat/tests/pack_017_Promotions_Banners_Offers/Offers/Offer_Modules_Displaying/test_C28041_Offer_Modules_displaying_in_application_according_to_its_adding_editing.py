import pytest
import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Offers.BaseOffersTest import BaseOffersTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Need to create offer module
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.offers
@pytest.mark.promotions_banners_offers
@vtest
class Test_C28041_Offer_Modules_displaying_in_application_according_to_its_adding_editing_deletion_in_CMS(BaseOffersTest):
    """
    TR_ID: C28041
    NAME: Offer Modules displaying in application according to its adding/editing/deletion in CMS
    DESCRIPTION: This test case verifies Offer Modules displaying in the application according to its adding/editing/deletion in CMS
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
        self.__class__.offer_module_name = f'{self.cms_config.constants.OFFER_MODULE_NAME} C28041'
        self.__class__.offer_module_name_without_offer = f'{self.cms_config.constants.OFFER_MODULE_NAME} C28041 without offer'

        if tests.settings.cms_env != 'prd0':
            all_cms_offer_modules = self.cms_config.get_offer_modules()
            offer_module = next((module for module in all_cms_offer_modules if module.get('name') == self.offer_module_name), None)
            self.__class__.offer_module_without_offer = next((module for module in all_cms_offer_modules if module.get('name') == self.offer_module_name_without_offer), None)

            if not offer_module:
                offer_module = self.cms_config.create_offer_module(name=self.offer_module_name)

            if not self.offer_module_without_offer:
                self.offer_module_without_offer = self.cms_config.create_offer_module(name=self.offer_module_name_without_offer)

            self.__class__.offer_module_id = offer_module.get('id')
            [self.cms_config.add_offer(showOfferOn='desktop', targetUri=target_uri, offer_module_id=self.offer_module_id)
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

    def test_001_add_new_offer_module_with_valid_data_and_with_no_offer_related_to_the_module_in_cmsload_oxygen_application_and_verify_offer_module_displaying(
            self):
        """
        DESCRIPTION: Add new Offer Module with valid data and with no Offer related to the Module in CMS.
        DESCRIPTION: Load Oxygen application and verify Offer Module displaying.
        EXPECTED: Offer Module without offers is NOT displayed in application
        """
        self.__class__.offer_widget = self.get_widget(
            cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn')
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        self.assertTrue(self.offer_widget,
                        msg=f'Offers module was not found among "{right_column_items.keys()}" widgets')

        self.__class__.offers = self.offer_widget.items_as_ordered_dict
        self.assertTrue(self.offers, msg='No Offer Modules found')

        flag = self.offer_module_name_without_offer.upper() in list(self.offers.keys())
        self.assertFalse(flag, msg=f'{self.offer_module_without_offer} offer is available in Offers list {self.offers.keys()}')

    def test_002_add_new_offer_module_with_valid_data_and_with_related_offers_in_cmsload_oxygen_application_and_verify_offer_module_displaying(
            self):
        """
        DESCRIPTION: Add new Offer Module with valid data and with related Offers in CMS.
        DESCRIPTION: Load Oxygen application and verify Offer Module displaying.
        EXPECTED: Offer Module with at least one Offer is displayed in the application
        """
        flag = False
        iteration = 0
        while iteration <= 10:
            flag = self.offer_module_name.upper() in list(self.offers.keys())
            if flag:
                break
            else:
                self.device.refresh_page()
                self.site.wait_content_state('Homepage')
                self.offer_widget = self.get_widget(
                    cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
                )
                self.offers = self.offer_widget.items_as_ordered_dict
                iteration = iteration + 1

        self.assertTrue(flag, msg=f'{self.offer_module_name} offer is NOT available in Offers list {self.offers.keys()}')

    def test_003_for_already_existing_offer_module_update_title_in_cmsload_oxygen_application_and_verify_updated_title_displaying_for_the_module(
            self):
        """
        DESCRIPTION: For already existing Offer Module update title in CMS.
        DESCRIPTION: Load Oxygen application and verify updated title displaying for the Module
        EXPECTED: **For Tablet:**
        EXPECTED: Updated title is displaying for the Module
        EXPECTED: **For Desktop:**
        EXPECTED: Only related to particular Module Offers images are displayed in Offer section next to Banners
        """
        self.__class__.offer_module_updated_name = f'{self.cms_config.constants.OFFER_MODULE_NAME} update C28041'
        self.cms_config.update_offer_module(offer_module_id=self.offer_module_id, name=self.offer_module_updated_name)

        flag = False
        iteration = 0
        while iteration <= 10:
            flag = self.offer_module_updated_name.upper() in list(self.offers.keys())
            if flag:
                break
            else:
                sleep(10)
                self.device.refresh_page()
                self.site.wait_content_state('Homepage')
                self.offer_widget = self.get_widget(
                    cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
                )
                self.offers = self.offer_widget.items_as_ordered_dict
                iteration = iteration + 1

        self.assertTrue(flag, msg=f'{self.offer_module_updated_name} offer is NOT available in Offers list {self.offers.keys()}')

    def test_004_select_already_existing_offer_module_and_delete_it_from_cmsload_oxygen_application_and_verify_deleted_offer_module_displaying(
            self):
        """
        DESCRIPTION: Select already existing Offer Module and delete it from CMS.
        DESCRIPTION: Load Oxygen application and verify deleted Offer Module displaying
        EXPECTED: Deleted Offer Module is NOT displayed in application
        """
        self.cms_config.delete_offer_modules(offer_module_id=self.offer_module_id)

        flag = False
        iteration = 0
        while iteration <= 10:
            flag = self.offer_module_updated_name.upper() in list(self.offers.keys())
            if not flag:
                break
            else:
                sleep(10)
                self.device.refresh_page()
                self.site.wait_content_state('Homepage')
                self.offer_widget = self.get_widget(
                    cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
                )
                self.offers = self.offer_widget.items_as_ordered_dict
                iteration = iteration + 1

        self.assertFalse(flag, msg=f'{self.offer_module_updated_name} offer is available in Offers list {self.offers.keys()}')
        self.cms_config._created_offer_module.remove(self.offer_module_id)
