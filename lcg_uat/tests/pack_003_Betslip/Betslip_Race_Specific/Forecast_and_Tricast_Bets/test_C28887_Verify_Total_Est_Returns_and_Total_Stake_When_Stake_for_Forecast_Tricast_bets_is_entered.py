import re
import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl  # need user with freebet for prod
# @pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.forecast_tricast
@pytest.mark.high
@pytest.mark.login
@pytest.mark.freebets
@vtest
class Test_C28887_Verify_Total_Est_Returns_and_Total_Stake_When_Stake_for_Forecast_Tricast_bets_is_entered(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C28887
    NAME: Verify 'Total Est. Returns' and 'Total Stake' When Stake for Forecast / Tricast bets is entered
    DESCRIPTION: This test case verifies the calculation of 'Total Est. Returns' and 'Total Stake' values when stake amount is entered for Forecast / Tricast bets.
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def enter_forecast_tricast_values_and_verify_fields(self, freebet=False, enter_stake=False):
        """
        This method fills forecast/tricast stake and free bet fields and verifies the outcomes
        :param freebet: True or False - use free bet available
        :param enter_stake: True or False - enter stake value or not
        :return: None
        """
        betslip = self.get_betslip_content()
        forecast_tricast_section = list(self.get_betslip_sections().Singles.items())
        for forecast_tricast_stake in forecast_tricast_section:
            stake_name, stake = forecast_tricast_stake
            stake.amount_form.enter_amount('')
            if freebet and enter_stake:
                selected_freebet = self.select_freebet_for_stake(stake=forecast_tricast_stake)
                freebet_stake = float(re.search(r'\d+.\d+', selected_freebet).group())
                self.enter_stake_amount(stake=forecast_tricast_stake)
                expected_total_stake = f'{"{0:.2f}".format(freebet_stake)} + {float(stake.amount_form.input.value)}'
                self.assertTrue(wait_for_result(lambda: betslip.total_stake == expected_total_stake,
                                                name='Total stake to update',
                                                timeout=3),
                                msg=f'Actual Total Stake: "{betslip.total_stake}" is not as expected: "{expected_total_stake}"')
            elif freebet:
                selected_freebet = self.select_freebet_for_stake(stake=forecast_tricast_stake)
                freebet_stake = float(re.search(r'\d+.\d+', selected_freebet).group())
                expected_total_stake = "{0:.2f}".format(freebet_stake)
                self.assertTrue(wait_for_result(lambda: str(float(betslip.total_stake)) == str(float(expected_total_stake)),
                                                name='Total stake to update',
                                                timeout=3),
                                msg=f'Actual Total Stake: "{betslip.total_stake}" is not as expected: "{expected_total_stake}"')
            else:
                self.enter_stake_amount(stake=forecast_tricast_stake)
                self.assertTrue(wait_for_result(lambda: str(float(betslip.total_stake)) == str(float(stake.amount_form.input.value)),
                                                name='Total stake to update',
                                                timeout=3),
                                msg=f'Actual Total Stake: "{betslip.total_stake}" is not as expected: "{stake.amount_form.input.value}"')
            total_est_returns = betslip.total_estimate_returns
            self.assertEqual(total_est_returns, 'N/A',
                             msg=f'Actual Total Est. Returns: "{total_est_returns}" is not as expected: "N/A"')
            if freebet:
                stake.remove_free_bet_link.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        EXPECTED: Events are created
        """

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=3,
                                                          forecast_available=True,
                                                          tricast_available=True)
        self.__class__.eventID = event_params.event_id

        self.site.login()
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', tricast=True)

    def test_001_open_bet_slip(self):
        """
        DESCRIPTION: Open 'BetSlip'
        DESCRIPTION: Verify that Est. Returns is N/A and Total Est. Returns is 0.00
        EXPECTED: Bet Slip is opened
        EXPECTED: Est. Returns is N/A
        EXPECTED: Total Est. Returns is 0.00
        """
        self.site.open_betslip()
        betslip = self.get_betslip_content()
        total_est_returns = betslip.total_estimate_returns
        self.assertEqual(total_est_returns, "0.00",
                         msg=f'Actual Total Est. Returns: "{total_est_returns}" is not as expected: "0.00"')

    def test_002_enter_stake_amount_manually(self):
        """
        DESCRIPTION: Enter stake amount manually in a 'Stake:' field for any 'Forecast (k)' or 'Tricast (k)' etc. bet and verify 'Total Est. Returns' and 'Total Stake' fields
        EXPECTED: 'Stake' field is pre-populated with entered value
        EXPECTED: 'Total Est. Returns' is ALWAYS equal to 'N/A' value no matter what price type of selection is added
        EXPECTED: 'Total Stake' = stake_amount*k, where: k - the number of combinations/outcomes contained in the forecast / tricast bet stake_amount - the stake which is entered manually
        """
        self.enter_forecast_tricast_values_and_verify_fields()

    def test_003_log_out_and_log_in_with_user_who_has_free_bets_available(self):
        """
        DESCRIPTION: Log out and log in with user who has free bets available
        EXPECTED: User is logged in
        """
        self.clear_betslip()
        self.site.logout()
        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', forecast=True)
        self.site.open_betslip()

    def test_004_enter_stake_via_free_bets(self):
        """
        DESCRIPTION: Enter stake via free bets and verify **'Total Est. Returns'** and **'Total Stake'** fields
        EXPECTED: 'Stake' field is NOT pre-populated with a value selected in free bet drop-down
        EXPECTED: **'Total Est. Returns'** is ALWAYS equal to 'N/A' value
        EXPECTED: no matter what price type of selection is added
        EXPECTED: **'Total Stake'** = free_bet,
        EXPECTED: where free_bet - free bet amount selected in the drop down
        """
        self.enter_forecast_tricast_values_and_verify_fields(freebet=True)

    def test_005_enter_stake_via_free_bets_and_enter_stake_manually(self):
        """
        DESCRIPTION: Enter stake via free bets AND enter stake manually ->
        DESCRIPTION: verify **'Total Est. Returns'** and **'Total Stake'** fields
        EXPECTED: *   'Stake' field is pre-populated with entered value
        EXPECTED: *   **'Total Est. Returns'** is ALWAYS equal to 'N/A' value
        EXPECTED:     no matter what price type of selection is added
        EXPECTED: *   **'Total Stake'** = free_bet + stake_amount*k
        EXPECTED: where:
        EXPECTED: k - the number of combinations/outcomes contained in the forecast / tricast bet
        EXPECTED: free_bet - free bet amount selected in the drop down
        EXPECTED: stake_amount - the stake which is entered manually
        """
        self.enter_forecast_tricast_values_and_verify_fields(freebet=True, enter_stake=True)
