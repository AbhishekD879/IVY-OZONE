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
class Test_C28883_To_archive_in_scope_of_OX_98_Verify_Forecast__Tricast_Section_Content(Common):
    """
    TR_ID: C28883
    NAME: [To archive in scope of OX 98] Verify 'Forecast' / 'Tricast' Section Content
    DESCRIPTION: This test case verifies the content within 'Forecast' / 'Tricast' section
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_add_two_or_three_race_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or three <Race> selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_002_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: *  Bet Slip is opened
        EXPECTED: *  Added selections are shown
        """
        pass

    def test_003_verify_forecast__tricasts_section(self):
        """
        DESCRIPTION: Verify 'Forecast' / 'Tricasts' section
        EXPECTED: *  Forecast / Tricasts section is shown below the 'Singles' section
        EXPECTED: *  Section title is "FORECAST/TRICASTS (n)", where n - the quantity of Forecast / Tricast bets
        EXPECTED: *  There is "-" sign to expand/collapse the section
        EXPECTED: *  Section is expanded by default
        EXPECTED: *  Section is collapsible/expandable
        """
        pass

    def test_004_verify_forecast__tricast_section_content(self):
        """
        DESCRIPTION: Verify 'Forecast' / 'Tricast' section content
        EXPECTED: 'Forecast' / 'Tricast' section consists of:
        EXPECTED: *   Event name and selections details as expandable/collapsible part of section
        EXPECTED: *   **'Forecast (k) / Tricast (k)'** section
        EXPECTED: *   **'Reverse Forecast (k) ', 'Combination Tricast (k)', 'Combination Forecast (k)'** sections - depending on quantity of added selections
        EXPECTED: *   **'Stake'** fields for each section
        EXPECTED: where  k - the number of combinations/outcomes contained in the forecast / tricast bet
        """
        pass

    def test_005_verify_event_and_selections_details_in_collapsed_view(self):
        """
        DESCRIPTION: Verify event and selections details in collapsed view
        EXPECTED: *    Event time and name is shown and correspond to the **'name'** attribute on event level
        EXPECTED: *    'Selections (n)' label is shown where n - number of selections based on which bets are build
        """
        pass

    def test_006_tap_plus_and_verify_selections_details_in_expanded_view(self):
        """
        DESCRIPTION: Tap '+' and verify selections details in expanded view
        EXPECTED: *   Selection order number, runner number and selection name are shown for each selection
        EXPECTED: *   Selection names correspond to the **'name'** attribute on outcome level
        EXPECTED: *   Selection numbers correspond to the **'runnerNumber'** attribute
        EXPECTED: *   Selections are shown in the order as they were added to the Bet Slip
        EXPECTED: *   'Re-order selections' button is displayed above the selections list
        """
        pass

    def test_007_add_two_or_three_selections_from_the_other_race_events_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or three selections from the other <Race> event's market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_008_open_bet_slip_and_verify_forecast__tricasts_section(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast' / 'Tricasts' section
        EXPECTED: For each event, it's own forecasts/tricasts betting options are build and shown as separate sub-sections in 'Forecast' / 'Tricasts' section
        """
        pass
