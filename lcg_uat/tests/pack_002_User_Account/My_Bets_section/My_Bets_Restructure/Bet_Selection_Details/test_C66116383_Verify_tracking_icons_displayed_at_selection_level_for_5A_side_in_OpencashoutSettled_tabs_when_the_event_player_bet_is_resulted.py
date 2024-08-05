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
class Test_C66116383_Verify_tracking_icons_displayed_at_selection_level_for_5A_side_in_OpencashoutSettled_tabs_when_the_event_player_bet_is_resulted(Common):
    """
    TR_ID: C66116383
    NAME: Verify  tracking icons displayed at selection level for 5A side in Open,cashout,Settled tabs when the event/player bet is resulted
    DESCRIPTION: This testcase tracking icons displayed at selection level for 5A side in settled tab when the event is resulted
    PRECONDITIONS: 5A side bet should be available in Open,Cashout tab
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

    def test_003_verify_5a_side_bet_displayed_in_open_tab(self):
        """
        DESCRIPTION: Verify 5A side bet displayed in open tab
        EXPECTED: 5A side be should be diasplayed with all the bet details
        """
        pass

    def test_004_verify_tracking_of_5a_side_event_when_any_of_the_player_bets_resultedwonlost(self):
        """
        DESCRIPTION: Verify tracking of 5A side event when any of the player bets resulted(Won/Lost)
        EXPECTED: Either tick or cross icons should be displayed for the respective player bets on open tab
        """
        pass

    def test_005_repeat_step_5_in_cash_out_tab_if_available(self):
        """
        DESCRIPTION: Repeat step 5 in Cash out tab (if available)
        EXPECTED: Result should be same
        """
        pass

    def test_006_verify_5a_side_bet_displayed_in_settled_tab_once_the_event_is_resulted(self):
        """
        DESCRIPTION: Verify 5A side bet displayed in Settled tab once the event is resulted
        EXPECTED: Either tick or cross icons should be displayed for the respective player bets on settled tab
        """
        pass
