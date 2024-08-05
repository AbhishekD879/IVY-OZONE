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
class Test_C9726411_Event_hub_Highlights_Carousel_displaying_based_on_date_and_time(Common):
    """
    TR_ID: C9726411
    NAME: Event hub: Highlights Carousel displaying based on date and time
    DESCRIPTION: This test case verifies Highlights Carousels displaying based on configured display date and time
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Event Hub > Highlights Carousel
    PRECONDITIONS: - You should have 3 active Highlights Carousels with active events in CMS > Sport Pages > Event Hub > Highlights Carousel:
    PRECONDITIONS: - - 1) 1st Highlights Carousel should be configured in past;
    PRECONDITIONS: - - 2) 2nd Highlights Carousel should be configured in future;
    PRECONDITIONS: - - 3) 3rd Highlights Carousel should be configured to include current date and time.
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: Verify Highlights Carousel displaying
        EXPECTED: Only Highlights Carousel that includes current date and time is displayed
        """
        pass

    def test_002___in_cms__sport_pages__event_hub__highlights_carousel_edit_currently_displayed_highlights_carousel_to_be_undisplayed_in_couple_minutes__in_cms__sport_pages__event_hub__highlights_carousel_edit_future_highlights_carousel_to_be_displayed_in_couple_minutes__wait_for_the_configured_time_and_refresh_the_page_in_application__verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: - In CMS > Sport Pages > Event hub > Highlights Carousel edit currently displayed Highlights Carousel to be undisplayed in couple minutes
        DESCRIPTION: - In CMS > Sport Pages > Event hub > Highlights Carousel edit future Highlights Carousel to be displayed in couple minutes
        DESCRIPTION: - Wait for the configured time and refresh the page in application
        DESCRIPTION: - Verify Highlights Carousel displaying
        EXPECTED: Only Highlights Carousel that includes current date and time is displayed
        """
        pass
