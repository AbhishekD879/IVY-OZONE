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
class Test_C2987419_Highlights_Carousel__displaying_in_play_events_cards_based_on_Display_In_Play_option(Common):
    """
    TR_ID: C2987419
    NAME: Highlights Carousel - displaying in-play events cards based on "Display In-Play" option
    DESCRIPTION: This test case verifies displaying of cards of in-play events based on "Display In-Play" option
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - "Display in-Play" option in Highlights Carousel above should be unchecked
    PRECONDITIONS: - Some of the events in Highlights Carousel above should be configured as in-play events (some already started and some not) and some prematch events
    PRECONDITIONS: - You should be on a home page in application
    PRECONDITIONS: NOTE: event is considered as in-play if: 1) It has market with enabled "Bet In Running" option; 2) It has "Bet In Play List" check box checked; 3) It has started or it has "Is Off" option set to "Yes".
    """
    keep_browser_open = True

    def test_001_verify_cards_displayed_in_highlights_carousel(self):
        """
        DESCRIPTION: Verify cards displayed in Highlights Carousel
        EXPECTED: Highlights Carousel contains only cards of not in-play events
        """
        pass

    def test_002___in_cms__sport_pages_homepage__highlights_carousel_enable_display_in_play_option_for_the_highlights_carousel_from_preconditions__in_application_refresh_the_page_and_verify_cards_displayed_in_highlights_carousel(self):
        """
        DESCRIPTION: - In CMS > Sport Pages> Homepage > Highlights Carousel enable "Display In-Play" option for the Highlights Carousel from preconditions
        DESCRIPTION: - In application refresh the page and verify cards displayed in Highlights Carousel
        EXPECTED: Highlights Carousel contains cards of not in-play and in-play events
        """
        pass
