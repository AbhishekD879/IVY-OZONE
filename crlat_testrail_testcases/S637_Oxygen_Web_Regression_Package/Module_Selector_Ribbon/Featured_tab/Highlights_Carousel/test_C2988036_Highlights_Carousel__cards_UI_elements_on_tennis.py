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
class Test_C2988036_Highlights_Carousel__cards_UI_elements_on_tennis(Common):
    """
    TR_ID: C2988036
    NAME: Highlights Carousel - cards UI elements on tennis
    DESCRIPTION: This test case verifies UI cards elements displaying for tennis
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Highlights Carousel" module should be "Active" in CMS > Sport Pages > Homepage > Highlights Carousel
    PRECONDITIONS: - You should have an active Highlights Carousels with active events in CMS > Sport Pages > Sport Categories > Tennis
    PRECONDITIONS: - "Display In-Play" option should be enabled in Highlights Carousel
    PRECONDITIONS: - You should have next events configured and added to Highlights Carousel: 1) prematch event without stream mapped; 2) prematch event with stream mapped; 3) live event without stream mapped; 4) live event with stream mapped; 5) live 2x2 event without mapped stream
    PRECONDITIONS: - All events should have active market from |Match Betting| market template with selections
    PRECONDITIONS: - You should be on a Tennis landing page > Matches tab
    """
    keep_browser_open = True

    def test_001_verify_cards_elements_in_highlights_carousel(self):
        """
        DESCRIPTION: Verify cards elements in Highlights Carousel
        EXPECTED: Prematch event without stream mapped:
        EXPECTED: - Event's start date and time at the top left corner
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 players under start date
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles 12
        EXPECTED: Prematch event with stream mapped:
        EXPECTED: - "Watch" label at the top left corner
        EXPECTED: - Event's start date and time at the top left corner
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 players under start date
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles 12
        EXPECTED: Live event without stream mapped:
        EXPECTED: - "Live" label at the top left corner
        EXPECTED: - Current set
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 players under "Live" label
        EXPECTED: - Green ball next to the attacking team
        EXPECTED: - 3 columns S, G, P with proper scores against players
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles 12
        EXPECTED: Live event with stream mapped:
        EXPECTED: - "Watch Live" label at the top left corner
        EXPECTED: - Current set
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 2 teams/players under "Watch Live" label
        EXPECTED: - Green ball next to the attacking team
        EXPECTED: - 3 columns S, G, P with proper scores against players
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles 12
        EXPECTED: Live 2x2 event without mapped stream
        EXPECTED: - "Live" label at the top left corner
        EXPECTED: - Current set
        EXPECTED: - ">" arrow at the top right corner (Ladbrokes only)
        EXPECTED: - 4 players in format "Player1/Player2 vs Player3/Player4" under "Live" label
        EXPECTED: - 3 columns S, G, P with proper scores against players
        EXPECTED: - Price buttons under the teams/players names with correct prices and titles 12
        """
        pass
