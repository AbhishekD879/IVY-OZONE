import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C2988649_Verify_ordering_of_custom_and_default_hardcoded_markets_within_the_market_selector(Common):
    """
    TR_ID: C2988649
    NAME: Verify ordering of custom and default (hardcoded) markets within the market selector
    DESCRIPTION: 
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: * CMS environments: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: * TI environments: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: * How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: * Create a coupon and add following markets: 'Over/Under First Half Home Team Total Goals 0.5', 'Win Either Half', 'First Team to Score'
    PRECONDITIONS: * Activate, make displayed and add prices for the following markets:
    PRECONDITIONS: <default markets>
    PRECONDITIONS: * 'Match Result',
    PRECONDITIONS: * 'Both Teams to Score',
    PRECONDITIONS: * 'Match Result & Both Teams To Score
    PRECONDITIONS: * 'Total Goals Over/Under 1.5',
    PRECONDITIONS: * 'Total Goals Over/Under 2.5',
    PRECONDITIONS: * 'Total Goals Over/Under 3.5',
    PRECONDITIONS: * 'To Win and Both Teams to Score',
    PRECONDITIONS: * 'Draw No Bet',
    PRECONDITIONS: * 'First-Half Result',
    PRECONDITIONS: * 'Score Goal in Both Halves'
    PRECONDITIONS: <custom markets>
    PRECONDITIONS: * 'Over/Under First Half Home Team Total Goals 0.5'
    PRECONDITIONS: * 'Win Either Half'
    PRECONDITIONS: * 'First Team to Score'
    PRECONDITIONS: * Add market selectors for the markets 'Over/Under First Half Home Team Total Goals 0.5', 'Win Either Half', 'First Team to Score'
    PRECONDITIONS: * Define the market selectors order:
    PRECONDITIONS: * 'Win Either Half'
    PRECONDITIONS: * 'Fist Team to Score'
    PRECONDITIONS: * 'Over/Under First Half Home Team Total Goals 0.5'
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Open Football > Coupons (Accas) page > Created coupon
    """
    keep_browser_open = True

    def test_001_clicktap_on_market_selector_verify_the_list_contains_custom_markets_and_default_markets(self):
        """
        DESCRIPTION: Click/Tap on Market Selector. Verify the list contains custom markets and default markets.
        EXPECTED: The market selector contains custom and default markets.
        EXPECTED: Custom markets are located in the top of the list and default markets are located in the bottom of the list.
        """
        pass

    def test_002_verify_custom_markets_ordering(self):
        """
        DESCRIPTION: Verify custom markets ordering
        EXPECTED: Custom markets are ordered as per ordering in the CMS:
        EXPECTED: * 'Win Either Half'
        EXPECTED: * 'Fist Team to Score'
        EXPECTED: * 'Over/Under First Half Home Team Total Goals 0.5'
        """
        pass

    def test_003_verify_default_markets_ordering(self):
        """
        DESCRIPTION: Verify default markets ordering
        EXPECTED: Default market order is predefined:
        EXPECTED: * 'Match Result',
        EXPECTED: * 'Both Teams to Score',
        EXPECTED: * 'Match Result & Both Teams To Score
        EXPECTED: * 'Total Goals Over/Under 1.5',
        EXPECTED: * 'Total Goals Over/Under 2.5',
        EXPECTED: * 'Total Goals Over/Under 3.5',
        EXPECTED: * 'To Win and Both Teams to Score',
        EXPECTED: * 'Draw No Bet',
        EXPECTED: * 'First-Half Result',
        EXPECTED: * 'Score Goal in Both Halves'
        """
        pass
