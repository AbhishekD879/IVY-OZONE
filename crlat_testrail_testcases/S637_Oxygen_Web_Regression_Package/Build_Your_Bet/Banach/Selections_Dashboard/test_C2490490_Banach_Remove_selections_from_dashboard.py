import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.build_your_bet
@vtest
class Test_C2490490_Banach_Remove_selections_from_dashboard(Common):
    """
    TR_ID: C2490490
    NAME: Banach. Remove selections from dashboard
    DESCRIPTION: This test case verifies possibility to delete dashboard selections by tapping on Delete button or on selections inside accordions.
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: For Odds calculation check Dev tools > Network: price request
    PRECONDITIONS: **At least 4 Banach selections are added to dashboard**
    PRECONDITIONS: **Dashboard is expanded**
    """
    keep_browser_open = True

    def test_001_tap_remove_button_for_the_top_selection_inside_dashboard(self):
        """
        DESCRIPTION: Tap "Remove" button for the top selection inside dashboard
        EXPECTED: - Selection is not highlighted within market accordion
        EXPECTED: - Selection is removed from dashboard
        EXPECTED: - Top selection name is updated on dashboard header
        EXPECTED: - Selections counter is updated on the dashboard header
        EXPECTED: - Odds value updated (from **price** request)
        """
        pass

    def test_002_tap_on_the_selection_that_is_added_to_dashboard_in_market_accordion(self):
        """
        DESCRIPTION: Tap on the selection that is added to Dashboard in market accordion
        EXPECTED: - Selection is not highlighted within market accordion
        EXPECTED: - Selection is removed from dashboard
        EXPECTED: - Top selection name is updated on dashboard header
        EXPECTED: - Selections counter is updated on the dashboard header
        EXPECTED: - Odds value is updated
        """
        pass

    def test_003_remove_more_selections_to_have_1_onlyby_tapping_remove_button_or_tapping_on_selections_in_market_accordions(self):
        """
        DESCRIPTION: Remove more selections to have 1 only
        DESCRIPTION: (by tapping Remove button or tapping on selections in market accordions)
        EXPECTED: - **Please add another selection to place bet** message appears above dashboard header
        """
        pass

    def test_004_remove_the_last_selection(self):
        """
        DESCRIPTION: Remove the last selection
        EXPECTED: - Dashboard disappears
        EXPECTED: - Message disappears
        """
        pass
