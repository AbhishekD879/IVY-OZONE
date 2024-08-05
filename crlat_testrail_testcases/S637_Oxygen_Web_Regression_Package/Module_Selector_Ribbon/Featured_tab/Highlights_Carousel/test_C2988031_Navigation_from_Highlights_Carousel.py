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
class Test_C2988031_Navigation_from_Highlights_Carousel(Common):
    """
    TR_ID: C2988031
    NAME: Navigation from Highlights Carousel
    DESCRIPTION: This test case verifies navigation from Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel: 1) 1st Highlights Carousel configured by EventIDs; 2) 2nd Highlights Carousel configured by TypeID
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_tap_any_events_card_from_both_highlights_carousels_and_verify_navigation(self):
        """
        DESCRIPTION: Tap any events' card from both Highlights Carousels and verify navigation
        EXPECTED: User is navigated to event details page of the respective event
        """
        pass

    def test_002___go_back_to_home_page__tap_see_all_link_on_highlights_carousel_configured_by_typeid(self):
        """
        DESCRIPTION: - Go back to home page
        DESCRIPTION: - Tap "See All" link on Highlights Carousel configured by TypeID
        EXPECTED: - User is navigated to Competitions page of the Type that the Highlights Carousel is configured and can see all events from that type
        EXPECTED: - If sport or type doesn't have corresponding Competitions page then empty Competitions page is shown with a message "No events found"
        """
        pass
