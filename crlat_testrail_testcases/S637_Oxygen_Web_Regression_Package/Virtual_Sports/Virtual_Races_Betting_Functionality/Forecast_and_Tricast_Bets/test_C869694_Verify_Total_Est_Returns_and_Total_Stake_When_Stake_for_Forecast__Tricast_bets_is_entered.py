import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869694_Verify_Total_Est_Returns_and_Total_Stake_When_Stake_for_Forecast__Tricast_bets_is_entered(Common):
    """
    TR_ID: C869694
    NAME: Verify 'Total Est. Returns' and 'Total Stake'  When Stake for Forecast / Tricast bets is entered
    DESCRIPTION: This test case verifies the calculation of 'Total Est. Returns' and 'Total Stake' values when stake amount is entered for Forecast / Tricast bets for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtul Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Ticket** :
    DESCRIPTION: BMA-9397 'Extend Forecast and Tricast betting to Virtual Sports'
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_the_virtual_race_event_details_page(self):
        """
        DESCRIPTION: Go to the <Virtual Race> event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_add_2_or_more_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add 2 or more selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_004_open_bet_slip(self):
        """
        DESCRIPTION: Open 'Bet Slip'
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_005_go_to_the_forecast__tricast_n_section(self):
        """
        DESCRIPTION: Go to the 'Forecast / Tricast (n)' section
        EXPECTED: 'Forecast / Tricast (n)' section is shown
        """
        pass

    def test_006_enter_stake_amount_manually_in_a_stake_field_for_any_forecast_k_or_tricast_k_etc_bet_and_verify_total_est_returns_and_total_stakefields(self):
        """
        DESCRIPTION: Enter stake amount manually in a 'Stake:' field for any 'Forecast (k)' or 'Tricast (k)' etc. bet and verify** 'Total Est. Returns' and 'Total Stake' **fields
        EXPECTED: *   'Stake field is pre-populated with entered value
        EXPECTED: *   **'Total Est. Returns'** is ALWAYS equal to 'N/A' value no matter what price type of selection is added
        EXPECTED: *   **'Total Stake'** = stake_amount*k,
        EXPECTED: where:
        EXPECTED: k - the number of combinations/outcomes contained in the forecast / tricast bet
        EXPECTED: stake_amount - the stake which is entered manually
        """
        pass

    def test_007_log_out_and_log_in_with_user_who_has_free_bets_available(self):
        """
        DESCRIPTION: Log out and log in with user who has free bets available
        EXPECTED: User is logged in
        """
        pass

    def test_008_enter_stake_via_free_bets_and_verify_total_est_returns_and_total_stake_fields(self):
        """
        DESCRIPTION: Enter stake via free bets and verify **'Total Est. Returns' **and** 'Total Stake' **fields
        EXPECTED: 'Stake:' field is NOT pre-populated with a value selected in free bet drop-down
        EXPECTED: **'Total Est. Returns'** is ALWAYS equal to 'N/A' value no matter what price type of selection is added
        EXPECTED: **'Total Stake'** = free_bet,
        EXPECTED: where free_bet - free bet amount selected in the drop down
        """
        pass

    def test_009_enter_stake_via_free_bets_and_enter_stake_manually___verifytotal_est_returnsandtotal_stakefields(self):
        """
        DESCRIPTION: Enter stake via free bets AND enter stake manually -> verify **'Total Est. Returns' **and** 'Total Stake' **fields
        EXPECTED: *   'Stake:' field is pre-populated with entered value
        EXPECTED: *   **'Total Est. Returns'** is ALWAYS equal to 'N/A' value no matter what price type of selection is added
        EXPECTED: *   **'Total Stake'** = free\_bet + stake\_amount*k
        EXPECTED: where:
        EXPECTED: k - the number of combinations/outcomes contained in the forecast / tricast bet
        EXPECTED: stake_amount - the stake which is entered manually
        """
        pass
