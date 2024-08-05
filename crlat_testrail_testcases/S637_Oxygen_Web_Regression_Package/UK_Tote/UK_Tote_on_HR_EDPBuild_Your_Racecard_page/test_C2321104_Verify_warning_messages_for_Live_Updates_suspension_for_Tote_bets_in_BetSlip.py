import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.races
@vtest
class Test_C2321104_Verify_warning_messages_for_Live_Updates_suspension_for_Tote_bets_in_BetSlip(Common):
    """
    TR_ID: C2321104
    NAME: Verify warning messages for Live Updates (suspension) for Tote bets in BetSlip
    DESCRIPTION: This test case verifies warning messages for Tote bets in the BetSlip, which appear when event/market/outcome are suspended
    DESCRIPTION: AUTOTEST [C2516346]
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is sufficient to cover the bet stake
    PRECONDITIONS: * Overask is disabled for the user in TI tool
    PRECONDITIONS: * User has added UK Tote bet (any pool type) to the betslip
    PRECONDITIONS: * Betslip is opened
    """
    keep_browser_open = True

    def test_001_suspend_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend current event in TI
        EXPECTED: Error message appears:
        EXPECTED: "Please beware some of your selections have been suspended"
        EXPECTED: "SUSPENDED" label is displayed in the center of the stake
        """
        pass

    def test_002_make_the_event_active_again_in_ti(self):
        """
        DESCRIPTION: Make the event active again in TI
        EXPECTED: Error message disappears
        """
        pass

    def test_003_suspend_market_from_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend market from current event in TI
        EXPECTED: Error message appears:
        EXPECTED: "Please beware some of your selections have been suspended"
        EXPECTED: "SUSPENDED" label is displayed in the center of the stake
        """
        pass

    def test_004_make_the_market_active_again_in_ti(self):
        """
        DESCRIPTION: Make the market active again in TI
        EXPECTED: Error message disappears
        """
        pass

    def test_005_suspend_one_or_more_selections_from_current_bet_in_ti(self):
        """
        DESCRIPTION: Suspend one or more selections from current bet in TI
        EXPECTED: Error message appears:
        EXPECTED: "Please beware some of your selections have been suspended"
        EXPECTED: "SUSPENDED" label is displayed in the center of the stake
        """
        pass

    def test_006_make_the_selections_active_again_in_ti(self):
        """
        DESCRIPTION: Make the selection(s) active again in TI
        EXPECTED: Error message disappears
        """
        pass
