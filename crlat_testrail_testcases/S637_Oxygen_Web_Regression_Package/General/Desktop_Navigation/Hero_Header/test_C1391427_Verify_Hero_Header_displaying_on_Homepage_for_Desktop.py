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
class Test_C1391427_Verify_Hero_Header_displaying_on_Homepage_for_Desktop(Common):
    """
    TR_ID: C1391427
    NAME: Verify Hero Header displaying on Homepage for Desktop
    DESCRIPTION: This test case verifies Hero Header displaying on Homepage for Desktop.
    PRECONDITIONS: The following data is available:
    PRECONDITIONS: - Enhanced Markets (Private Markets)
    PRECONDITIONS: - Enhanced Multiples
    PRECONDITIONS: - Banners
    PRECONDITIONS: - Offers
    PRECONDITIONS: - Banach events
    PRECONDITIONS: - Featured modules
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True

    def test_001_verify_hero_header_content_on_the_homepage(self):
        """
        DESCRIPTION: Verify Hero Header content on the Homepage
        EXPECTED: Main View 1 and Main View 2 columns are merged and contain the following element:
        EXPECTED: * AEM Banners section and Offer area (depends on screen width)
        EXPECTED: * Enhanced multiples carousel
        EXPECTED: Module Ribbon tabs are transformed in the next sections:
        EXPECTED: * Your Enhanced Markets
        EXPECTED: * In-Play & Live Stream
        EXPECTED: * Next Races Carousel
        EXPECTED: * Build Your Bet
        EXPECTED: * Featured area
        """
        pass
