import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C15392880_Vanilla_TO_BE_EDITEDPlace_a_bet_on_Quickbet_for_logged_in_user(Common):
    """
    TR_ID: C15392880
    NAME: [Vanilla] [TO BE EDITED]Place a bet on Quickbet for logged in user
    DESCRIPTION: Verify that logged in user is able to place a bet from QuickBet
    PRECONDITIONS: *Quickbet should be enabled in CMS
    PRECONDITIONS: *User should be logged in
    """
    keep_browser_open = True

    def test_001_open_vanilla(self):
        """
        DESCRIPTION: Open Vanilla
        EXPECTED: The application should be successfully loaded
        """
        pass

    def test_002_go_to_any_sport_eg_football___select_ant_odd(self):
        """
        DESCRIPTION: Go to any Sport (e.g Football)--> Select ant odd
        EXPECTED: QuickBet should appear in the bottom of the screen
        EXPECTED: "Place Bet" button should be disabled by default
        EXPECTED: ![](index.php?/attachments/get/31345)
        """
        pass

    def test_003_specify_any_quickstake_eg_5_(self):
        """
        DESCRIPTION: Specify any QuickStake (e.g. 5 )
        EXPECTED: "Place Bet" button should become enabled
        """
        pass

    def test_004_click_on_place_bet_button(self):
        """
        DESCRIPTION: Click on "Place Bet" button
        EXPECTED: Bet Receipt with all betting details should appear
        EXPECTED: Bet Receipt should contain "Reuse selection" and "Done" button
        EXPECTED: ![](index.php?/attachments/get/31346)
        """
        pass

    def test_005_click_on_reuse_selection_button(self):
        """
        DESCRIPTION: Click on "Reuse selection button"
        EXPECTED: The quick bet should be opened with the same bet but with empty stacked field and disabled "Place Bet" button
        """
        pass

    def test_006_specify_any_another_stake_eg_2_(self):
        """
        DESCRIPTION: Specify any Another Stake (e.g. 2 )
        EXPECTED: "Place Bet" button should become enabled
        """
        pass

    def test_007_click_on_place_bet_button(self):
        """
        DESCRIPTION: Click on "Place Bet" button
        EXPECTED: Bet Receipt with all betting details should appear
        EXPECTED: Bet Receipt should contain "Reuse selection" and "Done" button
        """
        pass

    def test_008_click_on_done_button(self):
        """
        DESCRIPTION: Click on "Done" button
        EXPECTED: Quick bet should disappear
        """
        pass

    def test_009_open_mybets(self):
        """
        DESCRIPTION: Open "MyBets"
        EXPECTED: Bets from step#4 and step#7 should be present.
        """
        pass
