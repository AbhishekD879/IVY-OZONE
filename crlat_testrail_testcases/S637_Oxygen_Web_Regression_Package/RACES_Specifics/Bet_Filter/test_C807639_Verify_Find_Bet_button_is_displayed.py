import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C807639_Verify_Find_Bet_button_is_displayed(Common):
    """
    TR_ID: C807639
    NAME: Verify Find Bet button is displayed
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_deploy_verify_bet_finder_button_when_bet_finder_component_is_not_built(self):
        """
        DESCRIPTION: [deploy] Verify Bet Finder button when Bet finder component is NOT built
        EXPECTED: Bet Finder button on Racing page is HIDDEN
        """
        pass

    def test_002_deploy_verify_bet_finder_button_when_bet_finder_component_is_built(self):
        """
        DESCRIPTION: [deploy] Verify Bet Finder button when Bet finder component is built
        EXPECTED: Bet Finder button on Racing page is DISPLAYED
        """
        pass
