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
@pytest.mark.medium
@pytest.mark.offers
@pytest.mark.promotions_banners_offers
@vtest
class Test_C28042_Offer_Module_displaying_depending_on_Disabled_Enabled_option_value(BaseOffersTest):
    """
    TR_ID: C28042
    NAME: Offer Module displaying depending on 'Disabled'/'Enabled' option value
    DESCRIPTION: This test case verifies Offer Modules displaying depending on 'Disabled'/'Enabled' option value in CMS
    PRECONDITIONS: 1) To load CMS use the next links:
    PRECONDITIONS: DEV -  https://coral-cms-dev0.symphony-solutions.eu/login
    PRECONDITIONS: TST2/QA -  https://coral-cms-tst2.symphony-solutions.eu/login
    PRECONDITIONS: STG2 - https://coral-cms-stg2.symphony-solutions.eu/login
    PRECONDITIONS: HL -  https://coral-cms-hl.symphony-solutions.eu/login
    PRECONDITIONS: PROD -  https://coral-cms.symphony-solutions.eu/login
    PRECONDITIONS: BETA - https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: 2) Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    PRECONDITIONS: 3) There are Offer Modules with 'Active' and 'Inactive' option value
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: Create offers for test
        """
        self.__class__.offer_module_name_active = f'Active {self.cms_config.constants.OFFER_MODULE_NAME} C28042'
        self.__class__.offer_module_name_inactive = f'Inactive {self.cms_config.constants.OFFER_MODULE_NAME} C28042'

        if tests.settings.cms_env != 'prd0':
            all_cms_offer_modules = self.cms_config.get_offer_modules()
            offer_module_active = next((module for module in all_cms_offer_modules if module.get('name') == self.offer_module_name_active), None)
            offer_module_inactive = next(
                (module for module in all_cms_offer_modules if module.get('name') == self.offer_module_name_inactive), None)

            if not offer_module_active:
                offer_module_active = self.cms_config.create_offer_module(name=self.offer_module_name_active)

            if not offer_module_inactive:
                offer_module_inactive = self.cms_config.create_offer_module(name=self.offer_module_name_inactive)

            self.__class__.offer_module_id_active = offer_module_active.get('id')
            self.__class__.offer_module_id_inactive = offer_module_inactive.get('id')

            [self.cms_config.add_offer(showOfferOn='desktop', targetUri=target_uri, offer_module_id=self.offer_module_id_active)
             for target_uri in ('/virtual-sports', '/sport/baseball', '/lotto', '/horse-racing')]

            [self.cms_config.add_offer(showOfferOn='desktop', targetUri=target_uri,
                                       offer_module_id=self.offer_module_id_inactive)
             for target_uri in ('/virtual-sports', '/sport/baseball', '/lotto', '/horse-racing')]

            self.cms_config.update_offer_module(offer_module_id=self.offer_module_id_inactive,
                                                name=self.offer_module_name_inactive,
                                                disabled=True)

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

    def test_001_select_offer_module_with_inactive_option_value_checked_in_cmsload_application_and_verify_the_module_displaying(self):
        """
        DESCRIPTION: Select Offer Module with 'Inactive' option value checked in CMS.
        DESCRIPTION: Load application and verify the Module displaying.
        EXPECTED: Inactive Offer Module is NOT displayed in application
        """
        self.__class__.offer_widget = self.get_widget(
            cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn')
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        self.assertTrue(self.offer_widget,
                        msg=f'Offers module was not found among "{right_column_items.keys()}" widgets')

        self.__class__.offers = self.offer_widget.items_as_ordered_dict
        self.assertTrue(self.offers, msg='No Offer Modules found')

        flag = self.offer_module_name_inactive.upper() in list(self.offers.keys())
        self.assertFalse(flag, msg=f'{self.offer_module_name_inactive} offer is available in Offers list {self.offers.keys()}')

    def test_002_select_offer_module_with_active_option_value_checked_in_cmsload_application_and_verify_the_module_displaying(
            self):
        """
        DESCRIPTION: Select Offer Module with 'Active' option value checked in CMS.
        DESCRIPTION: Load application and verify the Module displaying
        EXPECTED: Active Offer Module is displayed in application
        """
        flag = False
        iteration = 0
        while iteration <= 10:
            flag = self.offer_module_name_active.upper() in list(self.offers.keys())
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

        self.assertTrue(flag, msg=f'{self.offer_module_name_active} offer is NOT available in Offers list {self.offers.keys()}')

    def test_003_select_offer_module_with_inactive_option_value_checked_and_update_option_value_to_active_in_cmsload_application_and_verify_offer_module_displaying(self):
        """
        DESCRIPTION: Select Offer Module with 'Inactive' option value checked and update option value to 'Active' in CMS.
        DESCRIPTION: Load application and verify Offer Module displaying.
        EXPECTED: Newly enabled Offer Module appears in application
        """
        self.cms_config.update_offer_module(offer_module_id=self.offer_module_id_inactive,
                                            name=self.offer_module_name_inactive,
                                            disabled=False)
        flag = False
        iteration = 0
        while iteration <= 10:
            flag = self.offer_module_name_inactive.upper() in list(self.offers.keys())
            if flag:
                break
            else:
                self.device.refresh_page()
                sleep(30)
                self.site.wait_content_state('Homepage')
                self.offer_widget = self.get_widget(
                    cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
                )
                self.offers = self.offer_widget.items_as_ordered_dict
                iteration = iteration + 1

        self.assertTrue(flag,
                        msg=f'{self.offer_module_name_inactive} offer is NOT available in Offers list {self.offers.keys()}')

    def test_004_select_offer_module_with_active_option_value_and_update_option_value_to_inactiveload_application_and_verify_offer_module_displaying(self):
        """
        DESCRIPTION: Select Offer Module with 'Active' option value and update option value to 'Inactive'.
        DESCRIPTION: Load application and verify Offer Module displaying
        EXPECTED: Inactive Offer Module stops to display in application
        """
        self.cms_config.update_offer_module(offer_module_id=self.offer_module_id_active, name=self.offer_module_name_active,
                                            disabled=True)
        flag = False
        iteration = 0
        while iteration <= 10:
            flag = self.offer_module_name_active.upper() in list(self.offers.keys())
            if not flag:
                break
            else:
                self.device.refresh_page()
                sleep(30)
                self.site.wait_content_state('Homepage')
                self.offer_widget = self.get_widget(
                    cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
                )
                self.offers = self.offer_widget.items_as_ordered_dict
                iteration = iteration + 1

        self.assertFalse(flag,
                         msg=f'{self.offer_module_name_active} offer is available in Offers list {self.offers.keys()}')
