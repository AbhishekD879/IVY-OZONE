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
class Test_C66114019_Verify_displaying_icon_for_horse_racing_results_in_settle_tab_for_horse_it_has_not_won_but_only_PLACED(Common):
    """
    TR_ID: C66114019
    NAME: Verify displaying icon for horse racing results in settle tab for horse it has not won but only PLACED
    DESCRIPTION: This test case verify displaying icon for horse racing results in settle tab for horse it has not won but only PLACED
    PRECONDITIONS: Bets should be available in open/cashout tabs
    """
    keep_browser_open = True

    def test_000_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        pass

    def test_002_navigate_to_horse_racing_page(self):
        """
        DESCRIPTION: Navigate to Horse racing page
        EXPECTED: HR landing page is opened
        """
        pass

    def test_003_place_single_bets_on__races_from_different_meetings(self):
        """
        DESCRIPTION: Place single bets on  Races from different meetings
        EXPECTED: Bets should be placed successfully
        """
        pass

    def test_004_tap_on_my_bets(self):
        """
        DESCRIPTION: Tap on 'My bets'
        EXPECTED: My bets page/Bet slip widget is opened
        """
        pass

    def test_005_click_on_open_tab(self):
        """
        DESCRIPTION: Click on Open tab
        EXPECTED: Open'  tab is selected by default
        EXPECTED: Placed bet is displayed
        """
        pass

    def test_006_check_the_bets_placed_for_single(self):
        """
        DESCRIPTION: Check the bets placed for single
        EXPECTED: Bets should be available in open tab
        """
        pass

    def test_007_click_on_settle_tab_after_the_above_bets_are_settled(self):
        """
        DESCRIPTION: Click on Settle tab after the above bets are settled
        EXPECTED: Bets should be available in settle tab after settlement
        """
        pass

    def test_008_check_the_lcon_and__result_place_for_bet_which_is__not_won(self):
        """
        DESCRIPTION: Check the lcon and  Result place for bet which is  not won
        EXPECTED: Icon &amp; result places to be displayed below the event name  for  won but only PLACED
        EXPECTED: **SS**
        EXPECTED: ![](index.php?/attachments/get/7839d6e1-5ade-49d5-8c39-81dcc29c5504)
        """
        pass
