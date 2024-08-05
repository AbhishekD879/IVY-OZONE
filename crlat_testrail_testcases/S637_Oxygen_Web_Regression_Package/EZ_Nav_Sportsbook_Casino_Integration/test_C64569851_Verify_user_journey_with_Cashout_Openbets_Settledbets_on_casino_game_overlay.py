import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C64569851_Verify_user_journey_with_Cashout_Openbets_Settledbets_on_casino_game_overlay(Common):
    """
    TR_ID: C64569851
    NAME: Verify user journey with Cashout/Openbets/Settledbets on casino game overlay.
    DESCRIPTION: Verify user journey with Cashout/Openbets/Settledbets on casino game overlay.
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in.
    PRECONDITIONS: Note: Applies to only Mobile Web
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
        EXPECTED: Cashout (if available)
        EXPECTED: Openbets
        EXPECTED: Settledbets
        """
        pass

    def test_003_tap_cashout_tab(self):
        """
        DESCRIPTION: Tap 'Cashout' tab
        EXPECTED: * Cashout available bets are displayed
        EXPECTED: * 'GO TO SPORTS' CTA also displayed next to bets.
        """
        pass

    def test_004_tap_openbets_tab(self):
        """
        DESCRIPTION: Tap 'Openbets' tab
        EXPECTED: * User navigates to 'Sports' inner tab & available bets are displayed
        EXPECTED: * Lotto, Pools, In-shop  inner tabs also displayed with available bets
        EXPECTED: * 'GO TO SPORTS' CTA also displayed next to bets except In-shop tab.
        """
        pass

    def test_005_repeat_step_4_in_settledbets_tab(self):
        """
        DESCRIPTION: Repeat step-4 in 'Settledbets' tab
        EXPECTED: 
        """
        pass
