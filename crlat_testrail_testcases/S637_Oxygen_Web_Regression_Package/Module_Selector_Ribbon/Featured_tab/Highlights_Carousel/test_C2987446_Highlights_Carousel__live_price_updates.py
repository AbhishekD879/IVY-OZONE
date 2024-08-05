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
class Test_C2987446_Highlights_Carousel__live_price_updates(Common):
    """
    TR_ID: C2987446
    NAME: Highlights Carousel - live price updates
    DESCRIPTION: This test case verify live price changes in Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001___in_ti_tool_increase_the_price_for_one_of_the_selections_of_event_displayed_in_highlights_carousel__verify_live_updates_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool increase the price for one of the selections of event displayed in Highlights carousel
        DESCRIPTION: - Verify live updates in Highlights Carousel
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to red for a few seconds
        """
        pass

    def test_002___in_ti_tool_decrease_the_price_for_one_of_the_selections_of_event_displayed_in_highlights_carousel__verify_live_updates_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool decrease the price for one of the selections of event displayed in Highlights carousel
        DESCRIPTION: - Verify live updates in Highlights Carousel
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to blue for a few seconds
        """
        pass
