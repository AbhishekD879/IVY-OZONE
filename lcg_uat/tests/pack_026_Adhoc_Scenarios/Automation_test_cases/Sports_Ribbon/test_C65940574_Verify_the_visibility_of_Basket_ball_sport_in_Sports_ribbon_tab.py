from collections import OrderedDict
import pytest
from crlat_cms_client.utils.exceptions import CMSException
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_cms_reflection


def get_sport_tab_status(tab):
    check_events = tab.get("checkEvents")
    has_events = tab.get("hasEvents")
    enabled = tab.get("enabled")
    if not enabled:
        return False
    if check_events is None or has_events is None:
        raise CMSException(
            f'check_events:{check_events} and has_events:{has_events},The paremeters are not present in response')
    if check_events and not has_events:
        return False
    return True

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

class Test_C65940574_Verify_the_visibility_of_Basket_ball_sport_in_Sports_ribbon_tab(Common):
    """
    TR_ID: C65940574
    NAME: Verify the visibility of Basket ball sport in Sports ribbon tab
    DESCRIPTION: This test case is to validate About  sports ribbon tab as per cms configuration
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Configuration for  Basketball in LHN
    PRECONDITIONS: sport page->sport categories.
    PRECONDITIONS: 3)Click on Basketball sport category
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

    Basketball_config = {
        "title": "Basketball" if tests.settings.brand != "bma" else "Basketball".upper(),
        "categoryId": 6,
        "isTopSport": False,
        "targetUri": "sport/basketball",
        "ssCategoryCode": "BASKETBALL",
        "oddsCardHeaderType": "ONE_TWO_TYPE",
        "svgId": "basketball",
        "inApp": True,
        "showInHome": True,
        "showInPlay": True,
        "showScoreboard": True,
        "showInAZ": True,
    }
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_preconditions(self):
        """
         PRECONDITIONS: 1) User should have oxygen CMS access
         PRECONDITIONS: 2) Configuration for  Basketball in LHN
         PRECONDITIONS: sport page->sport categories.
         PRECONDITIONS: 3)Click on Basketball sport category
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
        # Get All Sport Categories
        sport_categories = self.cms_config.get_sport_categories()

        # Get Basketball From All Sport Categories
        self.__class__.Basketball = next(
            (sport_category for sport_category in sport_categories if
             sport_category['imageTitle'].strip().title() == "Basketball"), None)

        # Check If Basketball is Available in AllSport Categories
        if not self.Basketball:
            self.cms_config.create_sport_category(**self.Basketball_config)

    def test_001_launch_coralladbrokes_application(self):
        """
        DESCRIPTION: Launch Coral/Ladbrokes Application.
        EXPECTED: Application should be launched
        EXPECTED: Home page should be opened and sports ribbon tab should be displayed.
        """
        # Login to application
        self.site.login()
        self.site.wait_logged_in()

        # check id sport ribbon tab is displayed
        is_sports_ribbon_displayed = self.site.home.menu_carousel.is_displayed(expected_result=True, timeout=5)
        self.assertTrue(is_sports_ribbon_displayed, msg=f"Sports ribbon is not displayed on HomePage")

    def test_002_verify_presence_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify presence of Sports ribbon tab
        EXPECTED: Sports ribbon tab is applicable for Both logged in and Logged out user.
        """
        # Logout From application
        self.site.logout()
        self.site.wait_logged_out()

        # check id sport ribbon tab is displayed
        is_sports_ribbon_displayed = self.site.home.menu_carousel.is_displayed(expected_result=True, timeout=5)
        self.assertTrue(is_sports_ribbon_displayed, msg=f"Sports ribbon is not displayed on HomePage")

    def test_003_verify_scrollability_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Scrollability of sports ribbon tab
        EXPECTED: Should be left and right scrollable and Image alignment should not be disturbed while scrolling .
        """
        all_items_in_sport_ribbon = list(self.site.home.menu_carousel.items_as_ordered_dict.items())
        first_item_name, first_item = all_items_in_sport_ribbon[0]
        last_item_name, last_item = all_items_in_sport_ribbon[-1]
        first_item.scroll_to()
        self.assertTrue(first_item.is_displayed(scroll_to=False),
                        msg=f"The first item {first_item_name} is not displayed after scrolling to {first_item_name}")
        last_item.scroll_to()
        self.assertTrue(last_item.is_displayed(scroll_to=False),
                        msg=f"The Last item {last_item_name} is not displayed after scrolling to {last_item_name}")
        first_item.scroll_to()
        self.assertTrue(first_item.is_displayed(scroll_to=False),
                        msg=f"The first item {first_item_name} is not displayed after scrolling to {first_item_name}")

    def test_004_verify__basketball_sport_icon_is_displayed_and_clickable(self, should_be_present=True):
        """
        DESCRIPTION: Verify  Basketball sport icon is displayed and clickable
        EXPECTED: Basketball sport icon should be displayed and clickable
        """
        all_items_in_sport_ribbon = self.site.home.menu_carousel.items_as_ordered_dict
        if should_be_present:
            is_Basketball_present_in_sport_ribbon = wait_for_cms_reflection(
                func=lambda: self.site.home.menu_carousel
                .items_as_ordered_dict.get(self.Basketball_config.get('title')),
                ref=self,
                refresh_count=5,
                expected_result=True,
                timeout=10
            )
            self.assertTrue(is_Basketball_present_in_sport_ribbon,
                            msg=f"Item name {self.Basketball_config.get('title')} "
                                f"is not present in {all_items_in_sport_ribbon.keys()}")
        else:
            is_Basketball_present_in_sport_ribbon = wait_for_cms_reflection(
                func=lambda: self.site.home.menu_carousel
                .items_as_ordered_dict.get(self.Basketball_config.get('title')),
                ref=self,
                refresh_count=5,
                expected_result=False,
                timeout=10
            )
            self.assertFalse(is_Basketball_present_in_sport_ribbon,
                             msg=f"Item name {self.Basketball_config.get('title')} "
                                 f"is present in {all_items_in_sport_ribbon.keys()} Even after disabled")

    def test_005_verify_the_order_of_sport_by_using_drag_and_drop_in_cms(self):
        """
        DESCRIPTION: Verify the order of sport by using drag and drop in cms
        EXPECTED: Sport order should be changed after drag and drop in cms and same should be shown in Sport ribbon tab
        """
        #  covered in C65940577

    def test_006_verify__by_unchecking_show_in_sports_ribbon_tab_and_check_active_checkbox_in_cms(self):
        """
        DESCRIPTION: Verify  By unchecking "show in sports ribbon tab" and check "Active" checkbox in cms
        EXPECTED: Basketball sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(self.Basketball.get("id"), disabled=False, showInHome=False)
        self.test_004_verify__basketball_sport_icon_is_displayed_and_clickable(should_be_present=False)

        self.cms_config.update_sport_category(self.Basketball.get("id"), disabled=False, showInHome=True)
        self.test_004_verify__basketball_sport_icon_is_displayed_and_clickable(should_be_present=True)

    def test_007_verify_by_uncheck_activecheckbox_and_check_show_in_sports_ribbon_tab_in_cms(self):
        """
        DESCRIPTION: Verify By uncheck "Active"checkbox and check "show in sports ribbon tab" in cms
        EXPECTED: Basketball sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(self.Basketball.get("id"), disabled=True, showInHome=True)
        self.test_004_verify__basketball_sport_icon_is_displayed_and_clickable(should_be_present=False)

        self.cms_config.update_sport_category(self.Basketball.get("id"), disabled=False, showInHome=True)
        self.test_004_verify__basketball_sport_icon_is_displayed_and_clickable(should_be_present=True)

    def test_008_verify_by_click_on_basketball_icon_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify by Click on Basketball Icon in sport ribbon tab
        EXPECTED: Should redirect to Matches Tab of Basketball page.
        EXPECTED: By Default Matches tab should be opened.
        """
        Basketball_item = wait_for_cms_reflection(
            func=lambda: self.site.home.menu_carousel
            .items_as_ordered_dict.get(self.Basketball_config.get('title')),
            ref=self,
            refresh_count=5,
            expected_result=True,
            timeout=10
        )
        self.assertTrue(Basketball_item,
                        msg=f"Item name {self.Basketball_config.get('title')} "
                            f"is not present in {self.site.home.menu_carousel.items_as_ordered_dict.keys()}")

        Basketball_item.click()
        self.site.wait_content_state(state_name="Basketball")
        self.device.refresh_page()
        current_tab_on_Basketball_slp = self.site.basketball.tabs_menu.current
        self.assertEqual(current_tab_on_Basketball_slp.upper(), "Matches".upper(),
                         msg=f"Current Active tab is {current_tab_on_Basketball_slp},"
                             f"Expected tab is Matches")
        self.site.back_button.click()
        self.site.wait_content_state(state_name="Home", timeout=10)

    def test_009_verify_alignment_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Alignment of Sports ribbon tab
        EXPECTED: Alignment should be proper and below things need to veify:
        EXPECTED: Foreground Image
        EXPECTED: Backkground Image
        EXPECTED: Text Alignment.
        """
        #covered in C65940572

    def test_010_verify_sub_menu_tabs(self):
        """
        DESCRIPTION: Verify Sub menu tabs
        EXPECTED: All the configured sub menu tabs should be displayed as per cms
        EXPECTED: Inpay,Competitions,outrights and specials.
        """
        all_cms_tabs_by_order = OrderedDict()
        all_sub_tabs_for_Basketball = self.cms_config.get_sport_tabs(sport_id=self.Basketball_config.get("categoryId"))
        for tab in all_sub_tabs_for_Basketball:
            tab_available = get_sport_tab_status(tab)
            if tab_available:
                all_cms_tabs_by_order[tab.get('displayName').upper()] = tab

        Basketball_item = wait_for_cms_reflection(
            func=lambda: self.site.home.menu_carousel
            .items_as_ordered_dict.get(self.Basketball_config.get('title')),
            ref=self,
            refresh_count=5,
            expected_result=True,
            timeout=10
        )
        self.assertTrue(Basketball_item,
                        msg=f"Item name {self.Basketball_config.get('title')} "
                            f"is not present in {self.site.home.menu_carousel.items_as_ordered_dict.keys()}")
        Basketball_item.click()
        self.site.wait_content_state(state_name="Basketball")
        all_sub_tabs_for_Basketball_fe = self.site.basketball.tabs_menu.items_as_ordered_dict
        all_sub_tabs_for_Basketball_fe = [tab.upper() for tab in list(all_sub_tabs_for_Basketball_fe.keys())]
        self.assertListEqual(all_sub_tabs_for_Basketball_fe, list(all_cms_tabs_by_order.keys()))
