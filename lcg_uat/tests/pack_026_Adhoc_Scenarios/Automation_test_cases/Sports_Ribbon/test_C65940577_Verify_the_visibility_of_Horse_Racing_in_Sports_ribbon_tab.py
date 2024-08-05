import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_cms_reflection

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

class Test_C65940577_Verify_the_visibility_of_Horse_Racing_in_Sports_ribbon_tab(Common):
    """
    TR_ID: C65940577
    NAME: Verify the visibility of Horse Racing  in Sports ribbon tab
    DESCRIPTION: This test case is to validate About  sports ribbon tab as per cms configuration
    PRECONDITIONS: 1) User should have oxygen CMS access
    PRECONDITIONS: 2) Configuration for  Horse Racing in LHN
    PRECONDITIONS: sport page->sport categories.
    PRECONDITIONS: 3)Click on Horse Racing sport category
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

    def verify_of_sport_in_sport_menu_ribbon_tab(self, name ,expected_result = True):
        sport_tab= wait_for_cms_reflection(lambda: self.site.home.menu_carousel.items_as_ordered_dict.get(name),
                                             timeout=5, ref=self, haul=5, refresh_count=5,
                                             expected_result=expected_result)
        if expected_result:
            self.assertTrue(sport_tab, msg=f'{name} is not present in sport menu')
        else:
            self.assertFalse(sport_tab, msg=f'{name} is present in sport menu')

    def change_order_of_sport_in_sport_ribbon(self, sport_list: list, moving_id):
        sport_list.remove(moving_id)
        sport_list.insert(1, moving_id)
        new_order_list = sport_list
        self.cms_config.set_sport_category_ordering(new_order = new_order_list, moving_item = moving_id)
        wait_for_cms_reflection(lambda : list(self.site.home.menu_carousel.items_as_ordered_dict.keys()).index(self.sport_name)==1,
                                timeout=5, haul=5, ref=self)

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for  Horse Racing in LHN
        PRECONDITIONS: sport page->sport categories.
        PRECONDITIONS: 3)Click on Horse Racing sport category
        """
        sport_categories = self.cms_config.get_sport_categories()
        sport_category = next((category for category in sport_categories if category.get('imageTitle').strip().title() == 'Horse Racing'),None)
        if sport_category:
            if sport_category.get('disabled')==False and sport_category.get('showInHome') == True:
                horse_racing = sport_category
            else:
                horse_racing = self.cms_config.update_sport_category(sport_category_id=sport_category.get('id'), showInHome=True, disabled=False)
        else:
            horse_racing = self.cms_config.create_sport_category(title='Horse Racing',
                                                                 categoryId = self.ob_config.horseracing_config.category_id,
                                                                 ssCategoryCode='HORSE_RACING',
                                                                 tier='UNTIED',showInHome=True,
                                                                 targetUri = 'horse-racing')
        self.__class__.sport_name = horse_racing.get('imageTitle').upper().strip() if self.brand=='bma' else horse_racing.get('imageTitle').strip()
        self.__class__.sport_id = horse_racing.get('id')
        self.__class__.sport_ribbon_id_list = list(category.get('id') for category in self.cms_config.get_show_in_sports_ribbon())

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
        EXPECTED: Sports ribbon tab is applicable for Both logged in and Logged out user.
        """
        is_sports_menu_ribbon_displayed = self.site.home.menu_carousel.is_displayed()
        self.assertTrue(is_sports_menu_ribbon_displayed, msg=f'sport menu ribbon is not displayed')
        self.verify_of_sport_in_sport_menu_ribbon_tab(name = self.sport_name)
        self.site.login()
        is_sports_menu_ribbon_displayed = self.site.home.menu_carousel.is_displayed()
        self.assertTrue(is_sports_menu_ribbon_displayed, msg=f'sport menu ribbon is not displayed')
        self.verify_of_sport_in_sport_menu_ribbon_tab(name = self.sport_name)

    def test_003_verify_scrollability_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Scrollability of sports ribbon tab
        EXPECTED: Should be left and right scrollable and Image alignment should not be disturbed while scrolling .
        """
        sport_menu_items = list(self.site.home.menu_carousel.items_as_ordered_dict.items())
        first_item_name,first_item = sport_menu_items[0]
        last_item_name,last_item = sport_menu_items[-1]
        first_item.scroll_to()
        self.assertTrue(first_item.is_displayed(scroll_to=False),
                        msg=f"The first item {first_item_name} is not displayed after scrolling to {first_item_name}")
        last_item.scroll_to()
        self.assertTrue(last_item.is_displayed(scroll_to=False),
                        msg=f"The Last item {last_item_name} is not displayed after scrolling to {last_item_name}")

    def test_004_verify__horse_racing_sport_icon_is_displayed_and_clickable(self):
        """
        DESCRIPTION: Verify  Horse Racing sport icon is displayed and clickable
        EXPECTED: Horse Racing sport icon should be displayed and clickable
        """
        self.site.home.menu_carousel.click_item(self.sport_name)
        wait_content = self.site.wait_content_state(state_name='Horseracing')
        self.assertTrue(wait_content, msg='element is clickable')
        self.site.go_to_home_page()

    def test_005_verify_the_order_of_sport_by_using_drag_and_drop_in_cms(self):
        """
        DESCRIPTION: Verify the order of sport by using drag and drop in cms
        EXPECTED: Sport order should be changed after drag and drop in cms and same should be shown in Sport ribbon tab
        """
        self.change_order_of_sport_in_sport_ribbon(sport_list=self.sport_ribbon_id_list, moving_id=self.sport_id)
        sport_lists = list(self.site.home.menu_carousel.items_as_ordered_dict.keys())
        index_of_sport = sport_lists.index(self.sport_name)
        self.assertEqual(index_of_sport,1,msg=f'index position of {self.sport_name} in {index_of_sport} is not equal to 1')

    def test_006_verify__by_unchecking_show_in_sports_ribbon_tab_and_check_active_checkbox_in_cms(self):
        """
        DESCRIPTION: Verify  By unchecking "show in sports ribbon tab" and check "Active" checkbox in cms
        EXPECTED: Horse Racing sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id = self.sport_id, showInHome = False , disabled=False)
        self.verify_of_sport_in_sport_menu_ribbon_tab(name=self.sport_name,expected_result=False)
        self.cms_config.update_sport_category(sport_category_id=self.sport_id, showInHome=True, disabled=False)
        self.verify_of_sport_in_sport_menu_ribbon_tab(name=self.sport_name)

    def test_007_verify_by_uncheck_activecheckbox_and_check_show_in_sports_ribbon_tab_in_cms(self):
        """
        DESCRIPTION: Verify By uncheck "Active"checkbox and check "show in sports ribbon tab" in cms
        EXPECTED: Horse Racing sport should not display in Sports ribbon tab
        """
        self.cms_config.update_sport_category(sport_category_id = self.sport_id, showInHome = True , disabled=True)
        self.verify_of_sport_in_sport_menu_ribbon_tab(name=self.sport_name, expected_result=False)
        self.cms_config.update_sport_category(sport_category_id=self.sport_id, showInHome=True, disabled=False)
        self.verify_of_sport_in_sport_menu_ribbon_tab(name=self.sport_name)

    def test_008_verify_by_click_on_horse_racing_icon_in_sport_ribbon_tab(self):
        """
        DESCRIPTION: Verify by Click on Horse Racing Icon in sport ribbon tab
        EXPECTED: Should redirect to featured Tab of Horse Racing page.
        EXPECTED: By Default featured tab should be opened.
        EXPECTED: Lads: Meetings
        EXPECTED: Coral:Featured
        """
        self.site.home.menu_carousel.click_item(self.sport_name)
        self.site.wait_content_state(state_name='Horseracing')
        tab = vec.racing.RACING_DEFAULT_TAB_NAME
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, tab, msg=f'{current_tab} is not equal to {tab} in horse racing page')

    def test_009_verify_alignment_of_sports_ribbon_tab(self):
        """
        DESCRIPTION: Verify Alignment of Sports ribbon tab
        EXPECTED: Alignment should be proper and below things need to veify:
        EXPECTED: Foreground Image
        EXPECTED: Backkground Image
        EXPECTED: Text Alignment.
        """
        # covered in C65900572

    def test_010_verify_sub_menu_tabs(self):
        """
        DESCRIPTION: Verify Sub menu tabs
        EXPECTED: All the configured sub menu tabs should be displayed as per cms
        EXPECTED: future and specials tab are fixed tabs which should be displayed in FE.
        """
        actual_horse_racing_tabs = self.site.horse_racing.tabs_menu.items_names
        HR_tab_names = vec.racing.RACING_TAB_NAMES
        if self.brand=='ladbrokes' and self.cms_config.get_system_configuration_structure().get('NextRacesToggle').get('nextRacesTabEnabled') != True:
            HR_tab_names.remove(vec.racing.RACING_NEXT_RACES_NAME)
        self.assertListEqual(actual_horse_racing_tabs, HR_tab_names , msg=f'actual tabs {actual_horse_racing_tabs} is not equal to expected tabs {HR_tab_names}')