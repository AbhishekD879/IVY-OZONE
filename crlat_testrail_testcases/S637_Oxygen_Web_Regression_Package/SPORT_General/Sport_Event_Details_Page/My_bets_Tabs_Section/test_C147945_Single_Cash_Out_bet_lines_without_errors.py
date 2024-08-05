import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C147945_Single_Cash_Out_bet_lines_without_errors(Common):
    """
    TR_ID: C147945
    NAME: Single Cash Out bet lines without errors
    DESCRIPTION: This test case verifies single bet lines without errors on 'My bets' tab on Event Details page when the user is logged in.
    DESCRIPTION: *Jira Tickets*
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    DESCRIPTION: AUTOTEST [C1992430]
    DESCRIPTION: AUTOTEST [C2000370]
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed single bets on Pre Match or In-Play football, tennis, basketball events, special events and on events with eventSortCode not a match (e.g. tournament or outright) with and without Cash Out offer available
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: where
    PRECONDITIONS: X.XX - current OpenBet version;
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: NOTE: Sport icons are configured in CMS (Sport Categories -> <Sport Category> -> SVG Icon)
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets with available cash out
        EXPECTED: 
        """
        pass

    def test_002_verify_my_bets_tab(self):
        """
        DESCRIPTION: Verify 'My bets' tab
        EXPECTED: Bet sections are displayed for each bet
        """
        pass

    def test_003_verify_bet_section(self):
        """
        DESCRIPTION: Verify bet section
        EXPECTED: Separate section for each bet is present and includes following:
        EXPECTED: * Bet Section header
        EXPECTED: * Bet Section content with bet lines details
        """
        pass

    def test_004_verify_bet_section_header(self):
        """
        DESCRIPTION: Verify Bet Section header
        EXPECTED: * Bet Type is shown on each Bet Section header
        """
        pass

    def test_005_verify_bet_section_content__for_single__bet_with_available_cash_out(self):
        """
        DESCRIPTION: Verify Bet Section content  for **Single ** bet with available cash out
        EXPECTED: Single bet is displayed with the following information:
        EXPECTED: *   Badge with status of bet is displayed on the right side under Odds value (for resulted selections only).
        EXPECTED: *   Selection Name is displayed at the top of Bet Section
        EXPECTED: *   **FOR** **Release** **99** Odds with the relevant price of the selection is displayed on the same line with the Selection Name next to it (Odds should be shown in such format @1/2)
        EXPECTED: **FOR** **Release** **98** Odds with the relevant price of the selection is displayed on the same line with the Selection Name but right aligned
        EXPECTED: *   Market Name is displayed under Selection Name
        EXPECTED: *   Event Name is displayed under Market Name
        EXPECTED: *   Match Start Time/Match Date/'LIVE' badge/Match Clock/HT/FT/Finished labels /"Watch live" icon (if available) can be displayed next to Event Name
        EXPECTED: *   **For** **Release** **99** Live Scores (if available) are displayed on the same line as (next to) Match Start Time/Match Date/Match Clock/HT/FT/Finished labels
        EXPECTED: **For** **Release** **98** Live Scores (if available) are displayed on the same line as (next to) Match Start Time/Match Date/'LIVE' badge/Match Clock/HT/FT/Finished labels
        EXPECTED: *   Divider is displayed below
        EXPECTED: *   'Stake' label with the relevant currency symbol, the monetary value is displayed under CAS OUT button on gray line (below divider) (e.g. Unit Stake £1.00)
        EXPECTED: *   'Est. Returns' label and the relevant currency symbol and amount are displayed on the same line as Stake (e.g. Est. Returns £1.00), where amount uses x,xxx,xxx.xx format
        EXPECTED: *   Button with label "CASH OUT: <currency symbol><amount>" is displayed under line with 'Stake' and 'Est. Returns'. Text of label is centered within the button (on area without "PARTIAL CASHOUT" section)
        EXPECTED: *   Button with label "PARTIAL CASHOUT" is displayed under line with 'Stake' and 'Est. Returns'. Text of label is centered within the button
        EXPECTED: *   Slider for selecting the sum of partial cashout ' is displayed instead of Cash Out button after clicking on 'PARTIAL CASHOUT' button. By default for each bet the slider is at 50%. The sum which equals to 10%  of the full cahout is the lowest point for the slider. Highest point is full cashout value
        """
        pass

    def test_006_verify_line_with_too_long_selection_name(self):
        """
        DESCRIPTION: Verify line with too long Selection Name
        EXPECTED: * Long name of a selection is fully displayed
        EXPECTED: * After the name some space is present between Selection Name and Odds
        """
        pass

    def test_007_verify_line_with_too_long_market_name(self):
        """
        DESCRIPTION: Verify line with too long Market Name
        EXPECTED: Market Name is wrapped to the next line if it is too long to be shown in one line
        """
        pass

    def test_008_verify_event_name_for_event_with_eventsortcode__match(self):
        """
        DESCRIPTION: Verify Event Name for event with **eventSortCode = match**
        EXPECTED: * One player/team name is displayed on top of the other
        EXPECTED: * Event Name is wrapped to the next line if it is too long to be shown in one line
        """
        pass

    def test_009_clicktap_event_name(self):
        """
        DESCRIPTION: Click/Tap Event Name
        EXPECTED: Event Name is NOT clickable
        """
        pass

    def test_010_verify_event_name_for_event_with_eventsortcode_not_a_match_or_a_special_for_any_sport_ss_response_drilldowntagname_attribute_at_the_event_level_with_a_value_of_evflag_sp(self):
        """
        DESCRIPTION: Verify Event Name for event with eventSortCode not a match, or a special for any sport (SS response: drilldownTagName attribute at the event level with a value of EVFLAG_SP)
        EXPECTED: * Event name is displayed on one line by default
        EXPECTED: * If Event name is too long it should be wrapped to the next line
        """
        pass

    def test_011_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_without_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets without available cash out
        EXPECTED: 
        """
        pass

    def test_012_repeat_steps_2_8(self):
        """
        DESCRIPTION: Repeat steps #2-8
        EXPECTED: * Results are the same
        EXPECTED: * In step #5 Cash Out and Partial CashOut buttons are not shown under line with 'Stake' and 'Est. Returns'
        """
        pass
