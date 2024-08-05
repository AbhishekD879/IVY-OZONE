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
class Test_C2988648_Highlights_Carousel__one_card_displaying(Common):
    """
    TR_ID: C2988648
    NAME: Highlights Carousel - one card displaying
    DESCRIPTION: This test case verifies displaying of a single card in Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with 1 active event in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_a_single_card_in_highlights_carousel(self):
        """
        DESCRIPTION: Verify displaying of a single card in Highlights Carousel
        EXPECTED: Single card is normally sized and centered
        """
        pass

    def test_002___in_cms__sport_pages__homepage__highlights_carousel_add_one_more_active_event_to_your_highlights_carousel__in_application_refresh_the_page_and_verify_cards_displaying(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Homepage > Highlights Carousel add one more active event to your Highlights Carousel
        DESCRIPTION: - In application refresh the page and verify cards displaying
        EXPECTED: Cards have normal sizing and they are left aligned
        """
        pass

    def test_003___in_ti_tool_undisplay_or_result_one_of_the_displayed_events__in_application_verify_cards_displaying_without_page_refresh(self):
        """
        DESCRIPTION: - In TI tool undisplay or result one of the displayed events
        DESCRIPTION: - In application verify cards displaying without page refresh
        EXPECTED: Resulted or undisplayed event's card is removed in live and single card is normally sized and centered
        """
        pass
