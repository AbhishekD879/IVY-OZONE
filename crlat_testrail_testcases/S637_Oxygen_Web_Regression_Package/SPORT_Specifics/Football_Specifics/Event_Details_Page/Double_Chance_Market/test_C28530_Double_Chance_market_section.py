import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28530_Double_Chance_market_section(Common):
    """
    TR_ID: C28530
    NAME: Double Chance market section
    DESCRIPTION: This test case verifies Double Chance market section.
    DESCRIPTION: AUTOTEST Mobile: [C2745939]
    DESCRIPTION: AUTOTEST Desktop: [C2745946]
    PRECONDITIONS: Football events with Double Chance markets (name="Double Chance", name="First-Half Double Chance, name="Second-Half Double Chance")
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half-Time Double Chance"
    PRECONDITIONS: *   PROD: name="1st Half Double Chance"
    """
    keep_browser_open = True

    def test_001_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully
        """
        pass

    def test_002_go_to_double_chance_market_section(self):
        """
        DESCRIPTION: Go to 'Double Chance' market section
        EXPECTED: *   Section is present on Event Details Page and titled 'Double Chance'
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_003_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of Double Chance markets (Double Chance, Half-Time Double Chance, Second-Half Double Chance) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_004_expand_double_chance_market_section(self):
        """
        DESCRIPTION: Expand 'Double Chance' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Three buttons: '90 mins' (selected by default), '1st Half', '2nd Half'
        EXPECTED: *   <Home Team or Draw>, <Away Team or Draw>, <Home Team or Away Team> selections with corresponding price/odds buttons
        """
        pass

    def test_005_verify_double_chancemarket_shown_for_90_mins(self):
        """
        DESCRIPTION: Verify Double Chance market shown for '90 mins'
        EXPECTED: *   Only market with attribute **name="Double Chance" **is present
        EXPECTED: *   If market/outcomes within market are absent - nothing is shown within selected option
        """
        pass

    def test_006_verify_double_chancemarket_shown_for_1st_half(self):
        """
        DESCRIPTION: Verify Double Chance market shown for '1st Half'
        EXPECTED: *   Only market with attribute **name="First-Half Double Chance"/ "Half-Time Double Chance"**is present
        EXPECTED: *   If market/outcomes within market are absent - nothing is shown within selected option
        """
        pass

    def test_007_verify_double_chance_market_shown_for_2nd_half(self):
        """
        DESCRIPTION: Verify Double Chance market shown for '2nd Half'
        EXPECTED: *   Only market with attribute **name="Second-Half Double Chance" **is present
        EXPECTED: *   If market/outcomes within market are absent - nothing is shown within selected option
        """
        pass

    def test_008_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   selection is shown first - outcome with attribute **outcomeMeaningMinorCode="1"**
        EXPECTED: *   selection is shown second - outcome with attribute **outcomeMeaningMinorCode="2"**
        EXPECTED: *   selection is shown third - outcome with attribute **outcomeMeaningMinorCode="3"**
        """
        pass
