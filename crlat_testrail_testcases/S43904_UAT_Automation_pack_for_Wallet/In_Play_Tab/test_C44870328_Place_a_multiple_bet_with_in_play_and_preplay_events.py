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
class Test_C44870328_Place_a_multiple_bet_with_in_play_and_preplay_events(Common):
    """
    TR_ID: C44870328
    NAME: Place a multiple bet with in play and preplay events
    DESCRIPTION: This test case verifies placing a Multiples on inplay and preplay events
    PRECONDITIONS: UserName: goldenbuild1   Password: password1
    """
    keep_browser_open = True

    def test_001_load_httpsbeta_sportscoralcouklogin_with_user_with_positive_balance(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk/
        DESCRIPTION: Login with user with positive balance
        EXPECTED: Homepage opened
        EXPECTED: user is logged in
        """
        pass

    def test_002_add_several_selections_from_different_inplay_and_preplay_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from different inplay and preplay events to the betslip
        EXPECTED: Selections are displayed
        """
        pass

    def test_003_open_betslip_and_scroll_down_to_multiples_section(self):
        """
        DESCRIPTION: Open Betslip and scroll down to 'Multiples' section
        EXPECTED: Multiples are displayed
        """
        pass

    def test_004_enter_stake_for_one_of_available_multiples(self):
        """
        DESCRIPTION: Enter Stake for one of available Multiples
        EXPECTED: Est. Returns, Total Stake and Total Est. Returns fields are calculated
        """
        pass

    def test_005_tap_on_place_bet(self):
        """
        DESCRIPTION: Tap on 'Place Bet'
        EXPECTED: Multiple Bet is placed successfully (the one which had entered Stake, the rest Multiples are ignored)
        EXPECTED: User balance is decreased by Total Stake
        EXPECTED: Bet Receipt page is shown with the correct information about placed bet
        """
        pass

    def test_006_tap_reuse_selection_or_go_betting(self):
        """
        DESCRIPTION: Tap 'Reuse selection' or 'Go betting'
        EXPECTED: On clicking
        EXPECTED: Reuse selection > User is navigated to the betslip with the same selections
        EXPECTED: Go betting > User is navigated to the Previous page.
        """
        pass
