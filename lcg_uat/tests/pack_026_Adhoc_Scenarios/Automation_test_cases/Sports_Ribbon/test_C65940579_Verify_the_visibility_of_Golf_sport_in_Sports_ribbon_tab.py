import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_cms_reflection


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@pytest.mark.menu_ribbon
@vtest
class Test_C65940579_Verify_the_visibility_of_Golf_sport_in_Sports_ribbon_tab(Common):
    """
    TR_ID: C65940579
    NAME: Verify the visibility of Golf sport in Sports ribbon tab
    DESCRIPTION: This test case is to validate About  sports ribbon tab as per cms configuration
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Configuration for  Golf in LHN
    PRECONDITIONS: sport page->sport categories.
    PRECONDITIONS: 3)Click on Golf sport category
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
    PRECONDITIONS: -Is Multi-template Sport
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
    expected_tabs = []

    def expected_cms_tabs(self):
        tabs = self.cms_config.get_sport_tabs(sport_id=self.ob_config.golf_config.category_id)
        for tab in tabs:
            if not tab['enabled'] or (tab['checkEvents'] and not tab['hasEvents']):
                continue
            self.expected_tabs.append(tab['displayName'].upper())
        return self.expected_tabs

    def test_000_preconditions(self):
        """
        Desccription : Verify Sports ribbon menu for loggedin and loggedout Users.
        Expected : Sports ribbon should be display for loggedin and Loggedout Users.
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')
        self.assertTrue(self.site.home.menu_carousel.is_displayed(),
                        msg='Sports Ribbon is not displayed for logged user')
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        self.site.login()
        self.assertTrue(self.site.home.menu_carousel.is_displayed(),
                        msg='Sports Ribbon is not displayed for logged user')
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')

    def test_001_launch_coralladbrokes_application(self):
        """
        DESCRIPTION: Launch Coral/Ladbrokes Application.
        EXPECTED: Application should be launched
        EXPECTED: Home page should be opened and sports ribbon tab should be displayed.
        """
        # Covered in Precondition

    def test_002_verify_presence_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify presence of Sports ribbon tab
        EXPECTED: Sports ribbon tab is applicable for Both logged in and Logged out user.
        """
        # Covered in Precondition

    def test_003_verify_scrollability_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Scrollability of sports ribbon tab
        EXPECTED: Should be left and right scrollable and Image alignment should not be disturbed while scrolling .
        """
        # Covered in Precondition

    def test_004_verify__golf_sport_icon_is_displayed_and_clickable(self):
        """
        DESCRIPTION: Verify  Golf sport icon is displayed and clickable
        EXPECTED: Golf sport icon should be displayed and clickable
        """
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'].upper().strip() == 'GOLF':
                self.__class__.golf_sport = sport
                self.__class__.sport_id = sport['id']
                self.__class__.golf = sport['imageTitle'] if self.brand == 'ladbrokes' else sport['imageTitle'].upper()
                if sport['disabled'] or not sport['showInHome']:
                    self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                                          showInHome=True,
                                                          disabled=False)
                result = wait_for_cms_reflection(
                    lambda: self.site.home.menu_carousel.items_as_ordered_dict.get(
                        self.golf),
                    ref=self, timeout=10,
                    refresh_count=3, haul=10, expected_result=True)
                self.assertTrue(result, msg=f'Golf still not active in Sport  ribbon menu')
                self.site.home.menu_carousel.click_item(self.golf)
                self.site.wait_content_state(state_name='Golf', timeout=20)
                self.site.back_button_click()
                self.site.wait_content_state('HomePage')
                break
        else:
            raise VoltronException(f'GOLF sport not found in sports categories')

    def test_005_verify_the_order_of_sport_by_using_drag_and_drop_in_cms(self):
        """
        DESCRIPTION: Verify the order of sport by using drag and drop in cms
        EXPECTED: Sport order should be changed after drag and drop in cms and same should be shown in Sport ribbon tab
        """
        # Covered in Test Case ID : C65940577

    def test_006_verify__by_unchecking_show_in_sports_ribbon_tab_and_check_active_checkbox_in_cms(self):
        """
        DESCRIPTION: Verify  By unchecking "show in sports ribbon tab" and check "Active" checkbox in cms
        EXPECTED: Golf sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=False,
                                              disabled=False)
        result = wait_for_cms_reflection(
            lambda: self.site.home.menu_carousel.items_as_ordered_dict.get(
                self.golf),
            ref=self,timeout=10,
            refresh_count=3, haul=10, expected_result=False)
        self.assertFalse(result,msg = f'Golf still preset in Sport  ribbon menu')
        # Activating Golf sport in sport ribbon menu
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=True,
                                              disabled=False)
        result = wait_for_cms_reflection(
            lambda: self.site.home.menu_carousel.items_as_ordered_dict.get(
                self.golf),
            ref=self,timeout=10,
            refresh_count=3, haul=10, expected_result=True)
        self.assertTrue(result, msg=f'Golf still not active in Sport  ribbon menu')

    def test_007_verify_by_uncheck_activecheckbox_and_check_show_in_sports_ribbon_tab_in_cms(self):
        """
        DESCRIPTION: Verify By uncheck "Active"checkbox and check "show in sports ribbon tab" in cms
        EXPECTED: Golf sport should not display in Sports ribbon tab
        """

        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=True,
                                              disabled=True)
        result = wait_for_cms_reflection(
            lambda: self.site.home.menu_carousel.items_as_ordered_dict.get(
                self.golf),
            ref=self,timeout=10,
            refresh_count=3, haul=10, expected_result=False)
        self.assertFalse(result, msg=f'Golf still present in Sport ribbon menu')
        # Activating Golf sport in sport ribbon menu
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=True,
                                              disabled=False)
        result = wait_for_cms_reflection(
            lambda: self.site.home.menu_carousel.items_as_ordered_dict.get(
                self.golf),
            ref=self,timeout=10,
            refresh_count=3, haul=10, expected_result=True)
        self.assertTrue(result, msg=f'Golf still not active in Sport ribbon menu')

    def test_008_verify_by_click_on_golf_icon_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify by Click on Golf Icon in sport ribbon tab
        EXPECTED: Should redirect to Matches Tab of Golf page.
        EXPECTED: By Default Matches tab should be opened.
        """
        self.site.home.menu_carousel.click_item(self.golf)
        self.site.wait_content_state(state_name='Golf', timeout=20)
        self.__class__.expected_url = f'https://{tests.HOSTNAME}/{self.golf_sport["targetUri"]}'
        actual_url = self.device.get_current_url()
        self.assertEqual(actual_url, self.expected_url,
                         msg=f'actual url:{actual_url} is not equal to expected url:{self.expected_url}')
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                     self.ob_config.golf_config.category_id)
        current_sport_tab = self.site.golf.tabs_menu.current
        self.assertEqual(current_sport_tab, expected_sport_tab,
                            f'expected tab: "{expected_sport_tab}" is not found in "{current_sport_tab}"')

    def test_009_verify_alignment_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Alignment of Sports ribbon tab
        EXPECTED: Alignment should be proper and below things need to veify:
        EXPECTED: Foreground Image
        EXPECTED: Backkground Image
        EXPECTED: Text Alignment.
        """
        # Covered in C65940578

    def test_010_verify_sub_menu_tabs(self):
        """
        DESCRIPTION: Verify Sub menu tabs
        EXPECTED: All the configured sub menu tabs should be displayed as per cms
        EXPECTED: Inpay,Competitions,outrights and specials.
        """
        actual_golf_tabs = self.site.golf.tabs_menu.items_names
        expected_golf_tabs = self.expected_cms_tabs()
        self.assertListEqual(sorted(actual_golf_tabs), sorted(expected_golf_tabs), msg=f'both sub tabs are not equal')
