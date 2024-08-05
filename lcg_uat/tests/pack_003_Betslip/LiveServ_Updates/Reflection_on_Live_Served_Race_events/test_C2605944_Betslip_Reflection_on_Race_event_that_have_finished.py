import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # we can't finish event on prod/hl
@pytest.mark.user_journey_single_greyhound_race
@pytest.mark.betslip
@pytest.mark.liveserv_updates
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.results
@pytest.mark.desktop
@pytest.mark.medium
@vtest
class Test_C2605944_Betslip_Reflection_on_Race_event_that_have_finished(BaseBetSlipTest):
    """
    TR_ID: C2605944
    NAME: Betslip Reflection on <Race> event that have finished
    DESCRIPTION: This test case verifies betslip reflection on <Race> events that have finished
    PRECONDITIONS: LiveServer is available for In-Play <Race> events with the following attributes:
    PRECONDITIONS:    - drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS:    - isMarketBetInRun = "true"
    PRECONDITIONS: NOTE: LivePrice updates are NOT applicable for Outrights and Enhanced Multiples events
    PRECONDITIONS: [displayed:"N"] OR [result_conf:”Y”] attributes are received in LIVE SERV pushes
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test racing event
        """
        event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1)
        self.__class__.selection_name, self.__class__.selection_id = list(event_params.selection_ids.items())[0]
        self.__class__.marketID = event_params.market_id
        self.__class__.eventID = event_params.event_id

    def test_001_add_race_selection_to_the_Betslip(self):
        """
        DESCRIPTION: Add <Race> selection to the Betslip
        DESCRIPTION: Open the Betslip
        EXPECTED: Added selection is displayed in the Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip not opened')
        single_section = self.get_betslip_sections().Singles
        self.assertTrue(single_section, msg='"SINGLE" Betslip section was not found')
        self.__class__.stake = single_section.get(self.selection_name)
        self.assertTrue(self.stake, msg=f'Stake: "{self.selection_name}" section not found')

    def test_002_set_results_for_the_event(self):
        """
        DESCRIPTION: Set results for the event where selection belongs to and have Betslip opened to watch for updates
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
        self.ob_config.result_selection(selection_id=self.selection_id, market_id=self.marketID, event_id=self.eventID)
        self.ob_config.confirm_result(selection_id=self.selection_id, market_id=self.marketID, event_id=self.eventID)
        self.ob_config.settle_result(selection_id=self.selection_id, market_id=self.marketID, event_id=self.eventID)

        self.verify_betslip_is_suspended(stakes=[self.stake])
