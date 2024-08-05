import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C2987421_Highlights_Carousel__displaying_cards_of_resulted_events(Common):
    """
    TR_ID: C2987421
    NAME: Highlights Carousel - displaying cards of resulted events
    DESCRIPTION: This test case verifies displaying cards of resulted events
    DESCRIPTION: AUTOTEST [C9332662]
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - How to map video stream to event: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousels with 2 active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - "Display In-Play" option in Highlights Carousel above should be checked
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001___in_ti_tool_result_one_of_the_events_displayed_in_highlights_carousel__verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool result one of the events displayed in Highlights Carousel
        DESCRIPTION: - Verify cards displaying in Highlights Carousel
        EXPECTED: Card of the resulted event is undisplayed in live
        """
        pass

    def test_002___in_ti_tool_result_the_last_event_displayed_in_highlights_carousel__verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool result the last event displayed in Highlights Carousel
        DESCRIPTION: - Verify cards displaying in Highlights Carousel
        EXPECTED: Highlights Carousel is undisplayed in live as it has no more events to display
        """
        pass
