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
class Test_C874379_Verify_Offer_Module_Widgets_and_their_content(Common):
    """
    TR_ID: C874379
    NAME: Verify Offer Module Widgets and their content
    DESCRIPTION: This test case verifies Offer Module Widgets and their content
    DESCRIPTION: AUTOTEST [C49892696]
    PRECONDITIONS: How to create Offer in CMS: https://ladbrokescoral.testrail.com/index.php?/cases/view/28046&group_by=cases:section_id&group_order=asc&group_id=304275
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/offers
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    PRECONDITIONS: To verify the response from CMS to check if offers are received by the app, search  in Network -> XHR - /cms/api/v2/bma/offers/desktop
    """
    keep_browser_open = True

    def test_001_load_oxygen_app_on_tablet_deviceand_desktop_screen_resolution_less_than_1100px(self):
        """
        DESCRIPTION: Load Oxygen app on tablet device and Desktop (screen resolution less than 1100px)
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_verify_offer_modules_presence(self):
        """
        DESCRIPTION: Verify Offer Modules presence
        EXPECTED: * All available Offer Modules are present right after 'Favourites' widget (configurable in CMS on 'Widgets Page');
        EXPECTED: * Every Offer Module is displayed in separate section which is collapsible/expandable;
        """
        pass

    def test_003_verify_ordering_of_offer_modules(self):
        """
        DESCRIPTION: Verify ordering of Offer Modules
        EXPECTED: Offer Modules order corresponds to the set in CMS by drag-n-drop order on 'Offer Modules' page
        """
        pass

    def test_004_verify_module_content(self):
        """
        DESCRIPTION: Verify Module content
        EXPECTED: Each Module consists of:
        EXPECTED: *   Module title;
        EXPECTED: *   Related to particular Module Offers images;
        EXPECTED: *   Navigation pills
        """
        pass

    def test_005_verifymodule_title(self):
        """
        DESCRIPTION: Verify Module title
        EXPECTED: *   Module title is CMS-controllable ('title' field);
        EXPECTED: *   Module title should be not null or empty.
        """
        pass

    def test_006_verify_navigation_pills(self):
        """
        DESCRIPTION: Verify navigation pills
        EXPECTED: Navigation pills indicate displaying of current Offer image within particular Module
        """
        pass

    def test_007_verify_ordering_of_offers_images(self):
        """
        DESCRIPTION: Verify ordering of Offers images
        EXPECTED: Offers images order corresponds to the set in CMS by drag-n-drop order on 'Offer' page
        """
        pass

    def test_008_verify_navigation_between_offers_images(self):
        """
        DESCRIPTION: Verify navigation between Offers images
        EXPECTED: *   User can scroll left or right within each Module;
        EXPECTED: *   Images are displayed correctly;
        EXPECTED: *   Maximum 3 offers images can be presented;
        EXPECTED: *   Offers should be shown in continuous loop automatically.
        """
        pass

    def test_009_clicktap_on_the_offer_image(self):
        """
        DESCRIPTION: Click/Tap on the Offer image
        EXPECTED: * User is redirected to the page, path for which is set in 'Target Uri' field in CMS
        EXPECTED: * 'Target Uri' supports internal (e.g. football/today) and external (begins with http/https) Uri's
        """
        pass

    def test_010_load_oxygen_app_on_desktop__with_screen_resolution__1100px_width_and_verify_offer_modules_presence(self):
        """
        DESCRIPTION: Load Oxygen app on Desktop  with screen resolution >= 1100px width and verify Offer Modules presence
        EXPECTED: * All available Offer Modules are present at the Content Area next to AEM Banners
        EXPECTED: * Offer widget is NOT present at the Right column
        """
        pass

    def test_011_verify_ordering_of_offer_modules_and_offer_images(self):
        """
        DESCRIPTION: Verify ordering of Offer Modules and Offer Images
        EXPECTED: Every Offer Module contains Offer images in order set via CMS
        """
        pass

    def test_012_verify_module_content(self):
        """
        DESCRIPTION: Verify Module content
        EXPECTED: Each Module consists of:
        EXPECTED: * Related to particular Module Offers images
        EXPECTED: * Navigation Arrows
        """
        pass

    def test_013_verify_navigation_arrows(self):
        """
        DESCRIPTION: Verify Navigation Arrows
        EXPECTED: * Navigation Arrows are located at the left and right side of the Offer section
        EXPECTED: * Next or Previous Offer image appears after clicking on Right/Left Navigation Arrow
        EXPECTED: * Maximum 3 offer images can be presented inside one Offer Module
        EXPECTED: * All configured Modules are available
        EXPECTED: * Offer images are shown in continuous loop automatically
        """
        pass
