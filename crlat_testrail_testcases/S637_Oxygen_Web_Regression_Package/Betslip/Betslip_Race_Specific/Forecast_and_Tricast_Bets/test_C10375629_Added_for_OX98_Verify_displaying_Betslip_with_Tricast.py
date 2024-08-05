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
class Test_C10375629_Added_for_OX98_Verify_displaying_Betslip_with_Tricast(Common):
    """
    TR_ID: C10375629
    NAME: [Added for OX98] Verify displaying Betslip with Tricast
    DESCRIPTION: This test case verifies displaying Tricast in Betslip
    PRECONDITIONS: 1. Load app and login with user
    PRECONDITIONS: 2. Navigate to Horse Races/Greyhounds page and open any event
    PRECONDITIONS: 3. Select 'Tricast' tab
    PRECONDITIONS: 4. Select '1st', '2nd' and '3rd' runners
    PRECONDITIONS: 5. Tap 'Add to Betslip' button
    PRECONDITIONS: NOTE: This test case should be run for Horse Races and for Greyhounds
    """
    keep_browser_open = True

    def test_001_navigate_to_win_or_each_way_tab_on_horse_race_grayhound_event_pageverify_that_appropriate_runners_which_where_selected_on_tricast_tab_are_not_selected(self):
        """
        DESCRIPTION: Navigate to 'Win or each way' tab on Horse Race/ Grayhound event page
        DESCRIPTION: Verify that appropriate runners which where selected on 'Tricast`' tab are not selected
        EXPECTED: - Appropriate runners are not selected on 'Win or each way' tab (selections are not highlighted)
        EXPECTED: - Single bets for the respective selections are NOT automatically added to the Betslip
        """
        pass

    def test_002_navigate_to_betslipverify_that_tricast_single_bet_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Tricast Single bet is shown
        EXPECTED: Tricast bet is shown under SINGLES with appropriate elements:
        EXPECTED: - Remove button
        EXPECTED: - 'Stake' field
        EXPECTED: - Bet selection (Runners) information according to selected runners.
        EXPECTED: e.g. : 1 HorseDan
        EXPECTED: 2 HorseTed
        EXPECTED: 3 HourseBen
        EXPECTED: **From OX99**:
        EXPECTED: 1st HorseDan
        EXPECTED: 2nd HorseTed
        EXPECTED: 3rd HourseBen
        EXPECTED: - **From OX99** Event name and time
        EXPECTED: - Bet Sort: **Tricast**
        EXPECTED: - Total Stake information
        EXPECTED: - Total Est. Returns information displayed as 0 (zero) (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: - 'Place Bet' button
        EXPECTED: NOTE: No singles selections are added to Betslip - only Tricast is added to Betslip
        """
        pass

    def test_003_add_a_stakeverify_that_total_est_returns_is_displayed_na(self):
        """
        DESCRIPTION: Add a Stake
        DESCRIPTION: Verify that Total Est. Returns is displayed N/A
        EXPECTED: - The stake is added and shown in the 'Stake' and 'Total Stake' fields
        EXPECTED: - Total Est. Returns information displayed as N/A (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        """
        pass

    def test_004_add_a_selection_from_win_or_each_way_tab_on_horse_racegrayhound_edpverify_that_additional_single_selection_is_shown_in_betslip(self):
        """
        DESCRIPTION: Add a selection from 'Win or each way' tab on Horse race/Grayhound EDP
        DESCRIPTION: Verify that additional single selection is shown in Betslip
        EXPECTED: The Betslip is shown with 2 SINGLE selections:
        EXPECTED: - Tricast
        EXPECTED: - Single HR/Grayhound selection (e.g. Win or Each Way)
        """
        pass
