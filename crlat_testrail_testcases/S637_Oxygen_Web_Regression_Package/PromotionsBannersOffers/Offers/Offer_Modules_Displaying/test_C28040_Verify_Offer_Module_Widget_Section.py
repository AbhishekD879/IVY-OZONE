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
class Test_C28040_Verify_Offer_Module_Widget_Section(Common):
    """
    TR_ID: C28040
    NAME: Verify Offer Module Widget/Section
    DESCRIPTION: This test case verifies Offer Module Widgets/Section and their content
    DESCRIPTION: **Note:**
    DESCRIPTION: This test case applicable only for Tablet and Desktop < 1100px.
    DESCRIPTION: AUTOTEST: [C527833]
    PRECONDITIONS: 1. In CMS Prepare few (3 should be fine) offer modules with offers, at least one offer module with multiple offers inside (they can contain up to 3)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Make sure that several offer modules are created
    PRECONDITIONS: **Warning!**
    PRECONDITIONS: This test case applicable only for Tablet and Desktop with screen width less than 1100px. You can resize the browser window.
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: **How to create Offers and Offer modules in CMS**
    PRECONDITIONS: - Create several Offer modules with Offer images inside via CMS using the next path:
    PRECONDITIONS: * Offers -> Offer Modules -> Create Offer Module
    PRECONDITIONS: * Offers -> Offers -> Create Offer
    """
    keep_browser_open = True

    def test_001_verify_offer_modules_presence(self):
        """
        DESCRIPTION: Verify Offer Modules presence
        EXPECTED: *   All available Offer Modules are present in the 3-rd column
        EXPECTED: *   Every Offer Module is displayed in the separate section which is collapsible/expandable
        """
        pass

    def test_002_verify_ordering_of_offer_modules(self):
        """
        DESCRIPTION: Verify ordering of Offer Modules
        EXPECTED: Offer Modules order corresponds to the set in CMS by drag-n-drop order on 'Offer Modules' page
        """
        pass

    def test_003_verify_module_content(self):
        """
        DESCRIPTION: Verify Module content
        EXPECTED: Each Module consists of:
        EXPECTED: *   Module title
        EXPECTED: *   Related to particular Module Offers images
        EXPECTED: *   Navigation pills
        """
        pass

    def test_004_verifymodule_title(self):
        """
        DESCRIPTION: Verify Module title
        EXPECTED: *   Module title is CMS-controllable ('title' field)
        EXPECTED: *   Module title should be not null or empty
        """
        pass

    def test_005_verify_navigation_pills(self):
        """
        DESCRIPTION: Verify navigation pills
        EXPECTED: Navigation pills indicate displaying of current Offer image within particular Module
        """
        pass

    def test_006_verify_ordering_of_offers_images(self):
        """
        DESCRIPTION: Verify ordering of Offers images
        EXPECTED: Offers images order corresponds to the set in CMS by drag-n-drop order on 'Offer' page
        """
        pass

    def test_007_verify_navigation_between_offers_images(self):
        """
        DESCRIPTION: Verify navigation between Offers images
        EXPECTED: *   User can scroll left or right within each Module
        EXPECTED: *   Images are displayed correctly
        EXPECTED: *   Maximum 3 offers images can be presented inside one Offer Module
        EXPECTED: *   Offers should be shown in the continuous loop automatically
        """
        pass

    def test_008_create_some_new_modules_and_upload_images_of_different_height(self):
        """
        DESCRIPTION: Create some new modules and upload images of different height
        EXPECTED: Modules are created and visible on front-end
        """
        pass

    def test_009_verify_auto_adjusting_of_the_module_to_the_images_height(self):
        """
        DESCRIPTION: Verify auto-adjusting of the module to the image's height
        EXPECTED: * Module height should auto-adjust to the image's size
        EXPECTED: NOTE: Uploading 2-3 images of different sizes to the same module is considered to be incorrect configuration. In such case module will adjust to the size of the picture, which is first received in the response
        """
        pass

    def test_010_clicktap_on_the_offer_image(self):
        """
        DESCRIPTION: Click/Tap on the Offer image
        EXPECTED: *   After clicking/tapping on the Offer image user is redirected to the page, path for which is set in 'Target Uri' field in CMS
        EXPECTED: *   'Target Uri' supports internal (e.g. football/today) and external (begins with http/https) Uri's
        """
        pass
