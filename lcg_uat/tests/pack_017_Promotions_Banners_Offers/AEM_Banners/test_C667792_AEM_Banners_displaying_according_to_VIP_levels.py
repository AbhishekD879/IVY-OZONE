import pytest
import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.AEM_Banners.BaseAEMBannersTest import BaseAEMBannersTest


# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.banners
# @pytest.mark.aem_banners
# @pytest.mark.promotions_banners_offers
# @pytest.mark.mobile_only
# @pytest.mark.medium
# @pytest.mark.vanilla_adapted
# @vtest
@pytest.mark.na
class Test_C667792_AEM_Banners_displaying_according_to_VIP_levels(BaseAEMBannersTest):
    """
    TR_ID: C667792
    VOL_ID: C9698161
    NAME: AEM Banners displaying according to VIP levels
    DESCRIPTION: This test case AEM Banners displaying according to VIP levels
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. This test case should be checked on Mobile, Tablet, Desktop
    PRECONDITIONS: 3. To check data from **offer** response open Dev tools -> Network tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Define test users
        :return:
        """
        self.__class__.user_level_13 = tests.settings.gold_user_vip_level_13
        self.__class__.user_level_14 = tests.settings.platinum_user_vip_level_14
        if self.brand == 'ladbrokes':
            self.__class__.user_levels = {self.user_level_13: '62',
                                          self.user_level_14: '81'}
        else:
            self.__class__.user_levels = {self.user_level_13: '13',
                                          self.user_level_14: '14'}

    def test_001_log_in_with_user_that_has_vip_level__x(self):
        """
        DESCRIPTION: Log in with user that has VIP level = 'X'
        EXPECTED: User is logged in
        """
        self.site.login(username=self.user_level_13)
        result = self.site.contents.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='AEM Banners are not displayed')

    def test_002_check_dynamic_banners_loading(self):
        """
        DESCRIPTION: Check Dynamic Banners loading
        EXPECTED: * 'imsLevel/X/' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items received in response
        EXPECTED: * Dynamic Banners are displayed on FE according to response
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        offer_call = self.get_offers_url()
        self.assertTrue(offer_call, msg='Offers call was not found on page')
        self.assertIn('imsLevel/%s/' % self.user_levels[self.user_level_13], offer_call)

    def test_003_go_to_any_sport_race_landing_page_and_repeat_step_3(self):
        """
        DESCRIPTION: Go to any <Sport> / <Race> landing page and repeat step #3
        EXPECTED:
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state('football')
        self.test_002_check_dynamic_banners_loading()

    def test_004_log_out_and_repeat_steps_3_4(self):
        """
        DESCRIPTION: Log out and repeat steps #3-4
        """
        self.site.logout()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        offer_call = self.get_offers_url()
        self.assertIn('imsLevel/%s/' % self.user_levels[self.user_level_13], offer_call)

    def test_005_log_in_with_user_that_has_different_than_on_step_2_vip_level_and_repeat_steps_3_5(self):
        """
        DESCRIPTION: Log in with user that has different than on step #2 VIP level and repeat steps #3-5
        """
        self.site.login(username=self.user_level_14)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        offer_call = self.get_offers_url()
        self.assertIn('imsLevel/%s/' % self.user_levels[self.user_level_14], offer_call)
