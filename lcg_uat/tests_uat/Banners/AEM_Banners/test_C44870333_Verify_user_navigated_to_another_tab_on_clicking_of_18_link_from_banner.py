import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.p2
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C44870333_Verify_user_navigated_to_another_tab_on_clicking_of_18_link_from_banner(Common):
    """
    TR_ID: C44870333
    NAME: Verify user navigated to another tab on clicking of 18+ link from banner
    DESCRIPTION: This test case verifies AEM Banners displaying according to New / Existing Users
    PRECONDITIONS: AEM Banners should be enabled in CMS
    PRECONDITIONS: UserName : goldebuild1  Password: password1
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_log_in_with_user_new__existing_user(self):
        """
        DESCRIPTION: Log in with user new / existing user
        EXPECTED: User is logged in
        """
        self.site.login()

    def test_003_verify_aem_banners_on_hp(self):
        """
        DESCRIPTION: Verify AEM banners on HP
        EXPECTED: AEM banners are displayed on Homepage
        """
        system_configuration = self.cms_config.get_system_configuration_structure()
        banner_status = system_configuration.get('DynamicBanners')
        self.assertTrue(banner_status['enabled'], msg='"AEM banners" are not enabled')
        result = self.site.contents.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='"AEM Banners" are not displayed')

    def test_004_verify_user_navigated_to_correct_page_on_clicking_of_18plus_link_from_banner(self):
        """
        DESCRIPTION: Verify user navigated to correct page on clicking of 18+ link from banner
        EXPECTED: User navigated to promotion page
        """
        url_before_click = self.device.get_current_url()
        self.site.contents.aem_banner_section.active_banner.mouse_over()
        self.site.contents.aem_banner_section.active_banner.click()
        self.site.wait_content_state_changed()
        url_after_click = self.device.get_current_url()
        self.assertNotEqual(url_before_click, url_after_click,
                            msg=f'URL "{url_before_click}" before click is same as URL "{url_after_click}" after click')

    def test_005_repeat_step_4_for_all_sports_and_racing(self):
        """
        DESCRIPTION: repeat step #4 for all sports and racing
        EXPECTED: User navigated to promotion page
        """
        sports_list = ['horse-racing', 'sport/football', 'sport/tennis', 'greyhound-racing/today']
        for sports_name in sports_list:
            self.navigate_to_page(name=sports_name)
            self.test_004_verify_user_navigated_to_correct_page_on_clicking_of_18plus_link_from_banner()
