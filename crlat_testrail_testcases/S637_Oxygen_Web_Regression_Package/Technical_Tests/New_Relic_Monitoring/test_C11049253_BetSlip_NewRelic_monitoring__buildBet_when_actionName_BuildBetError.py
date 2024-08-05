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
class Test_C11049253_BetSlip_NewRelic_monitoring__buildBet_when_actionName_BuildBetError(Common):
    """
    TR_ID: C11049253
    NAME: BetSlip NewRelic monitoring - buildBet when actionName = 'BuildBetError'
    DESCRIPTION: This test case verifies 'buildBet' requests monitoring in NewRelic for BetSlip when actionName = 'BuildBetError'
    PRECONDITIONS: 1) Load New Relic https://insights.newrelic.com
    PRECONDITIONS: 2) Start writing the query to get data related to 'buildBet' actions in 'NRQL' field
    PRECONDITIONS: See example of the request:
    PRECONDITIONS: SELECT * FROM PageAction where actionName = 'BuildBetError' AND appName = 'CR-SPT-OXYGEN-MBFE-DEV0' AND username = 'natarey' LIMIT 100
    PRECONDITIONS: where
    PRECONDITIONS: types of envs:
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-DEV0 - dev0
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-TST0 - tst2
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-HLV0 - HL
    PRECONDITIONS: * CR-SPT-OXYGEN-MBFE-PRD1 - PROD
    PRECONDITIONS: 3) Load Oxygen app
    PRECONDITIONS: 4) Log in app
    PRECONDITIONS: 5) Simulate situation when BPP is down on env
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Use the next instruction for the simulation situation when BPP is down:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=How+to+simulate+the+situation+when+Site+Serve+is+down
    """
    keep_browser_open = True

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the BetSlip
        EXPECTED: * Selection is added to the BetSlip
        EXPECTED: * 'buildBet' request to BPP is failed
        EXPECTED: * 'Bet Placement Service Unavailable' pop-up appears
        """
        pass

    def test_002_open_new_relic_and_make_the_query(self):
        """
        DESCRIPTION: Open New Relic and make the query
        EXPECTED: The next attributes are received:
        EXPECTED: * timestamp
        EXPECTED: * username
        EXPECTED: * request/response duration
        EXPECTED: * selection id/s
        EXPECTED: * betType
        """
        pass

    def test_003_log_out_app(self):
        """
        DESCRIPTION: Log out app
        EXPECTED: User is successfully logged out
        """
        pass

    def test_004_repeat_steps_1_2(self):
        """
        DESCRIPTION: Repeat steps 1-2
        EXPECTED: 
        """
        pass
