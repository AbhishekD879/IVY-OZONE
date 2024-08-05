import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.build_your_bet
@vtest
class Test_C2490965_Banach_Trigger_selections_dashboard_and_price(Common):
    """
    TR_ID: C2490965
    NAME: Banach. Trigger selections dashboard and price
    DESCRIPTION: This test case verifies triggering Banach selections dashboard and price generation
    DESCRIPTION: AUTOTEST [C2592713]
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Examples of combinable Banach markets:**
    PRECONDITIONS: Match Result or Both teams to score + Double Chance + Anytime goalscorer + Over/Under markets + Correct Score
    PRECONDITIONS: Check price value: Open Dev tools > Network > **price** request
    PRECONDITIONS: * BYB **Coral**/Bet Builder **Ladbrokes** tab on event details page with Banach markets is loaded
    PRECONDITIONS: * App local storage is cleared
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Be aware that single bet placement is allowed for 'Player Bets' markets and it's described in https://ladbrokescoral.testrail.com/index.php?/cases/view/2911497 test case.
    """
    keep_browser_open = True

    def test_001_add_only_one_selection_to_dashboard(self):
        """
        DESCRIPTION: Add only one selection to dashboard
        EXPECTED: - Dashboard appears with slide animation and is expanded (when selection is added for the first time)
        EXPECTED: - **Please add another selection to place a bet** notification is shown above the dashboard
        """
        pass

    def test_002_add_one_more_selection_from_combinable_markets_accordions(self):
        """
        DESCRIPTION: Add one more selection from combinable markets accordions
        EXPECTED: - Notification disappears
        EXPECTED: - Odds area appears next to dashboard header
        EXPECTED: - Selections are highlighted within accordions
        """
        pass

    def test_003_verify_odds_area_for_fractional_odds_format(self):
        """
        DESCRIPTION: Verify Odds area for fractional odds format
        EXPECTED: - Odds value taken from **price** response is displayed
        EXPECTED: - Odds are displayed in fractional format defined in Settings
        EXPECTED: - PLACE BET text below odds
        """
        pass

    def test_004_change_odds_format_in_settings(self):
        """
        DESCRIPTION: Change odds format in Settings
        EXPECTED: Odds are changed to decimal
        """
        pass

    def test_005_navigate_back_to_edp_of_event_that_has_banach_markets_and_select_byb_coralbet_builder_ladbrokes_tab(self):
        """
        DESCRIPTION: Navigate back to EDP of event that has Banach markets and select BYB **Coral**/Bet Builder **Ladbrokes** tab
        EXPECTED: BYB **Coral**/Bet Builder **Ladbrokes** tab on event details page with Banach markets is loaded
        """
        pass

    def test_006_verify_odds_area_for_decimal_odds_format(self):
        """
        DESCRIPTION: Verify Odds area for decimal odds format
        EXPECTED: - Odds value taken from **price** response is displayed
        EXPECTED: - Odds are displayed in decimal format defined in Settings
        EXPECTED: - PLACE BET text below odds
        """
        pass

    def test_007_remove_all_selections_from_dashboard(self):
        """
        DESCRIPTION: Remove all selections from Dashboard
        EXPECTED: Dashboard is not displayed anymore on EDP
        """
        pass
