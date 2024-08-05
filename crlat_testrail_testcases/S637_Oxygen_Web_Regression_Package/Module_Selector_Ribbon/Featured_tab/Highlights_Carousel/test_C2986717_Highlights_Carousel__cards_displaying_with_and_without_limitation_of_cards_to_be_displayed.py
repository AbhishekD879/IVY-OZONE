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
class Test_C2986717_Highlights_Carousel__cards_displaying_with_and_without_limitation_of_cards_to_be_displayed(Common):
    """
    TR_ID: C2986717
    NAME: Highlights Carousel - cards' displaying with and without limitation of cards to be displayed
    DESCRIPTION: This test case verifies cards displaying when limitation of cards to be displayed is set and not
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel: 1) 1st Highlights Carousel should be configured by TypeID; 2) 2nd Highlight Carousel is configured by EvenIDs.
    PRECONDITIONS: - Both Highlights Carousels above should be without any limitation of cards to be displayed ("No. of Events" option in CMS)
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_cards_displaying_within_highlights_carousel_configured_by_event_ids(self):
        """
        DESCRIPTION: Verify cards displaying within Highlights Carousel configured by event ids
        EXPECTED: All cards of available events are displayed
        """
        pass

    def test_002___in_cms__sport_pages__homepage__highlights_carousel_set_some_limitation_x_of_events_to_be_displayed_for_highlights_carousel_configured_by_event_ids__verify_cards_displaying_within_highlights_carousels(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage > Highlights Carousel set some limitation "X" of events to be displayed for Highlights Carousel configured by event ids
        DESCRIPTION: - Verify cards displaying within Highlights Carousels
        EXPECTED: Highlights Carousel contain only "X" amount of cards
        """
        pass

    def test_003_repeat_steps_1_2_for_highlighs_carousel_configured_by_type_id(self):
        """
        DESCRIPTION: Repeat steps 1-2 for Highlighs Carousel configured by type ID
        EXPECTED: 
        """
        pass
