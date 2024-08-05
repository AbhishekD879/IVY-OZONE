import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C852689_Verify_Hero_Header_displaying_on_Lotto_page_for_Desktop(Common):
    """
    TR_ID: C852689
    NAME: Verify Hero Header displaying on Lotto page for Desktop
    DESCRIPTION: This test case verifies Hero Header displaying on Lotto page.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Lotto page is opened
    PRECONDITIONS: 3. 'Straight' tab is opened by default
    """
    keep_browser_open = True

    def test_001_verify_hero_header_content_on_the_lotto_page(self):
        """
        DESCRIPTION: Verify Hero Header content on the Lotto page
        EXPECTED: Main View 1 and Main View 2 columns are merged and contain the following element:
        EXPECTED: * Lotto header and 'Back' button
        EXPECTED: * Breadcrumbs trail
        EXPECTED: * AEM Banners section and Offer area (depends on screen width)
        """
        pass

    def test_002_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: 'Back' button is displayed on the Lotto header
        """
        pass

    def test_003_verify_breadcrumbs_trail_displaying(self):
        """
        DESCRIPTION: Verify Breadcrumbs trail displaying
        EXPECTED: * Breadcrumbs trail is displayed below Lotto header
        EXPECTED: * Breadcrumbs trail is displayed in the next format: 'Home' > 'Lotto'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_004_verify_offer_section_displaying_next_to_the_aem_banners_section(self):
        """
        DESCRIPTION: Verify Offer section displaying next to the AEM Banners section
        EXPECTED: * Offer section is displayed next to the Banners when page size is >=1100px
        EXPECTED: * Offer widget is displayed in the 4th column when page size <1100px, AEM Banners occupies whole column width
        """
        pass

    def test_005_verify_aem_banner_section_displaying(self):
        """
        DESCRIPTION: Verify AEM Banner section displaying
        EXPECTED: * AEM banners are displayed below Breadcrumbs trail
        EXPECTED: * AEM Banner and Offer sections are not displayed at all if there are no available banners
        """
        pass
