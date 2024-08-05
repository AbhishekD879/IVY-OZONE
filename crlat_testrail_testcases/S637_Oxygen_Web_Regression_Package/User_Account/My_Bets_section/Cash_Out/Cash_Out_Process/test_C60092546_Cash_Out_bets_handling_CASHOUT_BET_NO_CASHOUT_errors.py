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
class Test_C60092546_Cash_Out_bets_handling_CASHOUT_BET_NO_CASHOUT_errors(Common):
    """
    TR_ID: C60092546
    NAME: Cash Out bets handling CASHOUT_BET_NO_CASHOUT errors
    DESCRIPTION: This case verifies Cash Out bets handling receiving CASHOUT_BET_NO_CASHOUT errors
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed Single and Multiple bets with available cash out
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: CASHOUT_BET_NO_CASHOUT - This update can be triggered by resulting one of selection to L (Lose) and confirming it
    """
    keep_browser_open = True

    def test_001_open_my_bets_pagesection__cash_out_or_open_bets_tab(self):
        """
        DESCRIPTION: Open My Bets page/section > 'Cash Out' or 'Open Bets' tab
        EXPECTED: Single and Multiple bets with available cash out are present in selected tab
        """
        pass

    def test_002_single_bet_for_any_of_present_single_bet_events_trigger_cashout_bet_no_cashout_error_check_preconditions_observe_ui(self):
        """
        DESCRIPTION: **[Single bet]**
        DESCRIPTION: * For any of present single bet events trigger CASHOUT_BET_NO_CASHOUT error (check Preconditions)
        DESCRIPTION: * Observe UI
        EXPECTED: Cashout button is hidden from event on selected My Bets tab
        """
        pass

    def test_003__check_messages_in_current_cashout_ws_connectionindexphpattachmentsget122292771(self):
        """
        DESCRIPTION: * Check messages in current CashOut WS connection
        DESCRIPTION: ![](index.php?/attachments/get/122292771)
        EXPECTED: * betUpdate with cashoutStatus CASHOUT_BET_NO_CASHOUT is received
        """
        pass

    def test_004__send_any_cash_out_updates_for_the_selected_event_eg_price_updates_check_ui_and_current_cashout_ws_connection(self):
        """
        DESCRIPTION: * Send any Cash Out updates for the selected event (e.g. price updates)
        DESCRIPTION: * Check UI and current CashOut WS connection
        EXPECTED: * No changes on UI
        EXPECTED: * Any further updates from websocket (like cashout value updates) are ignored
        """
        pass

    def test_005_repeat_steps_1_4_for_multiples_bet(self):
        """
        DESCRIPTION: Repeat steps 1-4 for **Multiples** bet
        EXPECTED: Result is the same
        """
        pass

    def test_006_coral_only_navigate_to_edp_of_the_event_with_available_placed_bet_and_cash_out_open_my_bets_tab_on_edp(self):
        """
        DESCRIPTION: **[Coral only]**
        DESCRIPTION: * Navigate to EDP of the event with available placed bet and cash out
        DESCRIPTION: * Open 'My bets' tab on EDP
        EXPECTED: * EDP My Bets tab is displayed with placed bets including this event
        EXPECTED: * Cash Out is available for any present bet
        """
        pass

    def test_007_repeat_steps_1_4_for_my_bets_edp_page(self):
        """
        DESCRIPTION: Repeat steps 1-4 for **My Bets (EDP)** page
        EXPECTED: Result is the same
        """
        pass
