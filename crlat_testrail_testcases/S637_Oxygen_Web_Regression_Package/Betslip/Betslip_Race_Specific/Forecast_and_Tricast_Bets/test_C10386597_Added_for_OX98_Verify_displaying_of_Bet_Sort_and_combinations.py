import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C10386597_Added_for_OX98_Verify_displaying_of_Bet_Sort_and_combinations(Common):
    """
    TR_ID: C10386597
    NAME: [Added for OX98] Verify displaying of Bet Sort and combinations
    DESCRIPTION: This test case verifies displaying of Bet Sort and combinations for Forecast/Tricast in Betslip
    PRECONDITIONS: Load app and login with user
    PRECONDITIONS: Navigate to HR page and open any event
    PRECONDITIONS: Select the 'Forecast' tab
    PRECONDITIONS: Note: This test case should be run for HR and for Greyhounds
    """
    keep_browser_open = True

    def test_001_select_two_selection_from_any_placetap_add_to_betslip_and_navigate_to_betslipverify_that_reverse_forecast2_bet_is_shown_in_betslip(self):
        """
        DESCRIPTION: Select two selection from **ANY** Place
        DESCRIPTION: Tap 'Add to Betslip' and navigate to Betslip
        DESCRIPTION: Verify that 'Reverse Forecast(2)' bet is shown in Betslip
        EXPECTED: Bet is shown under SINGLES with appropriate elements:
        EXPECTED: - Remove button
        EXPECTED: - 'Stake' field
        EXPECTED: - Runners information according to selected runners (NOTE: Numbers for runner's place is not shown)
        EXPECTED: e.g. :  HorseDan
        EXPECTED: HorseTed
        EXPECTED: - Bet Sort: **Reverse Forecast 2**
        EXPECTED: - **From OX99** Event name and time
        EXPECTED: - Total Stake information
        EXPECTED: - Total Est. Returns information is displayed as 0 (zero) (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: - 'Place Bet' button
        """
        pass

    def test_002_navigate_back_to_forecast_tabselect_3_or_more_selections_from_any_placetap_add_to_betslip_and_navigate_to_betslipverify_that_combination_forecast_n_bet_is_shown_in_betslipnote_calculation_of_n_no_of_selections_x_next_lowest_number_eg_4_selections_picked_4_x_3__12(self):
        """
        DESCRIPTION: Navigate back to 'Forecast' tab
        DESCRIPTION: Select 3 or more selections from **ANY** Place
        DESCRIPTION: Tap 'Add to Betslip' and navigate to Betslip
        DESCRIPTION: Verify that 'Combination Forecast <N>' bet is shown in Betslip
        DESCRIPTION: Note: Calculation of N: No of selections x next lowest number eg 4 Selections picked 4 x 3 = 12
        EXPECTED: One more bet is shown under SINGLES with appropriate elements:
        EXPECTED: - Remove button
        EXPECTED: - 'Stake' field
        EXPECTED: - Runners information according to selected runners (NOTE: Numbers for runner's place is not shown)
        EXPECTED: e.g. :  HorseDan
        EXPECTED: HorseTed
        EXPECTED: HourseTest (Quantity of runners names equal to added 'ANY place' selections)
        EXPECTED: - Bet Sort: **Combination Forecast <N>**
        EXPECTED: - **From OX99** Event name and time
        EXPECTED: - Total Stake information
        EXPECTED: - Total Est. Returns information is displayed as 0 (zero) (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: - 'Place Bet' button
        """
        pass

    def test_003_navigate_to_tricast_tabselect_3_or_more_selections_from_any_placetap_add_to_betslip_and_navigate_to_betslipverify_that_combination_tricast_n_bet_is_shown_in_betslip(self):
        """
        DESCRIPTION: Navigate to 'Tricast' tab
        DESCRIPTION: Select 3 or more selections from **ANY** Place
        DESCRIPTION: Tap 'Add to Betslip' and navigate to Betslip
        DESCRIPTION: Verify that 'Combination Tricast <N>' bet is shown in Betslip
        EXPECTED: One more bet is shown under SINGLES with appropriate elements:
        EXPECTED: - Remove button
        EXPECTED: - 'Stake' field
        EXPECTED: - Runners information according to selected runners (NOTE: Numbers for runner's place is not shown)
        EXPECTED: e.g. :  HorseDan
        EXPECTED: HorseTed
        EXPECTED: HourseTest (Quantity of runners names equal to added 'ANY place' selections)
        EXPECTED: - Bet Sort: **Combination Tricast <N>**
        EXPECTED: - **From OX99** Event name and time
        EXPECTED: - Total Stake information
        EXPECTED: - Total Est. Returns information is displayed as 0 (zero) (**From OX99** Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: - 'Place Bet' button
        """
        pass
