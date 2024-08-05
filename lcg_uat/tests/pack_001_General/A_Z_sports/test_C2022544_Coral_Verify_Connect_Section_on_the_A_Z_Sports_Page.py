import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.base_test import BaseTest
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.cms_client_exception import CmsClientException


#@pytest.mark.crl_tst2
#@pytest.mark.crl_stg2  # Coral only
@pytest.mark.crl_hl
#@pytest.mark.crl_prod
@pytest.mark.cms
@pytest.mark.all_sports
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.mobile_only
@pytest.mark.safari
@vtest
@pytest.mark.connect_descoped
class Test_C2022544_Coral_Verify_Connect_Section_on_the_A_Z_Sports_Page(BaseTest):
    """
    TR_ID: C2022544
    VOL_ID: C9689871
    NAME: Coral Verify Connect Section on the A-Z Sports Page
    DESCRIPTION: This test case verifies 'Сonnect' section availability on the 'A-Z' page after opening via footer menu and via pressing the button 'A-Z' on the Sports menu ribbon
    PRECONDITIONS: Make sure Connect section in A-Z is turned on in CMS: System configuration -> Connect -> menu
    PRECONDITIONS: A user can be logged in/logged out
    PRECONDITIONS: CMS:
    PRECONDITIONS: https://CMS_ENDPOINT -> Chose 'sportsbook' channel -> 'Menus' -> 'Connect Menus'
    PRECONDITIONS: multi channel user: bluerabbit/ password
    PRECONDITIONS: in-shop user: 5000000000992144/ 1234
    """
    keep_browser_open = True
    connect_section_name = vec.retail.TITLE

    def test_001_load_sportsbook_application_and_tap_all_sports_button_on_the_footer_menu(self):
        """
        DESCRIPTION: Load sportsbook application and tap 'All Sports' button on the footer menu
        EXPECTED: 'All Sports' page is shown
        """
        footer_menu = self.cms_config.get_initial_data(cached=True).get('footerMenu')
        if not footer_menu:
            raise CmsClientException('Footer menu is not configured')
        self.__class__.all_sports_footer_item = next((item['linkTitle'] for item in footer_menu if 'az-sports' in item['targetUri']), None)
        if not self.all_sports_footer_item:
            raise CmsClientException('"All Sports" is not configured for "Footer Menu"')
        footer_item_all_sports = self.all_sports_footer_item.upper()
        self.__class__.all_sports_footer_button = \
            self.site.navigation_menu.get_footer_menu_item(name=footer_item_all_sports)
        self.assertTrue(self.all_sports_footer_button.is_displayed(), msg='"All Sports" button is not displayed')

        self.all_sports_footer_button.click()
        self.site.wait_content_state(state_name='AllSports')

    def test_002_scroll_down_the_list_of_sports_to_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Scroll down the list of sports to the bottom of the page
        EXPECTED: * There is the section 'Connect' at the bottom of the page
        EXPECTED: * The name of the section is 'Connect'
        EXPECTED: * Section contains list of items (that corresponds to CMS configurations) (one exception: 'User connect online' item is shown only for Logged in In-Shop user)
        """
        self.__class__.cms_connect_items = [item['linkTitle'] for item in
                                            self.cms_config.get_connect_menu_items()
                                            if all((not item['disabled'],
                                                    item['linkTitle'],
                                                    item['inApp'],
                                                    item['showItemFor'] == '' or item['showItemFor'].lower() == 'both'))]

        self.__class__.connect_section = self.site.all_sports.connect_section.items_as_ordered_dict
        self.assertTrue(self.connect_section, msg='No items found in "Connect" section')

        connect_section_name = self.site.all_sports.connect_section.name
        self.assertEqual(connect_section_name, self.connect_section_name,
                         msg=f'Actual section name: {connect_section_name} '
                         f'is not as expected: {self.connect_section_name}')

        connect_section_items = list(self.connect_section.keys())
        self.assertListEqual(connect_section_items, self.cms_connect_items,
                             msg=f'Actual menu items list: {connect_section_items} '
                             f'is not as expected: {self.cms_connect_items}')

    def test_003_tap_every_icon_from_connect_section(self):
        """
        DESCRIPTION: Tap every icon from 'Connect' section ('Use Connect Online', 'Shop Exclusive Promos', 'Shop Bet Tracker', 'Football Bet Filter', 'Saved Bet Filter', 'Shop Locator')
        EXPECTED: User is redirected to the appropriate page every time.
        """
        cms_connect_items_uri = [item['targetUri'] for item in
                                 self.cms_config.get_connect_menu_items()
                                 if all((not item['disabled'],
                                         item['linkTitle'],
                                         item['inApp'],
                                         item['showItemFor'] == '' or item['showItemFor'].lower() == 'both'))]

        for index, _ in enumerate(list(self.connect_section.items())):
            connect_section = self.site.all_sports.connect_section.items_as_ordered_dict
            item_name, item = list(connect_section.items())[index]
            self._logger.debug(f'Opening menu item {item_name}')
            item.item_icon.click()
            result = wait_for_result(lambda: cms_connect_items_uri[index] in self.device.get_current_url(),
                                     name=f'Navigate to "{cms_connect_items_uri[index]}"', timeout=3)
            self.assertTrue(result, msg=f'User is redirected to the wrong page: "{self.device.get_current_url()}", '
                                        f'expected is: "{cms_connect_items_uri[index]}"')
            # For now "You're Betting dialog" is switched off
            # if self.cms_connect_items[index] == 'Football Bet Filter':
            #     opened_dialog = self.site.wait_for_dialog('YOU\'RE BETTING', timeout=10)
            #     opened_dialog.close_dialog()
            # else:
            # self.assertTrue(result, msg=f'User is redirected to the wrong page: "{url}", expected is: "{item_uri}"')
            self.site.close_all_dialogs(async_close=False, timeout=3)
            self.all_sports_footer_button.click()

    def test_004_verify_connect_sections_items_ordering(self):
        """
        DESCRIPTION: Verify 'Connect' section's items ordering.
        EXPECTED: 'Connect' section's items are ordered as configured in CMS:
        EXPECTED: Menu -> Connect menu
        """
        connect_section_names = list(self.connect_section.keys())
        self.assertListEqual(connect_section_names, list(self.cms_connect_items),
                             msg=f'Connect sections are not ordered as in CMS:'
                                 f'\nActual: {connect_section_names}'
                                 f'\nExpected: {self.cms_connect_items}')
