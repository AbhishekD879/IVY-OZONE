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
class Test_C44870306_Verify_void_bet_behaviour_for_HR_Place_a_bet_on_HR_and_settle_it_as_void_selection_verify_on_the_my_bets_settle_bet_and_bet_history(Common):
    """
    TR_ID: C44870306
    NAME: Verify 'void' bet behaviour for HR. (Place a bet on HR and settle it as void selection, verify on the my bets settle bet and bet history)
    DESCRIPTION: 
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: Open bet configuration required
    """
    keep_browser_open = True

    def test_001_launch_the_appsite_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the app/site and login with valid Credentials
        EXPECTED: Successfully app launched and able to log in
        """
        pass

    def test_002_place_a_bet_on_hr(self):
        """
        DESCRIPTION: Place a bet on HR
        EXPECTED: placed bet successfully
        """
        pass

    def test_003_void_the_bet_in_open_bet_and_check_the_status_in_my_bets_and_bet_history(self):
        """
        DESCRIPTION: 'Void' the bet in open bet and check the status in my bets and bet history
        EXPECTED: User should see the 'void'bet in my bets in settled tab and bet history
        """
        pass

    def test_004_check_the_header_balance_update(self):
        """
        DESCRIPTION: Check the header balance update
        EXPECTED: Header balance should be updated
        """
        pass
