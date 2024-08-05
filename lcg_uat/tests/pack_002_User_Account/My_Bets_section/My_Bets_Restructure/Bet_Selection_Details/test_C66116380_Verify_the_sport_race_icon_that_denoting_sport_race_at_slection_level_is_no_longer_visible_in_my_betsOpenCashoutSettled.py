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
class Test_C66116380_Verify_the_sport_race_icon_that_denoting_sport_race_at_slection_level_is_no_longer_visible_in_my_betsOpenCashoutSettled(Common):
    """
    TR_ID: C66116380
    NAME: Verify the sport/race icon that denoting sport/race at slection level is no longer visible in my bets(Open,Cashout,Settled)
    DESCRIPTION: This testcase verifies the sport/race icon that denoting sport/race at slection level is no longer visible in my bets(Open,Cashout,Settled)
    PRECONDITIONS: 
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

    def test_002_add_sport_selections_to_betslip_and_place_bet(self):
        """
        DESCRIPTION: Add sport selections to betslip and place bet
        EXPECTED: Bet is placed successfully
        """
        pass

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_the_bet_palced_in_step_3_in_open_tab(self):
        """
        DESCRIPTION: Verify the bet palced in step 3 in open tab
        EXPECTED: Bet should be dispayed in open tab
        """
        pass

    def test_005_verify_the_bet_selection_area_in_open_tab(self):
        """
        DESCRIPTION: Verify the bet selection area in open tab
        EXPECTED: sport icon that denoting sport at slection level is no longer visible in open tab
        """
        pass

    def test_006_verify_the_bet_selection_area_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify the bet selection area in Cash out tab
        EXPECTED: sport icon that denoting sport at slection level is no longer visible in Cash out tab
        """
        pass

    def test_007_verify_the_bet_selection_area_in_settled_tab_once_it_is_resulted(self):
        """
        DESCRIPTION: Verify the bet selection area in Settled tab once it is resulted
        EXPECTED: sport icon that denoting sport at slection level is no longer visible in settled tab
        """
        pass

    def test_008_repeat__step_3_to_step_8_for_multiplecomplex_bets(self):
        """
        DESCRIPTION: Repeat  step 3 to step 8 for multiple/complex bets
        EXPECTED: Result should be same
        """
        pass

    def test_009_repeat__step_3_to_step_8_for_races(self):
        """
        DESCRIPTION: Repeat  step 3 to step 8 for races
        EXPECTED: Result should be same
        """
        pass

    def test_010_repeat__step_3_to_step_8_for_pools(self):
        """
        DESCRIPTION: Repeat  step 3 to step 8 for pools
        EXPECTED: Result should be same
        """
        pass

    def test_011_repeat__step_3_to_step_8_for_5a_side(self):
        """
        DESCRIPTION: Repeat  step 3 to step 8 for 5A side
        EXPECTED: Result should be same
        """
        pass

    def test_012_repeat__step_3_to_step_8_for_bybbb(self):
        """
        DESCRIPTION: Repeat  step 3 to step 8 for BYB/BB
        EXPECTED: Result should be same
        """
        pass
