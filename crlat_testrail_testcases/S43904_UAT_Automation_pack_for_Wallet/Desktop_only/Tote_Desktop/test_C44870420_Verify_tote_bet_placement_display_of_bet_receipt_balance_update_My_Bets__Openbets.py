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
class Test_C44870420_Verify_tote_bet_placement_display_of_bet_receipt_balance_update_My_Bets__Openbets(Common):
    """
    TR_ID: C44870420
    NAME: Verify tote bet placement, display of bet receipt , balance update, My Bets -> Openbets
    DESCRIPTION: 
    PRECONDITIONS: User is logged in.
    """
    keep_browser_open = True

    def test_001_launch_application(self):
        """
        DESCRIPTION: Launch Application.
        EXPECTED: Application is launched.
        """
        pass

    def test_002_navigate_to_totepool_market_from_any_hr_event_or_international_tote_pool(self):
        """
        DESCRIPTION: Navigate to Totepool market from any HR event or international Tote Pool.
        EXPECTED: Totepool market is opened.
        """
        pass

    def test_003_click_on_any_win_selection(self):
        """
        DESCRIPTION: Click on any win selection
        EXPECTED: A bar is opened at bottom which shows
        EXPECTED: 1 Win Selection
        EXPECTED: 2 Clear Selection
        EXPECTED: 3 Add to Betslip button in Green
        """
        pass

    def test_004_click_on_add_to_betslip(self):
        """
        DESCRIPTION: Click on ADD TO BETSLIP
        EXPECTED: Your selection is added to the betslip.
        """
        pass

    def test_005_verify_details_on_betslip(self):
        """
        DESCRIPTION: Verify details on betslip
        EXPECTED: User is able to see
        EXPECTED: 1 Win Totepool
        EXPECTED: 1 Win Selection
        EXPECTED: your selection name
        EXPECTED: Time, Event Name
        EXPECTED: Today
        EXPECTED: Stake Box
        EXPECTED: Potential Returns: N/A
        EXPECTED: Total Stake  £0.00
        EXPECTED: Total Potential Returns N/A
        """
        pass

    def test_006_enter_stake_and_place_bet_minimum_stake_is_200(self):
        """
        DESCRIPTION: Enter Stake and place bet (Minimum stake is £2.00)
        EXPECTED: User is able to see
        EXPECTED: 1 Win Totepool
        EXPECTED: 1 Win Selection
        EXPECTED: your selection name
        EXPECTED: Time, Event Name
        EXPECTED: Today
        EXPECTED: Stake for this bet: £2:00
        EXPECTED: Pot. Returns: N/A
        EXPECTED: Total Stake  £2.00
        EXPECTED: Total Potential Returns N/A
        """
        pass

    def test_007_verify_your_balance_update(self):
        """
        DESCRIPTION: verify your balance update
        EXPECTED: Balance should be updated accordingly.
        """
        pass
