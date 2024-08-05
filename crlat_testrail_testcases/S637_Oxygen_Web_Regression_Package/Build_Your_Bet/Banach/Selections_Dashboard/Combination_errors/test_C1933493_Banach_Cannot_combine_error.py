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
class Test_C1933493_Banach_Cannot_combine_error(Common):
    """
    TR_ID: C1933493
    NAME: Banach. Cannot combine error
    DESCRIPTION: Test case verifies error when user adds selections which cannot be combined to dashboard
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Examples of not valid selections combinations:
    PRECONDITIONS: - BOTH TEAMS TO SCORE IN BOTH HALFS - Yes + BOTH TEAMS TO SCORE - No
    PRECONDITIONS: - BOTH TEAMS TO SCORE IN BOTH HALFS - No + BOTH TEAM TO SCORE IN FIRST HALF - Yes
    PRECONDITIONS: - DOUBLE CHANCE 90 MINS - [Home team] or Draw + MATCH BETTING SECOND HALF - [Away team]
    PRECONDITIONS: - TOTAL GOALS 90 MINS - Over 0.5 Goals + [HOME TEAM] TOTAL GOALS - Under 0.5 + [AWAY TEAM] TOTAL GOALS - Under 0.5
    PRECONDITIONS: To see the error message from the provider check Dev tools > Network - "price" request
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Build Your Bet **Coral**/Bet Builder **Ladbrokes** tab on event details page is loaded
    """
    keep_browser_open = True

    def test_001_add_to_dashboard_selections_from_invalid_combinations_choose_which_is_available(self):
        """
        DESCRIPTION: Add to dashboard selections from invalid combinations (choose which is available)
        EXPECTED: - Error message from the provider is shown - it comes in **price** request "responseMessage" parameter
        EXPECTED: - "Place bet" button is hidden from Dashboard
        """
        pass

    def test_002_remove_some_selections_to_have_valid_combination(self):
        """
        DESCRIPTION: Remove some selections to have valid combination
        EXPECTED: * Error message disappears
        EXPECTED: * Odds area is shown with a price
        """
        pass
