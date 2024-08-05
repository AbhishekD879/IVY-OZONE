import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17752134_Vanilla_Place_bet_after_account_closure(Common):
    """
    TR_ID: C17752134
    NAME: [Vanilla] Place bet after account closure
    DESCRIPTION: This test case verifies bet placement after Sports product closure
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and have **Sports** product closed
    PRECONDITIONS: **How to close your account:**
    PRECONDITIONS: Log In -> 'My Account' -> 'Gambling Control'/'Responsible Gambling' -> 'Account Management'/'Account Closure&Reopening' -> click 'Choose' button -> select 'I want to close my account or section of it' -> select 'Sports' category -> set 'Duration' and 'Reason for closure' -> tap 'Close' button
    """
    keep_browser_open = True

    def test_001_make_a_bet_selection(self):
        """
        DESCRIPTION: Make a bet selection
        EXPECTED: Selection is added to Bet Slip.
        """
        pass

    def test_002_enter_stake(self):
        """
        DESCRIPTION: Enter stake
        EXPECTED: Stake is added
        """
        pass

    def test_003_click_the_place_bet_button(self):
        """
        DESCRIPTION: Click the **Place bet** button
        EXPECTED: Bet is not placed.
        """
        pass

    def test_004_go_to_settled_bets(self):
        """
        DESCRIPTION: Go to **Settled Bets**
        EXPECTED: Bet is not present there
        """
        pass

    def test_005_go_to_cash_out(self):
        """
        DESCRIPTION: Go to **Cash out**
        EXPECTED: Bet is not present there
        """
        pass

    def test_006_go_to_open_bets(self):
        """
        DESCRIPTION: Go to **Open bets**
        EXPECTED: Bet is not present there
        """
        pass
