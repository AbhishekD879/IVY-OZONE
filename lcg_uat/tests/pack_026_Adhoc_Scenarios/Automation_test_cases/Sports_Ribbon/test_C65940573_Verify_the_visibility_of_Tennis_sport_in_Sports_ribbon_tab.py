import pytest
from crlat_cms_client.utils.exceptions import CMSException
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.Common import Common
from voltron.utils.waiters import wait_for_cms_reflection, wait_for_haul


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.mobile_only
@pytest.mark.menu_ribbon
@vtest
class Test_C65940573_Verify_the_visibility_of_Tennis_sport_in_Sports_ribbon_tab(Common):
    """
    TR_ID: C65940573
    NAME: Verify the visibility of Tennis sport in Sports ribbon tab
    """
    keep_browser_open = True
    tennis = vec.olympics.TENNIS if tests.settings.brand=="ladbrokes" else vec.olympics.TENNIS.upper()
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def verify_sport_in_FE(self, expected_result=True):
        result = wait_for_cms_reflection(
            lambda: self.site.home.menu_carousel.items_as_ordered_dict.get(
                self.tennis),
            ref=self, timeout=10,
            refresh_count=3, haul=10, expected_result=expected_result)
        if expected_result:
            self.assertTrue(result, msg=f'Tennis is not preset in Sport  ribbon menu')
        else:
            self.assertFalse(result, msg=f'Tennis still preset in Sport  ribbon menu')

    def expected_cms_tabs(self):
        tabs = self.cms_config.get_sport_tabs(sport_id=self.ob_config.tennis_config.category_id)
        return [tab['displayName'].upper() for tab in tabs if not (not tab['enabled'] or (tab['checkEvents'] and not tab['hasEvents']))]
    def test_000_preconditions(self):
        """
        DESCRIPTION: This test case is to validate About  sports ribbon tab as per cms configuration
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for  Tennis in LHN
        PRECONDITIONS: sport page->sport categories.
        PRECONDITIONS: 3)Click on Tennis sport category
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
        self.site.wait_content_state(state_name='Homepage')
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
        self.site.login()

    def test_002_verify_presence_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify presence of Sports ribbon tab
        EXPECTED: Sports ribbon tab is applicable for Both logged in and Logged out user.
        """
        self.assertTrue(self.site.home.menu_carousel.is_displayed(),
                        msg='Sports Ribbon is not displayed for logged user')
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')

    def test_003_verify_scrollability_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Scrollability of sports ribbon tab
        EXPECTED: Should be left and right scrollable and Image alignment should not be disturbed while scrolling .
        """
        # Get All Items Form Sport ribbon
        all_items_in_sport_ribbon = list(self.site.home.menu_carousel.items_as_ordered_dict.items())
        # Get First Item
        first_item_name, first_item = all_items_in_sport_ribbon[0]
        # Get last Item
        last_item_name, last_item = all_items_in_sport_ribbon[-1]
        # Scroll to first item and validate first item is displayed
        first_item.scroll_to()
        self.assertTrue(first_item.is_displayed(scroll_to=False),
                        msg=f"The first item {first_item_name} is not displayed after scrolling to {first_item_name}")
        # Scroll to last item and validate last item is displayed
        last_item.scroll_to()
        self.assertTrue(last_item.is_displayed(scroll_to=False),
                        msg=f"The Last item {last_item_name} is not displayed after scrolling to {last_item_name}")

    def test_004_verify__tennis_sport_icon_is_displayed_and_clickable(self):
        """
        DESCRIPTION: Verify  Tennis sport icon is displayed and clickable
        EXPECTED: Tennis sport icon should be displayed and clickable
        """
        sports = self.cms_config.get_sport_categories()
        for sport in sports:
            if sport['imageTitle'].upper().strip() == self.tennis.upper():
                self.__class__.tennis_sport = sport
                self.__class__.sport_id = sport['id']
                if sport['disabled'] or not sport['showInHome']:
                    self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                                          showInHome=True,
                                                          disabled=False)
                self.verify_sport_in_FE(expected_result=True)
                self.site.home.menu_carousel.click_item(self.tennis)
                self.site.wait_content_state(state_name='Tennis', timeout=20)
                self.site.back_button_click()
                self.site.wait_content_state('HomePage')
                break
        else:
            raise CMSException(f'TENNIS sport not found in sports categories')

    def test_005_verify_the_order_of_sport_by_using_drag_and_drop_in_cms(self):
        """
        DESCRIPTION: Verify the order of sport by using drag and drop in cms
        EXPECTED: Sport order should be changed after drag and drop in cms and same should be shown in Sport ribbon tab
        """
        #COVERED IN C65940577

    def test_006_verify__by_unchecking_show_in_sports_ribbon_tab_and_check_active_checkbox_in_cms(self):
        """
        DESCRIPTION: Verify  By unchecking "show in sports ribbon tab" and check "Active" checkbox in cms
        EXPECTED: Tennis sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=False,
                                              disabled=False)
        self.verify_sport_in_FE(expected_result=False)

        #enabling again after disabling in sport ribbon
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=True,
                                              disabled=False)
        self.verify_sport_in_FE(expected_result=True)

    def test_007_verify_by_uncheck_activecheckbox_and_check_show_in_sports_ribbon_tab_in_cms(self):
        """
        DESCRIPTION: Verify By uncheck "Active"checkbox and check "show in sports ribbon tab" in cms
        EXPECTED: Tennis sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=True,
                                              disabled=True)
        self.device.refresh_page()
        self.verify_sport_in_FE(expected_result=False)

        #enabling again after disabling in sport ribbon
        self.cms_config.update_sport_category(sport_category_id=self.sport_id,
                                              showInHome=True,
                                              disabled=False)
        self.device.refresh_page()
        self.verify_sport_in_FE(expected_result=True)

    def test_008_verify_by_click_on_tennis_icon_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify by Click on tennis Icon in sport ribbon tab
        EXPECTED: Should redirect to Matches Tab of Tennis page.
        EXPECTED: By Default Matches tab should be opened.
        """
        self.site.home.menu_carousel.click_item(self.tennis)
        self.site.wait_content_state(state_name='tennis', timeout=20)
        expected_url = f'https://{tests.HOSTNAME}/{self.tennis_sport["targetUri"]}'
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, expected_url, msg=f'actual url"{current_url}" is not as same as "{expected_url}"')

    def test_009_verify_alignment_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Alignment of Sports ribbon tab
        EXPECTED: Alignment should be proper and below things need to veify:
        EXPECTED: Foreground Image
        EXPECTED: Backkground Image
        EXPECTED: Text Alignment.
        """
        #not automatable

    def test_010_verify_sub_menu_tabs(self):
        """
        DESCRIPTION: Verify Sub menu tabs
        EXPECTED: All the configured sub menu tabs should be displayed as per cms
        EXPECTED: Inpay,Competitions,outrights and specials.
        """
        sub_menu_tabs = list(self.site.tennis.tabs_menu.items_names)
        enabled_cms_tabs = self.expected_cms_tabs()
        self.assertEqual(enabled_cms_tabs, sub_menu_tabs, msg=f'tabs active in cms {enabled_cms_tabs} are not same as tabs active at frontend {sub_menu_tabs}')




