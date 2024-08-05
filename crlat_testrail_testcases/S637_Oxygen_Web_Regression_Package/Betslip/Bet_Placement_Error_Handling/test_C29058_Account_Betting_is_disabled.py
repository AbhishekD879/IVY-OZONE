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
class Test_C29058_Account_Betting_is_disabled(Common):
    """
    TR_ID: C29058
    NAME: Account Betting is disabled
    DESCRIPTION: This test case verifies  Error Handling when account betting is disabled.
    PRECONDITIONS: **How to Disable Betting for a User** https://confluence.egalacoral.com/display/SPI/How+to+Disable+Betting+for+a+User
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event details page
    PRECONDITIONS: **NOTE:** contact UAT team for all configurations
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_login_with_disabled_account_betting_for_certain_sport(self):
        """
        DESCRIPTION: Login with Disabled Account Betting for certain sport
        EXPECTED: User is logged in successfully
        """
        pass

    def test_003_add_a_selection_to_the_betslip_from_sport_which_is_disabled_for_this_user(self):
        """
        DESCRIPTION: Add a selection to the Betslip from sport which is disabled for this user
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_004_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: * Betslip is opened
        EXPECTED: * Added selection is displayed in the Betslip
        """
        pass

    def test_005_enter_correct_stakes_in_stake_field(self):
        """
        DESCRIPTION: Enter correct stakes in 'Stake' field
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        pass

    def test_006_clicktap_on_bet_now_button(self):
        """
        DESCRIPTION: Click/Tap on 'Bet Now' button
        EXPECTED: * Pop up with corresponding information from server appears which is notifying the user that betting is disabled
        EXPECTED: * User doesn't have possibility to place bets
        """
        pass

    def test_007_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED: Betslip is empty
        """
        pass

    def test_008_try_to_place_a_bet_for_an_event_from_another_sport_which_is_not_disabled_for_this_user(self):
        """
        DESCRIPTION: Try to place a bet for an event from another sport which is not disabled for this user
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_009_enable_account_betting_instruction_is_added_in_preconditions_or_ask_uat_team(self):
        """
        DESCRIPTION: Enable account betting (instruction is added in preconditions or ask UAT team)
        EXPECTED: Account betting is enabled
        """
        pass

    def test_010_repeat_steps__3___6(self):
        """
        DESCRIPTION: Repeat steps # 3 - 6
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_011_add_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selections from different events to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_012_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: * Betslip is opened
        EXPECTED: * Added selections are displayed in the Betslip
        EXPECTED: * 'Multiples' section is displayed
        """
        pass

    def test_013_repeat_steps__5___10(self):
        """
        DESCRIPTION: Repeat steps # 5 - 10
        EXPECTED: 
        """
        pass
