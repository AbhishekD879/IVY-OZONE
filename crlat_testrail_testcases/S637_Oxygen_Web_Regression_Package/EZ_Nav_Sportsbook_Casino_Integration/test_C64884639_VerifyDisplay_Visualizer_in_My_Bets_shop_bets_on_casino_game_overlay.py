import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64884639_VerifyDisplay_Visualizer_in_My_Bets_shop_bets_on_casino_game_overlay(Common):
    """
    TR_ID: C64884639
    NAME: VerifyDisplay Visualizer in My Bets->shop bets on casino game overlay.
    DESCRIPTION: VerifyDisplay Visualizer in My Bets-&gt;shop bets on casino game overlay.
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * Log in with account that has  in-shop inplay bets placed via his/her Connect Card number
    PRECONDITIONS: Note: Applicable to only mobile web
    """
    keep_browser_open = True

    def test_001_launch_any_casino_game(self):
        """
        DESCRIPTION: Launch any casino game
        EXPECTED: * User redirects to particular gaming page ex: Roulette page
        EXPECTED: * User able to see 'sports' icon on EZNav panel(header) in gaming page
        """
        pass

    def test_002_tap_sports_icon_from_eznav_panel(self):
        """
        DESCRIPTION: Tap 'sports' icon from ezNav panel
        EXPECTED: * User navigates to 'MyBets' overlay & displays below tabs:
        EXPECTED: Cashout
        EXPECTED: Openbets
        EXPECTED: Settledbets
        EXPECTED: Shop Bets
        """
        pass

    def test_003_ladbrokes_tap_openbets__gt_inshop_tabcoral_tap_shop_bets__gt_openbets_tab(self):
        """
        DESCRIPTION: Ladbrokes: Tap 'Openbets' -&gt; Inshop tab
        DESCRIPTION: Coral: Tap 'Shop Bets' -&gt; Openbets tab
        EXPECTED: * Openbets inplay Inshop bets are loaded displaying the “Bet Station slip” header with an Expand and Collapse arrow “^”
        """
        pass

    def test_004_check_the_visualization_for_inplay_inshop_bets(self):
        """
        DESCRIPTION: Check the visualization for inplay inshop bets
        EXPECTED: * Visualization is available under "Show More"
        """
        pass
