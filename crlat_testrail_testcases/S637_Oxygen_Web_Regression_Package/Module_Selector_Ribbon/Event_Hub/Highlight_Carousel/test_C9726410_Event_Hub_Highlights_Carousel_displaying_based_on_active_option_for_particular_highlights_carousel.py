import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726410_Event_Hub_Highlights_Carousel_displaying_based_on_active_option_for_particular_highlights_carousel(Common):
    """
    TR_ID: C9726410
    NAME: Event Hub: Highlights Carousel displaying based on "active" option for particular highlights carousel
    DESCRIPTION: This test case verifies Highlights Carousel displaying based on "Active" option for particular Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Event Hub > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Event Hub > Highlights Carousel
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_highlights_carousels_displaying(self):
        """
        DESCRIPTION: Verify Highlights Carousels displaying
        EXPECTED: 2 Highlights Carousels are displayed
        """
        pass

    def test_002___in_cms_gt_sport_pages_gt_event_hub_gt_highlights_carousel_deactivate_one_of_the_displayed_highlights_carousels__in_application_refresh_the_page_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: - In CMS &gt; Sport Pages &gt; Event hub &gt; Highlights Carousel deactivate one of the displayed Highlights Carousels
        DESCRIPTION: - In Application refresh the page and verify Highlights Carousel displaying
        EXPECTED: Only 1 active Highlights Carousel is displayed and deactivated Highlights Carousel is not displayed
        """
        pass

    def test_003___in_cms_gt_sport_pages_gt_event_hub_gt_highlights_carousel_deactivate_another_highlights_carousels_that_is_still_displayed__in_application_refresh_the_page_and_verify_highlights_carousel_displaying(self):
        """
        DESCRIPTION: - In CMS &gt; Sport Pages &gt; Event hub &gt; Highlights Carousel deactivate another Highlights Carousels that is still displayed
        DESCRIPTION: - In Application refresh the page and verify Highlights Carousel displaying
        EXPECTED: None Highlights Carousels are displayed
        """
        pass
