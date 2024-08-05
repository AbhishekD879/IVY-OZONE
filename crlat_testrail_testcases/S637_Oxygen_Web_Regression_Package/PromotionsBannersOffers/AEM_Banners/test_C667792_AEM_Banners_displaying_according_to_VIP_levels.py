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
class Test_C667792_AEM_Banners_displaying_according_to_VIP_levels(Common):
    """
    TR_ID: C667792
    NAME: AEM Banners displaying according to VIP levels
    DESCRIPTION: This test case AEM Banners displaying according to VIP levels
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. For Big Competition AEM Banners should be selected in CMS: ( e.g. COMPETITIONS -> WORLD CUP -> (FEATURED, PROMO) tabs, -> 'AEM module). 'Fusion team Page value' field should be populated manually from AEM Component page list. https://confluence.egalacoral.com/display/SPI/AEM+banners.+List+of+Fusion+team+Page
    PRECONDITIONS: 3. This test case should be checked on Mobile, Tablet, Desktop
    PRECONDITIONS: 4. To check data from **offer** response open Dev tools -> Network tab
    PRECONDITIONS: To check Request URL to banners please go to Dev tools -> Network -> All -> response.json -> Headers / Response
    PRECONDITIONS: To check Request URL to Target banners  please go to Dev tools -> Network -> All -> json?mbox=target-global-mbox... -> Headers / Response
    PRECONDITIONS: To check if target content is loaded on UI navigate to Console -> type window.adobe.target -> enter
    PRECONDITIONS: ![](index.php?/attachments/get/36029)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_user_that_has_vip_level__x(self):
        """
        DESCRIPTION: Log in with user that has VIP level = 'X'
        EXPECTED: User is logged in
        """
        pass

    def test_003_check_dynamic_banners_loading(self):
        """
        DESCRIPTION: Check Dynamic Banners loading
        EXPECTED: * 'imsLevel/X/' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items received in response
        EXPECTED: * Dynamic Banners are displayed on FE according to response
        """
        pass

    def test_004_go_to_any_sport__race_landing_page_and_repeat_step_3(self):
        """
        DESCRIPTION: Go to any <Sport> / <Race> landing page and repeat step #3
        EXPECTED: 
        """
        pass

    def test_005_go_to_the_world_cup_page_and_repeat_step_3(self):
        """
        DESCRIPTION: Go to the 'World Cup' page and repeat step #3
        EXPECTED: 
        """
        pass

    def test_006_log_out_and_repeat_steps_3_4(self):
        """
        DESCRIPTION: Log out and repeat steps #3-4
        EXPECTED: 
        """
        pass

    def test_007_log_in_with_user_that_has_different_than_on_step_2_vip_level_and_repeat_steps_3_5(self):
        """
        DESCRIPTION: Log in with user that has different than on step #2 VIP level and repeat steps #3-5
        EXPECTED: 
        """
        pass
