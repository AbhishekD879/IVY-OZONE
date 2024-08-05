import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.promotions_banners_offers
@vtest
class Test_C28116_Verify_Offer_Module_Widget_Section_displaying_depends_on_screen_resolution(Common):
    """
    TR_ID: C28116
    NAME: Verify Offer Module Widget/Section displaying depends on screen resolution
    DESCRIPTION: This test case verifies Offer Module Widget/Section displaying for Desktop depends on screen resolution
    DESCRIPTION: AUTOTEST: [C2608336]
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure that several offer modules are created
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    """
    keep_browser_open = True

    def test_001_resize_the_page_to__1100px_width_and_verify_offer_modules_location(self):
        """
        DESCRIPTION: Resize the page to < 1100px width and verify Offer Modules location
        EXPECTED: * Offer widget is present at the Right column
        EXPECTED: * Every Offer Module is displayed in a separate section
        """
        pass

    def test_002_resize_the_page_to__1100px_width_and_verify_offer_modules_location(self):
        """
        DESCRIPTION: Resize the page to >= 1100px width and verify Offer Modules location
        EXPECTED: * Offers are present next to AEM Banners
        EXPECTED: * Offer widget is NOT present at the Right column anymore
        """
        pass
