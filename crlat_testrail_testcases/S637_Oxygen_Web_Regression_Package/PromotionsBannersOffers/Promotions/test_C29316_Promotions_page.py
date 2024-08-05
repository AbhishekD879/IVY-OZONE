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
class Test_C29316_Promotions_page(Common):
    """
    TR_ID: C29316
    NAME: Promotions page
    DESCRIPTION: The purpose of this test case is to verify Promotions page and its content
    PRECONDITIONS: Make sure that there are promotion created in CMS and linked to active signposting promotions (by Event/Market Flags)
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: **'expandedAmount' **field be can found in 'System-configuration' section of CMS
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_navigate_to_promotions_page_from_sports_menu_ribbon_or_left_navigation_menu(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page from 'Sports Menu Ribbon' or 'Left Navigation' menu
        EXPECTED: * 'Promotions' page is opened
        EXPECTED: * List of all available promotions is present
        EXPECTED: * Promotions are displayed on 3 columns **For Desktop and Tablet in Landscape view**
        EXPECTED: * Promotions are displayed on 2 columns **For Tablet in Portrait view and For Desktop depends on page width**
        EXPECTED: * Promotions are displayed on 1 columns **For Mobile and For Desktop depends on page width**
        """
        pass

    def test_002_verify_promotions_page(self):
        """
        DESCRIPTION: Verify 'Promotions' page
        EXPECTED: * 'Promotions' page consists of:
        EXPECTED: *   'Back' button
        EXPECTED: *   **'Promotions'** page title
        EXPECTED: *   Page content
        EXPECTED: *   Section content
        """
        pass

    def test_003_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: By clicking/tapping the 'Back' button user is navigated to the previous page
        """
        pass

    def test_004_verify_page_content(self):
        """
        DESCRIPTION: Verify Page content
        EXPECTED: The list of all active promotions is shown
        """
        pass

    def test_005_verify_section_title(self):
        """
        DESCRIPTION: Verify Section title
        EXPECTED: Section title is set in CMS ('Title' field)
        """
        pass

    def test_006_verify_section_content(self):
        """
        DESCRIPTION: Verify section content
        EXPECTED: The section consists of:
        EXPECTED: *   Promotion image
        EXPECTED: *   Section title
        EXPECTED: *   Short description
        EXPECTED: *   'More info' button
        """
        pass

    def test_007_verify_promotion_image(self):
        """
        DESCRIPTION: Verify Promotion image
        EXPECTED: Promotion image is downloaded in CMS
        """
        pass

    def test_008_verify_short_description(self):
        """
        DESCRIPTION: Verify short description
        EXPECTED: * Short description is set in CMS ('Short description' field)
        EXPECTED: * Only the first 3 lines of text will be shown then the text will be truncated
        """
        pass

    def test_009_verify_more_info_button(self):
        """
        DESCRIPTION: Verify 'More info' button
        EXPECTED: By clicking/tapping 'More info' button user is navigated to Promotion Details page
        """
        pass
