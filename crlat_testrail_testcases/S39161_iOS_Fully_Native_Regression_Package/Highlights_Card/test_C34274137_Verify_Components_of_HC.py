import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.native
@vtest
class Test_C34274137_Verify_Components_of_HC(Common):
    """
    TR_ID: C34274137
    NAME: Verify Components of HC
    DESCRIPTION: This test case verifies displaying of HC WHEN  user is in Featured tab AND the Highlights carousel is configured in CMS
    DESCRIPTION: Ladbrokes design: https://zpl.io/ad1NwYl
    DESCRIPTION: Coral design: https://zpl.io/V1pyeOX
    PRECONDITIONS: 1. Build is installed;
    PRECONDITIONS: 2. Highlights carousel is configured in CMS
    PRECONDITIONS: Note:
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS:
    PRECONDITIONS: * Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have active Highlights Carousels with active events in CMS. Make sure that Highlights Carousel configured by TypeID/EventID
    """
    keep_browser_open = True

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        EXPECTED: App is launched
        EXPECTED: Featured tab is opened
        EXPECTED: Highlights carousel is displayed
        """
        pass

    def test_002_verify_components_of_hc(self):
        """
        DESCRIPTION: Verify components of HC
        EXPECTED: HC is displayed as per design:
        EXPECTED: - Title of the Highlights carousel
        EXPECTED: - View League link navigating to the competition type page
        EXPECTED: - Team names/Player names
        EXPECTED: - Watch(Pre-Play)/ Watch Live (InPlay)/Live(no stream available) Icon
        EXPECTED: - Scorecard of the game if InPlay with time elapsed
        EXPECTED: - Time and date if Pre Play
        EXPECTED: - 1X2 or 1 2 match result (Primary market) betting odds and the text above the odds button - only WW or WDW markets
        EXPECTED: - Team kits/Shields as uploaded in the CMS
        EXPECTED: Ladbrokes:
        EXPECTED: ![](index.php?/attachments/get/11473522)
        EXPECTED: Coral:
        EXPECTED: ![](index.php?/attachments/get/11473523)
        """
        pass
