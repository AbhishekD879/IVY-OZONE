import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870307_Verify_win_bet_behaviour_for_GH_Place_a_bet_on_GH_and_settle_it_as_win_selection_verify_on_the_my_bets_settle_bet_and_bet_history(Common):
    """
    TR_ID: C44870307
    NAME: Verify 'win' bet behaviour for GH. (Place a bet on GH and settle it as win selection, verify on the my bets settle bet and bet history)
    DESCRIPTION: - User should be logged in
    DESCRIPTION: - Open bet configuration required
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_the_appsite_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the app/site and login with valid credentials
        EXPECTED: Successfully app launched and user is on app
        """
        pass

    def test_002_place_a_bet_on_greyhounds_race(self):
        """
        DESCRIPTION: Place a bet on Greyhounds race
        EXPECTED: Bet placed successfully
        """
        pass

    def test_003_win_the_bet_in_open_bet_and_check_the_status_in_my_bets_and_bet_history(self):
        """
        DESCRIPTION: 'win' the bet in open bet and check the status in my bets and bet history
        EXPECTED: User should see the 'win'bet in my bets in settled tab and bet history
        """
        pass

    def test_004_verify_the_header_balance_update(self):
        """
        DESCRIPTION: verify the header balance update
        EXPECTED: Header balance should be updated
        """
        pass
