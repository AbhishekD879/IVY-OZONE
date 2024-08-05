import pytest
import tests
from tests.base_test import vtest
from time import sleep
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2 - NA for QA2
# @pytest.mark.stg2 - NA for QA2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.sanity
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2381455_Verifiy_Main_Navigation_functionality_on_Homepage_for_Desktop(Common):
    """
    TR_ID: C2381455
    NAME: Verifiy Main Navigation functionality on Homepage for Desktop
    DESCRIPTION: This test case verifies Main Navigation functionality on Homepage for Desktop.
    DESCRIPTION: Covered in AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=735048&group_order=asc
    PRECONDITIONS: 1. Open Oxygen app
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Items from 'Main Navigation', 'Sub Navigation' and 'Left Navigation' menus are CMS configurable.
    PRECONDITIONS: 1. 'Main Navigation' menu is configured by GVС
    PRECONDITIONS: 2. 'Sub Navigation'  menu  is configured in CMS: Menus -> Header SubMenu
    PRECONDITIONS: 3. 'Left Navigation'  menu  is configured in CMS: Menus -> Sport Categories
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    expected_url = "https://" + tests.HOSTNAME + "/"
    sport_dict = {'Promos': 'Promotions',
                  'Horse Racing International Tote': 'International Tote',
                  'Virtuals': 'Virtual',
                  'TableTennis01': 'Table Tennis',
                  'C. League': 'UEFA CHAMPIONS LEAGUE',
                  'UEFA': 'UEFA CHAMPIONS LEAGUE',
                  'Water Surfing': 'AZ test'}

    def test_001_verify_universal_header_content_for_the_logged_out_user(self):
        """
        DESCRIPTION: Verify Universal Header content for the logged out user
        EXPECTED: Following elements are displayed:
        EXPECTED: * 'Coral'/'Ladbrokes' logo
        EXPECTED: * 'Main Navigation' menu configured by GVC
        EXPECTED: * 'Join' button
        EXPECTED: * 'Log in' button
        """
        self.site.wait_content_state(state_name='HomePage')
        self.device.refresh_page()
        self.assertTrue(self.site.header.is_displayed(), msg='"Main Navigation" header is not found')
        self.assertTrue(self.site.header.brand_logo.is_displayed(), msg='"Brand logo" is not found on header')
        self.assertTrue(self.site.header.join_us.is_displayed(), msg='Top menu does not contain "Join" option')
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='Top menu does not contain "Login" option')

    def test_002_verify_universal_header_content_for_the_logged_in_user(self):
        """
        DESCRIPTION: Verify Universal Header content for the logged in user
        EXPECTED: The following items are displayed in the Universal header:
        EXPECTED: * 'Coral'/'Ladbrokes' logo
        EXPECTED: * 'Main Navigation' menu configured by GVC
        EXPECTED: * 'Balance' item with currency symbol and user's balance amount
        EXPECTED: * 'Deposit' Button
        EXPECTED: * 'My Account' itemf
        """
        self.site.login()
        self.assertTrue(self.site.header.brand_logo.is_displayed(), msg='"Brand logo" is not found on header')
        self.assertTrue(self.site.header.user_panel.balance.is_displayed(),
                        msg='Top menu does not contain "Balance" option')
        self.assertTrue(self.site.header.user_panel.deposit_button.is_displayed(),
                        msg='"Deposit button" not found')
        self.assertTrue(self.site.header.right_menu_button.avatar_icon.is_displayed(),
                        msg='"My Account Avatar" not found')

    def test_003_verify_items_displaying_on_main_navigation_menu(self):
        """
        DESCRIPTION: Verify items displaying on 'Main Navigation' menu
        EXPECTED: * 'Main Navigation' menu consists of tabs, that are configured by GVC
        EXPECTED: * SPORTS
        EXPECTED: * GAMING
        EXPECTED: * SLOTS
        EXPECTED: * LIVE CASINO
        EXPECTED: * CASINO
        EXPECTED: * BINGO
        EXPECTED: * POKER
        EXPECTED: * PROMOTIONS
        EXPECTED: * EXCHANGE
        EXPECTED: * THE GRID (or CONNECT for Coral)
        EXPECTED: * 'Sports' tab is selected by default
        """
        # Not able to verify sports tab is selected by default.So,verifying left navigation menu as it is displayed only for sports tab
        left_menu = self.site.sport_menu.sport_menu_items_group('Main')
        self.assertTrue(left_menu, msg='"Sports tab is not selected by default')
        header = self.site.header.top_menu.items_as_ordered_dict
        self.assertTrue(header, msg=' Header menu has no items')
        for tab_name, tab in list(header.items()):
            header = self.site.header.top_menu.items_as_ordered_dict
            expected_window = self.device.driver.current_window_handle
            if tab_name != "SPORTS":
                header[tab_name].click()
                self.site.wait_content_state_changed()
            if tab_name == "GAMING":
                tab_name = "GAMES"
            elif tab_name == "CASINO":
                if self.brand == 'bma':
                    tab_name = "CORALCASINO"
                else:
                    tab_name = "LADBROKESCASINO"
            elif tab_name == "LIVE CASINO":
                tab_name = "LIVECASINO"
            elif tab_name == "OFFERS" or tab_name == "PROMOTIONS":
                tab_name = "PROMOTIONS"
            elif tab_name == "CONNECT" or tab_name == "THE GRID":
                if self.brand == 'bma':
                    tab_name = "RETAIL"
                else:
                    tab_name = "THEGRID"
            elif tab_name == "JACKPOTS":
                tab_name = "JACKPOT"
            elif tab_name == "SLOTS":
                tab_name = "SLOTS"
            elif tab_name == "BINGO":
                tab_name = "BINGO"
            elif tab_name == "POKER":
                tab_name = "POKER"
            elif tab_name == "EXCHANGE":
                tab_name = "EXCHANGE"
            elif tab_name == "RESPONSIBLE GAMBLING":
                tab_name = vec.bma.FOOTER_LINK_UNIQUE_WORD[11]
            actual_page_url = self.device.get_current_url()
            self.assertIn(tab_name.lower().replace(" ", ""), actual_page_url.lower(),
                          msg=f'header item "{tab_name.lower()}" is not present in "{actual_page_url}"')
            if tab_name == "SPORTS":
                self.site.wait_content_state(state_name="homepage")
            else:
                self.navigate_to_page(name='homepage')
                self.site.wait_content_state('homepage')
            self.assertEqual(self.device.driver.current_window_handle, expected_window,
                             msg=f'user is not on the same window')

    def test_004_click_on_some_item_from_main_navigation_menu(self):
        """
        DESCRIPTION: Click on some item from 'Main Navigation' menu
        EXPECTED: * All items are clickable
        EXPECTED: * Selected item is highlighted to keep user oriented with current location
        EXPECTED: * Appropriate page is opened
        EXPECTED: * 'Main Navigation' menu is still displayed
        """
        # Covered in step 3

    def test_005_verify_items_displaying_on_sub_navigation_menu(self):
        """
        DESCRIPTION: Verify items displaying on 'Sub Navigation' menu
        EXPECTED: * 'Sub Navigation' menu consists of tabs, that are CMS configurable:
        EXPECTED: * Home
        EXPECTED: * Promotions
        EXPECTED: * In-Play
        EXPECTED: * Football
        EXPECTED: * Horse Racing
        EXPECTED: * Tennis
        EXPECTED: * Build Your Bet
        EXPECTED: * Virtual Sports
        EXPECTED: * #Yourcall
        EXPECTED: * Greyhounds
        EXPECTED: * News & Blogs
        EXPECTED: * None tab is not selected by default
        """
        sports = self.site.header.sport_menu.items_as_ordered_dict
        self.assertTrue(sports, msg='Header sub menu has no items')
        for sport_name, sport in list(sports.items()):
            sports = self.site.header.sport_menu.items_as_ordered_dict
            if sport_name in ['HOME', 'RACING SUPER SERIES', 'GRAND NATIONAL', '1-2-FREE', 'GREYHOUNDS', 'CORRECT 4', 'NEWS & BLOGS', '5-A-SIDE', 'AM.FOOTBALL']:
                continue
            else:
                sports[sport_name].click()
                self.site.wait_splash_to_hide()
                selected_sport = sports[sport_name].is_selected()
                self.assertTrue(selected_sport, msg=f'{sport_name} is not selected')

    def test_006_click_on_some_item_from_sub_navigation_menu(self):
        """
        DESCRIPTION: Click on some item from 'Sub Navigation' menu
        EXPECTED: * All items are clickable
        EXPECTED: * Selected item is highlighted to keep user oriented with current location
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        EXPECTED: * 'Sub Navigation' menu is still displayed
        """
        # Covered in step 5

    def test_007_verify_the_left_navigation_menu_displaying(self):
        """
        DESCRIPTION: Verify the 'Left Navigation' menu displaying
        EXPECTED: * 'Left Navigation' menu is displayed on every page across the app
        EXPECTED: * 'A-Z Sports' inscription is displayed at the top of 'Left Navigation' menu
        EXPECTED: * 'Left Navigation' menu consists of CMS configurable items that are displayed vertically
        """
        # Covered in step 8

    def test_008_select_some_item_on_left_navigation_menu(self):
        """
        DESCRIPTION: Select some item on 'Left Navigation' menu
        EXPECTED: * All items are clickable
        EXPECTED: * Selected item is highlighted to keep user oriented with current location
        EXPECTED: * Appropriate page is opened in the same or different tab depends on CMS configuration
        EXPECTED: * URL is the same as set in CMS
        EXPECTED: * 'Left Navigation' menu is still displayed
        EXPECTED: * All items within 'Left Navigation' menu are sorted in alphabetical order
        """
        left_menu = self.site.sport_menu.sport_menu_items_group('Main')
        self.assertTrue(left_menu, msg='"Left Navigation" menu not found')
        self.assertEqual(left_menu.name, vec.sb_desktop.AZ_SPORTS,
                         msg=f'Actual Name of left menu is: "{left_menu.name}" '
                             f'not: "{vec.sb_desktop.AZ_SPORTS}" as expected')
        allsports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
        self.assertListEqual([allsports.keys()], sorted([allsports.keys()]),
                             msg=f'Sports are not sorted in alphabetical A-Z order:'
                                 f'\nActual: {[allsports.keys()]}\nExpected: {sorted([allsports.keys()])}')
        sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict.keys()
        self.assertTrue(sports, msg='No sports found in "A-Z Sports" section')
        for sport in sports:
            az_sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(az_sports, msg='No sports found in "A-Z Sports" section')
            if sport in ['Correct 4', 'Euro 2020', 'Gaming', 'C.League', 'News & Blogs', 'Grand National', 'Live Casino', 'Responsible Gambling', 'Sports Roulette', 'Roulette', 'Slots', 'The Grid', 'Racing Super Series',
                         'Water Surfing', 'Matchday Rewards', 'Poker']:
                continue
            else:
                az_sports[sport].click()
                sleep(2)
                # redirect to homepage when no events are found for sport
                if self.device.get_current_url() == self.expected_url:
                    sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict.keys()
                    continue
                actual_header = self.site.sports_page.header_line.page_title.title
                if sport in self.sport_dict.keys():
                    self.assertEqual(self.sport_dict[sport].upper(), actual_header.upper(),
                                     msg=f'sport {sport.upper()} is not available in {actual_header}')
                else:
                    self.assertEqual(sport.upper(), actual_header.upper(),
                                     msg=f'sport {sport.upper()} is not available in {actual_header}')
                left_menu = self.site.sport_menu.sport_menu_items_group('Main')
                self.assertTrue(left_menu, msg=f'Left Navigation Menu not displayed on sport: "{sport}" page')
