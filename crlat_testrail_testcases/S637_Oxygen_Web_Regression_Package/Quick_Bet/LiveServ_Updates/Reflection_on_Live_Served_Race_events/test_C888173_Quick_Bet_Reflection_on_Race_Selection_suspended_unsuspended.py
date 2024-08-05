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
class Test_C888173_Quick_Bet_Reflection_on_Race_Selection_suspended_unsuspended(Common):
    """
    TR_ID: C888173
    NAME: Quick Bet Reflection on <Race> Selection suspended/unsuspended
    DESCRIPTION: This test case verifies Quick Bet reflection when <Race> selection is Suspended/Unsuspended.
    DESCRIPTION: AUTOTEST [C2011227]
    PRECONDITIONS: 1. To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: - Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: - LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Race> Event should be LiveServed:
    PRECONDITIONS: - Event should not be **Live** ( **isStarted - absent)**
    PRECONDITIONS: 3.  Event, Market, Outcome should be **Active** ( **eventStatusCode="A", marketStatusCode="A", outcomeStatusCode="A")**
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_race_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports ribbon
        EXPECTED: <Race> Landing page is opened
        """
        pass

    def test_003_go_to_today_tab(self):
        """
        DESCRIPTION: Go to 'Today' tab
        EXPECTED: Events for current day are displayed
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
        DESCRIPTION: Suspend selection in Backoffice tool. Trigger the following situation for this selection:
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
        EXPECTED: - Stake box, E/W option & Price(dropdown) are disabled
        EXPECTED: - 'LOGIN & PLACE BET' button and 'Add to Betslip' button are disabled
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
        EXPECTED: - Stake box, E/W option & Price(dropdown) are enabled
        EXPECTED: - 'LOGIN & PLACE BET' button and 'Add to Betslip' button are enabled
        """
        pass
