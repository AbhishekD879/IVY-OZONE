import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.AEM_Banners.BaseAEMBannersTest import BaseAEMBannersTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.p2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C44870332_Verify_functionality_of_banners_including_swipe_and_navigationNavigational_arrow_(BaseAEMBannersTest):
    """
    TR_ID: C44870332
    NAME: "Verify functionality of banners including swipe and navigation(Navigational arrow) "
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
        self.assertTrue(banner_status['enabled'], msg="AEM banner are not enabled")
        self.__class__.bannerSection = self.site.contents.aem_banner_section
        result = self.bannerSection.wait_for_banners()
        self.assertTrue(result, msg='"AEM Banners" are not displayed')

    def test_004_verify_functionality_of_banners_including_swipe_and_navigationnavigational_arrow(self):
        """
        DESCRIPTION: Verify functionality of banners including swipe and navigation(Navigational arrow)
        EXPECTED: User can scroll left or right within Banner Carousel
        EXPECTED: Dynamic Banners are navigated automatically
        EXPECTED: Dynamic Banners are shown in continuous loop
        EXPECTED: Verify the content is displayed correctly
        """
        # expected results in line 59,61 and 62 can not be automated
        if self.cms_config.get_system_configuration_structure()['DynamicBanners']['maxOffers'] > 1:
            cms_banners = self.get_initial_data_system_configuration().get('DynamicBanners', {})
            time_per_slide = cms_banners.get('timePerSlide')
            timeout = 2 * int(time_per_slide) if self.device_type == 'mobile' else 3 * int(time_per_slide)
            if self.brand == 'ladbrokes':
                start_banner_name = self.site.contents.aem_banner_section.active_banner.name
                wait_for_result(lambda: self.site.contents.aem_banner_section.active_banner.name != start_banner_name,
                                name='Next AEM banner to load',
                                timeout=timeout)
                next_banner_name = self.site.contents.aem_banner_section.active_banner.name
            else:
                banner_list = self.site.contents.aem_banner_section.items
                start_banner_name = banner_list[0].name
                wait_for_result(lambda: self.site.contents.aem_banner_section.items[0].name != start_banner_name,
                                name='Next AEM banner to load',
                                timeout=timeout)
                next_banner_name = self.site.contents.aem_banner_section.items[0].name
            self.assertNotEqual(start_banner_name, next_banner_name,
                                msg='Next AEM banner was not loaded automatically')

    def test_005_go_to_all_sport_or_race_page_and_repeat_step_4(self):
        """
        DESCRIPTION: Go to all <Sport> or <Race> page and repeat step #4
        EXPECTED: User can scroll left or right within Banner Carousel
        EXPECTED: Dynamic Banners are navigated automatically
        EXPECTED: Dynamic Banners are shown in continuous loop
        EXPECTED: Verify the content is displayed correctly
        """
        self.navigate_to_page(name=f'sport/{vec.Football.FOOTBALL_TITLE.lower()}')
        self.site.wait_content_state(vec.Football.FOOTBALL_TITLE.lower())
        self.test_004_verify_functionality_of_banners_including_swipe_and_navigationnavigational_arrow()

    def test_006_log_out_and_repeat_step_3_4_5(self):
        """
        DESCRIPTION: Log out and repeat step #3 #4 #5
        """
        self.site.logout()
        self.site.wait_content_state('Homepage')
        self.test_003_verify_aem_banners_on_hp()
        self.test_004_verify_functionality_of_banners_including_swipe_and_navigationnavigational_arrow()
        self.test_005_go_to_all_sport_or_race_page_and_repeat_step_4()
