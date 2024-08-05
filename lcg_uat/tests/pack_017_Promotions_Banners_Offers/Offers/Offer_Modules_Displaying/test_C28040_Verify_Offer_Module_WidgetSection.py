from time import sleep

import pytest

import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Offers.BaseOffersTest import BaseOffersTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.tablet
@pytest.mark.high
@pytest.mark.offers
@pytest.mark.promotions_banners_offers
@pytest.mark.screen_resolution
@vtest
class Test_C28040_Verify_Offer_Module_WidgetSection(BaseOffersTest):
    """
    TR_ID: C28040
    VOL_ID: C10700379
    NAME: Verify Offer Module Widget/Section.
    DESCRIPTION: This test case verifies Offer Module Widgets/Section and their content
    DESCRIPTION: **Note:**
    DESCRIPTION: This test case applicable only for Tablet and Desktop < 1100px.
    DESCRIPTION: AUTOTEST: [C527833]
    PRECONDITIONS: Load Oxygen app
    PRECONDITIONS: Make sure that several offer modules are created
    PRECONDITIONS: To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    minimum_allowed_width = 1099
    maximized_browser = False

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
            offer_module = next((module for module in all_cms_offer_modules if module.get('name') == f'{self.cms_config.constants.OFFER_MODULE_NAME} C28040'), None)
            if not offer_module:
                offer_module = self.cms_config.create_offer_module(name=f'{self.cms_config.constants.OFFER_MODULE_NAME} C28040')
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
        sleep(10)  # from cms offers module taking time to reflect in ui
        self.site.wait_content_state('Homepage')
        # set device resolution
        device_type = self.device_type
        if device_type == 'desktop':
            window_size = self.device.driver.get_window_size()
            self.device.set_viewport_size(width=self.minimum_allowed_width,
                                          height=window_size.get("height"))

    def test_001_verify_offer_modules_presence(self):
        """
        DESCRIPTION: Verify Offer Modules presence
        EXPECTED: * All available Offer Modules are present in the 3-rd column
        EXPECTED: * Every Offer Module is displayed in the separate section which is collapsible/expandable
        """
        self.__class__.offer_widget = self.get_widget(
            cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn'
        )
        right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(right_column_items, msg='Right menu items not found')
        self.assertTrue(self.offer_widget,
                        msg=f'Offers module was not found among "{right_column_items.keys()}" widgets')

        offers = self.offer_widget.items_as_ordered_dict
        self.assertTrue(offers, msg='No Offer Modules found')
        offer_names = offers.keys()
        for offer_name in offer_names:
            offer = offers[offer_name]
            offer.collapse()
            self.assertFalse(offer.is_expanded(expected_result=False),
                             msg=f'Offer {offer_name} is not collapsed after click')

            offer.expand()
            self.assertTrue(offer.is_expanded(), msg=f'Offer {offer_name} is not expanded after click')
            sleep(0.5)

    def test_002_verify_ordering_of_offer_modules(self):
        """
        DESCRIPTION: Verify ordering of Offer Modules
        EXPECTED: Offer Modules order corresponds to the set in CMS by drag-n-drop order on 'Offer Modules' page
        """
        self.__class__.offers = self.offer_widget.items_as_ordered_dict
        self.assertTrue(self.offers, msg='No Offer Modules found')
        cms_names = [module.upper() for module in self.available_cms_modules_and_offers.available_modules]
        module_names = [*self.offers]
        self.assertListEqual(cms_names, module_names,
                             msg=f'Available modules on the UI \n"{module_names} does not '
                             f'match modules from CMS \n"{cms_names}"')

    def test_003_verify_module_content(self):
        """
        DESCRIPTION: Verify Module content
        EXPECTED: Each Module consists of:
        EXPECTED: * Module title
        EXPECTED: * Related to particular Module Offers images
        EXPECTED: * Navigation pills
        """
        for module_name, module in self.offers.items():
            self.assertTrue(module_name, msg='Module title is empty')

            offers = module.items_as_ordered_dict
            self.assertTrue(offers, msg=f'No offers found for {module_name}')

            slide_dots = module.has_slide_dots()
            if len(offers) > 1:
                self.assertTrue(slide_dots, msg=f'Navigation dots are not shown for {module_name}')
            else:
                self.assertFalse(slide_dots, msg=f'Navigation dots are shown for {module_name}')

    def test_004_verify_module_title(self):
        """
        DESCRIPTION: Verify Module title
        EXPECTED: *   Module title is CMS-controllable ('title' field)
        EXPECTED: *   Module title should be not null or empty
        """
        # verified in step 3
        pass

    def test_005_verify_navigation_pills(self):
        """
        DESCRIPTION: Verify navigation pills
        EXPECTED: Navigation pills indicate displaying of current Offer image within particular Module
        """

        for module_name, module in self.offer_widget.items_as_ordered_dict.items():
            offers = module.items_as_ordered_dict
            self.assertTrue(offers, msg=f'No offers found for {module_name}')
            if len(offers) > 1:
                dots = module.slide_dots.items_as_ordered_dict
                self.assertTrue(dots, msg='No Slide dots found')

                # Works not correct, no way to automate

                # active_dot_index = next(
                #     (dot_index for dot_index, dot in dots.items() if dot.is_selected(timeout=0.3)), None)
                # self.assertIsNotNone(active_dot_index, msg=f'Active slide dot index for {module_name} was not found')
                # active_offer_index = next(
                #     (offer_index for offer_index, offer in offers.items() if offer.is_displayed(timeout=0)), None)
                # self.assertIsNotNone(active_offer_index, msg=f'Active slide index for {module_name} was not found')
                # self.assertEqual(active_offer_index, active_dot_index,
                #                  msg=f'Active offer index "{active_offer_index}" is not the same '
                #                      f'as active dot index "{active_dot_index}"')

    def test_006_verify_ordering_of_offer_images(self):
        """
        DESCRIPTION: Verify ordering of Offer Modules and Offer Images
        EXPECTED: Every Offer Module contains Offer images in order set via CMS
        """
        # note: destination url is the only one unique DOM attribute in the list of offers
        for module_name, module in self.offers.items():
            self.assertTrue(module_name, msg='Module title is empty')

            offers = module.items_as_ordered_dict
            self.assertTrue(offers, msg=f'No offers found for {module_name}')

            # note: destination url is the only one unique DOM attribute in the list of offers
            ui_urls = [offer.link.get_link() for offer_name, offer in offers.items()]
            cms_urls = [cms_offer.get('targetUri')
                        for cms_offer in self.available_cms_modules_and_offers.available_offers
                        if cms_offer.get('moduleName').upper() == module_name.upper()]

            self.assertListEqual(ui_urls, cms_urls, msg=f'List of UI URLs: \n{ui_urls} \n'
                                                        f'is not equal to list of CMS URLs: \n{cms_urls}')

    def test_007_verify_navigation_between_offers_images(self):
        """
        DESCRIPTION: Verify navigation between Offers images
        EXPECTED: User can scroll left or right within each Module
        EXPECTED: Images are displayed correctly
        EXPECTED: Maximum 3 offers images can be presented
        EXPECTED: Offers should be shown in continuous loop automatically
        """
        for module_name, module in self.offers.items():
            offers = module.items_as_ordered_dict
            self.assertTrue(offers, msg=f'No offers found for {module_name}')
            self.assertTrue(len(offers) <= 3, msg=f'There should be Maximum 3 offers, but {len(offers)} is shown')
            for offer_index, offer in offers.items():
                offer.scroll_to()
                link = offer.link
                self.assertTrue(any((link.has_image(), link.has_no_image())),
                                msg=f'Offer by index "{offer_index}" has neither picture nor placeholder')

    def test_009_create_some_new_modules_and_upload_images_of_different_height(self):
        """
        DESCRIPTION: Create some new modules and upload images of different height
        EXPECTED: Modules are created and visible on front-end
        """
        # can't upload images of different heights
        pass

    def test_009_verify_auto_adjust_of_the_module_to_the_images_height(self):
        """
        DESCRIPTION: Verify auto-adjusting of the module to the image's height
        EXPECTED: * Module height should auto-adjust to the image's size
        EXPECTED: NOTE: Uploading 2-3 images of different sizes to the same module is considered to be incorrect configuration. In such case module will adjust to the size of the picture, which is first received in the response
        """
        # can't upload images of different heights
        pass

    def test_010_click_tap_on_the_offer_image(self):
        """
        DESCRIPTION: Click/Tap on the Offer image
        EXPECTED: * User is redirected to the page, path for which is set in 'Target Uri' field in CMS
        EXPECTED: * Target Uri' supports internal (e.g. football/today) and external (begins with http/https) Uri's
        """
        module_name, module = list(self.offers.items())[-1]
        offers = module.items_as_ordered_dict
        self.assertTrue(offers, msg=f'No offers found for {module_name}')
        offer_index, offer = list(offers.items())[-1]
        offer.scroll_to()
        offer.link.click()
        self.site.wait_content_state_changed()
