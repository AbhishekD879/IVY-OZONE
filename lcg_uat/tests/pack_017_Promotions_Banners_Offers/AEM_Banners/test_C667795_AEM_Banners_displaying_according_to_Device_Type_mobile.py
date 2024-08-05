import pytest

from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.AEM_Banners.BaseAEMBannersTest import BaseAEMBannersTest


# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.banners
# @pytest.mark.aem_banners
# @pytest.mark.promotions_banners_offers
# @pytest.mark.mobile_only
# @vtest
@pytest.mark.na
class Test_C667795_AEM_Banners_displaying_according_to_Device_Type_mobile(BaseAEMBannersTest):
    """
    TR_ID: C667795
    VOL_ID: C9698444
    NAME: AEM Banners displaying according to Device Type Mobile
    DESCRIPTION: This test case verifies AEM Banners displaying according to Device Type
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. To check data from **offer** response open Dev tools -> Network tab
    PRECONDITIONS: 3. This test case should be checked on Mobile, Tablet, Desktop
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_mobile(self):
        """
        DESCRIPTION: Load Oxygen app on Mobile
        EXPECTED: Homepage is opened
        """
        result = self.site.contents.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='AEM Banners are not displayed')

    def test_002_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: * 'channels/mobile' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        """
        offer_call = self.get_offers_url()
        self.assertIn('channels/mobile', offer_call)

    def test_003_navigate_to_sport_page_and_repeat_step_2(self):
        """
        DESCRIPTION: Navigate to sport page and repeat step #2
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        offer_call = self.get_offers_url()
        self.assertTrue(offer_call, msg='Offers call was not found on page')
        self.assertIn('channels/mobile', offer_call)
