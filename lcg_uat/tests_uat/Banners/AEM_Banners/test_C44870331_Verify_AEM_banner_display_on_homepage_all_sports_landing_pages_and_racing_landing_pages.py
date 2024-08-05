import pytest
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p1
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C44870331_Verify_AEM_banner_display_on_homepage_all_sports_landing_pages_and_racing_landing_pages(Common):
    """
    TR_ID: C44870331
    NAME: Verify AEM banner display on homepage, all sports landing pages and racing landing pages.
    DESCRIPTION: This test case verifies AEM Banners displaying according to New / Existing Users
    PRECONDITIONS: AEM Banners should be enabled in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify AEM Banners are enabled in CMS
        PRECONDITIONS: AEM Banners should be enabled in CMS
        """
        system_configuration = self.cms_config.get_system_configuration_structure()
        banner_status = system_configuration.get('DynamicBanners')
        self.assertTrue(banner_status['enabled'], msg="AEM banner are not enabled")

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_log_in_with_user_new__existing_user(self):
        """
        DESCRIPTION: Log in with user new / existing user
        EXPECTED: User is logged in
        """
        self.site.login()

    def test_003_verify_aem_banners(self):
        """
        DESCRIPTION: Verify AEM banners
        EXPECTED: AEM banners are displayed on Homepage
        """
        result = self.site.home.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='AEM Banners are not displayed')

    def test_004_go_to_all__sport_or_race_page_and_repeat_step_3(self):
        """
        DESCRIPTION: Go to all  <Sport> or <Race> page and repeat step #3
        EXPECTED: AEM banners are displayed on all sports or races
        """
        if self.brand == 'bma':
            all_sports = vec.sb.ALL_SPORTS.upper()
        else:
            all_sports = vec.sb.ALL_SPORTS
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.click_item(all_sports)
            sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict.keys()
        else:
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict.keys()
        self.assertTrue(sports, msg='"Sports" list not found')
        for sport in sports:
            if self.device_type == 'mobile':
                az_sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            else:
                az_sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(az_sports, msg='"Sports" list not found')

            if sport in ['Baseball', 'Football', 'Tennis', 'Horse Racing', 'Greyhounds']:
                # Verifying AEM banners for top Sports.
                az_sports[sport].click()
                self.site.wait_splash_to_hide(4)
                self._logger.info(f'*** page is redirected to "{sport}" ***')
                self.test_003_verify_aem_banners()
                if self.device_type == 'mobile':
                    self.site.back_button.click()

    def test_005_log_out_and_verify_the_step_3__4(self):
        """
        DESCRIPTION: Log out and verify the step #3 & #4
        EXPECTED: AEM banners are displayed on Homepage
        EXPECTED: AEM banners are displayed on all sports or races
        """
        self.site.logout()
        self.site.wait_content_state("HomePage")
        self.test_003_verify_aem_banners()
        self.test_004_go_to_all__sport_or_race_page_and_repeat_step_3()
