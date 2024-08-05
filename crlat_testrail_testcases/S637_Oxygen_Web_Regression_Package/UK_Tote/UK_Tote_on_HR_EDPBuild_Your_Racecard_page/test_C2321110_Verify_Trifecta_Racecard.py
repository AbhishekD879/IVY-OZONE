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
class Test_C2321110_Verify_Trifecta_Racecard(Common):
    """
    TR_ID: C2321110
    NAME: Verify Trifecta Racecard
    DESCRIPTION: This test case verifies the racecard of Trifecta pool type of UK Tote
    DESCRIPTION: **Jira Tickets:**
    DESCRIPTION: [UK Tote: Implement HR Trifecta pool type] [1]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-28445
    PRECONDITIONS: * The HR event should have Trifecta pool type available
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

    def test_001_verify_trifecta_racecard_for_an_active_event(self):
        """
        DESCRIPTION: Verify Trifecta racecard for an **active** event
        EXPECTED: Trifecta racecard consists of:
        EXPECTED: * Current pool value (only shown if available)
        EXPECTED: * Runner number, name and information for each runner
        EXPECTED: * Runner silks (if available) for each runner
        EXPECTED: * "1st", "2nd", "3rd" and "Any" check boxes for each runner (all active by default)
        EXPECTED: Unnamed Favourite is NOT displayed at the end of list (BMA-50146)
        """
        pass

    def test_002_refresh_the_page_after_current_pool_value_changes(self):
        """
        DESCRIPTION: Refresh the page **after** current pool value changes
        EXPECTED: * Current pool value is updated upon page refresh
        """
        pass

    def test_003_lick_on_spotlight_downward_arrow_or_form_options_under_individual_selections(self):
        """
        DESCRIPTION: Сlick on spotlight (downward arrow) or form options under individual selections
        EXPECTED: The spotlight and form information under the selection are shown to the user
        """
        pass
