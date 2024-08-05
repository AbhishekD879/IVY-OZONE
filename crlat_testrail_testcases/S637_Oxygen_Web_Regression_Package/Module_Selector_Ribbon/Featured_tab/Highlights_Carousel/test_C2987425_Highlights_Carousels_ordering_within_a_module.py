import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.homepage_featured
@vtest
class Test_C2987425_Highlights_Carousels_ordering_within_a_module(Common):
    """
    TR_ID: C2987425
    NAME: Highlights Carousels ordering within a module
    DESCRIPTION: This test case verified ordering of Highlights Carousels
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_highlights_carousels_order(self):
        """
        DESCRIPTION: Verify Highlights Carousels order
        EXPECTED: Ordering is the same as in CMS > Sport Pages > Homepage > Highlights Carousel
        """
        pass

    def test_002___in_cms__sport_pages__homepage__highlights_carousel_change_the_order_of_displayed_highlights_carousels__verify_highlights_carousels_order(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage > Highlights Carousel change the order of displayed Highlights Carousels
        DESCRIPTION: - Verify Highlights Carousels order
        EXPECTED: Ordering is the same as in CMS > Sport Pages > Homepage > Highlights Carousel
        """
        pass
