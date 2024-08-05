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
class Test_C34288572_Verify_Kits_undisplaying(Common):
    """
    TR_ID: C34288572
    NAME: Verify Kits undisplaying
    DESCRIPTION: This test case verifies kits undisplaying WHEN one of the team being displayed in the highlights carousel card doesn't have kits mapped
    DESCRIPTION: Ladbrokes design: https://zpl.io/ad1NwYl
    DESCRIPTION: Coral design: https://zpl.io/V1pyeOX
    PRECONDITIONS: 1. app is installed and launched;
    PRECONDITIONS: 2. user is navigated to home page;
    PRECONDITIONS: 2. Highlights carousel is configured in CMS
    PRECONDITIONS: 3. One of the team being displayed in the highlights carousel card doesn't have kits
    PRECONDITIONS: Note:
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS:
    PRECONDITIONS: * Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have active Highlights Carousels with active events in CMS. Make sure that Highlights Carousel configured by TypeID/EventID
    """
    keep_browser_open = True

    def test_001_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_one_of_team_has_no_mapped_team_kit(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if one of team has NO mapped team kit
        EXPECTED: Both team kits are NOT displayed on Highlights Carousel configured
        """
        pass

    def test_002_verify_team_kits_displaying_on_events_cards_in_highlights_carousels_if_both_of_team_names_have_no_mapped_team_kit(self):
        """
        DESCRIPTION: Verify team kits displaying on events cards in Highlights Carousels if both of team names have NO mapped team kit
        EXPECTED: Both team kits are NOT displayed on Highlights Carousel configured
        """
        pass
