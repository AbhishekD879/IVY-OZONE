import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726404_Event_Hub_Highlights_Carousel__cards_displaying_based_on_undisplay_option_on_selection_market_event_levels(Common):
    """
    TR_ID: C9726404
    NAME: Event Hub: Highlights Carousel - cards' displaying based on "undisplay" option on selection/market/event levels
    DESCRIPTION: This test case verifies displaying of cards based on "undisplay" option on selection/market/event levels
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Event Hub > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Event Hub > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001___in_ti_tool_disable_display_option_for_one_of_the_selection_of_one_of_the_events_cards_displayed_in_highlights_carousel__verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool disable "display" option for one of the selection of one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Respective selection is undisplayed in live
        """
        pass

    def test_002___in_ti_tool_enable_display_option_for_the_selection_from_step_1__refresh_the_page_and_verify_selections_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool enable "display" option for the selection from step 1
        DESCRIPTION: - Refresh the page and verify selection's displaying in Highlights Carousel
        EXPECTED: Selection is displayed again
        """
        pass

    def test_003___in_ti_tool_disable_display_option_for_primary_market_of_one_of_the_events_cards_displayed_in_highlights_carousel__verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool disable "display" option for primary market of one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Respective card is undisplayed in live
        """
        pass

    def test_004___in_ti_tool_enable_display_option_for_primary_market_from_step_3__refresh_the_page_and_verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool enable "display" option for primary market from step 3
        DESCRIPTION: - Refresh the page and verify card's displaying in Highlights Carousel
        EXPECTED: Card is displayed
        """
        pass

    def test_005___in_ti_tool_disable_display_option_for_one_of_the_events_cards_displayed_in_highlights_carousel__verify_live_update_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool disable "display" option for one of the events' cards displayed in Highlights Carousel
        DESCRIPTION: - Verify live update in Highlights Carousel
        EXPECTED: Respective card is undisplayed in live
        """
        pass

    def test_006___in_ti_tool_enable_display_option_for_event_from_step_5__refresh_the_page_and_verify_cards_displaying_in_highlights_carousel(self):
        """
        DESCRIPTION: - In TI tool enable "display" option for event from step 5
        DESCRIPTION: - Refresh the page and verify card's displaying in Highlights Carousel
        EXPECTED: Card is displayed
        """
        pass
