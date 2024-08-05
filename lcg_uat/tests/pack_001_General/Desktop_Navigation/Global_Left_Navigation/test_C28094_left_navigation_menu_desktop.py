import pytest

import tests
from tests.base_test import vtest
from time import sleep
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.desktop
#@pytest.mark.desktop_only
@pytest.mark.left_menu
@pytest.mark.cms
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-52249')
@vtest
class Test_C28094_Verify_Desktop_Left_Navigation_Menu(BaseUserAccountTest):
    """
    TR_ID: C28094
    VOL_ID: C9689875
    NAME: Verify Global Left Navigation Menu functionality for Desktop
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    sports_name = ['football', 'basketball', 'american-football']
    az_sports_menu_title = 'A-Z Sports'
    skip_items = ['1']

    def test_001_load_oxygen_application_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen application on Desktop
        EXPECTED: Homepage is loaded
        """
        self.site.wait_content_state('HomePage', timeout=3)

    def test_002_check_the_global_left_navigation_view(self):
        """
        DESCRIPTION: Verify the 'Left Navigation' menu displaying
        EXPECTED:  - 'A-Z Sports' inscription is displayed at the top of 'Left Navigation' menu
        """
        left_menu = self.site.sport_menu.sport_menu_items_group('Main')
        self.assertTrue(left_menu, msg='"Left Navigation" menu not found')
        self.assertEqual(left_menu.name, self.az_sports_menu_title,
                         msg=f'Actual inscription of left menu is: "{left_menu.name}" '
                             f'not: "{self.az_sports_menu_title}" as expected')

    def test_003_select_first_five_items_from_az_menu(self):
        """
        DESCRIPTION: Select some item on 'Left Navigation' menu
        EXPECTED: - All items are clickable
        EXPECTED: - Selected item is highlighted to keep user oriented with current location
        EXPECTED: - Appropriate page is opened
        EXPECTED: - URL is the same as set in CMS
        EXPECTED: - 'Left Navigation' menu is still displayed
        """
        az_links = self.site.sport_menu.sport_menu_items_group('AZ').items_as_ordered_dict
        self.assertTrue(az_links, msg='No one item found in "A-Z Menu" section')

        sports = self.cms_config.get_left_menu_items()
        for sport in sports:
            if sport.upper() == 'FANZONE':
                sports.remove(sport)
                break
        self.assertListEqual(list(az_links.keys()), sports,
                             msg='Actual menu items order: \n["%s"] \nExpected: \n["%s"]'
                                 % ('", "'.join(az_links.keys()), '", "'.join(sports)))
        # At first iteration we have _content_state_name = '' and wait_content_state_changed() method pass
        # after 0 seconds without waiting for real content changed,
        # so need to set default _content_state_name as 'HomePage' not to fail test on first iteration
        self.site._content_state_name = 'HomePage'
        for az_link_name, az_link in list(az_links.items())[1:6]:
            if az_link_name in self.skip_items:
                continue
            item_link = az_link.link.get_link()
            az_link.click()
            sleep(3)
            title_text = self.site.contents.content_title_text
            link_name = az_link_name.upper() if self.brand == 'bma' else az_link_name
            if not "competition" in link_name:
                self.assertIn(link_name, title_text, msg=f'Selected sport: "{link_name}" page not opened, '
                                                         f'current opened page is: "{title_text}"')
                self.assertTrue(az_links[az_link_name].link.is_selected(),
                                msg=f'Left A-Z Menu link "{az_link_name}" not active after click')
                self.assertIn(item_link, self.device.get_current_url(),
                              msg=f'Current opened URL is: "{self.device.get_current_url()}" '
                                  f'not contains expected link: "{item_link}"')
                self.assertTrue(self.site.sport_menu.sport_menu_items_group('Main').is_displayed(),
                                msg=f'Left Navigation Menu section not displayed after click on item: {az_link_name}')

    def test_004_navigate_across_application_verify_left_menu_displaying(self):
        """
        DESCRIPTION: Navigate across the application and verify Left Navigation Menu displaying
        EXPECTED: Left Navigation Menu is permanently fixed and displayed throughout Desktop View Sportsbook
        """
        for sport in self.sports_name:
            self.navigate_to_page(sport)
            self.assertTrue(self.site.sport_menu.is_displayed(),
                            msg=f'Left Navigation Menu not displayed on sport: "{sport}" page')
            self.assertTrue(self.site.sport_menu.sport_menu_items_group('Main').is_displayed(),
                            msg=f'Left Navigation Menu section not found in on sport: "{sport}" page')
