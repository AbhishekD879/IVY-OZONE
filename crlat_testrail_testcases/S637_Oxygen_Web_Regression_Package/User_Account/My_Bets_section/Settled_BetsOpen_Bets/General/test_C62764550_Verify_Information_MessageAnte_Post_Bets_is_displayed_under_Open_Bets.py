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
class Test_C62764550_Verify_Information_MessageAnte_Post_Bets_is_displayed_under_Open_Bets(Common):
    """
    TR_ID: C62764550
    NAME: Verify Information Message(Ante Post Bets) is displayed under Open Bets
    DESCRIPTION: This test case verifies Information Message(Antepost Bets) is displayed under Open Bets
    PRECONDITIONS: login to the application
    """
    keep_browser_open = True

    def test_001_go_to_mybets__open_bets(self):
        """
        DESCRIPTION: Go to Mybets- open bets
        EXPECTED: An information message "If you require account or gambling history over longer periods, or details of unsettled bets placed over 1 year ago, please contact us" should be displayed under open bets.
        EXPECTED: Note: When user clicks on the Contact us icon- he is redirected to Help Center Page.
        """
        pass
