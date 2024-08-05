import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.bet_history_open_bets
@vtest
class Test_C49498686_Verify_that_no_SS_calls_for_resulted_events_are_executed_on_Open_Bets_Settled_Bets_(Common):
    """
    TR_ID: C49498686
    NAME: Verify that no SS calls for resulted events are executed on 'Open Bets'/'Settled Bets '
    DESCRIPTION: Verify that no SS calls for resulted events are executed on 'Open Bets'/'Settled Bets'
    PRECONDITIONS: 1. Load app
    PRECONDITIONS: 2. Log in with user that has Open Bets/Settled Bets with resulted bets (Race, Sport, Virtuals, Forecast/Tricast, Tote)
    PRECONDITIONS: 3. Open Dev Tools -> XHR filter -> filter all request to SS
    PRECONDITIONS: 4. Try to find the next request:
    PRECONDITIONS: https://{domain}/openbet-ssviewer/HistoricDrilldown/X.XX/ResultedEvent/{eventID}
    PRECONDITIONS: where,
    PRECONDITIONS: domain - valid domain URL
    PRECONDITIONS: X.XX - the latest version of OB
    PRECONDITIONS: eventID - id of event that user has placed the bet
    PRECONDITIONS: e.g https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/HistoricDrilldown/2.31/ResultedEvent/229739237
    """
    keep_browser_open = True

    def test_001_go_to_open_bets_tabpage(self):
        """
        DESCRIPTION: Go to 'Open Bets' tab/page
        EXPECTED: The 'Open Bets' tab/page is opened
        """
        pass

    def test_002_check_all_request_to_ss(self):
        """
        DESCRIPTION: Check all request to SS
        EXPECTED: * List of all open bets are displayed
        EXPECTED: * Multiple requests for **ResultedEvent** are NOT sent
        """
        pass

    def test_003_tap_settled_bets_tab(self):
        """
        DESCRIPTION: Tap 'Settled Bets' tab
        EXPECTED: The 'Settled Bets' tab is opened
        """
        pass

    def test_004_check_all_request_to_ss(self):
        """
        DESCRIPTION: Check all request to SS
        EXPECTED: * List of all settled bets are displayed
        EXPECTED: * Multiple requests for **ResultedEvent** are NOT sent
        """
        pass

    def test_005_select_history_for_settled_bet_for_1_month_3_monthsvia_date_picker_ui_element(self):
        """
        DESCRIPTION: Select history for settled bet for
        DESCRIPTION: * 1 month
        DESCRIPTION: * 3 months
        DESCRIPTION: via 'date picker' UI element
        EXPECTED: 
        """
        pass

    def test_006_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass
