import pytest

import tests
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.AEM_Banners.BaseAEMBannersTest import BaseAEMBannersTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.banners
# @pytest.mark.aem_banners
# @pytest.mark.promotions_banners_offers
# @pytest.mark.desktop
# @pytest.mark.medium
# @pytest.mark.safari
# @pytest.mark.login
# @vtest
@pytest.mark.na
class Test_C667794_AEM_Banners_displaying_according_to_Page(BaseAEMBannersTest):
    """
    TR_ID: C667794
    NAME: AEM Banners displaying according to Page
    DESCRIPTION: This test case verifies AEM Banners displaying according to Page
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. This test case should be checked on Mobile, Tablet, Desktop
    PRECONDITIONS: 3. To check data from **offer** response open Dev tools -> Network tab
    PRECONDITIONS: 4. User is logged out
    """
    keep_browser_open = True
    sport_url_params = {
        'sport/football': 'football',
        'horse-racing': 'horse-racing',
        'lotto': 'lotto',
        'tote': 'intl-tote'
    }

    def check_url_on_page(self, name):
        offer_call = wait_for_result(lambda: self.get_offers_url(),
                                     name='get AEM banners request is done',
                                     timeout=3)
        self.assertTrue(offer_call, msg=f'Get AEM banners request was not done on page: "{name}"')
        self.assertIn('pages/%s' % name, offer_call)

    def test_001_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        """
        result = self.site.contents.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='AEM Banners are not displayed')

    def test_002_check_aem_banner_request(self):
        """
        DESCRIPTION: Check request
        EXPECTED: * 'pages/homepage' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        """
        self.check_url_on_page(name='homepage')

    def test_003_go_to_the_next_pages_one_by_one_sport_race_lotto_international_tote_and_repeat_step_2(self):
        """
        DESCRIPTION: Go to the next pages one by one:
        DESCRIPTION: * <Sport>
        DESCRIPTION: * <Race>
        DESCRIPTION: * Lotto
        DESCRIPTION: * International Tote
        DESCRIPTION: and repeat step #2
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items configured in CMS (system-configuration/structure)
        """
        for sport, url_param in self.sport_url_params.items():
            self.navigate_to_page(name=sport)
            self.site.wait_content_state(state_name=sport.split('/')[-1])
            self.check_url_on_page(url_param)
            if not self.site.contents.has_aem_banners:
                self._logger.warning(f'*** Skipping verification of banners quantity '
                                     f'as they are not enabled for "{sport}"')
            else:
                dynamic_banners_config = self.get_initial_data_system_configuration().get('DynamicBanners', {})
                if not dynamic_banners_config:
                    dynamic_banners_config = self.cms_config.get_system_configuration_item('DynamicBanners')
                offers_count = dynamic_banners_config.get('maxOffers')
                if offers_count is None:
                    raise CmsClientException('maxOffers value not configured in CMS')
                actual_banners_number = self.site.contents.aem_banner_section.number_of_banners
                # in case when number of Banners on UI is less than maxOffers value from cms
                assertion_method = self.assertEqual if tests.settings.backend_env == 'prod' else self.assertLessEqual
                if actual_banners_number < offers_count:
                    offers_response = self.get_offers_response()
                    self.softAssert(assertion_method, actual_banners_number, len(offers_response),
                                    msg=f'Number of Banners displayed "{actual_banners_number}" does not correspond '
                                    f'to number of Dynamic Banners received in **offer** response: '
                                    f'"{len(offers_response)}"')
                else:
                    # VOL-3493 AEM banner quantity fix(quantity is limited by maxOffers from DynamicBanners in cms)
                    self.softAssert(assertion_method, actual_banners_number, offers_count,
                                    msg=f'Number of Banners displayed "{actual_banners_number}" does not correspond '
                                    f'to number of Dynamic Banners from cms: "{offers_count}"')

    def test_004_log_in_and_repeat_steps_2_3(self):
        """
        DESCRIPTION: Log in and repeat steps #2-3
        """
        self.site.login(async_close_dialogs=False)
        self.navigate_to_page(name='/')
        self.site.wait_content_state('Homepage')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')
        self.test_002_check_aem_banner_request()
        self.test_003_go_to_the_next_pages_one_by_one_sport_race_lotto_international_tote_and_repeat_step_2()
