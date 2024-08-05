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
class Test_C64569861_Verify_displaying_of_Stake_and_Potential_returns_on_the_My_Bets__Cashout_and_Openbets_page_on_casino_game_overlay(Common):
    """
    TR_ID: C64569861
    NAME: Verify displaying of Stake and Potential returns on the My Bets -> Cashout and Openbets page on casino game overlay.
    DESCRIPTION: Verify displaying of Stake and Potential returns on the My Bets -&gt; Cashout and Openbets page on casino game overlay.
    PRECONDITIONS: * Cashout Tab is enabled from CMS
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * User has placed a bet on SINGLE, DOUBLE, TREBLE,ACCA4 bets, LOTTO bets, POOLS bets
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
        EXPECTED: Cashout
        EXPECTED: Openbets
        EXPECTED: Settledbets
        """
        pass

    def test_003_tap_cashout_tabverify_stake__potentialestimated_returns(self):
        """
        DESCRIPTION: Tap 'Cashout' tab
        DESCRIPTION: Verify Stake & Potential/Estimated returns
        EXPECTED: * Stake is available
        EXPECTED: * 'Potential Returns'/'Est. Returns' is available that may be a value or N/A
        """
        pass

    def test_004_repeat_step_3_in_openbets_tab(self):
        """
        DESCRIPTION: Repeat step-3 in 'Openbets' tab
        EXPECTED: 
        """
        pass
