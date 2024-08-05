import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C2496164_Banach_Dashboard_in_closed_state_collapse_expand_chevron(Common):
    """
    TR_ID: C2496164
    NAME: Banach. Dashboard in closed state, collapse/expand chevron
    DESCRIPTION: Test case verifies collapse/expand chevron and Banach selections dashboard in closed state
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Banach selections are added to the dashboard**
    PRECONDITIONS: **Dashboard is expanded**
    """
    keep_browser_open = True

    def test_001_tap_on_close_chevron_button_on_dashboard_header(self):
        """
        DESCRIPTION: Tap on Close chevron button on dashboard header
        EXPECTED: Dashboard is closed and contains:
        EXPECTED: - Dashboard header
        EXPECTED: - Odds area
        """
        pass

    def test_002_verify_dashboard_header_in_closed_dashboard_state(self):
        """
        DESCRIPTION: Verify dashboard header in closed dashboard state
        EXPECTED: The following information is displayed:
        EXPECTED: - icon with number of selections
        EXPECTED: - BUILD YOUR BET **Coral**/BET BUILDER **Ladbrokes** text
        EXPECTED: - name of the first selections (separated by comma)
        EXPECTED: - "Open" chevron
        """
        pass

    def test_003_tap_open_chevron_button(self):
        """
        DESCRIPTION: Tap Open chevron button
        EXPECTED: Dashboard is expanded and contains selections from pre-conditions
        """
        pass
