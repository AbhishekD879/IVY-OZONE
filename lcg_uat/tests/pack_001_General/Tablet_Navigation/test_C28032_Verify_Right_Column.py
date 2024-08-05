import pytest
import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.Offers.BaseOffersTest import BaseOffersTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.tst2 # This functionality is no longer applicable from release 108
# @pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
# @pytest.mark.medium
# @pytest.mark.navigation
# @pytest.mark.tablet_only
# @pytest.mark.offers
# @pytest.mark.widgets
# @pytest.mark.slow
# @pytest.mark.timeout(1200)
@pytest.mark.na
@vtest
class Test_C28032_Verify_Right_Column(BaseOffersTest):
    """
    TR_ID: C28032
    VOL_ID: C10548295
    NAME: Verify Right Column
    DESCRIPTION: This test case verifies Right Column
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: *   BMA-7842 RIGHT COLUMN: Implementing Right column widget
    """
    maximized_browser = False
    keep_browser_open = True
    device_name = tests.tablet_default
    betslip_widget_name, offers_widget_name = None, None
    allow_dict = {
        'ALL SPORTS': 'AllSports',
        'CRICKET': 'CRICKET',
        'HORSE RACING': 'Horseracing',
        'FOOTBALL': 'FOOTBALL',
        'LOTTO': 'LOTTO',
        'IN-PLAY': 'INPLAY',
        'TENNIS': 'TENNIS',
        'VIRTUAL': 'VirtualSports',
        'GREYHOUNDS': 'GREYHOUNDRACING',
        'AUSSIERULES': 'AUSSIERULES',
        'BASKETBALL': 'BASKETBALL'
    }
    available_widgets = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get Betslip/Offers widget names
        """
        cms_banners = self.get_initial_data_system_configuration().get('DynamicBanners')
        if not cms_banners:
            self.cms_config.get_system_configuration_item('DynamicBanners')
        # add offer if it is not present
        available_modules, available_offers = self.get_available_cms_modules_and_offers(device='tablet')
        if tests.settings.cms_env != 'prd0' and (not available_modules or not available_offers):
            all_cms_offer_modules = self.cms_config.get_offer_modules()
            offer_module = next((module for module in all_cms_offer_modules if module.get('name') == f'{self.cms_config.constants.OFFER_MODULE_NAME} C28032'), None)
            if not offer_module:
                offer_module = self.cms_config.create_offer_module(name=f'{self.cms_config.constants.OFFER_MODULE_NAME} C28032')
            offer_module_id = offer_module.get('id')
            self.cms_config.add_offer(offer_module_id=offer_module_id)
        elif tests.settings.cms_env == 'prd0' and (not available_modules or not available_offers):
            raise CmsClientException('No available offers configured in CMS')

        self.__class__.betslip_widget_name = self.cms_config.constants.BETSLIP_WIDGET_NAME

        self.__class__.available_widgets.append(self.betslip_widget_name)

        self.__class__.offers_widget_name = self.get_filtered_widget_name(
            cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn')

        cms_widgets = self.cms_config.get_widgets()
        offer_widget = next((widget for widget in cms_widgets if widget['title'] == self.offers_widget_name.title()), None)
        self.__class__.offer_tablet_status = offer_widget.get('showOnTablet')
        if self.__class__.offer_tablet_status:
            self.__class__.available_widgets.append(self.offers_widget_name)

    def test_001_load_invictus_app_on_tablet_device(self):
        """
        DESCRIPTION: Load Invictus app on tablet device
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_verify_right_column_presence(self):
        """
        DESCRIPTION: Verify Right Column presence
        EXPECTED: Right Column is applicable to all sportsbook pages
        """
        self.__class__.right_column_items = self.site.right_column.items_as_ordered_dict
        self.assertTrue(self.right_column_items, msg='Right column items are not shown')
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        for item_name, item in all_items.items():
            if item_name.strip() not in self.allow_dict.keys():
                self._logger.warning(f'*** Item "{item_name}" skipped')
                continue
            self.site.wait_content_state('HomePage', timeout=3)
            self._logger.info(f'*** Navigating to "{item_name}"')
            self.site.home.menu_carousel.click_item(item_name)
            self.site.wait_content_state(self.allow_dict[item_name], timeout=3)
            self.assertTrue(self.site.right_column.items_as_ordered_dict, msg='Right column items are not shown')
            self.site.back_button_click()
            self.site.wait_content_state('HomePage', timeout=3)

    def test_003_verify_right_column_content(self):
        """
        DESCRIPTION: Verify Right Column content
        EXPECTED: Right Column consists of next elements:
        EXPECTED: *   BetSlip widget;
        EXPECTED: *   CMS-controlled Offer Module widgets.
        """
        for widget in self.available_widgets:
            self.assertIn(widget, self.right_column_items,
                          msg=f'Widget name "{widget}" not found in '
                              f'Right column widgets "{self.right_column_items.keys()}"]')
        if self.offer_tablet_status:
            offers_widget = self.get_widget(cms_type=self.cms_config.constants.OFFERS_WIDGET_TYPE, column='rightColumn')
            offers_widget.scroll_to()
            offers_widget.expand()
            offers = offers_widget.items_as_ordered_dict
            self.assertTrue(offers, msg='Offer module widget is empty')

    def test_004_verify_fixed_width_of_each_widget(self):
        """
        DESCRIPTION: Verify fixed width of each widget
        EXPECTED: Width for each widgets is 320 px
        """
        for name, item in self.right_column_items.items():
            self.assertEqual(item.size['width'], 320,
                             msg=f'Widget "{name}" width "{item.size["width"]} does not match expected width 290px')

    def test_005_rotate_device(self):
        """
        DESCRIPTION: Rotate device
        """
        self.device.rotate_90()

    def test_006_repeat_steps__2_4(self):
        """
        DESCRIPTION: Repeat steps # 2-4
        """
        self.test_002_verify_right_column_presence()
        self.test_003_verify_right_column_content()
        self.test_004_verify_fixed_width_of_each_widget()
