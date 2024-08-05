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
class Test_C58066932_Verify_stake_entering_when_same_selection_is_included_in_Single_W_E_Forecast_Tricast(Common):
    """
    TR_ID: C58066932
    NAME: Verify stake entering when same selection is included in Single W/E, Forecast/Tricast
    DESCRIPTION: This test case verifies whether price selected for Single bet is not duplicated for stake fields in Forecast/Tricast
    PRECONDITIONS: - User is logged in
    PRECONDITIONS: - User is on HR EDP
    """
    keep_browser_open = True

    def test_001_add_single_hr_selection_from_we_market_eg_horse_1_to_betslip(self):
        """
        DESCRIPTION: Add single HR selection from W/E market (eg. 'Horse 1') to Betslip
        EXPECTED: Selection is added to Betslip
        """
        pass

    def test_002_navigate_to_forecast_tab_on_hr_edp_of_same_race_and_add_same_selection_horse_1_as_1st_position_in_forecast_add_bet_to_betslip_as_well(self):
        """
        DESCRIPTION: Navigate to Forecast tab on HR EDP of same race and add same selection ('Horse 1') as 1st position in Forecast, add bet to Betslip as well
        EXPECTED: Forecast bet is added to Betslip
        """
        pass

    def test_003_navigate_to_tricast_tab_on_hr_edp_of_same_race_and_add_same_selection_horse_1_as_1st_position_in_tricast_add_bet_to_betslip_as_well(self):
        """
        DESCRIPTION: Navigate to Tricast tab on HR EDP of same race and add same selection ('Horse 1') as 1st position in Tricast, add bet to Betslip as well
        EXPECTED: Tricast bet is added to Betslip
        """
        pass

    def test_004_in_betslip_insert_price_into_stake_field_for_single_hr_selection_horse_1(self):
        """
        DESCRIPTION: In Betslip insert price into stake field for single HR selection ('Horse 1')
        EXPECTED: Price is inserted only for single selection
        """
        pass

    def test_005_in_ti_trigger_the_price_change_for_single_selection_eg_horse_1_and_check_stake_fields_for_all_bets(self):
        """
        DESCRIPTION: In TI trigger the price change for single selection (eg. 'Horse 1') and check stake fields for all bets
        EXPECTED: - Price is inserted only for single selection
        EXPECTED: - No duplicated prices for Forecast/Tricast bets are present
        """
        pass

    def test_006_refresh_the_page_and_check_stake_fields_for_all_bets_once_again(self):
        """
        DESCRIPTION: Refresh the page and check stake fields for all bets once again
        EXPECTED: - Price is inserted only for single selection
        EXPECTED: - No duplicated prices for Forecast/Tricast bets are present
        """
        pass

    def test_007_repeat_steps_above_for_the_ew_checkbox_ticked_for_single_we_bet(self):
        """
        DESCRIPTION: Repeat steps above for the 'E/W' checkbox ticked for Single W/E bet.
        EXPECTED: 
        """
        pass

    def test_008_repeat_all_steps_for_the_virtual_horse_racing(self):
        """
        DESCRIPTION: Repeat all steps for the Virtual Horse Racing
        EXPECTED: 
        """
        pass
