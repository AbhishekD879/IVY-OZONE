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
class Test_C28563_1st_Half__2nd_Half_Result_market_section(Common):
    """
    TR_ID: C28563
    NAME: 1st Half / 2nd Half Result market section
    DESCRIPTION: This test case verifies '1st Half / 2nd Half Result' market section on Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with 1st Half / 2nd Half Result markets (name="First-Half Result", name="Second-Half Result")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First-Half Result"
    PRECONDITIONS: *   PROD: name="1st Half Result"
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        pass

    def test_003_go_to_1st_half__2nd_half_result_market_section(self):
        """
        DESCRIPTION: Go to '1st Half / 2nd Half Result' market section
        EXPECTED: *   Section is present on Event Details Page and titled ‘1st Half / 2nd Half Result’
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_004_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of markets (First-Half Result, Second-Half Result) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_005_expand_1st_half__2nd_half_result_market_section(self):
        """
        DESCRIPTION: Expand '1st Half / 2nd Half Result' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Two filters: '1st Half Result' (selected by default), '2nd Half Result'
        EXPECTED: *   &lt;Home Team&gt;, &lt;Draw&gt;, &lt;Away Team&gt; selections with corresponding price/odds buttons
        """
        pass

    def test_006_verify_market_shown_for_1st_half_result(self):
        """
        DESCRIPTION: Verify market shown for '1st Half Result'
        EXPECTED: *   Only market with attribute **name="First-Half Result" **is present
        """
        pass

    def test_007_verify_market_shown_for_2nd_half_result(self):
        """
        DESCRIPTION: Verify market shown for '2nd Half Result'
        EXPECTED: *   Only market with attribute **name="Second-Half Result" **is present
        """
        pass

    def test_008_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   &lt;Home team&gt; selection is shown first (on the left side) - outcome with attribute **outcomeMeaningMinorCode="H"**
        EXPECTED: *   &lt;Draw&gt; selection is shown second (in the middle) - outcome with attribute **outcomeMeaningMinorCode="D"**
        EXPECTED: *   &lt;Away team&gt; selection is shown third (on the right side) - outcome with attribute **outcomeMeaningMinorCode="A"**
        """
        pass
