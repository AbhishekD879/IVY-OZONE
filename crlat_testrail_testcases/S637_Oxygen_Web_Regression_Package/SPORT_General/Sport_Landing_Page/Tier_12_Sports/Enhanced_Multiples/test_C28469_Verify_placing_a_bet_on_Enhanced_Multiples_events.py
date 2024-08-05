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
class Test_C28469_Verify_placing_a_bet_on_Enhanced_Multiples_events(Common):
    """
    TR_ID: C28469
    NAME: Verify placing a bet on Enhanced Multiples events
    DESCRIPTION: This test case verifies placing a bet on Enhanced Multiples events.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: **NOTE: Make sure you have  Enhanced Multiples events on Some sports (Sport events with typeName="Enhanced Multiples").**
    PRECONDITIONS: 1) http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) User is logged in
    """
    keep_browser_open = True

    def test_001_navigate_to_any_sports_page_where_enhanced_multiples_events_are_present(self):
        """
        DESCRIPTION: Navigate to any <Sports> page where Enhanced Multiples events are present
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_002_go_to_em_outcome_section(self):
        """
        DESCRIPTION: Go to EM Outcome section
        EXPECTED: 
        """
        pass

    def test_003_selectunselect_the_same_priceodds_button(self):
        """
        DESCRIPTION: Select/unselect the same Price/Odds button
        EXPECTED: Button is highlighted/unhighlighted respectively
        """
        pass

    def test_004_add_single_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single selection to bet slip
        EXPECTED: Bet indicator displays 1.
        """
        pass

    def test_005_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: The bet is present
        """
        pass

    def test_006_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event start time and event name (**'startTime'** and event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        pass

    def test_007_add_amount_to_bet_using_stake_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Estimated Returns**
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Total Est. Returns**
        """
        pass

    def test_008_clicktapbet_now_button(self):
        """
        DESCRIPTION: Click/Tap **'Bet Now**' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Confirmation message is shown
        EXPECTED: *   User's balance is decremented by entered stake
        """
        pass

    def test_009_clicktap_enhanced_multiples_tab_from_module_selector_ribbon_on_the_homepage(self):
        """
        DESCRIPTION: Click/Tap 'Enhanced Multiples' tab from Module Selector Ribbon on the Homepage
        EXPECTED: **For mobile/tablet:**
        EXPECTED: *   'Enhanced Multiples' tab is opened
        EXPECTED: *   All sections are collapsed by default
        EXPECTED: **For desktop:**
        EXPECTED: 'Enhanced Multiples' are displayed in carousel below banner area
        """
        pass

    def test_010_repeat_steps_3_9(self):
        """
        DESCRIPTION: Repeat steps 3-9
        EXPECTED: 
        """
        pass

    def test_011_for_desktoprepeat_steps_3_9_on_sports_event_details_page_but_only_for_pre_match_events(self):
        """
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Repeat steps 3-9 on <Sports> Event Details Page but only for Pre-match events
        EXPECTED: 
        """
        pass
