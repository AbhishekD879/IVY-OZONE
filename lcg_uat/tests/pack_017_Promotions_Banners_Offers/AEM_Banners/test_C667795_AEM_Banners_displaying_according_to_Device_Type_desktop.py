import pytest
import tests
from selenium.webdriver import ActionChains
from tests.base_test import vtest
from tests.pack_017_Promotions_Banners_Offers.AEM_Banners.BaseAEMBannersTest import BaseAEMBannersTest
from voltron.pages.shared import get_driver
from voltron.utils.waiters import wait_for_result


# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.banners
# @pytest.mark.aem_banners
# @pytest.mark.desktop
# @pytest.mark.promotions_banners_offers
# @pytest.mark.safari
# @vtest
@pytest.mark.na
class Test_C667795_AEM_Banners_displaying_according_to_Device_Type_desktop(BaseAEMBannersTest):
    """
    TR_ID: C667795
    VOL_ID: C9698690
    NAME: AEM Banners displaying according to Device Type Desktop
    DESCRIPTION: This test case verifies AEM Banners displaying according to Device Type
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. To check data from **offer** response open Dev tools -> Network tab
    PRECONDITIONS: 3. This test case should be checked on Mobile, Tablet, Desktop
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    sport_name = 'football'

    def test_001_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop
        EXPECTED: Homepage is opened
        """
        result = self.site.contents.aem_banner_section.wait_for_banners()
        self.assertTrue(result, msg='AEM Banners are not displayed')

    def test_002_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: Banner arrows are displayed
        EXPECTED: * 'channels//' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        """
        result = wait_for_result(lambda: self.site.contents.aem_banner_section.has_arrow_previous,
                                 name='Checking for Previous Arrow webelement',
                                 timeout=40)
        self.assertTrue(result, msg='Previous Arrow webelement returned null')
        we = self.site.contents.aem_banner_section.arrow_previous
        ActionChains(get_driver()).move_to_element(we).perform()
        self.assertTrue(self.site.contents.aem_banner_section.has_arrow_previous, msg='No < arrow found')
        self.assertTrue(self.site.contents.aem_banner_section.has_arrow_next, msg='No > arrow found')
        offer_call = self.get_offers_url()
        self.assertIn('channels/mobile/', offer_call)  # 'channels/mobile/' temporarily

    def test_003_navigate_to_sport_race_page_and_repeat_step_2(self):
        """
        DESCRIPTION: Navigate to sport/race page and repeat step #2
        """
        self.navigate_to_page(name=f'sport/{self.sport_name}')
        self.site.wait_content_state(self.sport_name)
        offer_call = self.get_offers_url()
        self.assertTrue(offer_call, msg=f'No offers call found on {self.sport_name.title()} page')
        self.assertIn('channels/mobile/', offer_call)  # 'channels/mobile/' temporarily
