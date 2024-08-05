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
class Test_C2987423_Highlights_Carousel__displaying_different_sports_cards_in_the_same_highlights_carousel(Common):
    """
    TR_ID: C2987423
    NAME: Highlights Carousel - displaying different sports cards in the same highlights carousel
    DESCRIPTION: This test case verifies displaying cards of events from different sports in one Highlights Carousel simultaneously
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - Event IDs added to  Highlights Carousel should be from different sports (e.g. Football, Tennis, Basketball)
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: Verify cards displaying in Highlights Carousel
        EXPECTED: - All cards of active events are displayed in Highlights Carousel
        EXPECTED: - Cards from different sports have the same size
        """
        pass
