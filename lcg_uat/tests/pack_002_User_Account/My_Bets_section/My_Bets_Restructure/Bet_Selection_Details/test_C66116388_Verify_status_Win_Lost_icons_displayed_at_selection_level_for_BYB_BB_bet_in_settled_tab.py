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
class Test_C66116388_Verify_status_Win_Lost_icons_displayed_at_selection_level_for_BYB_BB_bet_in_settled_tab(Common):
    """
    TR_ID: C66116388
    NAME: Verify  status (Win/Lost) icons displayed at selection level for BYB/BB bet in settled tab
    DESCRIPTION: This testcase verifies  status (Win/Lost) icons displayed at selection level for BYB/BB bet in settled tab
    PRECONDITIONS: BYB/BB bet should be available in Open,Cashout tab
    """
    keep_browser_open = True

    def test_000_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_001_login_to_the_application_with_valid_credentials_with_precondition(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition
        EXPECTED: User is logged in
        """
        pass

    def test_002_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_003_verify_bybbb_bet_displayed_in_open_tab(self):
        """
        DESCRIPTION: Verify BYB/BB bet displayed in open tab
        EXPECTED: BYB/BB  bet should be diasplayed with all the bet details
        """
        pass

    def test_004_verify_tracking_of_bybbb_bet_when_the_event_is_resultedwonlost(self):
        """
        DESCRIPTION: Verify tracking of BYB/BB bet when the event is resulted(Won/Lost)
        EXPECTED: Either tick or cross icons should be displayed on bet header in settled tab
        """
        pass
