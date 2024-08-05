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
class Test_C667794_AEM_Banners_displaying_according_to_Page(Common):
    """
    TR_ID: C667794
    NAME: AEM Banners displaying according to Page
    DESCRIPTION: This test case verifies AEM Banners displaying according to Page
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. For Big Competition AEM Banners should be selected in CMS: ( e.g. COMPETITIONS -> WORLD CUP -> (FEATURED, PROMO) tabs, -> 'AEM module). 'Fusion team Page value' field should be populated manually from AEM Component page list. https://confluence.egalacoral.com/display/SPI/AEM+banners.+List+of+Fusion+team+Page
    PRECONDITIONS: 3. This test case should be checked on Mobile, Tablet, Desktop
    PRECONDITIONS: 4. To check data from **json** response open Dev tools -> Network tab
    PRECONDITIONS: ![](index.php?/attachments/get/109061289)
    PRECONDITIONS: 5. User is logged out
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

    def test_002_verify_dynamic_banners_loading(self):
        """
        DESCRIPTION: Verify Dynamic Banners loading
        EXPECTED: * 'pages/homepage' parameter is present as path in request URL
        EXPECTED: * Response with 'statusCode:'200' is received upon this request
        EXPECTED: * Quantity of Banners displayed on FE corresponds to number of items configured in CMS (system-configuration/structure)
        EXPECTED: * Dynamic Banners are displayed on FE according to response
        """
        pass

    def test_003_go_to_the_next_pages_one_by_one_sport_race_lotto_international_tote_olympics_world_cup_featured_promo_spetialand_repeat_step_3(self):
        """
        DESCRIPTION: Go to the next pages one by one:
        DESCRIPTION: * <Sport>
        DESCRIPTION: * <Race>
        DESCRIPTION: * Lotto
        DESCRIPTION: * International Tote
        DESCRIPTION: * Olympics
        DESCRIPTION: * World Cup (FEATURED, PROMO, SPETIAL)
        DESCRIPTION: and repeat step #3
        EXPECTED: Dynamic Banners are displayed
        """
        pass

    def test_004_go_to_the_next_module_for_world_cup_page_one_by_one(self):
        """
        DESCRIPTION: Go to the next module for 'World Cup' page one by one:
        EXPECTED: Dynamic Banners are displayed
        """
        pass

    def test_005_log_in_and_repeat_steps_2_3(self):
        """
        DESCRIPTION: Log in and repeat steps #2-3
        EXPECTED: Dynamic Banners are displayed
        """
        pass
