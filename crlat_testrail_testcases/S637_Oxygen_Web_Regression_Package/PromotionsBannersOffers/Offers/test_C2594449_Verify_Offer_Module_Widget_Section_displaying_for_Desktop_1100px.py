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
class Test_C2594449_Verify_Offer_Module_Widget_Section_displaying_for_Desktop_1100px(Common):
    """
    TR_ID: C2594449
    NAME: Verify Offer Module Widget/Section displaying for Desktop >= 1100px
    DESCRIPTION: This test case verifies Offer Module Widget/Section displaying for Desktop on the page >= 1100px
    DESCRIPTION: AUTOTEST: [C2605272]
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

    def test_001_verify_offer_modules_presence(self):
        """
        DESCRIPTION: Verify Offer Modules presence
        EXPECTED: * Offers are present at the Content Area next to AEM Banners
        EXPECTED: * Offer widget is NOT present at the Right column
        """
        pass

    def test_002_verify_ordering_of_offer_modulesand_offer_images(self):
        """
        DESCRIPTION: Verify ordering of Offer Modules and Offer Images
        EXPECTED: Every Offer Module contains Offer images in order set via CMS
        """
        pass

    def test_003_verify_module_content(self):
        """
        DESCRIPTION: Verify Module content
        EXPECTED: Each Module consists of:
        EXPECTED: *   Related to particular Module Offers images
        EXPECTED: *   Navigation Arrows
        """
        pass

    def test_004_verify_navigation_arrows(self):
        """
        DESCRIPTION: Verify Navigation Arrows
        EXPECTED: * Navigation Arrows are located at the left and right side of the Offer section
        EXPECTED: * Navigation Arrows appear after mouse hovering on Offer images
        EXPECTED: * Next or Previous Offer image appears after clicking on Right/Left Navigation Arrow
        """
        pass

    def test_005_verify_navigation_between_offers_images(self):
        """
        DESCRIPTION: Verify navigation between Offers images
        EXPECTED: * Scrolling Offer images to the left or right using Navigation Arrows
        EXPECTED: * Maximum 3 offers images can be presented inside one Offer Module
        EXPECTED: * Offer images are shown in continuous loop automatically
        """
        pass

    def test_006_clicktap_on_the_offer_image(self):
        """
        DESCRIPTION: Click/Tap on the Offer image
        EXPECTED: * User is redirected to the page, path for which is set in 'Target Uri' field in CMS
        EXPECTED: * If link is Oxygen one (within current site) refresh should NOT happen (no splash screen displayed)
        EXPECTED: *  Target Uri' supports internal (e.g. football/today) and external (begins with http/https) Uri's
        """
        pass
