import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29074_Betslip_Reflection_on_Race_Market_Suspended_Unsuspended(Common):
    """
    TR_ID: C29074
    NAME: Betslip Reflection on <Race> Market Suspended/Unsuspended
    DESCRIPTION: This test case verifies Betslip reflection when <Race> Market is Suspended.
    DESCRIPTION: AUTOTEST [C2610563]
    PRECONDITIONS: 1. To get SiteServer info about event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. <Race> Event should be LiveServed:
    PRECONDITIONS: *   Event should not be **Live** (**isStarted - absent)**
    PRECONDITIONS: 3. Event, Market, Outcome should be **Active** (**eventStatusCode="A", ****marketStatusCode="A", ****outcomeStatusCode="A"****)**
    PRECONDITIONS: NOTE: contact UAT team for all configurations
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True

    def test_001_add_single_race_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add single <Race> selection to the Betslip
        EXPECTED: 
        """
        pass

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Added selection is displayed in the betslip
        """
        pass

    def test_003_trigger_the_following_situation_for_the_eventmarketstatuscodesfor_selected_market_typeand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for the event:
        DESCRIPTION: **marketStatusCode="S" **for selected market type
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: 1. 'Stake' field is disabled and greyed out.
        EXPECTED: 2. 'Bet Now' ('Log In and Bet') button is disabled and greyed out
        EXPECTED: 3. Error message 'Sorry, the market has been suspended' is shown on red background in the bottom of the Betslip
        EXPECTED: 3. Error message 'Please beware that 1 of your selections has been suspended' is shown on yellow background above disabled 'Bet Now' button
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass

    def test_004_trigger_the_following_situation_for_one_ofeventsmarketstatuscodeaand_at_the_same_time_have_betslip_page_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Trigger the following situation for one of events:
        DESCRIPTION: **marketStatusCode="A"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: 1. 'Stake' field and 'Bet Now' ('Log In and Bet') buttons are enabled and not greyed out.
        EXPECTED: 2. Both error messages disappear from the Betslip
        EXPECTED: **After OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended' is disappeared
        EXPECTED: Ladbrokes:
        EXPECTED: *  All selection box is enabled and are not greyed out.
        EXPECTED: * 'SUSPENDED' label is NOT shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is enabled and not greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended' is disappeared
        """
        pass
