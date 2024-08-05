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
class Test_C2987424_Highlights_Carousel__events_cards_ordering(Common):
    """
    TR_ID: C2987424
    NAME: Highlights Carousel - events cards ordering
    DESCRIPTION: This test case verifies order of cards displayed in Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_cards_order_in_highlights_carousel(self):
        """
        DESCRIPTION: Verify cards order in Highlights Carousel
        EXPECTED: Cards are order by Start Time, then by Display Order in TI tool and then in alphabetical order
        """
        pass
