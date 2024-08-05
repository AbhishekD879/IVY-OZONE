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
class Test_C66116386_Verify_tracking_icons_displayed_at_selection_level_for_BYB_BB_bet_in_OpencashoutSettled_tabs_when_the_event_market_is_resulted(Common):
    """
    TR_ID: C66116386
    NAME: Verify  tracking icons displayed at selection level for BYB/BB bet in Open,cashout,Settled tabs when the event/market is resulted
    DESCRIPTION: This testcase tracking icons displayed at selection level for BYB/BB bet in settled tab when the event is resulted
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

    def test_004_verify_tracking_of_bybbb_bet_when_any_of_the_market_is_resultedwonlost(self):
        """
        DESCRIPTION: Verify tracking of BYB/BB bet when any of the market is resulted(Won/Lost)
        EXPECTED: Either tick or cross icons should be displayed for the respective markets in open tab
        """
        pass

    def test_005_repeat_step_5_in_cash_out_tab_if_available(self):
        """
        DESCRIPTION: Repeat step 5 in Cash out tab (if available)
        EXPECTED: Result should be same
        """
        pass

    def test_006_verify_bybbb_bet_displayed_in_settled_tab_once_the_event_is_resulted(self):
        """
        DESCRIPTION: Verify BYB/BB bet displayed in Settled tab once the event is resulted
        EXPECTED: Either tick or cross icons Should be displayed for the respective markets in settled tab
        """
        pass
