import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C848905_Verify_Sports_Hero_Header_displaying_on_Sports_Landing_page_for_Desktop(Common):
    """
    TR_ID: C848905
    NAME: Verify Sports Hero Header displaying on Sports Landing page for Desktop
    DESCRIPTION: This test case verifies Sports Hero Header displaying on Sports Landing page content.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Sports Landing page is opened
    PRECONDITIONS: 3. 'Matches'->'Today' tab is opened by default
    PRECONDITIONS: 4. Enhanced Multiples are present
    PRECONDITIONS: 5. Offers are present
    """
    keep_browser_open = True

    def test_001_verify_sports_hero_header_content_on_the_sports_landing_page(self):
        """
        DESCRIPTION: Verify Sports Hero Header content on the Sports Landing page
        EXPECTED: Main View 1 and Main View 2 columns are merged and contain the following element:
        EXPECTED: * Sports header and 'Back' button
        EXPECTED: * Breadcrumbs trail
        EXPECTED: * AEM Banners section and Offer area (depends on screen width)
        EXPECTED: * Enhanced Multiples Caurosel
        EXPECTED: * Sports Sub tabs Menu
        """
        pass

    def test_002_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: 'Back' button is displayed on the Sports header
        """
        pass

    def test_003_verify_breadcrumbs_trail_displaying(self):
        """
        DESCRIPTION: Verify Breadcrumbs trail displaying
        EXPECTED: * Breadcrumbs trail is displayed below Sports header
        EXPECTED: * Breadcrumbs trail is displayed in the next format: 'Home' > 'Sports Name' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_004_verify_offer_section(self):
        """
        DESCRIPTION: Verify Offer section
        EXPECTED: * Offer section is displayed
        """
        pass

    def test_005_verify_aem_banners_section_displaying(self):
        """
        DESCRIPTION: Verify AEM Banners section displaying
        EXPECTED: * AEM banners are displayed below Breadcrumbs trail
        """
        pass

    def test_006_verify_enhanced_multiples_carousel_displaying(self):
        """
        DESCRIPTION: Verify Enhanced Multiples carousel displaying
        EXPECTED: * Enhanced Multiples carousel is displayed below AEM Banners section
        EXPECTED: * Enhanced Multiples carousel contains separated sports cards that are scrolled to right and left side
        """
        pass

    def test_007_verify_sports_subtabs_displaying(self):
        """
        DESCRIPTION: Verify Sports Subtabs displaying
        EXPECTED: The next Sports Subtabs are displayed for Football:
        EXPECTED: - 'In-Play'
        EXPECTED: - 'Matches'
        EXPECTED: - 'Competitions'
        EXPECTED: - 'Coupons'
        EXPECTED: - 'Outrights'
        EXPECTED: - 'Jackpot'
        EXPECTED: - 'Specials'
        EXPECTED: - 'Player Bets'
        EXPECTED: The next Sports Subtabs are displayed for other Sports:
        EXPECTED: - 'In-Play'
        EXPECTED: - 'Matches'
        EXPECTED: - 'Coupons'
        EXPECTED: - 'Outrights'
        """
        pass
