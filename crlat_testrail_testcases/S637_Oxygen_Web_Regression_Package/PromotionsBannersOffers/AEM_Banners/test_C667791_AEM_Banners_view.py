import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.promotions_banners_offers
@vtest
class Test_C667791_AEM_Banners_view(Common):
    """
    TR_ID: C667791
    NAME: AEM Banners view
    DESCRIPTION: This test case verifies AEM Banners view
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. For Big Competition AEM Banners should be selected in CMS: ( e.g. COMPETITIONS -> WORLD CUP -> (FEATURED, PROMO) tabs, -> 'AEM module). 'Fusion team Page value' field should be populated manually from AEM Component page list. https://confluence.egalacoral.com/display/SPI/AEM+banners.+List+of+Fusion+team+Page
    PRECONDITIONS: 3. To check data from **json** response open Dev tools -> Network tab
    PRECONDITIONS: ![](index.php?/attachments/get/109061290)
    PRECONDITIONS: 4. This test case should be checked on Mobile, Tablet, Desktop
    PRECONDITIONS: To check Request URL to banners please go to Dev tools -> Network -> All -> response.json -> Headers / Response
    PRECONDITIONS: To check Request URL to Target banners please go to Dev tools -> Network -> All -> json?mbox=target-global-mbox... -> Headers / Response
    PRECONDITIONS: To check if target content is loaded on UI navigate to Console -> type window.adobe.target -> enter
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: * Homepage is opened
        """
        pass

    def test_002_verify_dynamic_banners_presence(self):
        """
        DESCRIPTION: Verify Dynamic Banners presence
        EXPECTED: * Dynamic Banners are displayed on Promotions Banner Carousel
        """
        pass

    def test_003_verify_dynamic_banners_displaying(self):
        """
        DESCRIPTION: Verify Dynamic Banners displaying
        EXPECTED: * Navigation arrows are displayed at the left and right side of Banner (only Desktop and tablet versions)
        EXPECTED: * Number of Banners displayed correspond to quantity of Dynamic Banners configured in CMS (system-configuration/structure)
        EXPECTED: * Terms and Conditions placeholder is displayed below Banner image
        EXPECTED: * Progress bar is displayed under the Dynamic Banner if there are 2 or more banners received
        """
        pass

    def test_004_verify_dynamic_banner_image(self):
        """
        DESCRIPTION: Verify Dynamic Banner image
        EXPECTED: * Dynamic Banner image corresponds to **imgUrl** attribute from **json** response
        """
        pass

    def test_005_verify_dynamic_banners_size(self):
        """
        DESCRIPTION: Verify Dynamic Banners size
        EXPECTED: * Height of Dynamic Banner depends on the banner uploaded (max banner container's height is set to 400px - applicable for mobile version only)
        EXPECTED: * Width depends on screen resolution of device
        """
        pass

    def test_006_verify_terms_and_conditions_placeholder_html_overlay(self):
        """
        DESCRIPTION: Verify Terms and Conditions placeholder (HTML Overlay)
        EXPECTED: Terms and Conditions placeholder corresponds to **webTandC** attribute from **json** response
        """
        pass

    def test_007_verify_navigation_between_dynamic_banners(self):
        """
        DESCRIPTION: Verify navigation between Dynamic Banners
        EXPECTED: * User can scroll left or right within Banner Carousel
        EXPECTED: * Dynamic Banners are navigated automatically
        EXPECTED: * Dynamic Banners are shown in continuous loop
        """
        pass
