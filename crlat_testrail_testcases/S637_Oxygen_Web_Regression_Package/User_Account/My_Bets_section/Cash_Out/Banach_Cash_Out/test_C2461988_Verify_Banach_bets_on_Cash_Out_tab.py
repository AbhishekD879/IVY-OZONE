import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.cash_out
@vtest
class Test_C2461988_Verify_Banach_bets_on_Cash_Out_tab(Common):
    """
    TR_ID: C2461988
    NAME: Verify Banach bets on 'Cash Out' tab
    DESCRIPTION: Test case verifies Banach bet display on Cash out.
    DESCRIPTION: AUTOTEST [C2604496]
    PRECONDITIONS: Related to [Full Cash out][1], [Partial Cash out][2]
    PRECONDITIONS: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2507465
    PRECONDITIONS: [2]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2507463
    PRECONDITIONS: Build Your Bet CMS configuration
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check Open Bet data for event on Cash-out tab:
    PRECONDITIONS: in Dev tools > Network find **getBetDetails** request
    PRECONDITIONS: **User has placed Banach bet(s)**
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets__cash_out_and_verify_banach_bet_details(self):
        """
        DESCRIPTION: Navigate to My Bets > Cash-out and verify Banach bet details
        EXPECTED: Cash-out tab contains Banach bet with correct details of:
        EXPECTED: - bet type **Single**
        EXPECTED: - Selection names user has bet on, separated by comma, truncated into a few lines
        EXPECTED: - Build Your Bet **Coral**/Bet Builder **Ladbrokes** text
        EXPECTED: - Corresponding Event name which is redirecting users to corresponding Event Details Page
        EXPECTED: - Event start date in DD MMM, hh:mm AM/PM (time only displayed for Today's events)
        EXPECTED: - Stake <currency symbol> <value> (e.g., £10.00)
        EXPECTED: - Odds
        EXPECTED: - Est. Returns <currency symbol> <value> (e.g., £30.00)
        EXPECTED: - 'Cash Out <currency symbol> <value>' and 'Partial Cashout' buttons
        EXPECTED: **After BMA-50453:**
        EXPECTED: * 'Bet Receipt' label and its ID (e.g. O/15242822/0000017) are shown below the stake value (on the left)
        EXPECTED: * Date of bet placement is shown to the right of Bet Receipt id
        EXPECTED: * Date of bet placement is shown in a format hh:mm AM/PM - DD/MM (14:00 - 19 June)
        """
        pass
