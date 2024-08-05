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
class Test_C64668234_Verify_live_updates_on_casino_game_MYBETS_overlay(Common):
    """
    TR_ID: C64668234
    NAME: Verify live updates on casino game MYBETS overlay
    DESCRIPTION: Verify live updates on casino game MYBETS overlay
    PRECONDITIONS: * Cashout Tab is enabled from CMS
    PRECONDITIONS: * User should be in Gaming window
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * User has bets placed on inplay events in Openbets, cashout
    PRECONDITIONS: * User has BYB & 5A-side bets in openbets
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

    def test_003_tap_cashout_tab(self):
        """
        DESCRIPTION: Tap 'Cashout' tab
        EXPECTED: * Inplay Cashoutable bets are loaded
        """
        pass

    def test_004_in_ti_trigger_price_update_for_selection_which_was_placed_bet(self):
        """
        DESCRIPTION: In TI: trigger price update for selection which was placed bet
        EXPECTED: * Cashout value is updated accordingly
        """
        pass

    def test_005_in_ti_trigger_suspension_update_in_selectionmarketevent_level_on_which_the_bet_is_placed(self):
        """
        DESCRIPTION: In TI: trigger suspension update in selection/market/event level on which the bet is placed
        EXPECTED: * Bet becomes suspended (susp label is present on the left in event card, 'Cash Out &lt;value&gt;' button becomes 'Cash Out suspended' and greyed out
        """
        pass

    def test_006_in_ti_trigger_score_updates_for_bet_which_was_placed(self):
        """
        DESCRIPTION: In TI: trigger score updates for bet which was placed
        EXPECTED: * Score updates are received
        """
        pass

    def test_007_repeat_step456_in_openbets_tab(self):
        """
        DESCRIPTION: Repeat step4,5,6 in Openbets tab
        EXPECTED: 
        """
        pass

    def test_008_check_byb__5a_side_bets_when_it_is_live(self):
        """
        DESCRIPTION: Check BYB & 5A-side bets when it is live
        EXPECTED: * User able to see stats tracking indicators left to the selection
        """
        pass
