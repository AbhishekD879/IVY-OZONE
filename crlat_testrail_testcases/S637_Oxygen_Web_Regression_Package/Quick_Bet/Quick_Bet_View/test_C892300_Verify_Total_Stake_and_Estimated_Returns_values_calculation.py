import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@vtest
class Test_C892300_Verify_Total_Stake_and_Estimated_Returns_values_calculation(Common):
    """
    TR_ID: C892300
    NAME: Verify 'Total Stake' and 'Estimated Returns' values calculation
    DESCRIPTION: This test case verifies 'Total Stake' and 'Estimated Returns' values calculation on Quick Bet
    PRECONDITIONS: 1.  Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2.  Quick Bet functionality is available for Mobile ONLY
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage in loaded
        """
        pass

    def test_002_add_sport_race_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/ <Race> selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        """
        pass

    def test_003_enter_some_value_in_stake_field(self):
        """
        DESCRIPTION: Enter some value in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        pass

    def test_004_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is equal to Stake value entered
        """
        pass

    def test_005_verify_estimated_returns_value(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' value
        EXPECTED: 'Estimated Returns' value is calculated based on the formula:
        EXPECTED: **stake * Odds** if Odds has a decimal format
        EXPECTED: **(stake* Odds) + stake** - if Odds has fractional  format
        """
        pass

    def test_006_select_ew_option_for_race_selection(self):
        """
        DESCRIPTION: Select 'E/W' option (for <Race> selection)
        EXPECTED: 'E/W' option is selected
        """
        pass

    def test_007_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is calculated based on the formula:
        EXPECTED: **(stake * 2)**
        """
        pass

    def test_008_verify_estimated_returns_value(self):
        """
        DESCRIPTION: Verify 'Estimated Returns' value
        EXPECTED: 'Estimated Returns' is calculated based on the formula:
        EXPECTED: **Est.Returns  = Return1 + Return2**
        EXPECTED: **Return1 = stake*Odds +stake**
        EXPECTED: **Return2 =  (stake * Odds) * (eachnum/eachden) + stake**
        EXPECTED: 'Estimated Returns' value is equal to **N/A** in case of SP priceType selection added to Quick Bet
        """
        pass
