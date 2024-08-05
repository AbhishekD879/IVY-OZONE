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
class Test_C2988030_Highlights_Carousel__icon_and_title_displaying(Common):
    """
    TR_ID: C2988030
    NAME: Highlights Carousel - icon and title displaying
    DESCRIPTION: This test case verifies displaying of icon and title on Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousel with active events in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - Highlights Carousel should have icon attached (only SVG file type is supported)
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_icon_and_title_displaying_on_highlights_carousel(self):
        """
        DESCRIPTION: Verify icon and title displaying on Highlights Carousel
        EXPECTED: - Attached image is displayed to the left from the Highlights Carousel's title
        EXPECTED: - Highlights Carousel's title is the same as in CMS
        """
        pass

    def test_002___in_cms_remove_the_icon_from_highlights_carousel__in_cms_change_the_title_of_the_highlights_carousel__in_application_refresh_the_page_and_verify_icon_and_title_displaying_on_highlights_carousel(self):
        """
        DESCRIPTION: - In CMS remove the icon from Highlights Carousel
        DESCRIPTION: - In CMS change the title of the Highlights Carousel
        DESCRIPTION: - In application refresh the page and verify icon and title displaying on Highlights Carousel
        EXPECTED: - There is no image next to the Highlights Carousel's title
        EXPECTED: - Highlights Carousel's title is the same as in CMS
        """
        pass
