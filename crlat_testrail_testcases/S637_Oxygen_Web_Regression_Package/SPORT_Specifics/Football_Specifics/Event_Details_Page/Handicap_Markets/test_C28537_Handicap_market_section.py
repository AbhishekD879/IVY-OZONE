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
class Test_C28537_Handicap_market_section(Common):
    """
    TR_ID: C28537
    NAME: Handicap market section
    DESCRIPTION: This test case verifies Handicap market section
    DESCRIPTION: Test case needs to be run on Mobile/Tablet/Desktop.
    DESCRIPTION: AUTOTEST [C647554]
    PRECONDITIONS: Football events with Handicap markets (name="Handicap Match Result", name="Handicap First Half", name="Handicap Second Half")
    PRECONDITIONS: To retrieve markets and outcomes for event use:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. EN)
    PRECONDITIONS: Jira ticket: BMA-3900
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_navigate_to_footballlanding_page(self):
        """
        DESCRIPTION: Navigate to Football Landing Page
        EXPECTED: Football Landing Page is opened
        """
        pass

    def test_003_select_football_event_with_handicap_markets_available(self):
        """
        DESCRIPTION: Select Football event with Handicap Markets available
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_tapclick_on_all_markets_tab(self):
        """
        DESCRIPTION: Tap/click on 'All markets' tab
        EXPECTED: All available markets are shown
        """
        pass

    def test_005_find_handicap_results_section(self):
        """
        DESCRIPTION: Find 'Handicap Results' section
        EXPECTED: *   Section is present on Event Details Page and titled 'Handicap Results'
        EXPECTED: *   It is possible to collapse/expand section
        """
        pass

    def test_006_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If one of Handicap markets (Handicap Match Result, Handicap First Half, Handicap Second Half) has cashoutAvail="Y" then label Cash out should be displayed next to market section name
        """
        pass

    def test_007_expand_handicap_results_market_section(self):
        """
        DESCRIPTION: Expand 'Handicap Results' market section
        EXPECTED: Section consists of:
        EXPECTED: *   Three filters: '90 mins' (selected by default), '1st Half', '2nd Half'
        EXPECTED: *   <Home Team>, <Tie>, <Away Team> selections with corresponding price/odds buttons
        EXPECTED: *   First four Handicap markets are shown (sorted from highest to lowest  e.g.+2 +1 -1 -2 in columns).
        EXPECTED: *   'Show All' button is present (if more than 4 markets available)
        """
        pass

    def test_008_verify_handicap_markets_for_90_mins(self):
        """
        DESCRIPTION: Verify Handicap Markets for '90 mins'
        EXPECTED: *   Only markets which name attribute contains **name="Handicap**** Match Result" **value should be shown
        EXPECTED: *   If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        pass

    def test_009_tap_show_all_button(self):
        """
        DESCRIPTION: Tap 'Show all' button
        EXPECTED: *   All available '90 mins' Handicap Markets are displayed (sorted from highest to lowest e.g.+5, +4, +3, +2, +1, -1, -2, -3, -4, -5)
        EXPECTED: *   Button name is changed to 'Show Less'
        """
        pass

    def test_010_verify_market_header(self):
        """
        DESCRIPTION: Verify market header
        EXPECTED: The elements:
        EXPECTED: *   market header
        EXPECTED: *   filters '90 mins', '1st Half' and '2nd Half'
        """
        pass

    def test_011_tap_show_less_button(self):
        """
        DESCRIPTION: Tap 'Show less' button
        EXPECTED: *   First four Handicap Markets are shown (sorted from highest to lowest  e.g.+2 +1 -1 -2)
        EXPECTED: *   Button name is changed to 'Show All'
        """
        pass

    def test_012_verify_selections_displaying_for_markets(self):
        """
        DESCRIPTION: Verify selections displaying for markets
        EXPECTED: *   selection is shown first (on the left side) - outcome with attribute **outcomeMeaningMinorCode="H"**
        EXPECTED: *   selection is shown second (in the middle) - outcome with attribute **outcomeMeaningMinorCode="L"**
        EXPECTED: *   selection is shown third (on the right side) - outcome with attribute **outcomeMeaningMinorCode="A"**
        """
        pass

    def test_013_verify_handicap_markets_for_1st_half(self):
        """
        DESCRIPTION: Verify Handicap Markets for '1st Half'
        EXPECTED: 1. First four Handicap markets are shown (sorted from highest to lowest  e.g.+2 +1 -1 -2)
        EXPECTED: 2. Only markets which name attribute contains **name="Handicap**** First Half"** value should be shown
        EXPECTED: 3. If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        pass

    def test_014_repeat_steps_9_13(self):
        """
        DESCRIPTION: Repeat steps 9-13
        EXPECTED: 
        """
        pass

    def test_015_tap_2nd_half_filter(self):
        """
        DESCRIPTION: Tap '2nd Half' filter
        EXPECTED: 1. First four Handicap markets are shown (sorted from highest to lowest  e.g.+2 +1 -1 -2)
        EXPECTED: 2. Only markets which name attribute contains **name="****Handicap**** Second Half"** value should be shown
        EXPECTED: 3. If markets/outcomes within markets are absent - nothing is shown within selected option
        """
        pass

    def test_016_repeat_steps_9_13(self):
        """
        DESCRIPTION: Repeat steps 9-13
        EXPECTED: 
        """
        pass

    def test_017_check_handicap_markest_in_all_collections_all_markets_main_markets_handicap_markets(self):
        """
        DESCRIPTION: Check handicap markest in all collections: All Markets, Main Markets, Handicap Markets
        EXPECTED: View is the same for 90 mins, 1st Half and 2nd Half in all collections
        """
        pass

    def test_018_verify_handicap_results_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Handicap Results' section in case of data absence
        EXPECTED: 'Handicap Results' section is not shown if:
        EXPECTED: *   all markets that section consists of are absent
        EXPECTED: *   all markets that section consists of do not have any outcomes
        """
        pass
