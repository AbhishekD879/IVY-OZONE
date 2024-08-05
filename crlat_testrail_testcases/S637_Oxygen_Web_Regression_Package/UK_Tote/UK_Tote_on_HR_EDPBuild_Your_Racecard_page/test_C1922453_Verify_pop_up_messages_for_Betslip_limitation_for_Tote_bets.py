import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1922453_Verify_pop_up_messages_for_Betslip_limitation_for_Tote_bets(Common):
    """
    TR_ID: C1922453
    NAME: Verify pop-up messages for Betslip limitation for Tote bets
    DESCRIPTION: This test case verifies pop-up messages for Tote bets in Betslip which appears in the next cases:
    DESCRIPTION: * user tries to add a Tote bet to Betslip and he doesn't have any bets in the Betslip
    DESCRIPTION: * user tries to add a Tote bet to Betslip and he already has Tote bets in the Betslip
    DESCRIPTION: * user tries to add a Tote bet to Betslip and he already has regular (non-Tote) bets in the Betslip
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is sufficient to cover the bet stake
    PRECONDITIONS: * There are no bets in Betslip
    PRECONDITIONS: * Quick Bet functionality is enabled in CMS
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Tote" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Totepool are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- endpoint .symphony-solutions.eu)
    PRECONDITIONS: endpoint can be found using devlog
    """
    keep_browser_open = True

    def test_001_make_selection_and_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Make selection and tap 'ADD TO BETSLIP' button
        EXPECTED: * Bet builder disappears
        EXPECTED: * Tote bet is added to Betslip (betslip icon displays correct indicator)
        EXPECTED: * Selections become unchecked
        EXPECTED: * No pop-up messages appears (as there were no bets in Betslip)
        EXPECTED: * Footer menu is displayed
        """
        pass

    def test_002_make_some_more_selections_and_press_add_to_betslip_button(self):
        """
        DESCRIPTION: Make some more selections and press Add to betslip button
        EXPECTED: Pop-up message appears:
        EXPECTED: * The header of message: "NOTICE"
        EXPECTED: * The text of message: "You already have one or more selections in the bet slip that can't be combined, please remove those selections to add any new selection"
        EXPECTED: * "OK" button is displayed
        """
        pass

    def test_003_tap_ok_button(self):
        """
        DESCRIPTION: Tap "OK" button
        EXPECTED: * Pop-up message disappears
        EXPECTED: * User is remaining on the same page
        EXPECTED: * Selections are not removed (are still checked)
        """
        pass

    def test_004_open_betslip_and_remove_selections_using_delete_button_or_place_bets(self):
        """
        DESCRIPTION: Open betslip and remove selections (using 'Delete' button) or place bets
        EXPECTED: * Betslip is empty
        EXPECTED: * "Your betslip is empty" message is displayed
        """
        pass

    def test_005_add_any_single_or_multiple_selection_to_betslip_not_tote_events(self):
        """
        DESCRIPTION: Add any single or multiple selection to betslip (not tote events)
        EXPECTED: * Quick Bet is closed after tapping 'Add to Betslip' button
        EXPECTED: * Bet is added to Betslip
        """
        pass

    def test_006_make_another_tote_selection_and_tap_add_to_betslip(self):
        """
        DESCRIPTION: Make another tote selection and tap Add to betslip
        EXPECTED: Pop-up message appears:
        EXPECTED: * The header of message: "NOTICE"
        EXPECTED: * The text of message: "You already have one or more selections in the bet slip that can't be combined, please remove those selections to add any new selection"
        EXPECTED: * "OK" button is displayed
        """
        pass

    def test_007_tap_ok_button(self):
        """
        DESCRIPTION: Tap "OK" button
        EXPECTED: * Pop-up message disappears
        EXPECTED: * User is remaining on the same page
        EXPECTED: * Selections are not removed (are still checked)
        """
        pass

    def test_008_remove_selections_from_betslip_using_delete_button_or_place_a_bet_and_add_new_selections_from_tote_pool_to_betslip(self):
        """
        DESCRIPTION: Remove selections from betslip (using delete button or place a bet) and add new selections from tote pool to betslip
        EXPECTED: * Bet builder disappears
        EXPECTED: * Tote bet is added to Betslip
        EXPECTED: * No pop-up messages appears (as there were no bets in Betslip)
        EXPECTED: * Betslip indicator is increased by 1
        """
        pass

    def test_009_repeat_step__7(self):
        """
        DESCRIPTION: Repeat step # 7
        EXPECTED: * Quick Bet is closed after tapping 'Add to Betslip' button
        EXPECTED: Pop-up message appears:
        EXPECTED: * The header of message: "NOTICE"
        EXPECTED: * The text of message: "You already have one or more selections in the bet slip that can't be combined, please remove those selections to add any new selection"
        EXPECTED: * "OK" button is displayed
        """
        pass

    def test_010_tap_ok_button(self):
        """
        DESCRIPTION: Tap "OK" button
        EXPECTED: * Pop-up message disappears
        EXPECTED: * User is remaining on the same page
        EXPECTED: * Selections are not removed (are still checked)
        """
        pass
