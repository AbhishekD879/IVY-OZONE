import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C2635874_No_Banner_Carousel_if_no_available_Banners(Common):
    """
    TR_ID: C2635874
    NAME: No Banner Carousel if no available Banners
    DESCRIPTION: This test case verifies absence of Banner carousel in case there are no available Banners
    PRECONDITIONS: No Banners
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: 
        """
        pass

    def test_002_verify_banners_carousel(self):
        """
        DESCRIPTION: Verify Banners Carousel
        EXPECTED: * Banners Carousel is not displayed on the Homepage or Sport Landing pages
        EXPECTED: * There is no empty space, the rest of the content is displayed correctly
        """
        pass
