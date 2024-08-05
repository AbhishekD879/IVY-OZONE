from time import sleep

import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
import voltron.environments.constants as vec
from voltron.utils.content_manager import ContentManager
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.cms
@pytest.mark.all_sports
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.mobile_only
@pytest.mark.safari
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-1847')
class Test_C28387_Verify_All_Sports_Page(BaseUserAccountTest):
    """
    TR_ID: C28387
    NAME: Verify All Sports Page
    DESCRIPTION: This test case verifies functionality of 'A-Z' page which can be opened via footer menu and via pressing the button 'A-Z' on the Sport menu ribbon
    PRECONDITIONS: 1. Sports are configured in CMS: Sports Pages > Sport Categories
    PRECONDITIONS: 2. 'Top Sports' are configured in CMS for some Sports
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Is Top Sport' check box is checked)
    PRECONDITIONS: 3. 'A-Z Sports' is configured in CMS for some Sports
    PRECONDITIONS: (Sports Pages > Sport Categories > <Sport> 'Show in AZ' check box is checked)
    PRECONDITIONS: 4. Oxygen application is loaded
    """
    keep_browser_open = True
    sport_name = 'Football'
    all_sports_page = 'az-sports'
    all_sports_page_name = vec.sb.ALL_SPORTS

    def fanzone_subscription(self):
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, timeout=30)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        wait_for_result(lambda: dialog_confirm.confirm_button.is_displayed(), timeout=10,
                        name='"CONFIRM" button to be displayed.')
        dialog_confirm.confirm_button.click()
        sleep(7)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5,
                        name='"EXIT" button to be displayed.')
        dialog_alert.exit_button.click()

    def test_001_open_all_sports_page(self):
        """
        DESCRIPTION: Open 'All Sports' page
        EXPECTED: *  'All Sports' page is opened
        EXPECTED: *  The following sections are present: Top Sports, A-Z
        """
        if self.brand == 'ladbrokes' :
            self.fanzone_subscription()
        self.navigate_to_page(name=self.all_sports_page)
        az_sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
        self.assertTrue(az_sports, msg='No sports found in "A-Z Sports" section')

        top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(top_sports, msg='No sports found in "Top Sports" section')

    def test_002_verify_page_header_and_back_button(self):
        """
        DESCRIPTION: Verify page header and Back button
        EXPECTED: *   Page header is 'All Sports'
        EXPECTED: *   Tap on Back button gets user back to previous page
        """
        page_title = self.site.all_sports.header_line.page_title.title
        self.assertEqual(page_title, self.all_sports_page_name,
                         msg=f'Page header: {page_title} is not as expected: {self.all_sports_page_name}')

        self.site.back_button_click()
        self.site.wait_content_state(state_name='HomePage')

    def test_003_verify_top_sports_section(self):
        """
        DESCRIPTION: Verify 'Top Sports' section
        EXPECTED: *  Section is displayed only if Top Sports are configured in CMS
        EXPECTED: *  Sports are displayed in a list view
        EXPECTED: *  No icon is displayed next to a Sport name
        EXPECTED: *  Only Sports with the CMS setting 'is Top Sport?' are shown in this section
        """
        if self.device_type != 'mobile':
            self.navigate_to_page(name=self.all_sports_page)
        else:
            footer_menu = self.cms_config.get_initial_data(cached=True).get('footerMenu')
            if not footer_menu:
                raise CmsClientException('Footer menu is not configured')
            self.__class__.all_sports_footer_item = next(
                (item['linkTitle'] for item in footer_menu if 'az-sports' in item['targetUri']), None)
            if not self.all_sports_footer_item:
                raise CmsClientException('"All Sports" is not configured for "Footer Menu"')
            footer_item_all_sports = self.all_sports_footer_item if self.brand != 'bma' else self.all_sports_footer_item.upper()
            self.__class__.all_sports_footer_button = \
                self.site.navigation_menu.get_footer_menu_item(name=footer_item_all_sports)
            self.assertTrue(self.all_sports_footer_button.is_displayed(), msg='"All Sports" button is not displayed')
            self.all_sports_footer_button.click()
        self.site.wait_content_state(state_name='AllSports')

        self.__class__.cms_top_sports = [sport['imageTitle'].strip() for sport in self.cms_config.get_sport_categories()
                                         if all((not sport['disabled'],
                                                 sport['imageTitle'],
                                                 sport['hasEvents'],
                                                 sport['isTopSport']))]

        top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(top_sports, msg='No sports found in "Top Sports" section')

        for sport_name, sport in top_sports.items():
            self.assertFalse(sport.item_icon.is_displayed(),
                             msg=f'Sport icon for "{sport.item_name}" should not be displayed')

        self.__class__.top_sports_names = list(top_sports.keys())
        self.assertListEqual(self.top_sports_names, self.cms_top_sports,
                             msg=f'Sports are not sorted in alphabetical A-Z order:'
                             f'\nActual: {self.top_sports_names}\nExpected: {self.cms_top_sports}')

    def test_004_tap_on_any_sport_from_top_sports_section(self):
        """
        DESCRIPTION: Tap on any sport from 'Top Sports' section
        EXPECTED: Corresponding Sport Landing page is opened
        """
        top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(top_sports, msg='No top sports items found')
        sport_name, sport_value = next(((sport_name, sport_value) for sport_name, sport_value in top_sports.items()
                                        if sport_name.lower() in ContentManager().pages.keys()), (None, None))
        self.assertTrue(sport_name, msg=f'No known sport found in top menu "{top_sports.keys()}"')
        sport_value.click()
        self.site.wait_content_state(state_name=sport_name)

    def test_005_verify_top_sports_ordering(self):
        """
        DESCRIPTION: Verify 'Top Sports' ordering
        EXPECTED: Top Sports are ordered like configured in CMS (configurations made by dragging)
        """
        self.site.back_button_click()
        self.site.wait_content_state(state_name='AllSports')

        top_sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
        self.assertTrue(top_sports, msg='No top sports items found')

        self.assertListEqual(self.top_sports_names, self.cms_top_sports,
                             msg=f'Sports are not sorted in alphabetical A-Z order:'
                                 f'\nActual: {self.top_sports_names}\nExpected: {self.cms_top_sports}')

    def test_006_verify_az_section(self):
        """
        DESCRIPTION: Verify 'A-Z' section
        EXPECTED: *  Title is 'A-Z'
        EXPECTED: *  There are Sport name and icon
        EXPECTED: *  Only Sports with the CMS setting 'Show in A-Z' are shown in this section
        """
        cms_az_sports = [sport['imageTitle'].strip() for sport in self.cms_config.get_sport_categories()
                         if all((not sport['disabled'],
                                 sport['imageTitle'],
                                 sport['hasEvents'],
                                 sport['showInAZ']))]

        self.__class__.az_sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
        self.assertTrue(self.az_sports, msg='No sports found in "A-Z Sports" section')

        for sport_name, sport in self.az_sports.items():
            self.assertTrue(sport.item_icon.is_displayed(),
                            msg=f'Sport icon for "{sport.item_name}" is not displayed')
            self.assertIn(sport_name, cms_az_sports,
                          msg=f'Sport {sport_name} should not be shown in the list')

    def test_007_verify_sports_ordering(self):
        """
        DESCRIPTION: Verify sports ordering
        EXPECTED: All sports are shown in alphabetical A-Z order
        """
        all_sports_names = list(self.az_sports.keys())
        self.assertListEqual(all_sports_names, sorted(all_sports_names),
                             msg=f'Sports are not sorted in alphabetical A-Z order:'
                                 f'\nActual: {all_sports_names}\nExpected: {sorted(all_sports_names)}')

    def test_008_tap_any_sport_item(self):
        """
        DESCRIPTION: Tap any sport item
        EXPECTED: Sport Landing page is opened
        """
        # TODO: https://jira.egalacoral.com/browse/VOL-1847
        self.az_sports[self.sport_name].click()
        self.site.wait_content_state(state_name=self.sport_name)
