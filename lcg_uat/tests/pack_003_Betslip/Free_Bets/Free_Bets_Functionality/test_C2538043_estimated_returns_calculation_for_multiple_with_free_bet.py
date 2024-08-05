import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't grant freebets on prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.freebets
@pytest.mark.est_returns
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C2538043_EstimatedReturnsCalculationForMultipleWithFreeBet(BaseBetSlipTest):
    """
    TR_ID: C2538043
    NAME: Estimated Returns Calculation For Multiple with Free Bet
    PRECONDITIONS: Make sure user has free bets available.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as a user which has free bets available.
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = event.selection_ids
        self.__class__.first_selection = event.team1

        second_event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.second_selection_ids = second_event.selection_ids
        self.__class__.second_selection = second_event.team1
        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)

    def test_001_add_several_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add several selections from different events to the Bet Slip
        EXPECTED: Selections are added
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.first_selection],
                                                         self.second_selection_ids[self.second_selection]))

    def test_002_go_to_multiples_section(self):
        """
        DESCRIPTION: Go to 'Multiples' section
        """
        self.__class__.multiples_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(self.multiples_section, msg='Multiples section is not displayed.')

    def test_003_select_free_bet_from_the_drop_down(self):
        """
        DESCRIPTION: Select free bet from the dropdown
        EXPECTED: *  Free bet is chosen
        EXPECTED: *  'Stake' field is empty
        """
        self.__class__.stake_name, self.__class__.stake = list(self.multiples_section.items())[0]
        self._logger.info('*** Verifying stake "%s"' % self.stake_name)

        self.__class__.odds = self.stake.odds

        self.stake.use_free_bet_link.click()
        self.__class__.freebet_stake = self.select_free_bet()

        self.assertEqual(self.stake.amount_form.input.value, '', msg='"Stake" input field should remain empty')

    def test_004_verify_total_est_returns_value(self):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: **'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: **freebet * bets[i].payout.potential - freebet **
        EXPECTED: *   bets[i].payout.potential attribute is taken from 'builtBet' responce;
        EXPECTED: *   'i' - number of corresponding multiple bet;
        EXPECTED: *   id = 'symbol of bet type' (e.g. id  = 'DBL' - double, 'TBL' - treble).
        EXPECTED: NOTE: for each multiple bet type there are two identical lines with id. One of them is calculated with 'Each way' option, second - without. Take into consideration line where is id calculated without 'Each way' option
        """
        self.verify_estimated_returns(
            est_returns=float(self.get_betslip_content().total_estimate_returns),
            odds=self.odds, bet_amount=0, freebet_amount=float(self.freebet_stake)
        )

    def test_005_select_free_bet_option_and_enter_stake_amount_manually(self):
        """
        DESCRIPTION: Select free bet option and enter stake amount manually
        EXPECTED: *  Free bet is selected
        EXPECTED: *  Entered stake is displayed in the 'Stake' field
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        self.assertEqual(self.stake.amount_form.input.value, str(self.bet_amount),
                         msg=f'"Stake" input field should contain just entered value: {self.bet_amount}. '
                             f'Current value is {self.stake.amount_form.input.value}')

    def test_006_verify_total_est_returns_value(self):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: **'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: **(freebet + stake) * bets[i].payout.potential - freebet **
        """
        self.verify_estimated_returns(
            est_returns=float(self.get_betslip_content().total_estimate_returns),
            odds=self.odds, bet_amount=self.bet_amount, freebet_amount=float(self.freebet_stake))
