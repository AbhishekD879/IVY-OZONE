import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.menu_ribbon
@pytest.mark.reg164_fix
@pytest.mark.mobile_only
@vtest
class Test_C65940576_Verify_the_visibility_of_Tier2Volley_Ballsport_in_Sports_ribbon_tab(Common):
    """
    TR_ID: C65940576
    NAME: Verify the visibility of Tier2(Volley Ball)sport in Sports ribbon tab
    DESCRIPTION: This test case is to validate About  sports ribbon tab as per cms configuration
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Configuration for  Volley Ball in LHN
    PRECONDITIONS: sport page->sport categories.
    PRECONDITIONS: 3)Click on Volley Ball sport category
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
    sport_name = None
    sport_id = None
    expected_tabs = []

    def verify_of_sport_in_sport_menu_ribbon_tab(self, sport_name, expected_result=True):
        count = 12
        sport_status = self.site.home.menu_carousel.items_as_ordered_dict.get(sport_name)
        while (expected_result != bool(sport_status)) and count:
            count -= 1
            wait_for_haul(5)
            self.device.refresh_page()
            sport_status = self.site.home.menu_carousel.items_as_ordered_dict.get(sport_name)

        if expected_result:
            self.assertTrue(sport_status, msg=f'Sport name "{sport_status}" is not present in sport menu ribbon')
        else:
            self.assertFalse(sport_status, msg=f'Sport name "{sport_status}" is present in sport menu ribbon')

    def expected_cms_tabs(self):
        tabs = self.cms_config.get_sport_tabs(sport_id=self.ob_config.volleyball_config.category_id)
        for tab in tabs:
            if not tab['enabled'] or (tab['checkEvents'] and not tab['hasEvents']):
                continue
            self.expected_tabs.append(tab['displayName'].upper())
        return self.expected_tabs

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for  Volleyball in Sport category
        PRECONDITIONS: sport page->sport categories.
        PRECONDITIONS: 3)Click on Volleyball sport category
        """
        sport_categories = self.cms_config.get_sport_categories()
        sport_category = next((category for category in sport_categories if category.get('imageTitle').strip().title() == 'Volleyball'),None)
        if sport_category:
            if not sport_category.get('disabled') and sport_category.get('showInHome'):
                volleyball = sport_category
            else:
                volleyball = self.cms_config.update_sport_category(sport_category_id=sport_category.get('id'), showInHome=True, disabled=False)
        else:
            volleyball = self.cms_config.create_sport_category(title='Volleyball',
                                                               categoryId = self.ob_config.volleyball_config.category_id,
                                                               ssCategoryCode='VOLLEYBALL',
                                                               tier='TIER_2',showInHome=True,
                                                               targetUri='sport/volleyball')
        self.__class__.sport_name = volleyball.get('imageTitle').upper().strip() if self.brand == 'bma' else volleyball.get('imageTitle').strip()
        self.__class__.sport_id = volleyball.get('id')

    def test_001_launch_coralladbrokes_application(self):
        """
        DESCRIPTION: Launch Coral/Ladbrokes Application.
        EXPECTED: Application should be launched
        EXPECTED: Home page should be opened and sports ribbon tab should be displayed.
        """
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='HomePage')

    def test_002_verify_presence_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify presence of Sports ribbon tab
        EXPECTED: Sports ribbon tab is applicable for Both loggedIn and LoggedOut user.
        """
        is_sports_menu_ribbon_displayed = self.site.home.menu_carousel.is_displayed()
        self.assertTrue(is_sports_menu_ribbon_displayed, msg=f'sport menu ribbon tab is not displayed')
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.sport_name)
        self.site.login()
        is_sports_menu_ribbon_displayed = self.site.home.menu_carousel.is_displayed()
        self.assertTrue(is_sports_menu_ribbon_displayed, msg=f'sport menu ribbon tab is not displayed')
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.sport_name)

    def test_003_verify_scrollability_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Scrollability of sports ribbon tab
        EXPECTED: Should be left and right scrollable and Image alignment should not be disturbed while scrolling .
        """
        sport_menu_items = list(self.site.home.menu_carousel.items_as_ordered_dict.items())
        first_item_name, first_item = sport_menu_items[0]
        last_item_name, last_item = sport_menu_items[-1]
        first_item.scroll_to()
        self.assertTrue(first_item.is_displayed(scroll_to=False),
                        msg=f"The first item {first_item_name} is not displayed after scrolling to {first_item_name}")
        last_item.scroll_to()
        self.assertTrue(last_item.is_displayed(scroll_to=False),
                        msg=f"The Last item {last_item_name} is not displayed after scrolling to {last_item_name}")

    def test_004_verify__volley_ball_sport_icon_is_displayed_and_clickable(self):
        """
        DESCRIPTION: Verify  Volley Ball sport icon is displayed and clickable
        EXPECTED: Volley Ball sport icon should be displayed and clickable
        """
        self.site.home.menu_carousel.click_item(self.sport_name)
        wait_content = self.site.wait_content_state(state_name='Volleyball')
        self.assertTrue(wait_content, msg='Not able to click on sport Icon')
        self.site.go_to_home_page()

    def test_005_verify_the_order_of_sport_by_using_drag_and_drop_in_cms(self):
        """
        DESCRIPTION: Verify the order of sport by using drag and drop in cms
        EXPECTED: Sport order should be changed after drag and drop in cms and same should be shown in Sport ribbon tab
        """
        # Covered in Test case Id : C65940577
        pass

    def test_006_verify__by_unchecking_show_in_sports_ribbon_tab_and_check_active_checkbox_in_cms(self):
        """
        DESCRIPTION: Verify  By unchecking "show in sports ribbon tab" and check "Active" checkbox in cms
        EXPECTED: Volley Ball sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id=self.sport_id, showInHome=False, disabled=False)
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.sport_name, expected_result=False)
        self.cms_config.update_sport_category(sport_category_id=self.sport_id, showInHome=True, disabled=False)
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.sport_name)

    def test_007_verify_by_uncheck_activecheckbox_and_check_show_in_sports_ribbon_tab_in_cms(self):
        """
        DESCRIPTION: Verify By uncheck "Active"checkbox and check "show in sports ribbon tab" in cms
        EXPECTED: Volley Ball sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id=self.sport_id, showInHome=True, disabled=True)
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.sport_name, expected_result=False)
        self.cms_config.update_sport_category(sport_category_id=self.sport_id, showInHome=True, disabled=False)
        self.verify_of_sport_in_sport_menu_ribbon_tab(sport_name=self.sport_name)

    def test_008_verify_by_click_on_volley_ball_icon_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify by Click on Volley Ball Icon in sport ribbon tab
        EXPECTED: Should redirect to Matches Tab of Volley Ball page.
        EXPECTED: By Default Matches tab should be opened.
        """
        self.site.home.menu_carousel.click_item(self.sport_name)
        self.site.wait_content_state_changed()
        matches_tab_status = self.cms_config \
            .get_sport_tab_status(sport_id=self.ob_config.volleyball_config.category_id,
                                  tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches)
        if matches_tab_status:
            tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper()
            current_tab = self.site.sports_page.tabs_menu.current.upper()
            self.assertEqual(current_tab, tab, msg=f'{current_tab} is not equal to {tab} in volleyball sport landing page')

    def test_009_verify_alignment_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Alignment of Sports ribbon tab
        EXPECTED: Alignment should be proper and below things need to verify:
        EXPECTED: Foreground Image
        EXPECTED: Background Image
        EXPECTED: Text Alignment.
        """
        pass
        # covered in C65900572

    def test_010_verify_sub_menu_tabs(self):
        """
        DESCRIPTION: Verify Sub menu tabs
        EXPECTED: All the configured sub menu tabs should be displayed as per cms
        EXPECTED: In-play,Competitions, outrights and specials.
        """
        actual_volleyball_tabs = self.site.sports_page.tabs_menu.items_names
        self.expected_cms_tabs()
        self.assertListEqual(sorted(actual_volleyball_tabs), sorted(self.expected_tabs),
                             msg=f'actual sub tabs {actual_volleyball_tabs} are not equal to expected sub tabs {self.expected_tabs}')