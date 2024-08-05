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
class Test_C66132269_Verify_no_dividers_between_the_selections_for_TOTE_Multi_Leg_Bets_Placepot_Quadpot_Jackpot_ITV7etc(Common):
    """
    TR_ID: C66132269
    NAME: Verify  no dividers between the selections for TOTE Multi Leg Bets (Placepot, Quadpot, Jackpot, ITV7,etc)
    DESCRIPTION: This test case Verify  no dividers between the selections for TOTE Multi Leg Bets (Placepot, Quadpot, Jackpot, ITV7,etc)
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
        EXPECTED: Totepool market should be available with (WIN,Place,Exacta,Trifacta,Placepot,jackpot,ITV7placepot)
        """
        pass

    def test_000_place_bet_on_the_below_markets_for_multi_legs_placepotquadpotjackpotitv7placepot(self):
        """
        DESCRIPTION: Place bet on the below markets for multi-legs :
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

    def test_000_check_each_selection_for_tote_multi_leg_style_bets_placed(self):
        """
        DESCRIPTION: Check each selection for Tote Multi-leg style bets placed
        EXPECTED: No dividers between  each selections  it should be as per Figma deign
        EXPECTED: ![](index.php?/attachments/get/b5cec03a-4dc4-43cb-8bbc-90650d6774b0)
        """
        pass

    def test_000_go_to_settle_bets_after_the_pool_bets_got_settled(self):
        """
        DESCRIPTION: Go to settle bets after the pool bets got settled
        EXPECTED: Settle tab should be available with settled pool bets
        EXPECTED: ![](index.php?/attachments/get/d91407f5-b54a-4dbb-bad5-a55d93426abb)
        """
        pass

    def test_000_check_tote_multi_leg_bets(self):
        """
        DESCRIPTION: Check Tote Multi-leg bets
        EXPECTED: No dividers between  each selections  it should be as per Figma deign
        EXPECTED: ![](index.php?/attachments/get/ff1f6e03-fd1a-405f-8484-ab7818f59ecb)
        """
        pass
