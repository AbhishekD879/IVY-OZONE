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
class Test_C147946_Multiple_Cash_Out_bet_lines_without_errors(Common):
    """
    TR_ID: C147946
    NAME: Multiple Cash Out bet lines without errors
    DESCRIPTION: This test case verifies multiple bet lines without errors on 'My bets' tab on Event Details page when the user is logged in
    DESCRIPTION: *Jira Tickets:*
    DESCRIPTION: [BMA-24370 My Bets Improvement : Cashout redesign main bet details area and Remove accordions header changes] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24370
    DESCRIPTION: **Autotest:**
    DESCRIPTION: Mobile - [C9698014](https://ladbrokescoral.testrail.com/index.php?/cases/view/9698014)
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed multiple bets on Pre Match or In-Play football, tennis, basketball events, special events and on events with eventSortCode not a match (e.g.  outright) with and without Cash Out offer available
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
        EXPECTED: * Bet Section content with Cash Out bet lines details
        """
        pass

    def test_004_verify_bet_section_header(self):
        """
        DESCRIPTION: Verify Bet Section header
        EXPECTED: * Bet Type is shown on each Bet Section header
        EXPECTED: * 'Each/Way' label (if available) is displayed next to bet type in brackets
        """
        pass

    def test_005_verify_bet_section_content__for_multiple_bet(self):
        """
        DESCRIPTION: Verify Bet Section content  for **Multiple** bet
        EXPECTED: - The first leg of multiple bet is fully displayed with the following elements:
        EXPECTED: *  Badge with status of bet is displayed on the right side under Odds value (for resulted selections only).
        EXPECTED: *  Selection Name is displayed at the top of Bet Section
        EXPECTED: *  **FOR** **Release** **99** Odds with the relevant price of the selection is displayed on the same line with the Selection Name next to it (Odds should be shown in such format @1/2)
        EXPECTED: **FOR** **Release** **98** Odds with the relevant price of the selection is displayed on the same line with the Selection Name but right aligned
        EXPECTED: *  Market Name and Each Way terms (if available) are  displayed under Selection Name
        EXPECTED: *  Event Name is displayed under Market Name
        EXPECTED: *  Match Start Time/Match Date/'LIVE' badge/Match Clock/HT/nth Set/FT/Finished labels / "Watch live" icon (if available) can be displayed next to Event Name
        EXPECTED: *  **For** **Release** **99** Live Scores (if available) are displayed on the same line as (next to) Match Start Time/Match Date/Match Clock/HT/FT/Finished labels
        EXPECTED: **For** **Release** **98** Live Scores (if available) are displayed on the same line as (next to) Match Start Time/Match Date/'LIVE' badge/Match Clock/HT/FT/Finished labels
        EXPECTED: *  Clickable navigation dots are displayed centered under the in-play clock/current set/time/date. Number of dots corresponds to number of legs. Dot that corresponds to the leg that is currently on view highlighted with a different color (e.g. for the first leg in multiple bet first dot is highlighted)
        EXPECTED: *  Divider is displayed below
        EXPECTED: * On the right side of first default leg, the next leg is displayed slightly
        EXPECTED: * 'Unit Stake' label with the relevant currency symbol, the monetary value is displayed under CASH OUT button on gray line (below divider) (e.g. Unit Stake £1.00)
        EXPECTED: * 'Total Stake' label with the relevant currency symbol and the monetary value is displayed below 'Unit Stake' label (e.g. Total Stake £1.00), where stake uses x,xxx,xxx.xx format
        EXPECTED: * 'Est. Returns' label and the relevant currency symbol and amount are displayed on the same line as Stake (e.g. Est. Returns £1.00), where amount uses x,xxx,xxx.xx format
        EXPECTED: * Button with label "CASH OUT: <currency symbol><amount>" is displayed under line with 'Stake' and 'Est. Returns'. Text of label is centered within the button (on area without "PARTIAL CASHOUT" section)
        EXPECTED: * Button with label "PARTIAL CASHOUT" is displayed under line with 'Stake' and 'Est. Returns'. Text of label is centered within the button
        EXPECTED: * Slider for selecting the sum of partial cashout is displayed instead of Cash Out button after clicking on 'PARTIAL CASHOUT' button. By default for each bet the slider is at 50%. The sum which equals to 10% of the full cahout is the lowest point for the slider. Highest point is full cashout value
        """
        pass

    def test_006_verify_unit_stake_and_total_stake_values_correctness(self):
        """
        DESCRIPTION: Verify 'Unit Stake' and 'Total Stake' values correctness
        EXPECTED: 'Unit Stake' and 'Total Stake' values correspond to **respTransGetBetDetails.bets.[i].stakePerLine** and **respTransGetBetDetails.bets.[i].stake** attibutes accordingly from **getbetdetail(s)** response,
        EXPECTED: where [i] - number of cash out bets available
        EXPECTED: **NOTE** that 'Unit Stake' value s displayed ONLY when **legType="E"** is present in **getbetdetail(s)** response
        """
        pass

    def test_007_verify_each_way_terms_if_available(self):
        """
        DESCRIPTION: Verify Each Way terms (if available)
        EXPECTED: * Each way terms are displayed if **'isEachWayAvailable' = 'true'** attribute is present in response
        EXPECTED: * Terms correspond to the **'eachWayFactorNum'**, **'eachWayFactorDen'** and **'eachWayPlaces'** attributes from response
        EXPECTED: * Terms are displayed in the following format:
        EXPECTED: "x/y odds - places z,j,k"
        EXPECTED: where:
        EXPECTED: * x = eachWayFactorNum
        EXPECTED: * y= eachWayFactorDen
        EXPECTED: * z,j,k = eachWayPlaces
        """
        pass

    def test_008_verify_line_with_too_long_selection_name(self):
        """
        DESCRIPTION: Verify line with too long Selection Name
        EXPECTED: * Selection Name is truncated with 3 dots if it is too long to be shown in one line with Odds
        EXPECTED: * After the truncation some space is present between Selection Name and Odds
        """
        pass

    def test_009_verify_line_with_too_long_market_name(self):
        """
        DESCRIPTION: Verify line with too long Market Name
        EXPECTED: Market Name is truncated with 3 dots if it is too long to be shown in one line
        """
        pass

    def test_010_verify_event_name_for_event_with_eventsortcode__match(self):
        """
        DESCRIPTION: Verify Event Name for event with **eventSortCode = match**
        EXPECTED: * One player/team name is displayed on top of the other
        EXPECTED: * Event Name is truncated with 3 dots if it is too long to be shown in one line
        """
        pass

    def test_011_verify_event_name_for_event_with_eventsortcode_not_a_match_or_a_special_for_any_sport_ss_response_drilldowntagname_attribute_at_the_event_level_with_a_value_of_evflag_sp(self):
        """
        DESCRIPTION: Verify Event Name for event with eventSortCode not a match, or a special for any sport (SS response: drilldownTagName attribute at the event level with a value of EVFLAG_SP)
        EXPECTED: * Event name is displayed on one line by default
        EXPECTED: * If Event name is too long it should go on two lines
        EXPECTED: * If Event name is too long to display on two lines then the name is truncated at the end of the second line
        """
        pass

    def test_012_click_by_event_name(self):
        """
        DESCRIPTION: Click by Event Name
        EXPECTED: Event Details page is opened for corresponding event from Multiple bet
        """
        pass

    def test_013_verify_multiple_bet(self):
        """
        DESCRIPTION: Verify Multiple bet
        EXPECTED: * Each leg in the multiple bet is listed one below each other
        EXPECTED: * Width of preview pane for each leg is equal to width of 'My Bets' page/'Bet Slip' widget
        EXPECTED: * 'Unit Stake', 'Total Stake' and 'Est. Returns' with the relevant currency symbol and amount, Cash Out/Partial CashOut buttons  are displayed underneath the last leg of multiple bet
        EXPECTED: * Preview pane for the next legs is not displayed on the right side of each leg
        """
        pass

    def test_014_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_bets_without_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets without available cash out
        EXPECTED: 
        """
        pass

    def test_015_repeat_steps_2_17(self):
        """
        DESCRIPTION: Repeat steps #2-17
        EXPECTED: * Results are the same
        EXPECTED: * In step #5 Cash Out and Partial CashOut buttons are not displayed under line with 'Stake' and 'Est. Returns'.
        """
        pass
