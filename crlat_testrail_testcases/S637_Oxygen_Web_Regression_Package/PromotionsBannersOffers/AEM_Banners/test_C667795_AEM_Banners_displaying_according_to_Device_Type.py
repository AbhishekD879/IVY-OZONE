import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C667795_AEM_Banners_displaying_according_to_Device_Type(Common):
    """
    TR_ID: C667795
    NAME: AEM Banners displaying according to Device Type
    DESCRIPTION: This test case verifies AEM Banners displaying according to Device Type
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. To check data from **json** response open Dev tools -> Network tab
    PRECONDITIONS: ![](index.php?/attachments/get/109061288)
    PRECONDITIONS: 3. This test case should be checked on Mobile, Tablet, Desktop
    PRECONDITIONS: To check Request URL to banners please go to Dev tools -> Network -> All -> response.json -> Headers / Response
    PRECONDITIONS: To check Request URL to Target banners  please go to Dev tools -> Network -> All -> json?mbox=target-global-mbox... -> Headers / Response
    PRECONDITIONS: To check if target content is loaded on UI navigate to Console -> type window.adobe.target -> enter
    PRECONDITIONS: ![](index.php?/attachments/get/36029)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_mobile(self):
        """
        DESCRIPTION: Load Oxygen app on Mobile
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: * 'channels/mobile' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items received in response
        EXPECTED: * Dynamic Banners received in **offer** response are displayed on Promotions Banner Carousel
        """
        pass

    def test_003_navigate_to_sportrace_page_and_repeat_step_2(self):
        """
        DESCRIPTION: Navigate to sport/race page and repeat step #2
        EXPECTED: 
        """
        pass

    def test_004_repeat_steps__1_2_for_tablet(self):
        """
        DESCRIPTION: Repeat steps # 1-2 for Tablet
        EXPECTED: Results are the same
        """
        pass

    def test_005_load_oxygen_app_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop
        EXPECTED: Homepage is opened
        """
        pass

    def test_006_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: * 'channels//' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items received in response
        EXPECTED: * Dynamic Banners received in **json** response are displayed on Promotions Banner Carousel
        EXPECTED: **NOTE** currently 'channels/mobile' parameter is sent for Desktop
        """
        pass

    def test_007_navigate_to_sportrace_page_and_repeat_step_6(self):
        """
        DESCRIPTION: Navigate to sport/race page and repeat step #6
        EXPECTED: 
        """
        pass
