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
class Test_C667796_AEM_Banners_links_opening(Common):
    """
    TR_ID: C667796
    NAME: AEM Banners links opening
    DESCRIPTION: This test case verifies AEM Banners links opening
    PRECONDITIONS: 1. AEM Banners should be enabled in CMS
    PRECONDITIONS: 2. To check data from **offer** response open Dev tools -> Network tab
    PRECONDITIONS: 3. This test case should be checked on Mobile, Tablet
    PRECONDITIONS: -
    PRECONDITIONS: Please note that number of banners between IOS and Android platforms may differ for the same page.
    PRECONDITIONS: To check Request URL to banners please go to Dev tools -> Network -> All -> response.json -> Headers / Response
    PRECONDITIONS: To check Request URL to Target banners  please go to Dev tools -> Network -> All -> json?mbox=target-global-mbox... -> Headers / Response
    PRECONDITIONS: To check if target content is loaded on UI navigate to Console -> type window.adobe.target -> enter
    PRECONDITIONS: ![](index.php?/attachments/get/36029)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: * Homepage is opened
        EXPECTED: * Dynamic Banners are displayed on Promotions Banner Carousel
        """
        pass

    def test_002_tap_dynamic_banner(self):
        """
        DESCRIPTION: Tap Dynamic Banner
        EXPECTED: * New browser tab is opened if appTarget/webTarget ":_blank" received in **offers** / **rg**, otherwise in same browser tab
        EXPECTED: * User is navigated to URL received in **offers** or **rg** -> "appUrl" / "webUrl" response
        EXPECTED: -
        EXPECTED: Note that this area doesn't always have a response for a tap(on TST2 env-t)
        """
        pass

    def test_003_tap_on_togglehtml_overlay_on_the_banner(self):
        """
        DESCRIPTION: Tap on toggle/HTML overlay on the Banner
        EXPECTED: * New browser tab is opened if app_target:"_blank" received in  **offers**, otherwise in same browser tab
        EXPECTED: * User is navigated to URL received in **offers** or **rg** -> "mobTandCLink:" / "webTandCLink" response
        """
        pass

    def test_004_go_to_any_sport__race_landing_or_details_page_and_repeat_step_2_3(self):
        """
        DESCRIPTION: Go to any <Sport> / <Race> landing or details page and repeat step #2-3
        EXPECTED: 
        """
        pass
