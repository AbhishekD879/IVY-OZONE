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
class Test_C66114016_Verify_in_settled_bets_NumberX_of_Selections_gets_displayed_in_dead_heat_message_that_are_involved_in_dead_heat(Common):
    """
    TR_ID: C66114016
    NAME: Verify in settled bets Number(X) of Selections gets displayed in dead heat message that are involved in dead heat
    DESCRIPTION: This test case Verify in settled bets Number(X) of Selections gets displayed in dead heat message that are involved in dead heat
    PRECONDITIONS: Bets should be available in open/cashout settle tabs
    PRECONDITIONS: Any of the bets should be affected with Dead Heat
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

    def test_003_place_singlemultiple_bets(self):
        """
        DESCRIPTION: Place single/Multiple bets
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

    def test_006_check_the_bets_placed_for_singlemultiples(self):
        """
        DESCRIPTION: Check the bets placed for single/multiples
        EXPECTED: Bets should be available in open tab
        """
        pass

    def test_007_click_on_settle_tab_after_the_above_bets_are_settled(self):
        """
        DESCRIPTION: Click on Settle tab after the above bets are settled
        EXPECTED: Bets should be available in settle tab after settlement
        """
        pass

    def test_008_check_the_bet_has_been_affected_with_dead_heat_for_any_of_the_bets(self):
        """
        DESCRIPTION: Check the bet has been affected with Dead Heat for any of the bets
        EXPECTED: No change in functionality
        EXPECTED: Dead heat Signposting with x selections should display as per Figma deign
        EXPECTED: ![](index.php?/attachments/get/35cf4b5d-afc6-42b6-9c9a-3c1e3dffd104)
        """
        pass
