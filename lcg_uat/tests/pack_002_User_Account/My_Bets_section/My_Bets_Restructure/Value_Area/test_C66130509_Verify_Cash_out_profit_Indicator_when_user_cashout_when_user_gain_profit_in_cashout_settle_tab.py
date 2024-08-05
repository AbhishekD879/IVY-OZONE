import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C66130509_Verify_Cash_out_profit_Indicator_when_user_cashout_when_user_gain_profit_in_cashout_settle_tab(Common):
    """
    TR_ID: C66130509
    NAME: Verify Cash out profit Indicator when user cashout when user gain profit in cashout/settle tab
    DESCRIPTION: This test case Verify Cash out profit Indicator when user cashout when user gain profit in cashout/settle tab
    PRECONDITIONS: User should login successfully with valid credentials
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_navigate_to_any_sportrace(self):
        """
        DESCRIPTION: Navigate to any Sport/Race
        EXPECTED: Sports/racing EDP page should be open
        """
        pass

    def test_002_click_on_the_selection_single_multiple(self):
        """
        DESCRIPTION: Click on the selection single /multiple
        EXPECTED: Selection should be added to betslip
        """
        pass

    def test_003_enter_stake_on_single_multiples_and_click_on_place_bet_cta(self):
        """
        DESCRIPTION: Enter stake on single /multiples and click on place bet CTA
        EXPECTED: Bets should be placed successfully for singles and multiples
        """
        pass

    def test_004_navigate_to_my_bets_ampgtopen(self):
        """
        DESCRIPTION: Navigate to My Bets-&amp;gt;Open
        EXPECTED: Open tab is available with the bets
        """
        pass

    def test_005_check_for_the_bets_places(self):
        """
        DESCRIPTION: Check for the bets places
        EXPECTED: Bets should be available for singles and multiples
        """
        pass

    def test_006_cashout_for_the_particular_bet_where_the_user_can_get_more_returns_compared_to_the_stake_amount(self):
        """
        DESCRIPTION: Cashout for the particular bet where the user can get more returns compared to the Stake amount
        EXPECTED: User should be able to do cashout successfully
        """
        pass

    def test_007_check_that_the_cashout_message_is_displayed_along_with_profit_indicated(self):
        """
        DESCRIPTION: Check that the cashout message is displayed along with profit indicated
        EXPECTED: Check the cashout message and  profit indicator  with Green background as per Figma deign
        EXPECTED: **Ladbrokes**
        EXPECTED: ![](index.php?/attachments/get/f030718d-9d98-4af3-ab37-8effd88a63a6)
        """
        pass

    def test_008_tab_on_settled_tab(self):
        """
        DESCRIPTION: Tab on settled tab
        EXPECTED: settled bets tab is opened
        """
        pass

    def test_009_check_for_the_above_bets_after_settle_which_are_cashout(self):
        """
        DESCRIPTION: Check for the above bets after settle which are cashout
        EXPECTED: User should be displayed with "You Cashed Out: &Acirc;&pound;75.74! with profit indicator and with Green background as per Figma deign
        EXPECTED: **Ladbrokes**
        EXPECTED: ![](index.php?/attachments/get/6186525e-ab8c-49e4-8ce8-eaa084cb4142)
        """
        pass
