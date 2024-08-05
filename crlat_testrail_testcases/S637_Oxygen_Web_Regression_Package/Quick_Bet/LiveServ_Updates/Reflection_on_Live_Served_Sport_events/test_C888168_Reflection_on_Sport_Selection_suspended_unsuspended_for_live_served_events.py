import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C888168_Reflection_on_Sport_Selection_suspended_unsuspended_for_live_served_events(Common):
    """
    TR_ID: C888168
    NAME: Reflection on <Sport> Selection suspended/unsuspended for live served events
    DESCRIPTION: This test case verifies Quick Bet reflection when <Sport> Selection is Suspended/Unsuspended.
    DESCRIPTION: Note: TEST2 environment does not support LiveServer. Therefore to get price changes this should be triggered manually, and only for one event/market/outcome at a time. LIVE environment support LiveServ updates.
    PRECONDITIONS: 1. To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: - Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: - XXXXXXX - event id
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Sport> Event should be LiveServed:
    PRECONDITIONS: - Event should be **Live (isStarted=true)**
    PRECONDITIONS: - Event should be **in-Pla**y:
    PRECONDITIONS: - drilldown****TagNames=EVFLAG_BL
    PRECONDITIONS: - **isMarketBetInRun=true**
    PRECONDITIONS: - rawIsOffCode="Y "or isStarted=true, rawIsOffCode="-"
    PRECONDITIONS: 3. Event, Market, Outcome should be **Active** ( **eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    PRECONDITIONS: This test case is applied only for **Mobile application**.
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_go_to_the_in_play_tab(self):
        """
        DESCRIPTION: Go to the 'In-Play' tab
        EXPECTED: 'In-Play' page with list of events is opened
        """
        pass

    def test_004_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_005_make_single_selection(self):
        """
        DESCRIPTION: Make single selection
        EXPECTED: Quick Bet is opened with selection added
        """
        pass

    def test_006_suspend_selection_in_backoffice_tool_trigger_the_following_situation_for_this_selectionselectionstatuscode_seventstatuscode_amarketstatuscode_a(self):
        """
        DESCRIPTION: Suspend Selection in Backoffice tool. Trigger the following situation for this selection:
        DESCRIPTION: selectionStatusCode= **"S"**
        DESCRIPTION: eventStatusCode= **"A"**
        DESCRIPTION: marketStatusCode= **"A"**
        EXPECTED: 
        """
        pass

    def test_007_check_update_in_quick_bet(self):
        """
        DESCRIPTION: Check update in Quick Bet
        EXPECTED: * 'Your Selection has been Suspended' warning message is displayed on yellow(Coral)/cyan(Ladbrokes) background below 'QUICK BET' header
        EXPECTED: - Stake field becomes disabled
        EXPECTED: - 'LOGIN & PLACE BET' and 'Add to Betslip' buttons are disabled
        """
        pass

    def test_008_unsuspend_selection_in_backoffice_tool_trigger_the_following_situation_for_this_selectionselectionstatuscode_aeventstatuscode_amarketstatuscode_a(self):
        """
        DESCRIPTION: Unsuspend selection in Backoffice tool. Trigger the following situation for this selection:
        DESCRIPTION: selectionStatusCode= **"A"**
        DESCRIPTION: eventStatusCode= **"A"**
        DESCRIPTION: marketStatusCode= **"A"**
        EXPECTED: 
        """
        pass

    def test_009_check_update_in_quick_bet(self):
        """
        DESCRIPTION: Check update in Quick Bet
        EXPECTED: - Message is removed
        EXPECTED: - Stake field becomes enabled
        EXPECTED: - 'LOGIN & PLACE BET' and 'Add to Betslip' buttons are enabled
        """
        pass
