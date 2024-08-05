import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C44870200_Verify_the_selection_availability_when_viewing_the_racecard_Forecast_and_tricast_displayed_in_separate_tab_Check_only_two_Selections_are_highligted_for_forecast_and_three_for_tricast_And_any_option_available_for_both_foirecast_and_tricast_Veri(Common):
    """
    TR_ID: C44870200
    NAME: "Verify the selection availability when viewing the racecard -Forecast and tricast displayed in separate tab -Check only two Selections are highligted for forecast and three for tricast ...And any option available for both foirecast and tricast -Veri
    DESCRIPTION: "Verify the selection availability when viewing the racecard
    DESCRIPTION: -Forecast and tricast displayed in separate tab
    DESCRIPTION: -Check only two Selections are highligted for forecast and three for tricast ...And any option available for both foirecast and tricast
    DESCRIPTION: -Verify that the non-runners shouldnot be shown in forecast and tricast tabs
    DESCRIPTION: - Check bet placement is working fine and display of betslip and betreceipt"
    PRECONDITIONS: Login into Application
    PRECONDITIONS: Navigate to 'HR/Greyhounds' page
    PRECONDITIONS: Choose event -> see that Ferecast/Tricast Tab is available
    PRECONDITIONS: Navigate to Ferecast/Tricast Tab
    """
    keep_browser_open = True

    def test_001_verify_the_selection_availability_when_viewing_the_racecard_for_forecast(self):
        """
        DESCRIPTION: Verify the selection availability when viewing the racecard for forecast
        EXPECTED: Only two selections should be  highligted for forecast
        EXPECTED: And any option available
        """
        pass

    def test_002_verify_the_selection_availability_when_viewing_the_racecard_for_forecast(self):
        """
        DESCRIPTION: Verify the selection availability when viewing the racecard for forecast
        EXPECTED: Only three selections should  be highligted for tricast
        EXPECTED: And any option available
        """
        pass

    def test_003_verify_that_the_non_runners_shouldnot_be_shown_in_forecast_and_tricast_tabs(self):
        """
        DESCRIPTION: Verify that the non-runners shouldnot be shown in forecast and tricast tabs
        EXPECTED: 
        """
        pass

    def test_004_select_forecast_tab(self):
        """
        DESCRIPTION: Select 'Forecast' tab
        EXPECTED: Forecast tab is selected
        """
        pass

    def test_005_select_1st_and_2nd_runners(self):
        """
        DESCRIPTION: Select '1st' and '2nd' runners
        EXPECTED: 1st and 2nd selections are highlighted
        """
        pass

    def test_006_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap 'Add to Betslip' button
        EXPECTED: Selections are added to betslip
        """
        pass

    def test_007_navigate_to_betslipverify_that_forecast_single_bet_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Forecast Single bet is shown
        EXPECTED: Forecast bet is shown under SINGLES with appropriate elements:
        EXPECTED: 'Remove' button
        EXPECTED: 'Stake' field
        EXPECTED: Bet selection (Runners) information according to selected runners. e.g. : 1 HorseDan 2 HorseTed From OX99: 1st HorseDan 2nd HorseTed
        EXPECTED: Event name and time
        EXPECTED: Bet Sort: Forecast
        EXPECTED: Total Stake information
        EXPECTED: Coral: Estimated Returns; Ladbrokes: Potential Returns'
        EXPECTED: 'Place Bet' button
        EXPECTED: NOTE: No singles selections are added to Betslip - only Forecast is added to Betslip
        """
        pass

    def test_008_add_a_stakeverify_that_total_est_returns_is_displayed_na(self):
        """
        DESCRIPTION: Add a Stake
        DESCRIPTION: Verify that Total Est. Returns is displayed N/A
        EXPECTED: The stake is added and shown in the 'Stake' and 'Total Stake' fields
        EXPECTED: ( Coral: Estimated Returns; Ladbrokes: Potential Returns')
        """
        pass

    def test_009_select_tricast_tab(self):
        """
        DESCRIPTION: Select 'Tricast' tab
        EXPECTED: Tricast tab is selected
        """
        pass

    def test_010_select_1st_2nd_and_3rd_runners(self):
        """
        DESCRIPTION: Select '1st', '2nd' and '3rd' runners
        EXPECTED: 1st , 2nd and 3rd selections are highlighted
        """
        pass

    def test_011_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap 'Add to Betslip' button
        EXPECTED: Selections are added to betslip
        """
        pass

    def test_012_navigate_to_betslipverify_that_tricast_single_bet_is_shown(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that Tricast Single bet is shown
        EXPECTED: Tricast bet is shown under SINGLES with appropriate elements:
        EXPECTED: Remove button
        EXPECTED: 'Stake' field
        EXPECTED: Bet selection (Runners) information according to selected runners. e.g. : 1 HorseDan 2 HorseTed 3 HourseBen : 1st HorseDan 2nd HorseTed 3rd HourseBen
        EXPECTED: Event name and time
        EXPECTED: Bet Sort: Tricast
        EXPECTED: Total Stake information
        EXPECTED: Coral: Estimated Returns; Ladbrokes: Potential Returns')
        EXPECTED: 'Place Bet' button
        EXPECTED: NOTE: No singles selections are added to Betslip - only Tricast is added to Betslip
        """
        pass

    def test_013_add_a_stakeverify_that_total_est_returns_is_displayed_na(self):
        """
        DESCRIPTION: Add a Stake
        DESCRIPTION: Verify that Total Est. Returns is displayed N/A
        EXPECTED: The stake is added and shown in the 'Stake' and 'Total Stake' fields
        EXPECTED: Total Est. Returns information displayed as N/A ( Coral: Estimated Returns; Ladbrokes: Potential Returns')
        """
        pass
