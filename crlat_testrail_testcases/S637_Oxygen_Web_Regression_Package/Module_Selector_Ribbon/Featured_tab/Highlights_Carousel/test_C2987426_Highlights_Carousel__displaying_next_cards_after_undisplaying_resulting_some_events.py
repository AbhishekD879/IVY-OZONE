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
class Test_C2987426_Highlights_Carousel__displaying_next_cards_after_undisplaying_resulting_some_events(Common):
    """
    TR_ID: C2987426
    NAME: Highlights Carousel - displaying next cards after undisplaying/resulting some events
    DESCRIPTION: This test case verifies that Highlights Carousel with provided limitation of displayed events shows next events after some of the already displayed events have been undisplayed/resulted and there are more to show
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - "No. of Events" should be set in Highlights Carousel and it should be less then the amount of events provided in Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001___in_ti_tool_undisplay_and_result_some_events_that_are_already_displayed_in_highlights_carousel__in_application_refresh_the_page_and_verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool undisplay and result some events that are already displayed in Highlights Carousel
        DESCRIPTION: - In application refresh the page and verify cards displaying in Highlights Carousel
        EXPECTED: - Cards of events that were undisplayed/resulted are not shown and next active events according to order are displayed instead of them
        EXPECTED: - Limitation is kept and amount of cards doesn't exceed it
        """
        pass
