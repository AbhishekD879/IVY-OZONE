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
class Test_C59516839_Highlight_Carousel__Verify_that_more_than_two_Highlight_Carousels_are_configured_on_CMS_and_displayed_on_Homepage(Common):
    """
    TR_ID: C59516839
    NAME: Highlight Carousel - Verify that more than two Highlight Carousels are configured on CMS and displayed on Homepage
    DESCRIPTION: Test case verifies that more than two Highlight Carousels are configured on CMS and displayed on Homepage
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel: 1) 1st Highlights Carousel should be configured by TypeID; 2) 2nd Highlight Carousel is configured by EventIDs.
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_highlights_carousels_displaying_on_homepage(self):
        """
        DESCRIPTION: Verify Highlights Carousels displaying on Homepage
        EXPECTED: 2 Highlights Carousels are displayed
        """
        pass

    def test_002_in_cms__sport_pages__homepage__highlights_carousel_configure_one_more_highlights_carousel_by_typeid(self):
        """
        DESCRIPTION: In CMS > Sport Pages > Homepage > Highlights Carousel configure one more Highlights Carousel by TypeID
        EXPECTED: New created Highlights Carousel is saved in CMS without any error messages
        """
        pass

    def test_003_verify_highlights_carousel_displaying_on_homepage(self):
        """
        DESCRIPTION: Verify Highlights Carousel displaying on Homepage
        EXPECTED: 3 Highlights Carousels are displayed
        """
        pass

    def test_004_in_cms__sport_pages__homepage__highlights_carousel_configure_one_more_highlights_carousel_by_eventid(self):
        """
        DESCRIPTION: In CMS > Sport Pages > Homepage > Highlights Carousel configure one more Highlights Carousel by EventID
        EXPECTED: New created Highlights Carousel is saved in CMS without any error messages
        """
        pass

    def test_005_verify_highlights_carousel_displaying_on_homepage(self):
        """
        DESCRIPTION: Verify Highlights Carousel displaying on Homepage
        EXPECTED: 4 Highlights Carousels are displayed
        """
        pass
