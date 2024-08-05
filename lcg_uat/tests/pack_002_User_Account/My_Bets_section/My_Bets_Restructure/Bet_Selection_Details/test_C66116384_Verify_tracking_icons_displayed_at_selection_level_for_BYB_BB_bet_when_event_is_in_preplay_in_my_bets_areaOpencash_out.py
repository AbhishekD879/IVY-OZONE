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
class Test_C66116384_Verify_tracking_icons_displayed_at_selection_level_for_BYB_BB_bet_when_event_is_in_preplay_in_my_bets_areaOpencash_out(Common):
    """
    TR_ID: C66116384
    NAME: Verify  tracking icons displayed at selection level for BYB/BB bet when event is in preplay in my bets area(Open,cash out)
    DESCRIPTION: This testcase verifies tracking icons displayed at selection level for BYB/BB bet when event is in preplay in my bets area(Open,cash out)
    PRECONDITIONS: BYB/BB bet preplay event should be available in Open,Cashout tab
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
        EXPECTED: BYB/BB should be diasplayed with all the bet details
        """
        pass

    def test_004_verify_tracking_for_bybbb_bet_in_open_tab(self):
        """
        DESCRIPTION: Verify tracking for BYB/BB bet in open tab
        EXPECTED: Tracking should be displayed in grey color as per figma
        """
        pass

    def test_005_verify_tracking_for_bybbb_in_cash_out_tabif_availbale(self):
        """
        DESCRIPTION: Verify tracking for BYB/BB in Cash out tab(if availbale)
        EXPECTED: Tracking should be displayed in grey color as per figma
        """
        pass
