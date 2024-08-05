import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C883635_Verify_Bet_Placement_when_Stake_is_lower_than_Min_Stake(Common):
    """
    TR_ID: C883635
    NAME: Verify Bet Placement when Stake is lower than Min Stake
    DESCRIPTION: This test case verifies Bet Placement when Stake is lower than Min Stake
    DESCRIPTION: AUTOTEST: [C1293645]
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * User is logged in and has positive balance
    PRECONDITIONS: * 'MinStake' value can be viewed or changed on selection level in OpenBet Ti tool
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_one_sport_selection(self):
        """
        DESCRIPTION: Tap one <Sport> selection
        EXPECTED: * Selected price/odds are highlighted in green
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_003_enter_value_which_is_lower_than_minstake_allowed_in_stake_field(self):
        """
        DESCRIPTION: Enter value which is lower than **minStake** allowed in 'Stake' field
        EXPECTED: * 'Stake' field is populated with entered value
        """
        pass

    def test_004_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: * Bet is NOT placed
        EXPECTED: * 'Stake is too low' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        """
        pass

    def test_005_verify_warning_message_presence(self):
        """
        DESCRIPTION: Verify warning message presence
        EXPECTED: Warning message does not disappear after tapping out of its area
        """
        pass

    def test_006_tap_x_button_on_quick_bet(self):
        """
        DESCRIPTION: Tap 'X' button on Quick Bet
        EXPECTED: Quick Bet is closed
        """
        pass

    def test_007_add__race_selection_to_quick_bet_and_repeat_steps_3_5(self):
        """
        DESCRIPTION: Add  <Race> selection to Quick Bet and repeat steps #3-5
        EXPECTED: 
        """
        pass
