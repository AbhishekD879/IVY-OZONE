import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C2036496_Place_a_bet_when_the_users_deposit_limit_0_NULL(Common):
    """
    TR_ID: C2036496
    NAME: Place a bet when the user's deposit limit = '0'/NULL
    DESCRIPTION: This test case verifies bet placement functionality when user's deposit limit = '0'/NULL
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User doesn't have deposit limits defined
    PRECONDITIONS: * User's account balance is sufficient to cover a bet stake
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_any_sport(self):
        """
        DESCRIPTION: Open any <Sport>
        EXPECTED: <Sport> landing page is opened
        """
        pass

    def test_003_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_004_open_betslip__singles_section(self):
        """
        DESCRIPTION: Open Betslip-> 'Singles' section
        EXPECTED: 'Singles' section is opened
        """
        pass

    def test_005_enter_stakes_in_stake_field(self):
        """
        DESCRIPTION: Enter stakes in 'Stake' field
        EXPECTED: * Value is entered and displayed properly
        EXPECTED: * All needed validations work properly
        """
        pass

    def test_006_tap_on_bet_now_button(self):
        """
        DESCRIPTION: Tap on 'Bet Now' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        pass
