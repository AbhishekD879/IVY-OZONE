import pytest
from crlat_cms_client.utils.exceptions import CMSException
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result, wait_for_haul


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
class Test_C65940578_Verify_the_visibility_of_Greyhounds_in_Sports_ribbon_tab(Common):
    """
    TR_ID: C65940578
    NAME: Verify the visibility of Greyhounds in Sports ribbon tab
    DESCRIPTION: This test case is to validate About  sports ribbon tab as per cms configuration
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Configuration for  Greyhounds in LHN
    PRECONDITIONS: sport page->sport categories.
    PRECONDITIONS: 3)Click on Greyhounds  category
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

    def verify_of_sport_in_sport_menu_ribbon_tab(self, sport_name, expected_result=True):
        count = 12
        sport_status = self.site.home.menu_carousel.items_as_ordered_dict.get(sport_name)
        while (expected_result != bool(sport_status)) and count:
            count -= 1
            wait_for_haul(5)
            self.device.refresh_page()
            sport_status = self.site.home.menu_carousel.items_as_ordered_dict.get(sport_name)

        if expected_result:
            self.assertTrue(sport_status, msg=f'{sport_status} is not present in sport menu')
        else:
            self.assertFalse(sport_status, msg=f'{sport_status} is present in sport menu')

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
        # Covered in Preconditions

    def test_002_verify_presence_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify presence of Sports ribbon tab
        EXPECTED: Sports ribbon tab is applicable for Both logged in and Logged out user.
        """
        # covered in Preconditions

    def test_003_verify_scrollability_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Scrollability of sports ribbon tab
        EXPECTED: Should be left and right scrollable and Image alignment should not be disturbed while scrolling .
        """
        # covered in Preconditions

    def test_004_verify__greyhounds__icon_is_displayed_and_clickable(self):
        """
        DESCRIPTION: Verify  Greyhounds  icon is displayed and clickable
        EXPECTED: Greyhounds  icon should be displayed and clickable
        """
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'].upper() == 'GREYHOUNDS':
                self.__class__.greyhounds_sport = sport
                self.__class__.sport_id = sport['id']
                self.__class__.greyhounds = sport['imageTitle'] if self.brand == 'ladbrokes' else sport[
                    'imageTitle'].upper()
                if sport['disabled'] or not sport['showInHome']:
                    self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                                          showInHome=True,
                                                          disabled=False)
                self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.greyhounds)
                self.site.home.menu_carousel.click_item(self.greyhounds)
                self.site.wait_content_state(state_name='Greyhounds', timeout=20)
                self.site.back_button_click()
                self.site.wait_content_state('HomePage')
                break
        else:
            raise CMSException(f'GREYHOUNDS sport not found in sports categories')

    def test_005_verify_the_order_of_sport_by_using_drag_and_drop_in_cms(self):
        """
        DESCRIPTION: Verify the order of sport by using drag and drop in cms
        EXPECTED: Sport order should be changed after drag and drop in cms and same should be shown in Sport ribbon tab
        """
        # Covered in Test Case ID : C65940577

    def test_006_verify__by_unchecking_show_in_sports_ribbon_tab_and_check_active_checkbox_in_cms(self):
        """
        DESCRIPTION: Verify  By unchecking "show in sports ribbon tab" and check "Active" checkbox in cms
        EXPECTED: Greyhounds  should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=False,
                                              disabled=False)
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.greyhounds, expected_result=False)
        # Activating Greyhounds sport in sport ribbon menu
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=True,
                                              disabled=False)
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.greyhounds)

    def test_007_verify_by_uncheck_activecheckbox_and_check_show_in_sports_ribbon_tab_in_cms(self):
        """
        DESCRIPTION: Verify By uncheck "Active"checkbox and check "show in sports ribbon tab" in cms
        EXPECTED: Greyhounds  should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=True,
                                              disabled=True)
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.greyhounds, expected_result=False)
        # Activating Greyhounds sport in sport ribbon menu
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=True,
                                              disabled=False)
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.greyhounds)

    def test_008_verify_by_click_on_greyhounds_icon_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify by Click on Greyhounds Icon in sport ribbon tab
        EXPECTED: Should redirect to todayTab of Greyhounds page.
        EXPECTED: By Default today tab should be opened.
        EXPECTED: Lads: Nextraces
        EXPECTED: Coral:Today
        """
        self.site.home.menu_carousel.click_item(self.greyhounds)
        self.site.wait_content_state(state_name='Greyhounds', timeout=20)
        self.__class__.expected_url = f'https://{tests.HOSTNAME}{self.greyhounds_sport["targetUri"]}'
        actual_url = self.device.get_current_url()
        self.assertEqual(actual_url, self.expected_url, msg=f'actual url:{actual_url} is not equalto expected url:{self.expected_url}')
        if self.brand == 'ladbrokes':
            current_sport_tab = self.site.greyhound.tabs_menu.current
            self.assertEqual(vec.racing.RACING_NEXT_RACES_NAME, current_sport_tab, msg='Next Races tab is not available')
        else:
            current_sport_tab = self.site.greyhound.tabs_menu.current
            self.assertEqual(vec.sb.SPORT_DAY_TABS.today, current_sport_tab, msg=f'Today tab is not available')

    def test_009_verify_alignment_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Alignment of Sports ribbon tab
        EXPECTED: Alignment should be proper and below things need to veify:
        EXPECTED: Foreground Image
        EXPECTED: Backkground Image
        EXPECTED: Text Alignment.
        """
        pass

    def test_010_verify_sub_menu_tabs(self):
        """
        DESCRIPTION: Verify Sub menu tabs
        EXPECTED: All the configured sub menu tabs should be displayed as per cms
        EXPECTED: Inpay,Competitions,outrights and specials.
        """
        actual_greyhound_tabs = self.site.greyhound.tabs_menu.items_names
        if self.brand == 'ladbrokes':
            for greyhound_tab in vec.Racing.GREYHOUND_TAB_NAMES:
                self.assertIn(greyhound_tab, actual_greyhound_tabs,
                              msg=f'Expected tab: "{greyhound_tab}" is not available in the'
                                  f'Actual tabs: "{actual_greyhound_tabs}"')
        else:
            for greyhound_tab in vec.sb.SPORT_DAY_TABS:
                self.assertIn(greyhound_tab, actual_greyhound_tabs, msg=f'Expected tab: "{greyhound_tab}" is not '
                                                                        f'available in the Actual tabs: "{actual_greyhound_tabs}"')
