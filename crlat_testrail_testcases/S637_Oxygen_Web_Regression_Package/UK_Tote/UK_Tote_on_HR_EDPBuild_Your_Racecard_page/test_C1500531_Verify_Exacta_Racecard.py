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
class Test_C1500531_Verify_Exacta_Racecard(Common):
    """
    TR_ID: C1500531
    NAME: Verify Exacta Racecard
    DESCRIPTION: This test case verifies the racecard of Exacta pool type of UK Tote
    DESCRIPTION: AUTOTEST: [C2069896]
    DESCRIPTION: AUTOTEST: [C2080049]
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
    PRECONDITIONS: * The horse racing event should have Exacta markets available
    PRECONDITIONS: Cannot run the step #3 (cannot influence  the current pool value changes)
    """
    keep_browser_open = True

    def test_001_select_exacta_tab(self):
        """
        DESCRIPTION: Select "Exacta" tab
        EXPECTED: * "Exacta" tab is selected
        EXPECTED: * Exacta racecard is shown
        """
        pass

    def test_002_verify_exacta_racecard_for_an_active_event(self):
        """
        DESCRIPTION: Verify Exacta racecard for an **active** event
        EXPECTED: Exacta racecard consists of:
        EXPECTED: * Current pool value (only shown if available)
        EXPECTED: * Runner number, name and information for each runner
        EXPECTED: * Runner silks (if available) for each runner
        EXPECTED: * "1st", "2nd", and "Any" check boxes for each runner (all active by default)
        EXPECTED: Unnamed Favourite is NOT displayed at the end of list (BMA-50146)
        """
        pass

    def test_003_refresh_the_page_after_current_pool_value_changes(self):
        """
        DESCRIPTION: Refresh the page **after** current pool value changes
        EXPECTED: * Current pool value is updated upon page refresh
        """
        pass

    def test_004_lick_on_spotlight_downward_arrow_or_form_options_under_individual_selections(self):
        """
        DESCRIPTION: Сlick on spotlight (downward arrow) or form options under individual selections
        EXPECTED: The spotlight and form information under the selection are shown to the user
        """
        pass

    def test_005_select_the_1st_check_box_for_any_runner(self):
        """
        DESCRIPTION: Select the **"1st"** check box for any runner
        EXPECTED: * The check box is selected
        EXPECTED: * All other "1st" check boxes are disabled
        EXPECTED: * "2nd" check box **for this runner** is disabled
        EXPECTED: * All "Any" check boxes on the racecard are disabled as well
        EXPECTED: * Bet builder appears at the bottom (with disabled 'Add to betslip' button)
        """
        pass

    def test_006_uncheck_the_1st_check_box_and_select_the_2nd_check_box_for_any_runner(self):
        """
        DESCRIPTION: Uncheck the "1st" check box and select the **"2nd"** check box for any runner
        EXPECTED: * The check box is selected
        EXPECTED: * All other "2nd" check boxes are disabled
        EXPECTED: * "1st" check box **for this runner** is disabled
        EXPECTED: * All "Any" check boxes on the racecard are disabled as well
        EXPECTED: * Bet builder appears at the bottom (with disabled 'Add to betslip' button)
        """
        pass

    def test_007_select_the_1st__and_2nd_check_boxes_together_for_any_runners(self):
        """
        DESCRIPTION: Select the **"1st"**  and **"2nd"** check boxes together for any runners
        EXPECTED: * The check boxes are selected
        EXPECTED: * All other check boxes on the racecard are disabled
        EXPECTED: * Bet builder appears at the bottom with enabled 'Add to betslip' button and Clear selection link
        """
        pass

    def test_008_uncheck_the_1st_and_2nd_check_boxes(self):
        """
        DESCRIPTION: Uncheck the **"1st"** and **"2nd"** check boxes
        EXPECTED: * All check boxes are active again
        EXPECTED: * Bet builder disappears
        """
        pass

    def test_009_select_any_check_box_for_any_runner(self):
        """
        DESCRIPTION: Select **"Any"** check box for any runner
        EXPECTED: * Check box is selected
        EXPECTED: * All "1st" and "2nd" check boxes are disabled
        EXPECTED: * Others "Any" check boxes on the racecard are enabled
        EXPECTED: * Bet builder appears
        """
        pass

    def test_010_select_any_check_boxes_for_2_3_more_runners(self):
        """
        DESCRIPTION: Select **"Any"** check boxes for 2-3 more runners
        EXPECTED: * User is able to select "Any" check boxes for multiple runners
        EXPECTED: * All "1st" and "2nd" check boxes are still disabled
        """
        pass

    def test_011_verify_exacta_racecard_with_a_suspended_selection(self):
        """
        DESCRIPTION: Verify Exacta racecard with a **suspended selection**
        EXPECTED: * All check boxes for suspended selection are disabled
        EXPECTED: * All check boxes for active selections are active
        """
        pass

    def test_012_verify_exacta_racecard_for_a_suspended_event(self):
        """
        DESCRIPTION: Verify Exacta racecard for a **suspended** event
        EXPECTED: * All check boxes on the racecard are disabled
        """
        pass

    def test_013_verify_case_when_the_event_changes_from_active_to_suspended_while_the_user_is_on_the_page(self):
        """
        DESCRIPTION: Verify case when the event changes from active to suspended while the user is on the page
        EXPECTED: * The event changes to suspended in real time
        EXPECTED: * All check boxes become disabled in real time
        """
        pass

    def test_014_verify_case_when_the_event_changes_from_suspended_to_active_while_the_user_is_on_the_page(self):
        """
        DESCRIPTION: Verify case when the event changes from suspended to active while the user is on the page
        EXPECTED: * The event changes to active in real time
        EXPECTED: * All check boxes become active in real time
        """
        pass
