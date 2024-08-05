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
class Test_C66132242_Verify_Event_location_and_score_location_for_5_A_Side_in_all_the_tabs(Common):
    """
    TR_ID: C66132242
    NAME: Verify Event location and score location for 5-A-Side in  all the tabs
    DESCRIPTION: This test case verify Event location and score location for 5-A-Side in  all the tabs
    PRECONDITIONS: BYB/BB event should be available
    PRECONDITIONS: Bets should be available in  open/cashout(if available),settle  tabs for BYB/BB
    """
    keep_browser_open = True

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Homepage is opened
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: User should login successfully with valid credentials
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Football landing page  should opened
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: User should be able to navigate to Football Event Details page
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Bet Builder/Build Your Bet tab should be opened
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Selections are added to bet slip
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Bet receipt is displayed
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: User Balance is updated
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Bets  should be available in open tab
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: BB/BYB  bet available in open tab
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Event name should be  show above the  legs  below the bet header
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: BYB/BB settle bets should be displayed
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Event name should be  show above the  legs  below the bet header
        """
        pass

    def test_000_(self):
        """
        DESCRIPTION: 
        EXPECTED: Scores should be shown between the selections in settle bets
        """
        pass
