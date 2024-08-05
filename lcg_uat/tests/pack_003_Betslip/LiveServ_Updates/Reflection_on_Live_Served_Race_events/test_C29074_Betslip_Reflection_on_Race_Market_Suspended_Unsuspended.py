import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.betslip
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C29074_Betslip_Reflection_on_Race_Market_Suspended_Unsuspended(BaseBetSlipTest):
    """
    TR_ID: C29074
    NAME: Betslip Reflection on <Race> Market Suspended/Unsuspended
    DESCRIPTION: This test case verifies Betslip reflection when <Race> Market is Suspended.
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
    horse_name = None
    betnow_section = None

    def test_001_add_single_race_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add single <Race> selection to the Betslip
        """
        race_event = self.ob_config.add_UK_racing_event(number_of_runners=1)
        self.__class__.eventID = race_event.event_id
        self.__class__.marketID = race_event.market_id
        self.__class__.horse_name = (list(race_event.selection_ids.keys())[0])
        self.open_betslip_with_selections(race_event.selection_ids[self.horse_name])

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: Added selection is displayed in the betslip
        """
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section.get(self.horse_name)
        self.assertTrue(self.stake, msg=f'"{self.horse_name}" stake is not available')

    def test_003_trigger_suspension_of_the_market(self):
        """
        DESCRIPTION: Trigger the following situation for the event:
        DESCRIPTION: **marketStatusCode="S" **for selected market type
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
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
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, active=False, displayed=True)

        self.verify_betslip_is_suspended(stakes=[self.stake])

    def test_004_make_the_market_active_again(self):
        """
        DESCRIPTION: Trigger the following situation for one of events:
        DESCRIPTION: **marketStatusCode="A"**
        DESCRIPTION: and at the same time have Betslip page opened to watch for updates
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
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, active=True, displayed=True)

        self.verify_betslip_is_active(stakes=[self.stake], is_stake_filled=False)
