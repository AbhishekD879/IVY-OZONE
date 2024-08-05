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
class Test_C29037_Multiples_ordering(Common):
    """
    TR_ID: C29037
    NAME: Multiples ordering
    DESCRIPTION: This test case verifies ordering of Multiples within Bet Slip page.
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-5409 (Accums to appear top of the list in Multiples View on BetSlip)
    DESCRIPTION: BMA-20069 Show correct ACCA option top of betslip
    DESCRIPTION: AUTOTEST [C527781]
    DESCRIPTION: AUTOTEST [C1501904]
    PRECONDITIONS: Note: Multiples may not be available after adding Special events to the Betslip.
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_open_any_sport(self):
        """
        DESCRIPTION: Open any sport
        EXPECTED: 
        """
        pass

    def test_003_add_two_selections_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add two selections from different events to the betslip
        EXPECTED: 
        """
        pass

    def test_004_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: **Before OX99*
        EXPECTED: 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: Multiples are available for added selections
        """
        pass

    def test_005_verify_order_of_multiples(self):
        """
        DESCRIPTION: Verify order of Multiples
        EXPECTED: *   'Double' bet type is the first in the list at any time within 'Multiples' section
        EXPECTED: *   The rest bet types are displayed below 'Multiples' section as they are returned from OpenBet
        """
        pass

    def test_006_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED: 
        """
        pass

    def test_007_add_three_selections_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add three selections from different events to the betslip
        EXPECTED: 
        """
        pass

    def test_008_verify_order_of_multiples(self):
        """
        DESCRIPTION: Verify order of Multiples
        EXPECTED: **Before OX99**
        EXPECTED: *   'Treble' bet type is shown in separate section 'Place your ACCA (n)' at any time which is shown as the first section in the betslip, where n- number of singles added
        EXPECTED: *   The rest bet types are displayed below 'Multiples' section as they are returned from OpenBet
        EXPECTED: **After OX99**
        EXPECTED: * 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: * 'TREBLE' bet type is shown the first under 'Multiples'
        EXPECTED: * The rest bet types are displayed below 'Multiples' section as they are returned from OpenBet
        """
        pass

    def test_009_clear_betslip(self):
        """
        DESCRIPTION: Clear Betslip
        EXPECTED: 
        """
        pass

    def test_010_add_three_or_more_selections_from_different_events_to_thebetslip(self):
        """
        DESCRIPTION: Add three or more selections from different events to the betslip
        EXPECTED: 
        """
        pass

    def test_011_verify_order_of_multiples(self):
        """
        DESCRIPTION: Verify order of Multiples
        EXPECTED: **Before OX99**
        EXPECTED: *   'Accumulator(n)' bet type is shown in separate section 'Place your ACCA (n)' at any time which is shown as the first section in the betslip, where n- number of singles added
        EXPECTED: *   The rest bet types are displayed below 'Multiples' section as they are returned from OpenBet
        EXPECTED: **After OX99**
        EXPECTED: * 'Multiples' section is displayed as the last section within 'Bet Slip'
        EXPECTED: * '(n) Fold Acca' bet type is shown the first under 'Multiples', where n- number of singles added
        EXPECTED: * The rest bet types are displayed below 'Multiples' section as they are returned from OpenBet
        """
        pass

    def test_012_manually_remove_selections_to_leave_in_the_betslip_three_selections(self):
        """
        DESCRIPTION: Manually remove selection(s) to leave in the betslip three selections
        EXPECTED: Multiples are rebuilt
        """
        pass

    def test_013_repeat_step_8(self):
        """
        DESCRIPTION: Repeat step №8
        EXPECTED: 
        """
        pass

    def test_014_manually_remove_selection_to_leave_in_the_betslip_two_selections(self):
        """
        DESCRIPTION: Manually remove selection to leave in the betslip two selections
        EXPECTED: Multiples are rebuilt
        """
        pass

    def test_015_repeat_step_5(self):
        """
        DESCRIPTION: Repeat step №5
        EXPECTED: 
        """
        pass
