import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2696854_TEMP_Verify_Coupon_configuring_for_non_popular_markets(Common):
    """
    TR_ID: C2696854
    NAME: [TEMP] Verify Coupon configuring for non-popular markets
    DESCRIPTION: 
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: * CMS environments: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: * TI environments: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: * How to create a coupon: https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: * Create the coupons for the upcoming event with the following markets:
    PRECONDITIONS: * COUPON1: 'To Win to Nil' - default market
    PRECONDITIONS: * COUPON2: 'Total Goals Over/Under 1.5' - default market
    PRECONDITIONS: * COUPON3: 'Over/Under First Half Home Team Total Goals 0.5'
    PRECONDITIONS: * COUPON4: 'Over/Under First Half Home Team Total Goals 0.5', 'Win Either Half', 'First Team to Score'
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
    PRECONDITIONS: * Configure market selectors via CMS > Football Coupons > Market Selectors, add following selectors:
    PRECONDITIONS: * Template name: 'Total Goals Over/Under 1.5', set a custom title, headers
    PRECONDITIONS: * Template name: 'Over/Under First Half Home Team Total Goals 0.5', set a custom title
    PRECONDITIONS: * Template name: 'Win Either Half', set a custom title, headers
    PRECONDITIONS: * Template name: 'First Team to Score', set a custom title, headers
    PRECONDITIONS: * Define the market selectors order:
    PRECONDITIONS: * 'Win Either Half'
    PRECONDITIONS: * 'Fist Team to Score'
    PRECONDITIONS: * 'Over/Under First Half Home Team Total Goals 0.5'
    PRECONDITIONS: * Add COUPON4 to the active Coupon Segment
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Open Football > Coupons (Accas) page
    """
    keep_browser_open = True

    def test_001_open_coupon1_and_verify_the_default_market_is_opened(self):
        """
        DESCRIPTION: Open COUPON1 and verify the default market is opened.
        EXPECTED: "Match Result" market is displayed by default
        EXPECTED: * Market title is default
        EXPECTED: * Headers titles are default
        """
        pass

    def test_002_tap_on_market_selector_verify_the_list_contains_default_markets_only(self):
        """
        DESCRIPTION: Tap on Market Selector. Verify the list contains default markets only.
        EXPECTED: * Market Selector dropdown is opened
        EXPECTED: * "Match Result" is on the top of the list and marked as selected
        EXPECTED: * The list of markets contains default markets only
        """
        pass

    def test_003_open_coupon2_and_verify_the_default_market_is_opened(self):
        """
        DESCRIPTION: Open COUPON2 and verify the default market is opened.
        EXPECTED: "Total Goals Over/Under 1.5" market is displayed by default
        EXPECTED: * Market title is as set in the CMS
        EXPECTED: * Headers titles are as set in the CMS
        """
        pass

    def test_004_tap_on_market_selector_verify_the_list_contains_default_markets_only(self):
        """
        DESCRIPTION: Tap on Market Selector. Verify the list contains default markets only.
        EXPECTED: * Market Selector dropdown is opened
        EXPECTED: * "Total Goals Over/Under 1.5" (custom name) is on the top of the list and marked as selected
        EXPECTED: * The list of markets contains default markets only
        """
        pass

    def test_005_open_coupon3_and_verify_the_default_market_is_opened(self):
        """
        DESCRIPTION: Open COUPON3 and verify the default market is opened.
        EXPECTED: "Over/Under First Half Home Team Total Goals 0.5" market is displayed by default
        EXPECTED: * Market title is as set in the CMS
        EXPECTED: * Headers titles are default
        """
        pass

    def test_006_tap_on_market_selector_verify_the_list_contains_custom_market_and_default_markets(self):
        """
        DESCRIPTION: Tap on Market Selector. Verify the list contains custom market and default markets.
        EXPECTED: * Market Selector dropdown is opened
        EXPECTED: * "Over/Under First Half Home Team Total Goals 0.5" (custom name) is on the top of the list and marked as selected
        EXPECTED: * Other custom markets are not displayed
        EXPECTED: * All the list of the default markets is below
        """
        pass

    def test_007_open_coupon4_and_verify_the_default_market_is_opened(self):
        """
        DESCRIPTION: Open COUPON4 and verify the default market is opened.
        EXPECTED: "Win Either Half" market is displayed by default
        EXPECTED: * Market title is as set in the CMS
        EXPECTED: * Headers titles are as set in the CMS
        """
        pass

    def test_008_tap_on_market_selector_verify_the_list_contains_custom_market_and_default_markets(self):
        """
        DESCRIPTION: Tap on Market Selector. Verify the list contains custom market and default markets.
        EXPECTED: * Market Selector dropdown is opened
        EXPECTED: * "Win Either Half" (custom name) is on the top of the list and marked as selected
        EXPECTED: * Other custom markets are displayed
        EXPECTED: * All the list of the default markets is below
        """
        pass

    def test_009_verify_the_default_markets_ordering(self):
        """
        DESCRIPTION: Verify the default markets ordering
        EXPECTED: Default market order is predefined:
        EXPECTED: * 'Match Result',
        EXPECTED: * 'Both Teams to Score',
        EXPECTED: * 'Match Result & Both Teams To Score **Ladbrokes added from OX 100.3**
        EXPECTED: * 'Total Goals Over/Under 1.5',
        EXPECTED: * 'Total Goals Over/Under 2.5',
        EXPECTED: * 'Total Goals Over/Under 3.5',
        EXPECTED: * 'To Win and Both Teams to Score',
        EXPECTED: * 'Draw No Bet',
        EXPECTED: * 'First-Half Result',
        EXPECTED: * 'To Win to Nil' **Ladbrokes removed from OX 100.3**
        EXPECTED: * 'Score Goal in Both Halves'
        """
        pass

    def test_010_verify_the_custom_markets_ordering(self):
        """
        DESCRIPTION: Verify the custom markets ordering
        EXPECTED: Custom markets are ordered as per order in the CMS
        """
        pass

    def test_011_change_coupon4_set_display__false_for_default_and_non_default_market_verify_markets_with_display__false_disappear_from_the_market_selectors_list(self):
        """
        DESCRIPTION: Change COUPON4. Set Display = false for default and non-default market. Verify markets with Display = false disappear from the market selectors list.
        EXPECTED: Markets with Display = false are not shown within the list.
        """
        pass

    def test_012_change_coupon4_set_display__true_for_default_and_non_default_market_verify_markets_appear_in_the_selector_after_the_refresh(self):
        """
        DESCRIPTION: Change COUPON4. Set Display = true for default and non-default market. Verify markets appear in the selector after the refresh.
        EXPECTED: Markets appear in the market selector.
        """
        pass
