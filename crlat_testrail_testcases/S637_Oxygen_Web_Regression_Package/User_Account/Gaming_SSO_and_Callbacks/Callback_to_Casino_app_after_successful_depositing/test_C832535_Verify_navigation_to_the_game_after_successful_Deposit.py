import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C832535_Verify_navigation_to_the_game_after_successful_Deposit(Common):
    """
    TR_ID: C832535
    NAME: Verify navigation to the game after successful Deposit
    DESCRIPTION: This test case verifies navigation to the game after successful deposit when navigation to the deposit page from the played game was made
    DESCRIPTION: **Jira tickets:**
    DESCRIPTION: *   BMA-9373 Introduce button to go back to previous game from successful deposit journey
    PRECONDITIONS: When User is taken to the mcasino.coral.co.uk then mcasino site sets gameBaseURL  to mcasino.coral.co.uk/?ref=bma
    PRECONDITIONS: gameBaseURL example:  https://wap-stg1.coral.co.uk/en/?game=irm3sc&username=stage&real=1&temptoken={tempToken}
    PRECONDITIONS: where username and temptoken are set to current user session.
    PRECONDITIONS: Pay attention to the environment you are testing on
    """
    keep_browser_open = True

    def test_001_load_oxygen_and_log_in(self):
        """
        DESCRIPTION: Load Oxygen and log in
        EXPECTED: User is logged in
        """
        pass

    def test_002_go_to_gaming(self):
        """
        DESCRIPTION: Go to 'Gaming'
        EXPECTED: 'Gaming' page is opened
        """
        pass

    def test_003_go_into_any_game(self):
        """
        DESCRIPTION: Go into any game
        EXPECTED: - Game is opened
        EXPECTED: - gameBaseURL is set to correct cookie link (see Preconditions)
        """
        pass

    def test_004_enter_total_bet_higher_than_your_balance(self):
        """
        DESCRIPTION: Enter total bet higher than your balance
        EXPECTED: Insufficient balance message appears
        """
        pass

    def test_005_click_to_deposit_from_the_game(self):
        """
        DESCRIPTION: Click to deposit from the game
        EXPECTED: User is redirected to the Oxygen deposit page
        """
        pass

    def test_006_enter_the_info_required_to_make_a_deposit(self):
        """
        DESCRIPTION: Enter the info required to make a deposit
        EXPECTED: Successful message appears
        """
        pass

    def test_007_verify_navigation_to_the_game_after_successful_deposit(self):
        """
        DESCRIPTION: Verify navigation to the game after successful Deposit
        EXPECTED: In case of successful deposit User is redirected to the game he just came from
        """
        pass

    def test_008_verify_navigation_to_the_game_after_unsuccessful_deposit(self):
        """
        DESCRIPTION: Verify navigation to the game after unsuccessful Deposit
        EXPECTED: In case of unsuccessful deposit User stays on Deposit page
        """
        pass

    def test_009_tap_on__back_button(self):
        """
        DESCRIPTION: Tap on '<' back button
        EXPECTED: User is redirected to the game he just came from
        """
        pass
