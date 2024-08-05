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
class Test_C28560_Draw_No_Bet_market_section(Common):
    """
    TR_ID: C28560
    NAME: Draw No Bet market section
    DESCRIPTION: This test case verifies 'Draw No Bet' market section on Event Details Page
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with draw no bet markets (Draw No Bet, Half-Time Draw No Bet, Second-Half Draw No Bet)
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half-Time Draw No Bet"
    PRECONDITIONS: *   PROD: name="1st Half Draw No Bet"
    PRECONDITIONS: **Jira ticket: **BMA-4072
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_003_go_to_draw_no_bet_market_section(self):
        """
        DESCRIPTION: Go to 'Draw No Bet' market section
        EXPECTED: *   Section is present on Event Details Page and titled ‘Draw No Bet’
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_004_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of markets (Draw No Bet, Half-Time Draw No Bet, Second-Half Draw No Bet) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_005_expand_draw_no_bet_market_section(self):
        """
        DESCRIPTION: Expand 'Draw No Bet' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Three filters: '90 mins' (selected by default), '1st Half', '2nd Half'
        EXPECTED: *   <Home Team> and <Away Team> selections with corresponding price/odds buttons
        """
        pass

    def test_006_verify_market_shown_for_90_mins(self):
        """
        DESCRIPTION: Verify market shown for '90 mins'
        EXPECTED: Only market with attribute **name="Draw No Bet" **is present
        """
        pass

    def test_007_verify_market_shown_for_1st_half(self):
        """
        DESCRIPTION: Verify market shown for '1st Half'
        EXPECTED: Only market with attribute **name="Half-Time Draw No Bet" **is present
        """
        pass

    def test_008_verify_market_shown_for_2nd_half(self):
        """
        DESCRIPTION: Verify market shown for '2nd Half'
        EXPECTED: Only market with attribute **name="Second-Half Draw No Bet"** is present
        """
        pass

    def test_009_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   <Home team> selection is shown first (on the left side) - outcome with attribute **outcomeMeaningMinorCode="H"**
        EXPECTED: *   <Away team> selection is shown second (on the right side) - outcome with attribute **outcomeMeaningMinorCode="A"**
        """
        pass
