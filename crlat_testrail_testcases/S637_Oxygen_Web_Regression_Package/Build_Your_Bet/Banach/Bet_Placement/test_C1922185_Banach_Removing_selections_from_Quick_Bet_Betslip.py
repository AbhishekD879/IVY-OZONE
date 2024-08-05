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
class Test_C1922185_Banach_Removing_selections_from_Quick_Bet_Betslip(Common):
    """
    TR_ID: C1922185
    NAME: Banach. Removing selections from Quick Bet Betslip
    DESCRIPTION: Test case verifies Banach selections removal from Quick bet betslip and storing in dashboard
    DESCRIPTION: AUTOTEST [C2594011]
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check the following WS for details on adding selection to Quick bet and placing bet: remotebetslip websocket
    PRECONDITIONS: |||:Operation|:Banach code
    PRECONDITIONS: || Client adds selections to remote betslip | 50001
    PRECONDITIONS: || Response message for adding selections | 51001
    PRECONDITIONS: || Client message to remove selections from betslip |30001
    PRECONDITIONS: || Response message when selections removed |30002
    PRECONDITIONS: Build Your Bet **Coral**/Bet Builder **Ladbrokes** tab on event details page is loaded and selections are added to dashboard
    """
    keep_browser_open = True

    def test_001_tap_on_place_bet_button(self):
        """
        DESCRIPTION: Tap on "Place bet" button
        EXPECTED: - Betslip with price field and numeric keyboard appears
        """
        pass

    def test_002_tap_back_button(self):
        """
        DESCRIPTION: Tap "Back" button
        EXPECTED: - Betslip is removed
        EXPECTED: - Dashboard with "Place bet" button is shown
        EXPECTED: - Selections are present on UI
        """
        pass

    def test_003_expand_dashboard(self):
        """
        DESCRIPTION: Expand dashboard
        EXPECTED: Selections are saved in dashboard
        """
        pass
