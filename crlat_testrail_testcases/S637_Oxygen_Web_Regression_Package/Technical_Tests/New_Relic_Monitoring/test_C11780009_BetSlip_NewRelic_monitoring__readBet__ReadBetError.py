import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C11780009_BetSlip_NewRelic_monitoring__readBet__ReadBetError(Common):
    """
    TR_ID: C11780009
    NAME: BetSlip NewRelic monitoring - readBet - ReadBetError
    DESCRIPTION: This test case verifies 'readBet' requests monitoring in NewRelic for BetSlip when actionName = 'ReadBetError'
    PRECONDITIONS: ) Load New Relic https://insights.newrelic.com
    PRECONDITIONS: 2) Start writing the query to get data related to 'readBet' actions in 'NRQL' field
    PRECONDITIONS: See example of the request:
    PRECONDITIONS: SELECT * FROM PageAction where actionName = 'ReadBetError' AND appName = '{ENDPOINT}' AND username = '{username}' LIMIT 100
    PRECONDITIONS: where
    PRECONDITIONS: types of envs:
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-DEV0 - dev0
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-TST0 - tst2
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-HLV0 - HL
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-PRD1 - PROD
    PRECONDITIONS: 3) Load Oxygen app
    PRECONDITIONS: 4) Log in app
    PRECONDITIONS: Note:
    PRECONDITIONS: Use the next instruction for the simulation situation when BPP is down:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+simulate+the+situation+when+Site+Serve+is+down
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the BetSlip
        EXPECTED: Selection is added to the BetSlip
        """
        pass

    def test_002_place_bet_use_bir_delay(self):
        """
        DESCRIPTION: Place bet (use BIR delay)
        EXPECTED: Bet placement process is started
        """
        pass

    def test_003_simulate_situation_when_bpp_is_down_on_env(self):
        """
        DESCRIPTION: Simulate situation when BPP is down on env
        EXPECTED: 'readBet' request to BPP is failed
        EXPECTED: 'Bet Placement Service Unavailable' pop-up appears
        """
        pass

    def test_004_open_new_relic_and_make_the_query(self):
        """
        DESCRIPTION: Open New Relic and make the query
        EXPECTED: The next attributes are received:
        EXPECTED: * timestamp (should be there by default)
        EXPECTED: * actionName - ReadBetError
        EXPECTED: * username
        EXPECTED: * request/response duration
        EXPECTED: * full response payload
        """
        pass
