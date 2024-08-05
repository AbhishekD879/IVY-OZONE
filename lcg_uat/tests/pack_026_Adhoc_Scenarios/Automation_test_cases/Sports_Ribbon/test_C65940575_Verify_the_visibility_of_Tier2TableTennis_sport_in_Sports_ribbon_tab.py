import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.menu_ribbon
@pytest.mark.mobile_only
@vtest
class Test_C65940575_Verify_the_visibility_of_Tier2TableTennis_sport_in_Sports_ribbon_tab(Common):
    """
    TR_ID: C65940575
    NAME: Verify the visibility of Tier2(TableTennis) sport in Sports ribbon tab
    DESCRIPTION: This test case is to validate About  sports ribbon tab as per cms configuration
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Configuration for  Table tennis in LHN
    PRECONDITIONS: sport page->sport categories.
    PRECONDITIONS: 3)Click on Table tennis sport category
    PRECONDITIONS: 4)Enter All mandatory Fields and click on save button:
    PRECONDITIONS: -Image title
    PRECONDITIONS: -Category id
    PRECONDITIONS: -SS category id
    PRECONDITIONS: -Target URI
    PRECONDITIONS: -Tier
    PRECONDITIONS: 5)Check below required fields in general sport configuration:
    PRECONDITIONS: -Active
    PRECONDITIONS: -In App
    PRECONDITIONS: -Show In Play
    PRECONDITIONS: -Show in Sports Ribbon
    PRECONDITIONS: -Show in AZ
    PRECONDITIONS: -And Enter below required fields
    PRECONDITIONS: -Title
    PRECONDITIONS: -Category Id
    PRECONDITIONS: -SS Category Code
    PRECONDITIONS: -Target Uri
    PRECONDITIONS: -Odds card header type
    PRECONDITIONS: -SVG Icon
    PRECONDITIONS: -Filename
    PRECONDITIONS: -Icon
    PRECONDITIONS: -Segmentation
    """
    keep_browser_open = True
    title = vec.olympics.TABLETENNIS

    def get_sport_fe(self, expected_result=True, haul=5):
        title = self.title if self.site.brand == 'ladbrokes' else self.title.upper()
        sport = wait_for_cms_reflection(
            lambda: self.site.home.menu_carousel.items_as_ordered_dict.get(title), ref=self, timeout=5, haul=haul,
            refresh_count=3,
            expected_result=expected_result
        )
        if sport:
            sport.scroll_to()
        return sport

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Sports pages > Sports category
        """
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'].strip().upper() == self.title.upper():
                self.__class__.sport = self.cms_config.update_sport_category(sport_category_id=sport['id'],
                                                                             disabled=False, showInHome=True)
                break
        else:
            raise VoltronException(f'{vec.olympics.TABLETENNIS} sport not found in sports categories')

    def test_001_launch_coralladbrokes_application(self):
        """
        DESCRIPTION: Launch Coral/Ladbrokes Application.
        EXPECTED: Application should be launched
        EXPECTED: Home page should be opened and sports ribbon tab should be displayed.
        """
        self.site.wait_content_state("homepage")
        self.assertTrue(self.site.home.menu_carousel.is_displayed(),
                        msg=f'sport category "{self.title}" is not appearing, actual categories "{self.site.home.menu_carousel.items_as_ordered_dict.keys()}"')

    def test_002_verify_presence_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify presence of Sports ribbon tab
        EXPECTED: Sports ribbon tab is applicable for Both logged in and Logged out user.
        """
        self.site.login()
        self.assertTrue(self.site.home.menu_carousel.is_displayed(),
                        msg=f'sport category "{self.title}" is not appearing, actual categories "{self.site.home.menu_carousel.items_as_ordered_dict.keys()}"')

    def test_003_verify_scrollability_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Scrollability of sports ribbon tab
        EXPECTED: Should be left and right scrollable and Image alignment should not be disturbed while scrolling .
        """
        # This step is covered in C65940577

    def test_004_verify__table_tennis_sport_icon_is_displayed_and_clickable(self):
        """
        DESCRIPTION: Verify  Table tennis sport icon is displayed and clickable
        EXPECTED: Table tennis sport icon should be displayed and clickable
        """
        # covered in step 008

    def test_005_verify_the_order_of_sport_by_using_drag_and_drop_in_cms(self):
        """
        DESCRIPTION: Verify the order of sport by using drag and drop in cms
        EXPECTED: Sport order should be changed after drag and drop in cms and same should be shown in Sport ribbon tab
        """
        # This tep is covered in test case C65940577

    def test_006_verify__by_unchecking_show_in_sports_ribbon_tab_and_check_active_checkbox_in_cms(self):
        """
        DESCRIPTION: Verify  By unchecking "show in sports ribbon tab" and check "Active" checkbox in cms
        EXPECTED: Table tennis sport should not display in Sports ribbon tab
        """
        self.assertTrue(self.get_sport_fe(),
                        msg=f'sport category "{self.title}" is not appearing, actual categories "{self.site.home.menu_carousel.items_as_ordered_dict.keys()}"')

        self.cms_config.update_sport_category(sport_category_id=self.sport['id'], showInHome=False)
        self.assertFalse(self.get_sport_fe(expected_result=False),
                         msg=f'sport category "{self.title}" is appearing, actual categories "{self.site.home.menu_carousel.items_as_ordered_dict.keys()}"')

    def test_007_verify_by_uncheck_activecheckbox_and_check_show_in_sports_ribbon_tab_in_cms(self):
        """
        DESCRIPTION: Verify By uncheck "Active"checkbox and check "show in sports ribbon tab" in cms
        EXPECTED: Table tennis sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id=self.sport['id'], disabled=True, showInHome=True)
        wait_for_haul(3)
        self.assertFalse(self.get_sport_fe(expected_result=False),
                         msg=f'sport category "{self.title}" is appearing, actual categories "{self.site.home.menu_carousel.items_as_ordered_dict.keys()}"')

    def test_008_verify_by_click_on_table_tennis_icon_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify by Click on Table tennis Icon in sport ribbon tab
        EXPECTED: Should redirect to Matches Tab of Table tennis page.
        EXPECTED: By Default Matches tab should be opened.
        """
        self.cms_config.update_sport_category(sport_category_id=self.sport['id'], disabled=False, showInHome=True)
        table_tennis = self.get_sport_fe()
        self.assertTrue(table_tennis,
                        msg=f'sport category "{self.title}" is not appearing, actual categories "{self.site.home.menu_carousel.items_as_ordered_dict.keys()}"')

        # Sports Icon verification
        self.assertTrue(table_tennis.is_displayed(), msg='Table tennis sports icon is not displayed')
        table_tennis.link.click()
        url_from_cms = f"https://{tests.HOSTNAME}/{self.sport['targetUri']}"
        self.assertEqual(url_from_cms, self.device.get_current_url(),
                         msg=f'Actual opened window URL: \n"{self.device.get_current_url()}", '
                             f'\nexpected configured in CMS: \n"{url_from_cms}"')

        # Check if Matches Tab Is Selected By Default
        current_tab = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab.upper(), "Matches".upper(),
                         msg=f"Current Active tab is {current_tab},"
                             f"Expected tab is Matches")

    def test_009_verify_alignment_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Alignment of Sports ribbon tab
        EXPECTED: Alignment should be proper and below things need to veify:
        EXPECTED: Foreground Image
        EXPECTED: Backkground Image
        EXPECTED: Text Alignment.
        """
        # this step is covered in C65940572

    def test_010_verify_sub_menu_tabs(self):
        """
        DESCRIPTION: Verify Sub menu tabs
        EXPECTED: All the configured sub menu tabs should be displayed as per cms
        EXPECTED: Inpay,Competitions,outrights and specials.
        """

        expected_tabs = []
        tabs_in_cms = self.cms_config.get_sport_tabs(sport_id=self.sport['categoryId'])
        for tab in tabs_in_cms:
            if tab['enabled'] and not (tab['checkEvents'] and not tab['hasEvents']):
                expected_tabs.append(tab['displayName'].upper())
        actual_tabs = list(self.site.contents.tabs_menu.items_as_ordered_dict.keys())

        self.assertListEqual(actual_tabs, expected_tabs,
                             msg=f'There are few expected tabs missed: Expected: \n"{expected_tabs}". '
                                 f'Current tabs list: \n"{actual_tabs}"')
