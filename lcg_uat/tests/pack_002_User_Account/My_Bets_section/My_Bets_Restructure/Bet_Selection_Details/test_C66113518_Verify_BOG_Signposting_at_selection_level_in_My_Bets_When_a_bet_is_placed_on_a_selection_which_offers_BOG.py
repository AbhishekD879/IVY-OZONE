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
class Test_C66113518_Verify_BOG_Signposting_at_selection_level_in_My_Bets_When_a_bet_is_placed_on_a_selection_which_offers_BOG(Common):
    """
    TR_ID: C66113518
    NAME: Verify BOG Signposting at selection level in My Bets When a bet is placed on a selection which offers BOG
    DESCRIPTION: This testcase verifies BOG Signposting at selection level in My Bets When a bet is placed on a selection which offers BOG
    PRECONDITIONS: Horse racing Bets on selections which offers BOG should be avilable in open,cash out,Settled tabs
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials_with_precondition1(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition1
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_horse_racing_bets_which_offers_bog_in_open_tab(self):
        """
        DESCRIPTION: Verify Horse racing Bets which offers BOG in open tab
        EXPECTED: BOG signposting should be displayed as per figma provided
        EXPECTED: ![](index.php?/attachments/get/e2cb367f-a7d5-4c49-a85a-87412586a732)
        """
        pass

    def test_004_click_on_cash_out(self):
        """
        DESCRIPTION: Click on cash out
        EXPECTED: Cash out tab is opened
        """
        pass

    def test_005_verify_horse_racing_bets_which_offers_bog_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify Horse racing Bets which offers BOG in Cash out tab
        EXPECTED: BOG signposting should be displayed as per figma provided
        EXPECTED: ![](index.php?/attachments/get/8018c3b8-c366-464a-ae05-c5065e24140f)
        """
        pass

    def test_006_click_on_settled_tab(self):
        """
        DESCRIPTION: Click on settled tab
        EXPECTED: Settled tab is opened
        """
        pass

    def test_007_verify_horse_racing_bets_which_offers_bog_in_settled_tab(self):
        """
        DESCRIPTION: Verify Horse racing Bets which offers BOG in Settled tab
        EXPECTED: BOG signposting should be displayed as per figma provided
        EXPECTED: ![](index.php?/attachments/get/c3672d1b-ff48-41db-a851-13c8013c3d0a)
        """
        pass
