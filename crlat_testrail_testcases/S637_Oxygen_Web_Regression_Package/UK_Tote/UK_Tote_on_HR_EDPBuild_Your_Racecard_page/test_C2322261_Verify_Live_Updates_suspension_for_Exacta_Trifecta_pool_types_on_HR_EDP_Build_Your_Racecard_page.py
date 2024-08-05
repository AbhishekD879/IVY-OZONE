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
class Test_C2322261_Verify_Live_Updates_suspension_for_Exacta_Trifecta_pool_types_on_HR_EDP_Build_Your_Racecard_page(Common):
    """
    TR_ID: C2322261
    NAME: Verify Live Updates (suspension) for Exacta/Trifecta pool types on HR EDP/Build Your Racecard page
    DESCRIPTION: This test case verifies Live Updates (suspension) for Exacta/Trifecta pool types on HR EDP/Build Your Racecard page
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [UK Tote: Implement HR Exacta pool type] [1]
    DESCRIPTION: [UK Tote: Implement HR Trifecta pool type] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28444
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-28445
    PRECONDITIONS: * The HR event should have Exacta and Trifecta pool types available
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
    """
    keep_browser_open = True

    def test_001_suspend_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend current event in TI
        EXPECTED: All Exacta check boxes become disabled in real time
        """
        pass

    def test_002_make_the_event_active_again_in_ti(self):
        """
        DESCRIPTION: Make the event active again in TI
        EXPECTED: All Exacta check boxes become active in real time
        """
        pass

    def test_003_suspend_market_from_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend market from current event in TI
        EXPECTED: All Exacta check boxes become disabled in real time
        """
        pass

    def test_004_make_the_market_active_again_in_ti(self):
        """
        DESCRIPTION: Make the market active again in TI
        EXPECTED: All Exacta check boxes become active in real time
        """
        pass

    def test_005_suspend_one_or_more_selections_from_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend one or more selections from current event in TI
        EXPECTED: Particular suspended Exacta check boxes become disabled in real time
        """
        pass

    def test_006_make_the_selections_active_again_in_ti(self):
        """
        DESCRIPTION: Make the selection(s) active again in TI
        EXPECTED: Particular suspended Exacta check boxes become active again in real time
        """
        pass

    def test_007_repeat_steps_1_6_for_trifecta_pool_type(self):
        """
        DESCRIPTION: Repeat steps 1-6 for Trifecta pool type
        EXPECTED: 
        """
        pass
