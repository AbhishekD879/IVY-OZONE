import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C15392879_Vanilla_Logged_in_user_Place_a_Bet_on_Betslip(Common):
    """
    TR_ID: C15392879
    NAME: [Vanilla] [Logged in user] Place a Bet on Betslip
    DESCRIPTION: This test case verifies bet placement when the user is Logged in
    PRECONDITIONS: *Betslep should be enabled in CMS
    PRECONDITIONS: *User should be logged in and have a positive deposit
    PRECONDITIONS: *Selection should be added to betslip
    """
    keep_browser_open = True

    def test_001_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 1.  Betslip is opened
        EXPECTED: 2.  Added single selections are present
        EXPECTED: 3. 'Place bet' button is disabled
        EXPECTED: ![](index.php?/attachments/get/10272583)
        """
        pass

    def test_002_enter_at_least_one_stake_for_any_single_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any single selection
        EXPECTED: 1. Stake is entered and displayed correctly
        EXPECTED: 2. 'Place bet' button becomes enabled
        """
        pass

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: Bet is placed successfully as for logged in user
        """
        pass

    def test_004_add_several_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from different events to the Betslip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_005_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 1.  Betslip is opened
        EXPECTED: 2.  Added multiple selections are present
        """
        pass

    def test_006_add_stake_for_any_selection_in_multiples_section_and_repeat_steps_3(self):
        """
        DESCRIPTION: Add stake for any selection in Multiples section and Repeat steps #3
        EXPECTED: 
        """
        pass
