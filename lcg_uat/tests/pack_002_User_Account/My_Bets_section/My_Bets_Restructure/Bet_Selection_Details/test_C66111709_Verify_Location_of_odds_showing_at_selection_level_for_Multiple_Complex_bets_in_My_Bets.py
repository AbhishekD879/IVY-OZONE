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
class Test_C66111709_Verify_Location_of_odds_showing_at_selection_level_for_Multiple_Complex_bets_in_My_Bets(Common):
    """
    TR_ID: C66111709
    NAME: Verify Location of odds showing at selection level for Multiple/Complex bets in My Bets
    DESCRIPTION: This testcase verifies the location of odds showing at selection level for Multiple/Complex bets in My Bets
    PRECONDITIONS: Multiple/Complex bets should be available in Open ,cash out settled tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_location_of_odds_displayed_for_the_multiplecomplex_bets_in_open_tab(self):
        """
        DESCRIPTION: Verify location of Odds displayed for the multiple/complex bets in Open tab
        EXPECTED: Location of the Odds at selection level to be placed on the right hand side. Should be displayed as per figma
        EXPECTED: ![](index.php?/attachments/get/4caa037f-569b-478f-a27e-4614203acdff)
        """
        pass

    def test_004_verify_location_of_odds_displayed_for_the_multiplecomplex_bets_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify location of Odds displayed for the multiple/complex bets in Cash out tab
        EXPECTED: Location of the Odds at selection level to be placed on the right hand side. Should be displayed as per figma
        """
        pass

    def test_005_verify_location_of_odds_displayed_for_the_multiplecomplex_bets_in_settled_tab(self):
        """
        DESCRIPTION: Verify location of Odds displayed for the multiple/complex bets in Settled tab
        EXPECTED: Location of the Odds at selection level to be placed on the right hand side. Should be displayed as per figma
        EXPECTED: ![](index.php?/attachments/get/1e34f86e-fcfd-442f-9bdd-592897bea808)
        """
        pass

    def test_006_repeat_step_4_6__by_placing_single_bets_for_tier1_and_tier2_sports(self):
        """
        DESCRIPTION: Repeat step 4-6  by placing single bets for tier1 and tier2 Sports
        EXPECTED: Result should be same
        """
        pass
