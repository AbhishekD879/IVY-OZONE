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
class Test_C1922449_Verify_UK_Pools_Suspensions_on_Open_Bets(Common):
    """
    TR_ID: C1922449
    NAME: Verify UK Pools Suspensions on Open Bets
    DESCRIPTION: This test case verifies the displayed contents of a Exacta tote bet in the Bet History section of My Bets
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed several tote UK Tote bets
    """
    keep_browser_open = True

    def test_001_navigate_to_open_bets_tabsuspend_the_selection_in_back_office(self):
        """
        DESCRIPTION: Navigate to Open Bets tab
        DESCRIPTION: Suspend the selection in back office
        EXPECTED: * Displayed tote bet is greyed out
        EXPECTED: * 'Suspended' tag is displayed
        """
        pass

    def test_002_unsuspend_the_selection(self):
        """
        DESCRIPTION: Unsuspend the selection
        EXPECTED: * Displayed grey out overlay should revert to active
        EXPECTED: * 'Suspended' tag is removed
        """
        pass

    def test_003_suspend_the_market_for_current_bet_in_back_office(self):
        """
        DESCRIPTION: Suspend the market for current bet in back office
        EXPECTED: * Displayed tote bet is greyed out
        EXPECTED: * 'Suspended' tag is displayed
        """
        pass

    def test_004_unsuspend_the_market(self):
        """
        DESCRIPTION: Unsuspend the market
        EXPECTED: * Displayed grey out overlay should revert to active
        EXPECTED: * 'Suspended' tag is removed
        """
        pass

    def test_005_suspend_the_event_for_current_bet_in_back_office(self):
        """
        DESCRIPTION: Suspend the event for current bet in back office
        EXPECTED: * Displayed tote bet is greyed out
        EXPECTED: * 'Suspended' tag is displayed
        """
        pass

    def test_006_unsuspend_the_event(self):
        """
        DESCRIPTION: Unsuspend the event
        EXPECTED: * Displayed grey out overlay should revert to active
        EXPECTED: * 'Suspended' tag is removed
        """
        pass
