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
class Test_C66132270_Verify_suspended_state_for_pool_bets(Common):
    """
    TR_ID: C66132270
    NAME: Verify  suspended state for pool bets
    DESCRIPTION: This test case verify  suspended state for pool bets
    PRECONDITIONS: User should have a Horse Racing event
    PRECONDITIONS: Totepool market should be available
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_000_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        pass

    def test_000_navigate_to__horse_racing_page(self):
        """
        DESCRIPTION: Navigate to  Horse racing page
        EXPECTED: Horse racing page is opened with all the available meetings
        """
        pass

    def test_000_check_for_the_events_which_has_totepools(self):
        """
        DESCRIPTION: Check for the events which has Totepools
        EXPECTED: Totepool market should be availabel with (WIN,Place,Exacta,Trifacta,Placepot,jackpot,ITV7placepot)
        """
        pass

    def test_000_place_bet_on_the_below_markets_for_multi_legs_winplaceexactatrifactaplacepotquadpotjackpotitv7placepot(self):
        """
        DESCRIPTION: Place bet on the below markets for multi-legs :
        DESCRIPTION: WIN
        DESCRIPTION: Place
        DESCRIPTION: Exacta
        DESCRIPTION: Trifacta
        DESCRIPTION: Placepot
        DESCRIPTION: Quadpot
        DESCRIPTION: Jackpot
        DESCRIPTION: ITV7placepot
        EXPECTED: Bets should be placed successfully on all the mention markets
        """
        pass

    def test_000_navigate_to_my_bets_openpool_bets(self):
        """
        DESCRIPTION: Navigate to my bets-open(Pool bets)
        EXPECTED: Open tab should be available with the tote  bets placed
        """
        pass

    def test_000_check_the_pool_bets_available(self):
        """
        DESCRIPTION: Check the pool bets available
        EXPECTED: All the type of  pool bets should be available
        """
        pass

    def test_000_check_if_the_any_bets_got_suspend(self):
        """
        DESCRIPTION: Check if the any bets got suspend
        EXPECTED: Suspended bet should be as per Figma deign
        EXPECTED: ![](index.php?/attachments/get/978e45d5-cad6-423e-af51-fcd8b32c40db)
        """
        pass

    def test_000_go_to_settle_bets_after_the_pool_bets_got_settled(self):
        """
        DESCRIPTION: Go to settle bets after the pool bets got settled
        EXPECTED: Settle tab should be available with settled pool bets
        """
        pass

    def test_000_check_if_the_any_bets_got_suspend(self):
        """
        DESCRIPTION: Check if the any bets got suspend
        EXPECTED: Suspended bet should be as per Figma deign
        EXPECTED: ![](index.php?/attachments/get/92117265-39b6-4349-a275-ce16d0c59f24)   ![](index.php?/attachments/get/f1277832-c42d-497c-b074-c9f9e5e8d2f7)
        """
        pass
