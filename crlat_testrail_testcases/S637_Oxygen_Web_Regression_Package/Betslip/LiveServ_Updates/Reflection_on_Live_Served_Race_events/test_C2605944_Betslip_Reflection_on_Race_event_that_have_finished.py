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
class Test_C2605944_Betslip_Reflection_on_Race_event_that_have_finished(Common):
    """
    TR_ID: C2605944
    NAME: Betslip Reflection on <Race> event that have finished
    DESCRIPTION: This test case verifies betslip reflection on <Race> events that have finished
    DESCRIPTION: AUTOTEST Mobile: [C2610026]
    DESCRIPTION: AUTOTEST Desktop: [C2610565]
    PRECONDITIONS: LiveServer is available for In-Play <Race> events with the following attributes:
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: isMarketBetInRun = "true"
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: NOTE: LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events
    PRECONDITIONS: **[displayed:"N"] OR [result_conf:”Y”] attributes are received in LIVE SERV pushes.**
    PRECONDITIONS: Dev Tools->Network->All->push
    PRECONDITIONS: Use http://backoffice-tst2.coral.co.uk/ti/ for triggering events undisplaying or setting results.
    """
    keep_browser_open = True

    def test_001_add_race_selection_to_the_betslip__and_open_the_betslip(self):
        """
        DESCRIPTION: Add <Race> selection to the Betslip  and open the Betslip
        EXPECTED: Added selection is displayed in the Betslip
        """
        pass

    def test_002_set_results_for_the_event_where_selection_belongs_to_and_have_betslip_opened_to_watch_for_updates(self):
        """
        DESCRIPTION: Set results for the event where selection belongs to and have Betslip opened to watch for updates
        EXPECTED: **Before OX99**
        EXPECTED: * Error messages 'Sorry, the outcome/market/event has been suspended' (depends on what comes in response from server) are shown below corresponding singles
        EXPECTED: * Stake' field and 'Bet Now' buttons are disabled and greyed out
        EXPECTED: * Warning message 'Please beware that 1 of your selections has been suspended' is shown on the yellow background in the bottom of the Betslip
        EXPECTED: **After OX99**
        EXPECTED: After OX99
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login&Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is shown at the center of selection
        EXPECTED: * 'Place Bet' ( 'Login and Place Bet') button is disabled and greyed out
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        pass
