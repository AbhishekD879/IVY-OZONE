import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.all_sports
@pytest.mark.desktop_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C65949655_Verify_A_Z_menu_display_as_per_CMS_config(Common):
    """
    TR_ID: C65949655
    NAME: Verify A-Z menu display as per CMS config.
    DESCRIPTION: this testcase verifies A-Z menu display as per CMS config.
    PRECONDITIONS: 1. Login to CMS
    PRECONDITIONS: 2. Navigate to CMS-> Sports category-> Sports category radio
    PRECONDITIONS: button should be selected by default
    PRECONDITIONS: 3. Navigate to CMS-> Sports category-> Click on sports ribbon applicable for mobile only
    PRECONDITIONS: 4. Note: make sure that "show in A-Z" and "show in sports ribbon" should be enable in sports level config
    PRECONDITIONS: Navigate to CMS-> Sports category-> Click on any sport-> click on "general sport configration"
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1) User should have oxygen CMS access
        PRECONDITIONS: 2) Configuration for  All Sports in LHN
        PRECONDITIONS: sport page->sport categories.
        PRECONDITIONS: 3)Click on All Sports sport category and make sure that "show in A-Z" and "show
                        in sports ribbon" should be enable in sports level config
        """
        sport_categories = self.cms_config.get_sport_categories()
        sport_category = next((category for category in sport_categories if category.get('imageTitle').strip().title() == 'All Sports'),None)
        if sport_category:
            if sport_category.get('disabled')==False and sport_category.get('showInHome') == True :
                all_sport = sport_category
            else:
                all_sport = self.cms_config.update_sport_category(sport_category_id=sport_category.get('id'), showInHome=True, disabled=False)
        else:
            all_sport = self.cms_config.create_sport_category(title='All Sports',
                                                                 categoryId = 0,
                                                                 ssCategoryCode='az-sports',
                                                                 tier='UNTIED',showInHome=True,
                                                                 targetUri = 'az-sports',showInAZ=True)
        self.__class__.sport_name = all_sport.get('imageTitle').upper().strip() if self.brand=='bma' else all_sport.get('imageTitle').strip()

        cms_footer_menus = self.cms_config.get_cms_menu_items(menu_types='Footer Menus').get('Footer Menus')
        all_sport_footer_menu = next((menu for menu in cms_footer_menus if menu.get('targetUri')=='az-sports' and menu.get('disabled')==False),None)
        if not all_sport_footer_menu:
            raise CmsClientException('all sport  is not configured in CMS')
        self.__class__.all_sport_footer_menu_name = all_sport_footer_menu.get('linkTitle').upper().strip() if self.brand=='bma' else all_sport_footer_menu.get('linkTitle').strip()

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch application
        EXPECTED: application launched successfully
        """
        self.site.go_to_home_page()

    def test_002_mobile_verify_all_sports_in_footer_menu(self):
        """
        DESCRIPTION: Mobile: Verify All Sports in footer menu
        EXPECTED: All Sports should be display in footer menu
        """
        if self.device_type =='mobile':
            footer_menues = list(self.site.navigation_menu.items_as_ordered_dict.keys())
            self.assertIn(self.all_sport_footer_menu_name, footer_menues, msg=f'{self.all_sport_footer_menu_name} is not present in {footer_menues}')

    def test_003_click_on_all_sports_from_footer_menu(self):
        """
        DESCRIPTION: Click on All Sports from footer menu
        EXPECTED: A-Z Sports menu should be display
        """
        if self.device_type == 'mobile':
            footer_menu = self.site.navigation_menu.items_as_ordered_dict.get(self.all_sport_footer_menu_name)
            footer_menu.click()
            self.site.wait_content_state(state_name='AllSports')
            az_sports_name = self.site.all_sports.a_z_sports_section.name
            expected_name = vec.SB.AZ_SPORTS.upper()
            self.assertEqual(az_sports_name.upper(), expected_name, msg=f'"{expected_name}" section is not displayed in all sports')

    def test_004_mobile_verify_all_sports_in_sports_ribbon(self):
        """
        DESCRIPTION: Mobile: Verify All Sports in sports ribbon
        EXPECTED: All Sports should be display in sports ribbon
        """
        if self.device_type == 'mobile':
            self.site.back_button.click()
            self.site.wait_content_state(state_name='HomePage')
            is_sports_ribbon_displayed = self.site.home.menu_carousel.is_displayed()
            self.assertTrue(is_sports_ribbon_displayed, msg=f'sport menu ribbon is not displayed')
            sport_ribbon_list = list(self.site.home.menu_carousel.items_as_ordered_dict.keys())
            self.assertIn(self.sport_name, sport_ribbon_list, msg=f'{self.sport_name} is not present in sport ribbon list {sport_ribbon_list}')
            all_sports = self.site.home.menu_carousel.items_as_ordered_dict.get(self.sport_name)
            all_sports.link.click()
            self.site.wait_content_state(state_name='AllSports')
            az_sports_name = self.site.all_sports.a_z_sports_section.name
            expected_name = vec.SB.AZ_SPORTS.upper()
            self.assertEqual(az_sports_name.upper(), expected_name, msg=f'"{expected_name}" section is not displayed in all sports')

    def test_005_click_on_all_sports_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on All Sports from sports ribbon
        EXPECTED: A-Z Sports menu should be display
        """
        # covered in above step

    def test_006_desktop_verify_a_z__menu_on_left_side(self):
        """
        DESCRIPTION: Desktop: Verify A-Z  menu on left side
        EXPECTED: A-Z Sports menu should be display
        """
        if self.device_type == 'desktop':
            az_sports = self.site.sport_menu
            self.assertTrue(az_sports, msg='A-Z sport menu is not displayed')
            az_links = self.site.sport_menu.sport_menu_items_group('AZ')
            self.assertTrue(az_links, msg='"A-Z Menu" section is not found')


