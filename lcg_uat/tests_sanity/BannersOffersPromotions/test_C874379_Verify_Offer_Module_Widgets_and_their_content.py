import pytz
from datetime import datetime
from time import sleep

import pytest

import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Offers.BaseOffersTest import BaseOffersTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from crlat_ob_client.utils.date_time import get_date_time_object


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@pytest.mark.offers
@pytest.mark.widgets
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.tablet
@vtest
class Test_C874379_Verify_Offer_Module_Widgets_and_their_content(BaseOffersTest):
    """
    TR_ID: C874379
    VOL_ID: C49892696
    NAME: Verify Offer Module Widgets and their content
    DESCRIPTION: This test case verifies Offer Module Widgets and their content
    PRECONDITIONS: How to create Offer in CMS: https://ladbrokescoral.testrail.com/index.php?/cases/view/28046&group_by=cases:section_id&group_order=asc&group_id=304275
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/offers
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    maximized_browser = False
    keep_browser_open = True
    device_name = tests.desktop_default
    maximum_allowed_width = 1099
    minimum_allowed_width = 1101
    time_pattern = '%Y-%m-%dT%H:%M:%S.000Z'

    def wait_for_active_offer_number(self, expected_number: str):
        result = wait_for_result(lambda: self.offers_module.get_active_offer_number() == expected_number,
                                 name=f'Current offer number to be "{expected_number}"',
                                 poll_interval=0.1,
                                 timeout=5)
        self.assertTrue(result, msg=f'"{expected_number}" offer is not displayed, instead displayed "{self.offers_module.get_active_offer_number()}" offer')

    def get_cms_offer_urls_for_module(self, module_name: str) -> list:
        """
        Get Offers URI's from CMS based on public result for specified module offer
        :param module_name: offer module name
        :return: Offers URI's
        """
        specified_cms_offers = next((module.get('offers') for module in self.all_cms_modules
                                     if module.get('name').lower() == module_name.lower()))

        cms_urls = [cms_offer.get('targetUri') for cms_offer in specified_cms_offers if
                    'new' in cms_offer.get('showToCustomer') and
                    datetime.strptime(cms_offer.get('displayTo'), self.time_pattern).replace(tzinfo=pytz.timezone('GB')) >
                    get_date_time_object(days=0, time_format=self.time_pattern)]
        return cms_urls if len(cms_urls) <= 3 else cms_urls[:3]

    def get_cms_offer_urls(self) -> list:
        """
        Method returns list with available offers Uri's for offers section (when screen with is higher then 1100px)
        It takes up to three offer for each module
        :return: available offers Uri's
        """
        cms_urls = []
        for module in self.all_cms_modules:
            offers = module.get('offers')
            offers_for_module = []
            for offer in offers:
                if 'new' in offer.get('showToCustomer')\
                        and datetime.strptime(offer.get('displayTo'), self.time_pattern)\
                        .replace(tzinfo=pytz.timezone('GB')) > get_date_time_object(days=0, time_format=self.time_pattern):
                    offers_for_module.append(offer.get('targetUri'))

            offers_for_module = offers_for_module if len(offers_for_module) <= 3 else offers_for_module[:3]
            cms_urls += offers_for_module

        result = []
        for uri in cms_urls:
            if uri.startswith('http'):
                result.append(uri)
            else:
                result.append(f'https://{tests.HOSTNAME}/{uri.lstrip("/")}')

        return result

    def test_000_preconditions(self):
        """
        DESCRIPTION: Setup Offer Module
        """
        cms_banners = self.get_initial_data_system_configuration().get('DynamicBanners', {})
        if not cms_banners:
            cms_banners = self.cms_config.get_system_configuration_item('DynamicBanners')
        use_aem_offer_modules_banners = cms_banners.get('useAemOfferModulesBanners', False)
        if use_aem_offer_modules_banners:
            raise CmsClientException('CMS offers won\'t be shown as AEM offers are enabled')

        if tests.settings.cms_env != 'prd0':
            offer_name = f'{self.cms_config.constants.OFFER_MODULE_NAME} C874379'
            offer_module = self.cms_config.create_offer_module(name=offer_name)
            [self.cms_config.add_offer(showOfferOn='both', targetUri=target_uri,
                                       offer_module_id=offer_module.get('id'))
             for target_uri in ('/virtual-sports', '/sport/baseball', '/lotto', '/horse-racing')]

            wait_for_result(
                lambda: any([offer_name.lower() in offer.get('name').lower() for offer in self.cms_config.get_offers_for_device_type(self.device_type)]),
                name='Added CMS Offer to be present in response',
                poll_interval=3,
                timeout=60)

        self.__class__.all_cms_modules = self.cms_config.get_offers_for_device_type(self.device_type)

        self.__class__.offers_widget_name = self.get_filtered_widget_name(cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE,
                                                                          column='rightColumn')

        self.__class__.available_cms_modules_and_offers = self.get_available_cms_modules_and_offers()
        self.__class__.available_cms_offers = self.available_cms_modules_and_offers.available_offers

        if not self.all_cms_modules:
            raise CmsClientException(f'No offers configured in CMS for brand "{self.brand.title()}"')
        if not self.available_cms_modules_and_offers.available_modules:
            raise CmsClientException(f'No offer modules configured in CMS for brand "{self.brand.title()}"')
        if not self.available_cms_offers:
            raise CmsClientException(f'No offers configured in CMS for brand "{self.brand.title()}"')

    def test_001_load_oxygen_app_on_tablet_device_and_desktop_screen_resolution_less_than_1100px(self):
        """
        DESCRIPTION: Load Oxygen app on tablet device and Desktop (screen resolution less than 1100px)
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

        if self.device_type == 'desktop':
            window_size = self.device.driver.get_window_size()
            self.device.set_viewport_size(width=self.maximum_allowed_width,
                                          height=window_size.get("height"))

    def test_002_verify_offer_modules_presence(self):
        """
        DESCRIPTION: Verify Offer Modules presence
        EXPECTED: * All available Offer Modules are present right after 'Favourites' widget (configurable in CMS on 'Widgets Page');
        EXPECTED: * Every Offer Module is displayed in separate section which is collapsible/expandable;
        """
        self.__class__.offer_widget = self.get_widget(
            cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
        )

        offers = self.offer_widget.items_as_ordered_dict
        self.assertTrue(offers, msg='No Offer Modules found')
        for offer_name, offer in offers.items():
            offer.collapse()
            self.assertFalse(offer.is_expanded(expected_result=False),
                             msg=f'Offer "{offer_name}" is not collapsed after click')

            offer.expand()
            self.assertTrue(offer.is_expanded(), msg=f'Offer "{offer_name}" is not expanded after click')

    def test_003_verify_ordering_of_offer_modules(self):
        """
        DESCRIPTION: Verify ordering of Offer Modules
        EXPECTED: Offer Modules order corresponds to the set in CMS by drag-n-drop order on 'Offer Modules' page
        """
        self.__class__.offers = self.offer_widget.items_as_ordered_dict
        self.assertTrue(self.offers, msg='No Offer Modules found')
        cms_names = [module.upper() for module in self.available_cms_modules_and_offers.available_modules]
        module_names = list(self.offers.keys())
        self.assertEqual(cms_names, module_names,
                         msg=f'Available modules on the UI "{module_names} '
                         f'does not match modules from CMS "{cms_names}"')

    def test_004_verify_module_content(self):
        """
        DESCRIPTION: Verify Module content
        EXPECTED: Each Module consists of:
        EXPECTED: *   Module title;
        EXPECTED: *   Related to particular Module Offers images;
        EXPECTED: *   Navigation pills
        """
        for module_name, module in self.offers.items():
            self.assertTrue(module_name, msg='Module title is empty')

            offers = module.items_as_ordered_dict
            self.assertTrue(offers, msg=f'No offers found for "{module_name}"')

            slide_dots = module.has_slide_dots(timeout=0)
            if len(offers) > 1:
                self.assertTrue(slide_dots, msg=f'Navigation dots are not shown for {module_name}')
            else:
                self.assertFalse(slide_dots, msg=f'Navigation dots are shown for {module_name}')

    def test_005_verify_module_title(self):
        """
        DESCRIPTION: Verify Module title
        EXPECTED: *   Module title is CMS-controllable ('title' field);
        EXPECTED: *   Module title should be not null or empty.
        """
        self._logger.warning('*** This step is verified in step 4, skipped verification here')

    def test_006_verify_navigation_pills(self):
        """
        DESCRIPTION: Verify navigation pills
        EXPECTED: Navigation pills indicate displaying of current Offer image within particular Module
        """
        for module_name, module in self.offer_widget.items_as_ordered_dict.items():
            offers = module.items_as_ordered_dict
            self.assertTrue(offers, msg=f'No offers found for "{module_name}"')
            if len(offers) > 1:
                dots = module.slide_dots.items_as_ordered_dict
                self.assertTrue(dots, msg='No Slide dots found')

                for dot_number, dot in dots.items():
                    dot_number += 1
                    dot.click()
                    self.assertTrue(dot.is_selected(), msg=f'Dot "{dot_number}" is not selected after click')
                    wait_for_result(lambda: module.get_active_offer_number() == str(dot_number),
                                    poll_interval=0.5,
                                    timeout=5,
                                    name='Active offer to change')

                    active_offer = module.get_active_offer_number()
                    self.assertEqual(active_offer, str(dot_number),
                                     msg=f'"{str(dot_number)}" offer is not displayed, instead displayed "{active_offer}" offer')

    def test_007_verify_ordering_of_offers_images(self):
        """
        DESCRIPTION: Verify ordering of Offers images
        EXPECTED: Offers images order corresponds to the set in CMS by drag-n-drop order on 'Offer' page
        """
        # note: destination url is the only one unique DOM attribute in the list of offers
        for module_name, module in self.offers.items():
            self.assertTrue(module_name, msg='Module title is empty')

            offers = module.items_as_ordered_dict
            self.assertTrue(offers, msg=f'No offers found for "{module_name}"')

            # note: destination url is the only one unique DOM attribute in the list of offers
            ui_urls = [offer.link.get_link() for offer_name, offer in offers.items()]
            cms_urls = self.get_cms_offer_urls_for_module(module_name)

            self.assertListEqual(sorted(ui_urls), sorted(cms_urls), msg=f'List of UI URLs: \n"{sorted(ui_urls)}" \n'
                                 f'is not equal to list of CMS URLs: \n"{sorted(cms_urls)}"')

    def test_008_verify_navigation_between_offers_images(self):
        """
        DESCRIPTION: Verify navigation between Offers images
        EXPECTED: *   User can scroll left or right within each Module;
        EXPECTED: *   Images are displayed correctly;
        EXPECTED: *   Maximum 3 offers images can be presented;
        EXPECTED: *   Offers should be shown in continuous loop automatically.
        """
        for module_name, module in self.offers.items():
            offers = module.items_as_ordered_dict
            self.assertTrue(offers, msg=f'No offers found for "{module_name}"')
            self.assertTrue(len(offers) <= 3, msg=f'There should be Maximum "3" offers, but "{len(offers)}" is shown')
            for offer_index, offer in offers.items():
                offer.scroll_to()
                link = offer.link
                self.assertTrue(any((link.has_image(), link.has_no_image())),
                                msg=f'Offer by index "{offer_index}" has neither picture nor placeholder')

    def test_009_click_tap_on_the_offer_image(self):
        """
        DESCRIPTION: Click/Tap on the Offer image
        EXPECTED: * User is redirected to the page, path for which is set in 'Target Uri' field in CMS
        EXPECTED: * 'Target Uri' supports internal (e.g. football/today) and external (begins with http/https) Uri's
        """
        module_name, module = list(self.offers.items())[-1]
        offers = module.items_as_ordered_dict
        self.assertTrue(offers, msg=f'No offers found for "{module_name}"')
        offer_index, offer = list(offers.items())[-1]
        offer.scroll_to()
        offer.link.click()
        self.site.wait_content_state_changed()

    def test_010_load_oxygen_app_on_desktop__with_screen_resolution__1100px_width_and_verify_offer_modules_presence(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop  with screen resolution >= 1100px width and verify Offer Modules presence
        EXPECTED: * Offers are present at the Content Area next to AEM Banners
        EXPECTED: * Offer widget is NOT present at the Right column
        """
        if self.device_type == 'tablet':
            self._logger.warning('*** This step is desktop only, skipped for tablet execution')
            return

        if self.device_type == 'desktop':
            window_size = self.device.driver.get_window_size()
            self.device.set_viewport_size(width=self.minimum_allowed_width,
                                          height=window_size.get("height"))

        self.navigate_to_page(name='Home')
        self.site.wait_content_state('Homepage')

        self.__class__.offers = self.site.home.offers.items_as_ordered_dict
        self.assertTrue(self.offers, msg='No offers shown')

        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        self.assertNotIn(self.offers_widget_name, right_column_items.keys(),
                         msg=f'Widget is present among "{right_column_items.keys()}"')

    def test_011_verify_ordering_of_offer_modules_and_offer_images(self):
        """
        DESCRIPTION: Verify ordering of Offer Modules and Offer Images
        EXPECTED: Every Offer Module contains Offer images in order set via CMS
        """
        if self.device_type == 'tablet':
            self._logger.warning('*** This step is desktop only, skipped for tablet execution')
            return

        # note: destination url is the only one unique DOM attribute in the list of offers
        ui_urls = [offer.link.get_link() for offer_name, offer in self.offers.items()]
        cms_urls = self.get_cms_offer_urls()

        self.assertListEqual(sorted(ui_urls), sorted(cms_urls), msg=f'List of UI URLs: \n{ui_urls} \n '
                             f'is not equal to list of CMS URLs: \n{cms_urls}')

    def test_012_verify_module_content(self):
        """
        DESCRIPTION: Verify Module content
        EXPECTED: Each Module consists of:
        EXPECTED: * Related to particular Module Offers images
        EXPECTED: * Navigation Arrows
        """
        if self.device_type == 'tablet':
            self._logger.warning('*** This step is desktop only, skipped for tablet execution')
            return

        self.site.home.offers.scroll_to()

        self.site.home.offers.mouse_over()
        if len(self.offers) > 1:
            self.assertTrue(any((self.site.home.offers.has_left_arrow(), self.site.home.offers.has_right_arrow())),
                            msg='Offers section does not contain neither left nor right arrows')
        else:
            self.assertFalse(all((self.site.home.offers.has_left_arrow(expected_result=False),
                                  self.site.home.offers.has_right_arrow(expected_result=False))),
                             msg='Offers section contains left or right arrow')

        for offer_index, offer in reversed(list(self.offers.items())):
            link = offer.link
            self.assertTrue(link.has_image(), msg=f'Offer by index "{offer_index}" has no image')

    def test_013_verify_navigation_arrows(self):
        """
        DESCRIPTION: Verify Navigation Arrows
        EXPECTED: * Navigation Arrows are located at the left and right side of the Offer section
        EXPECTED: * Next or Previous Offer image appears after clicking on Right/Left Navigation Arrow
        EXPECTED: * Maximum 3 offers images can be presented inside one Offer Module
        EXPECTED: * Offer images are shown in continuous loop automatically
        """
        if self.device_type == 'tablet':
            self._logger.warning('*** This step is desktop only, skipped for tablet execution')
            return

        self.__class__.offers_module = self.site.home.offers
        offers_count = len(self.offers)
        expected_offers_count = len(self.available_cms_modules_and_offers.available_offers)
        self.assertEqual(offers_count, expected_offers_count,
                         msg=f'Actual offers count "{offers_count}" != Expected "{expected_offers_count}"')

        if len(self.offers) <= 1:
            self._logger.warning('*** Verifications below are possible only in case if there is more than 1 offer')
            return

        self.offers_module.mouse_over()

        # to make sure attribute style="transform: translate3d(-100%, 0px, 0px);" will appear
        if offers_count > 1 and self.offers_module.has_right_arrow(timeout=1):
            self.offers_module.right_arrow.click()

        current_offer = self.offers_module.get_active_offer_number()
        result = wait_for_result(lambda: self.offers_module.get_active_offer_number() == current_offer,
                                 poll_interval=0.1,
                                 timeout=5,
                                 name='Active offer to change in loop automatically')
        self.assertTrue(result, msg='Offer is not changed in loop automatically')

        # scroll to the first offer
        while self.offers_module.has_left_arrow(timeout=0):
            self.offers_module.left_arrow.click()
            sleep(0.5)  # to wait until new offer will be loaded

        self.wait_for_active_offer_number(expected_number='1')

        if offers_count > 1:
            self.assertFalse(self.offers_module.has_left_arrow(expected_result=False), msg='Left arrow is displayed')
            self.assertTrue(self.offers_module.has_right_arrow(), msg='Right arrow is not displayed')

            self.offers_module.right_arrow.click()

            self.wait_for_active_offer_number(expected_number='2')

            if offers_count > 2:
                self.assertTrue(self.offers_module.has_left_arrow(), msg='Left arrow is displayed')
                self.assertTrue(self.offers_module.has_right_arrow(), msg='Right arrow is not displayed')

                self.offers_module.right_arrow.click()

                self.wait_for_active_offer_number(expected_number='3')
            else:
                self.assertFalse(self.offers_module.has_right_arrow(expected_result=False), msg='Right arrow is displayed')
                self.assertTrue(self.offers_module.has_left_arrow(), msg='Left arrow is not displayed')
        else:
            self.assertFalse(self.offers_module.has_left_arrow(expected_result=False), msg='Left arrow is displayed')
            self.assertFalse(self.offers_module.has_right_arrow(expected_result=False), msg='Right arrow is displayed')
