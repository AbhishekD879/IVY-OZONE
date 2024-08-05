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
class Test_C34288571_Verify_Kits_displaying(Common):
    """
    TR_ID: C34288571
    NAME: Verify Kits displaying
    DESCRIPTION: This test case verifies that kits are displayed WHEN the kits are available for both the teams displayed in the highlights carousel card
    DESCRIPTION: Ladbrokes design: https://zpl.io/ad1NwYl
    DESCRIPTION: Coral design: https://zpl.io/V1pyeOX
    PRECONDITIONS: 1. app is installed and launched;
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

    def test_001_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_team_name_has_mapped_team_kit(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if team name has mapped team kit
        EXPECTED: Team kits are displayed correctly according to mapped teams in Highlights Carousel configured
        """
        pass
