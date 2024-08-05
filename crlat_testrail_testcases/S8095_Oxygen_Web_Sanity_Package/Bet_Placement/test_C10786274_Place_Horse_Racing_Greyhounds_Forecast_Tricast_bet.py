import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C10786274_Place_Horse_Racing_Greyhounds_Forecast_Tricast_bet(Common):
    """
    TR_ID: C10786274
    NAME: Place Horse Racing/Greyhounds Forecast/Tricast bet
    DESCRIPTION: TO EDIT: TC SHOULD BE SPLIT INTO COUPLE OF SEPARATE TC. HORSE RACING AND GREYHOUNDS CAN NOT BE TESTED IN ONE CASE!!!
    DESCRIPTION: Bet Placement - Verify that the customer can place a Forecast/Tricast Bet on Horse Racing/Greyhounds
    DESCRIPTION: AUTOTEST [C49345817]
    PRECONDITIONS: Forecast and Tricast checkboxes are checked in TI for Horce Racing/Greyhound event (**Event1**)
    PRECONDITIONS: Login to application with positive balance user
    """
    keep_browser_open = True

    def test_001_navigate_to_horse_racing_page_from_the_menuopenevent1horse_racinggreyhounds_eventverify_that_forecasttricast_tabs_are_shown(self):
        """
        DESCRIPTION: Navigate to Horse Racing Page from the Menu
        DESCRIPTION: Open**Event1**Horse Racing/Greyhounds event
        DESCRIPTION: Verify that Forecast/Tricast tabs are shown
        EXPECTED: Forecast/Tricast tabs are shown Horse Racing/Greyhounds event
        """
        pass

    def test_002_navigate_to_forecast_tabselect_1st_and_2nd_runner_and_add_to_betslipnavigate_to_betslipverify_that_forecast_bet_is_added_to_betslip(self):
        """
        DESCRIPTION: Navigate to Forecast tab
        DESCRIPTION: Select 1st and 2nd runner and add to Betslip
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Forecast' bet is added to Betslip
        EXPECTED: Single 'Forecast' bet is added to Betslip
        """
        pass

    def test_003_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        pass

    def test_004_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        pass

    def test_005_select_two_any_runnersnavigate_to_betslipverify_that_reverse_forecast_2_bet_is_added_to_betslip(self):
        """
        DESCRIPTION: Select two 'ANY' runners
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Reverse Forecast 2' bet is added to Betslip
        EXPECTED: Single 'Reverse Forecast 2' bet is added to Betslip
        """
        pass

    def test_006_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        pass

    def test_007_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        pass

    def test_008_select_more_than_two_any_runnersnavigate_to_betslipverify_that_combination_forecast_n_bet_is_added_to_betslip(self):
        """
        DESCRIPTION: Select more than two 'ANY' runners
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Combination Forecast N' bet is added to Betslip
        EXPECTED: Single 'Combination Forecast N' bet is added to Betslip
        EXPECTED: where N is No of selections x next lowest number eg 4 Selections picked 4 x 3 = 12
        """
        pass

    def test_009_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        pass

    def test_010_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        pass

    def test_011_click_on_my_bets_button_from_the_header___select_open_betsverify_that_placed_bets_are_shown(self):
        """
        DESCRIPTION: Click on My Bets button from the header -> Select 'Open Bets'
        DESCRIPTION: Verify that placed bets are shown
        EXPECTED: Forecast, Reverse Forecast and Combination Forecast bets are shown
        """
        pass

    def test_012_navigate_to_horse_racing_page_from_the_menuopenevent1horse_racinggreyhounds_eventnavigate_to_tricast_tabselect_1st_2nd_and_3rd_runner_and_add_to_betslipnavigate_to_betslipverify_that_tricast_bet_is_added_to_betslip(self):
        """
        DESCRIPTION: Navigate to Horse Racing Page from the Menu
        DESCRIPTION: Open**Event1**Horse Racing/Greyhounds event
        DESCRIPTION: Navigate to Tricast tab
        DESCRIPTION: Select 1st, 2nd, and 3rd runner and add to Betslip
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Tricast' bet is added to Betslip
        EXPECTED: Single 'Tricast' bet is added to Betslip
        """
        pass

    def test_013_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        pass

    def test_014_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        pass

    def test_015_select_three_or_more_any_runnersnavigate_to_betslipverify_that_combination_tricast_n_bet_is_added_to_betslip(self):
        """
        DESCRIPTION: Select three or more 'ANY' runners
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that 'Combination Tricast N' bet is added to Betslip
        EXPECTED: Single 'Combination Tricast N' bet is added to Betslip
        EXPECTED: where N is No of selections x next two lowest numbers
        EXPECTED: eg 4 Selections picked 4 x 3 x 2 = 24
        EXPECTED: 5 Selections picked 5 x 4 x 3 = 60 etc.
        """
        pass

    def test_016_add_stake_and_click_on_place_bet_button(self):
        """
        DESCRIPTION: Add Stake and click on 'Place Bet' button
        EXPECTED: - The bet is successfully placed
        EXPECTED: - Bet receipt is shown
        """
        pass

    def test_017_click_on_done_button(self):
        """
        DESCRIPTION: Click on 'Done' button
        EXPECTED: The customer is redirected to the Horse Racing/Greyhounds event details page
        """
        pass

    def test_018_click_on_my_bets_button_from_the_header___select_open_betsverify_that_placed_bets_are_shown(self):
        """
        DESCRIPTION: Click on My Bets button from the header -> Select 'Open Bets'
        DESCRIPTION: Verify that placed bets are shown
        EXPECTED: Tricast and Combination Tricast bets are shown
        """
        pass
