import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C2987500_Highlights_Carousel_module_ordering(Common):
    """
    TR_ID: C2987500
    NAME: Highlights Carousel module ordering
    DESCRIPTION: This test case verifies ordering of Highlights Carousel module
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have configured and enabled any another module in CMS > Sport Pages > Homepage
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_highlights_carousel_module_displaying_order(self):
        """
        DESCRIPTION: Verify Highlights Carousel module displaying order
        EXPECTED: Highlights Carousel module is displayed according to order in CMS > Sport Pages > Homepage
        """
        pass

    def test_002___in_cms_sport_pages__homepage_change_the_order_of_highlights_carousel_module__refresh_the_page_in_application_and_verify_highlights_carousel_module_displaying_order(self):
        """
        DESCRIPTION: - In CMS >Sport Pages > Homepage change the order of "Highlights Carousel" module
        DESCRIPTION: - Refresh the page in application and verify "Highlights Carousel" module displaying order
        EXPECTED: Highlights Carousel module is displayed according to order in CMS > Sport Pages > Homepage
        """
        pass
