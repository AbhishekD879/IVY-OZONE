import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C2323011_Lost_Status_of_UK_bet_on_Settled_Bets(Common):
    """
    TR_ID: C2323011
    NAME: Lost Status of UK bet on Settled Bets
    DESCRIPTION: This test case verifies the displaying of Lost Status of UK bets on Settled
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed UK Tote Bets
    PRECONDITIONS: For Resulting selection/market/event use link in back office https://backoffice-tst2.coral.co.uk/ti/hierarchy/event/event ID
    """
    keep_browser_open = True

    def test_001_result_the_bet_as_lost_in_back_officeopen_settled_bets_poolsverify_uk_tote_bet_display(self):
        """
        DESCRIPTION: Result the bet as **Lost** in back office
        DESCRIPTION: Open Settled Bets->Pools
        DESCRIPTION: Verify UK Tote bet display
        EXPECTED: Corresponding Bet Status appears for UK Tote bet at the left side on Bet header:
        EXPECTED: * 'LOST label is shown in Grey color
        EXPECTED: * Total returns are displayed as 0 funds
        """
        pass
