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
class Test_C66116382_Verify_tracking_icons_displayed_at_selection_level_for_5A_side_when_the_match_is_live_in_my_bets_areaOpencash_out(Common):
    """
    TR_ID: C66116382
    NAME: Verify  tracking icons displayed at selection level for 5A side when the match is live in my bets area(Open,cash out)
    DESCRIPTION: This testcase verifies tracking icons displayed at selection level for 5A side when the match is live in my bets area(Open,cash out)
    PRECONDITIONS: 5A side bet on inplay event should be available in Open,Cashout tab
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

    def test_004_verify_tracking_for_5a_side_event_in_open_tab(self):
        """
        DESCRIPTION: Verify tracking for 5A side event in open tab
        EXPECTED: Tracking should be displayed in up and down arrows as per figma
        """
        pass

    def test_005_verify_tracking_for_5a_side_event_in_cash_out_tabif_availbale(self):
        """
        DESCRIPTION: Verify tracking for 5A side event in Cash out tab(if availbale)
        EXPECTED: Tracking should be displayed in up and down arrows as per figma
        """
        pass
