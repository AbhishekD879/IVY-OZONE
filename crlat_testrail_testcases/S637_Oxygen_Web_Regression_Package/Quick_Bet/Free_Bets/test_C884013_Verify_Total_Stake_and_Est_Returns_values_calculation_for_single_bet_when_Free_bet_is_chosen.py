import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C884013_Verify_Total_Stake_and_Est_Returns_values_calculation_for_single_bet_when_Free_bet_is_chosen(Common):
    """
    TR_ID: C884013
    NAME: Verify 'Total Stake' and 'Est. Returns' values calculation for single bet when Free bet is chosen
    DESCRIPTION: Update: Requires calrificaiton on how to calculate est. returns for Each way bet
    DESCRIPTION: This test case verifies 'Stake' and 'Est. Returns' values calculation for single bet when Free bet is chosen
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. The user is logged in and has free bets added
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: * [How to add Free bets to user`s account] [1]
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    """
    keep_browser_open = True

    def test_001_add_sportraceselection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/<Race>selection to Quick Bet
        EXPECTED: * Quick Bet is displayed at the bottom of the page
        EXPECTED: * "Use Free Bet" link is displayed under event name
        """
        pass

    def test_002_tap_use_free_bet_link_and_select_free_bet_from_the_pop_up(self):
        """
        DESCRIPTION: Tap "Use Free Bet" link and select Free bet from the pop-up
        EXPECTED: Free bet is selected
        """
        pass

    def test_003_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is equal to Free bet value chosen
        """
        pass

    def test_004_verify_est_returnscoralpotential_returnsladbrokes_value(self):
        """
        DESCRIPTION: Verify 'Est. Returns'(Coral)/'Potential Returns'(Ladbrokes) value
        EXPECTED: 'Est. Returns'/'Potential Returns'value is calculated based on the formula:
        EXPECTED: **free_bet * Odds - free_bet** if Odds has a decimal format
        EXPECTED: **free_bet * ((priceNum/priceDen)+1) - free_bet** - if Odds has fractional  format
        """
        pass

    def test_005_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Stake' field is populated with value
        """
        pass

    def test_006_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is equal to Free bet value chosen + Stake value entered
        EXPECTED: *[From OX100]*
        EXPECTED: 2 values are displayed in 'Total Stake' : FB £X.XX + £X.XX [value of stake]
        """
        pass

    def test_007_verify_est_returnscoralpotential_returnsladbrokes_value(self):
        """
        DESCRIPTION: Verify 'Est. Returns'(Coral)/'Potential Returns'(Ladbrokes) value
        EXPECTED: 'Est. Returns'/'Potential Returns' value is calculated based on the formula:
        EXPECTED: **(free_bet + stake) * ((priceNum/priceDen)+1) - free_bet** - if Odds has fractional  format
        EXPECTED: **(free_bet + stake) * Odds - free_bet** - if Odds has decimal  format
        EXPECTED: where
        EXPECTED: free_bet - a selected free bet amount
        EXPECTED: stake - stake amount which is entered manually
        EXPECTED: Odds - a fractional displaying of Price/Odds button
        """
        pass

    def test_008_select_ew_option_for_race_selection(self):
        """
        DESCRIPTION: Select 'E/W' option (for <Race> selection)
        EXPECTED: 'E/W' option is selected
        """
        pass

    def test_009_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is calculated based on the formula:
        EXPECTED: **free_bet + (stake * 2)**
        EXPECTED: *[From OX100]*
        EXPECTED: 2 values are displayed in 'Total Stake' : FB £X.XX + £X.XX [stake * 2]
        """
        pass

    def test_010_verify_est_returnscoralpotential_returnsladbrokes_value(self):
        """
        DESCRIPTION: Verify 'Est. Returns'(Coral)/'Potential Returns'(Ladbrokes) value
        EXPECTED: 'Est. Returns'/'Potential Returns' value is calculated based on the formula:
        EXPECTED: **Est.Returns = Return1 + Return2**
        EXPECTED: **Return1 = (stake + (1/2 * freebet)) * Odds + (stake + (1/2 * free_bet)) - free_bet**
        EXPECTED: **Return2 = (stake + (1/2 * free_bet)) * Odds * (eachnum/eachden) + (stake + (1/2 * free_bet))**
        EXPECTED: 'Est. Returns'/'Potential Returns' value is equal to **N/A** in case of SP priceType selection added to Quick Bet
        """
        pass

    def test_011_remove_value_from_stake_field(self):
        """
        DESCRIPTION: Remove value from 'Stake' field
        EXPECTED: 'Total Stake' field is empty
        EXPECTED: *[From OX100]*
        EXPECTED: FB £X.XX is displayed in 'Total Stake'
        """
        pass

    def test_012_verify_est_returnscoralpotential_returnsladbrokes_value(self):
        """
        DESCRIPTION: Verify 'Est. Returns'(Coral)/'Potential Returns'(Ladbrokes) value
        EXPECTED: 'Est. Returns'/'Potential Returns' value is calculated based on the formula:
        EXPECTED: **Est.Returns = Return1 + Return2**
        EXPECTED: **Return1 = (1/2 * freebet) * Odds +(1/2 * free_bet) - freebet**
        EXPECTED: **Return2 = (1/2 * freebet) * Odds * (eachnum/eachden) + (1/2 * freebet)**
        EXPECTED: 'Est. Returns'/'Potential Returns' value is equal to **N/A** in case of SP priceType selection added to Quick Bet
        """
        pass
