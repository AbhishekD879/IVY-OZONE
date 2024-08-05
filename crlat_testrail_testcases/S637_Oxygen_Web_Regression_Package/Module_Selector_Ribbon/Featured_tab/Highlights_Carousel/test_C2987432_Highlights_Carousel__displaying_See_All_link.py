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
class Test_C2987432_Highlights_Carousel__displaying_See_All_link(Common):
    """
    TR_ID: C2987432
    NAME: Highlights Carousel - displaying "See All" link
    DESCRIPTION: This test case verifies displaying of "See All" link on Highlights Carousel
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have 2 active Highlights Carousels with active events in CMS > Sport Pages > Homepage > Highlights Carousel: 1) 1st Highlights Carousel configured by EventIDs; 2) 2nd Highlights Carousel configured by TypeID
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001_verify_see_all_link_displaying_on_highlights_carousel(self):
        """
        DESCRIPTION: Verify "See All" link displaying on Highlights Carousel
        EXPECTED: - Highlights Carousel configured by TypeID has "See All" link displayed at the top right corner
        EXPECTED: - Highlights Carousel configured by EventIDs doesn't have "See All" link displayed
        """
        pass
