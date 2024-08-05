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
class Test_C9726409_Event_hub_Highlights_Carousel_displaying_based_on_active_option_for_a_whole_module(Common):
    """
    TR_ID: C9726409
    NAME: Event hub: Highlights Carousel displaying based on "active" option for a whole module
    DESCRIPTION: This test case verifies that active Highlights Carousels are not displayed if "Highlights Carousel" module is deactivated
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Event Hub > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Event Hub > Highlights Carousel
    PRECONDITIONS: - You should be on a home page > Event Hub tab in application
    """
    keep_browser_open = True

    def test_001_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Verify Highlights Carousel displaying
        EXPECTED: 2 Highlights Carousels are displayed
        """
        pass

    def test_002___in_cms__sport_pages__event_hub__highlights_carousel___deactivate_the_highlights_carousel_module__in_application_refresh_the_page_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Event Hub > Highlights Carousel - deactivate the "Highlights carousel" module
        DESCRIPTION: - In application refresh the page and verify Highlights Carousel displaying
        EXPECTED: Highlights Carousels are not displayed
        """
        pass

    def test_003___in_cms__sport_pages__event_hub__highlights_carousel___activate_the_highlights_carousel_module__in_application_refresh_the_page_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Event hub > Highlights Carousel - activate the "Highlights carousel" module
        DESCRIPTION: - In application refresh the page and verify Highlights Carousel displaying
        EXPECTED: 2 Highlights Carousels are displayed
        """
        pass
