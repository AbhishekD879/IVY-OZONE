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
class Test_C2986449_Verify_currency_behavior_on_UK_tote_race_card(Common):
    """
    TR_ID: C2986449
    NAME: Verify currency behavior on UK tote race card
    DESCRIPTION: This test case verifies user and pool currency display on UK HR race card.
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
    PRECONDITIONS: * Event should have any pool type available (Win/Place/Execta/Trifecta...).
    PRECONDITIONS: Scenario 1:
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: Scenario 2:
    PRECONDITIONS: * User is logged in and user currency is same as pool currency
    PRECONDITIONS: Scenario 3:
    PRECONDITIONS: User is logged in with different currency then pool currency
    """
    keep_browser_open = True

    def test_001_verify_pool_value_currency_as_per_scenario_1(self):
        """
        DESCRIPTION: Verify pool value currency as per scenario 1
        EXPECTED: * 'Current pool' value is displayed right under pool type on the left (if available)
        EXPECTED: * 'Current pool' value is displayed only in pool currency and pool currency sign (eg. Current pool:AU$2212)
        """
        pass

    def test_002_navigate_through_the_pool_type_tabs_winplaceexectatrifecta_and_verify_the_pool_value_currency_display(self):
        """
        DESCRIPTION: Navigate through the pool type tabs (Win/Place/Execta/Trifecta...) and verify the pool value currency display
        EXPECTED: 'Current pool' value is displayed only in pool currency and pool currency sign for all available pool types
        """
        pass

    def test_003_verify_pool_value_currency_and_user_currency_as_per_scenario_2(self):
        """
        DESCRIPTION: Verify pool value currency and user currency as per scenario 2
        EXPECTED: * 'Current pool' value is displayed right under pool type on the left (if available)
        EXPECTED: * 'Current pool' value is displayed only in pool currency and pool currency sign (eg. Current pool:AU$2212)
        """
        pass

    def test_004_navigate_through_the_pool_type_tabs_and_verify_both_pool_and_user_currencies_display(self):
        """
        DESCRIPTION: Navigate through the pool type tabs and verify both pool and user currencies display
        EXPECTED: 'Current pool' value is displayed only in pool currency and pool currency sign for all available pool types
        """
        pass

    def test_005_verify_pool_value_currency_and_user_currency_as_per_scenario_3(self):
        """
        DESCRIPTION: Verify pool value currency and user currency as per scenario 3
        EXPECTED: 'Current pool' value is displayed right under pool type on the left (if available) and user currency value is displayed afterwards through the slash (eg. Current pool:€1.29 / AU$2.12)
        """
        pass

    def test_006_navigate_through_the_pool_type_tabs_and_verify_both_pool_and_user_currencies_display(self):
        """
        DESCRIPTION: Navigate through the pool type tabs and verify both pool and user currencies display
        EXPECTED: 'Current pool' value is displayed in pool currency and pool currency sign and user currency value is displayed afterwards through the slash for all available pool types
        """
        pass
