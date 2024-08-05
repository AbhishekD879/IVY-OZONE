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
class Test_C29317_Promotion_Details_page(Common):
    """
    TR_ID: C29317
    NAME: Promotion Details page
    DESCRIPTION: The purpose of this test case is to verify Promotions details page and its content
    DESCRIPTION: AUTOTEST: [C1119890]
    PRECONDITIONS: Make sure that there are promotions in CMS
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_promotions_page_from_sports_menu_ribbon_or_left_navigation_menu(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page from 'Sports Menu Ribbon' or 'Left Navigation' menu
        EXPECTED: * 'Promotions' page is opened
        EXPECTED: * List of all available promotions is present
        EXPECTED: * Promotions are displayed on 3 columns **For Desktop and Tablet in Landscape view**
        EXPECTED: * Promotions are displayed on 2 columns **For Tablet in Portrait view and For Desktop depends on page width**
        EXPECTED: * Promotions are displayed on 1 columns **For Mobile and For Desktop depends on page width**
        """
        pass

    def test_003_clicktap_more_information_button(self):
        """
        DESCRIPTION: Click/Tap 'More information' button
        EXPECTED: Promotion Details page is opened
        """
        pass

    def test_004_verify_promotion_details_page(self):
        """
        DESCRIPTION: Verify Promotion Details page
        EXPECTED: Promotion Details page consists of:
        EXPECTED: *   'Back' button
        EXPECTED: *   **'Promotions'** page title
        EXPECTED: *   Section title
        EXPECTED: *   Promotion image
        EXPECTED: *   Promotion description
        EXPECTED: *   'Terms and Conditions' panel
        """
        pass

    def test_005_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: By clicking/tapping the 'Back' button user is navigated to the previous page
        """
        pass

    def test_006_navigate_back_to_the_promotion_details_page(self):
        """
        DESCRIPTION: Navigate back to the Promotion Details page
        EXPECTED: Promotion Details page is opened
        """
        pass

    def test_007_verify_section_title(self):
        """
        DESCRIPTION: Verify Section title
        EXPECTED: * Section title is set in CMS ('Title' field)
        EXPECTED: * Section title is displayed on expandable/collapsible accordion
        EXPECTED: * Accordion is expanded by default
        """
        pass

    def test_008_verify_promotion_image(self):
        """
        DESCRIPTION: Verify Promotion image
        EXPECTED: Promotion image is downloaded in CMS
        """
        pass

    def test_009_verify_promotion_description(self):
        """
        DESCRIPTION: Verify Promotion description
        EXPECTED: Promotion description is set in CMS ('Description' field)
        """
        pass

    def test_010_verify_terms_and_conditions_panel(self):
        """
        DESCRIPTION: Verify 'Terms and Conditions' panel
        EXPECTED: * 'Terms and Conditions' panel is configured in CMS ('T&C' field)
        EXPECTED: * 'Terms and Conditions' panel is expandable/collapsible
        EXPECTED: * 'Terms and Conditions' panel is expanded by default
        """
        pass
