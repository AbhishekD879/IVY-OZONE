import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C9229255_In_play_module_layout_on_Featured_tab_at_the_Homepage(Common):
    """
    TR_ID: C9229255
    NAME: 'In-play' module layout on 'Featured' tab at the Homepage
    DESCRIPTION: This test case verifies 'In-play' module layout on 'Featured' tab at the Homepage
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The homepage is opened and 'Featured' tab is selected
    PRECONDITIONS: 3. 'In-Play' module with live events is displayed in 'Featured' tab
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - 'In-Play' module should be enabled in CMS > Sports Configs > Structure > In-Play module
    PRECONDITIONS: - 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
    PRECONDITIONS: - At least 2 Sports with Live event are added in CMS > Sports Pages > Homepage > In-Play module > Add Sport > Set number of events for Sport
    PRECONDITIONS: - To check data received in featured-sports MS open Dev Tools > Network > WS > featured-sports
    """
    keep_browser_open = True

    def test_001_verify_in_play_module_layout(self):
        """
        DESCRIPTION: Verify 'In-Play' module layout
        EXPECTED: 'In-Play' module consists of:
        EXPECTED: * In-Play header
        EXPECTED: * Sports container
        EXPECTED: * Event cards
        """
        pass

    def test_002_verify_in_play_module_header(self):
        """
        DESCRIPTION: Verify 'In-Play' module header
        EXPECTED: 'In-Play' module header contains:
        EXPECTED: * 'In-Play' text
        EXPECTED: * 'See all (XX)>' link
        """
        pass

    def test_003_verify_sports_container(self):
        """
        DESCRIPTION: Verify Sports container
        EXPECTED: * Sports are grouped by SportID
        EXPECTED: * Events are grouped by TypeID
        EXPECTED: * SportName is displayed on Odds Card Header and corresponds to 'categoryName' attribute
        EXPECTED: * Home/Draw/Away or 1/2 (depending on 3 or 2 way primary market) displayed on Odds Card Header
        """
        pass

    def test_004_verify_event_card_elements(self):
        """
        DESCRIPTION: Verify event card elements
        EXPECTED: * Team names/players names
        EXPECTED: * Live/Watch live icons (if available)
        EXPECTED: * Scores (if available)
        EXPECTED: * Match time (if available)
        EXPECTED: * Fav icon (Football only)(Coral only)
        EXPECTED: * Price/odds buttons
        EXPECTED: * 'XX more' link (above Price/odds buttons for Ladbrokes) (below Price/odds buttons for Coral)
        """
        pass
