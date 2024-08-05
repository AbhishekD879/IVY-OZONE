import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2069260_Verify_integrating_third_party_Shop_Locator_as_Retail_feature(Common):
    """
    TR_ID: C2069260
    NAME: Verify integrating third party Shop Locator as Retail feature
    DESCRIPTION: This test case verifies integrating third-party Shop Locator into SportsBook.
    PRECONDITIONS: **Note that on UI Retail page should be named as 'Connect' for Coral App and 'The Grid' for Ladbrokes**
    PRECONDITIONS: A user has opened the Shop Locator
    PRECONDITIONS: The way to get to Shop Locator:
    PRECONDITIONS: - Open SB app -> Sports Menu Ribbon -> Connect OR The Grid -> Shop Locator
    """
    keep_browser_open = True

    def test_001_open_shop_locator(self):
        """
        DESCRIPTION: Open Shop Locator
        EXPECTED: Shop locator screen is opened:
        EXPECTED: - Breadcrumb shows '<' and 'Shop Locator'
        EXPECTED: - A search box with default value 'NW1', 'Near me' button, and 'List ' button are under 'Shop Locator' title
        EXPECTED: - A map is opened on 'NW1' location by default
        """
        pass

    def test_002_verify_breadcrumb__and_shop_locator(self):
        """
        DESCRIPTION: Verify breadcrumb '<' and 'Shop Locator'
        EXPECTED: * '< Shop Locator' redirects user to the previous page
        """
        pass

    def test_003_as_it_is_a_third_party_shop_locator_check_if_shop_locator_is_corresponding_to_ladbrokes_the_grid_shop_locatorhttpsthegridladbrokescomenshoplocator_in_general(self):
        """
        DESCRIPTION: As it is a third party Shop Locator, check if shop locator is corresponding to [Ladbrokes The Grid Shop Locator](https://thegrid.ladbrokes.com/en/shoplocator) in general.
        EXPECTED: * The shop locator view is similar to [Ladbrokes The Grid Shop Locator](https://thegrid.ladbrokes.com/en/shoplocator)
        EXPECTED: * Searching mechanism works in the same way as for The Grid (try to find the same location on both SportBook and The Grid)
        """
        pass
