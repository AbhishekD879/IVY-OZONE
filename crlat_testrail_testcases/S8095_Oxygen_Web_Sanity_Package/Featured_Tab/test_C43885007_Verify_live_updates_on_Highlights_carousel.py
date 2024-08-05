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
class Test_C43885007_Verify_live_updates_on_Highlights_carousel(Common):
    """
    TR_ID: C43885007
    NAME: Verify live updates on 'Highlights' carousel
    DESCRIPTION: This test case verifies live updates on 'Highlights' carousel
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage -> 'Featured' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) 'Highlights' carousel module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: 2) You should have 2 active 'Highlights' carousels with active events in CMS > Sports Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - 1st Highlights Carousel should be configured by TypeID
    PRECONDITIONS: - 2nd Highlight Carousel is configured by EvenIDs
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 2) To verify data for created Highlights Carousel use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "HighlightCarouselModule" and choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/32857095)
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
