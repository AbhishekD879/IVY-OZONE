import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2912419_Verify_Live_Updates_suspension_for_Win_Place_BetBuilder_on_HR_EDP(Common):
    """
    TR_ID: C2912419
    NAME: Verify Live Updates (suspension) for Win/Place BetBuilder on HR EDP
    DESCRIPTION: This test case verifies Live Updates (suspension) for Win/Place BetBuilder on HR EDP
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Win/Place pool types is available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Choose the particular event from the 'Race Grid'
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: **AND REPEAT FOR**
    PRECONDITIONS: Build Your Racecard page for specific Event ("Tote" tab) **Desktop**:
    PRECONDITIONS: * Navigate to HR landing page
    PRECONDITIONS: * Click 'Build a Racecard' button
    PRECONDITIONS: * Select at least one Event with Totepool are available
    PRECONDITIONS: * Click 'Build Your Racecard' button
    PRECONDITIONS: * Select 'Tote' tab
    PRECONDITIONS: To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True

    def test_001_selecta_1_win_bet(self):
        """
        DESCRIPTION: Selecta 1 Win Bet
        EXPECTED: * Tote Bet Builder appears
        EXPECTED: * 'ADD TO BETSLIP' button is an active
        """
        pass

    def test_002_suspend_one_selected_selection(self):
        """
        DESCRIPTION: Suspend one selected selection
        EXPECTED: * Suspended selection is unselected
        EXPECTED: * Tote Bet Builder disappears
        """
        pass

    def test_003_selecta_1_win_bet(self):
        """
        DESCRIPTION: Selecta 1 Win Bet
        EXPECTED: * Tote Bet Builder appears
        EXPECTED: * 'ADD TO BETSLIP' button is an active
        """
        pass

    def test_004_suspend_current_market(self):
        """
        DESCRIPTION: Suspend current market
        EXPECTED: * All suspended selections are unselected
        EXPECTED: * Tote Bet Builder disappears
        """
        pass

    def test_005_make_the_market_active_again_and_select_1_win_bet(self):
        """
        DESCRIPTION: Make the market active again and Select 1 Win Bet
        EXPECTED: * Tote Bet Builder appears
        EXPECTED: * 'ADD TO BETSLIP' button is an active
        """
        pass

    def test_006_suspend_current_event(self):
        """
        DESCRIPTION: Suspend current event
        EXPECTED: * All suspended selections are unselected
        EXPECTED: * Tote Bet Builder disappears
        """
        pass

    def test_007_make_the_event_active_again_and_select_1_win_bet(self):
        """
        DESCRIPTION: Make the event active again and Select 1 Win Bet
        EXPECTED: * Tote Bet Builder appears
        EXPECTED: * 'ADD TO BETSLIP' button is an active
        """
        pass

    def test_008_suspend_current_win_pool(self):
        """
        DESCRIPTION: Suspend current Win pool
        EXPECTED: * All suspended selections are unselected
        EXPECTED: * Tote Bet Builder disappears
        """
        pass

    def test_009_repeat_steps_1_9_for_1_place_bet(self):
        """
        DESCRIPTION: Repeat steps 1-9 for 1 Place Bet
        EXPECTED: 
        """
        pass
