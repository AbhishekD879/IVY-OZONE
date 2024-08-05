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
class Test_C29009_Verify_Betslip_sections(Common):
    """
    TR_ID: C29009
    NAME: Verify Betslip sections
    DESCRIPTION: This test case verifies Betslip sections
    DESCRIPTION: Autotest [C9690030]
    PRECONDITIONS: Customer can view the Betslip logged in or logged out
    PRECONDITIONS: Multiples may not be available after adding Special events to the Betslip depending on response from OB
    PRECONDITIONS: Multiples are formed from selections from different events
    """
    keep_browser_open = True

    def test_001_add_sportselection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add <Sport>selection to the Bet Slip
        EXPECTED: Bet Slip counter is 1
        """
        pass

    def test_002_go_to_the_bet_slip(self):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: *   The 'Your Selections (1)' section is shown
        EXPECTED: *   Added selection is displayed
        """
        pass

    def test_003_add_one_more_selection_from_another_sport_event(self):
        """
        DESCRIPTION: Add one more selection from another <Sport> event
        EXPECTED: Bet Slip counter is 2
        """
        pass

    def test_004_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to Bet Slip
        EXPECTED: *  Singles section is shown with a header 'Your Selections (2)'
        EXPECTED: *  'All single stakes' label and input field appear in Singles section (for Coral only)
        EXPECTED: *  The 'Multiples' section is shown right after 'Singles'
        EXPECTED: *  A list of available multiples bets is shown
        """
        pass

    def test_005_add_one_more_selections_from_another_sport_event(self):
        """
        DESCRIPTION: Add one more selections from another <Sport> event
        EXPECTED: Bet Slip counter is 3
        """
        pass

    def test_006_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to Bet Slip
        EXPECTED: *  Singles section is shown with a header 'Your Selections (3)'
        EXPECTED: * 'All single stakes' label and input field appear in Singles section (for Coral only)
        EXPECTED: *  Multiples combinations of all selections are shown within this section (e.g. Treble 1, Accumulator (4) 1 Bets)
        """
        pass

    def test_007_provide_same_verifications_for_race_events(self):
        """
        DESCRIPTION: Provide same verifications for <Race> events
        EXPECTED: 
        """
        pass

    def test_008__na_from_ox_98add_three_race_selections_from_one_market(self):
        """
        DESCRIPTION: **( N/A from OX 98)**
        DESCRIPTION: Add three Race selections from one market
        EXPECTED: Bet Slip counter is increased by number of added selections
        """
        pass

    def test_009__na_from_ox_98go_to_bet_slip(self):
        """
        DESCRIPTION: **( N/A from OX 98)**
        DESCRIPTION: Go to Bet Slip
        EXPECTED: *   The "Forecasts/Tricasts" section is shown right after 'Singles'
        EXPECTED: *   A list of available "Forecasts/Tricasts" bets is shown
        EXPECTED: *   'Multiples' section is shown after "Forecasts/Tricasts"
        """
        pass
