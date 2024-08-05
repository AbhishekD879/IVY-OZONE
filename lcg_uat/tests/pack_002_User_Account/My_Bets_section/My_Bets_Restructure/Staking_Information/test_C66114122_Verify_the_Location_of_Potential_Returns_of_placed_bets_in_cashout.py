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
class Test_C66114122_Verify_the_Location_of_Potential_Returns_of_placed_bets_in_cashout(Common):
    """
    TR_ID: C66114122
    NAME: Verify the Location of Potential Returns of placed bets  in cashout
    DESCRIPTION: This test case is to verify the Location of Potential Returns of placed bets  in cashout
    PRECONDITIONS: cashout available events data should be available
    """
    keep_browser_open = True

    def test_000_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application should be launched without any issues
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User should be able to login without any issues
        """
        pass

    def test_002_go_to_any_sport_from_sports_ribbon__a_z_menu(self):
        """
        DESCRIPTION: Go to any sport from sports ribbon / A-Z menu
        EXPECTED: Should be able to navigate to sport landing page
        """
        pass

    def test_003_place_single_and_multiple_bets_from_different_events(self):
        """
        DESCRIPTION: place single and multiple bets from different events
        EXPECTED: single and multiple bets should be placed successfully
        """
        pass

    def test_004_go_to_my_bets_and_verify_recently_placed_bets(self):
        """
        DESCRIPTION: Go to My bets and verify recently placed bets
        EXPECTED: Recently placed bets should be listed down under open Note: The bets will display in expanded state by default
        """
        pass

    def test_005_navigate_to_cashout_tab_and_verify_bets(self):
        """
        DESCRIPTION: Navigate to Cashout tab and verify bets
        EXPECTED: The bets which are displayed under open should be displayed under cashout tab Note: Cashout unavailable bets will not dislay under cashout
        """
        pass

    def test_006_verify_the_location_of_the_potential_returns_for_recently_placed_bet(self):
        """
        DESCRIPTION: Verify the location of the potential returns for recently placed bet
        EXPECTED: Location of the potential returns should be displayed in line with odds and right justified within the staking area
        EXPECTED: ![](index.php?/attachments/get/c3a969bf-810f-4802-ba52-49d3c720b89e)
        """
        pass

    def test_007_click_on_anywhere_on_the_bet_header_to_collapse_the_bet_and_verify(self):
        """
        DESCRIPTION: Click on anywhere on the bet header to collapse the bet and verify
        EXPECTED: User should be able to collapse bet by clicking on bet header
        """
        pass

    def test_008_verify_the_location_of_the_potential_returns_for_recently_placed_bet_after_collapsing_the_bet(self):
        """
        DESCRIPTION: Verify the location of the potential returns for recently placed bet after collapsing the bet
        EXPECTED: Location of the potential returns should be displayed in line with stake and right side alligned
        EXPECTED: ![](index.php?/attachments/get/f92e958b-cbaa-463f-ae4b-60396a81ce93)
        """
        pass

    def test_009_repeat_step_3_to_step_9_by_placing_bets_in_lottos_and_pools_along_with_races(self):
        """
        DESCRIPTION: Repeat step 3 to step 9 by placing bets in lottos and pools along with races
        EXPECTED: Result will be same as above
        """
        pass
