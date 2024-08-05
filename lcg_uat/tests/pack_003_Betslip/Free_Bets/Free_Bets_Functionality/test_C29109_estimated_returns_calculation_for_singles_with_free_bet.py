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
class Test_C29109_Estimated_Returns_Calculation_For_Singles_with_Free_Bet(BaseBetSlipTest):
    """
    TR_ID: C29109
    NAME: 'Estimated Returns' Calculation For Singles with Free Bet
    DESCRIPTION: This test case verifies calculation of Estimated Returns value for a Single Bet when free bet is selected
    PRECONDITIONS: Make sure user has free bets available.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add event
        DESCRIPTION: Log in as a user with free bets available
        EXPECTED: Event is present in OB
        EXPECTED: User is logged in
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = event.selection_ids
        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)

    def test_001_add_single_bet_to_the_bet_slip(self):
        """
        DESCRIPTION: Add Single Bet to the Bet Slip
        EXPECTED: Selection is added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])

    def test_002_go_to_betslip_singles_section(self):
        """
        DESCRIPTION: Go to 'BetSlip', 'Singles' section
        EXPECTED: 'Singles' section is shown
        """
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertTrue(self.singles_section, msg='Betslip Singles section is not displayed.')
        self.assertTrue(len(self.singles_section.items()) == 1,
                        msg='One stake should be found in betslip Singles section.')

    def test_003_select_free_bet_from_the_dropdown(self):
        """
        DESCRIPTION: Select free bet from the dropdown
        EXPECTED: Free bet is chosen
        EXPECTED: 'Stake' field is empty
        """
        self.__class__.stake_name, self.__class__.stake = list(self.singles_section.items())[0]
        self.__class__.odds = self.stake.odds

        self.stake.freebet_tooltip.click()
        self.stake.use_free_bet_link.click()
        self.__class__.freebet_stake = self.select_free_bet()

        self.assertEqual(self.stake.amount_form.input.value, '', msg='"Stake" input field should remain empty')

    def test_004_verify_total_est_returns_value(self):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: 'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: if Odds in a fractional format:
        EXPECTED: free_bet* (priceNum/priceDen+1) - freebet
        EXPECTED: OR
        EXPECTED: if Odds in a decimal format:
        EXPECTED: free_bet* Odds - freebet
        """
        self.verify_estimated_returns(
            est_returns=float(self.get_betslip_content().total_estimate_returns),
            odds=self.odds, bet_amount=0, freebet_amount=float(self.freebet_stake))

    def test_005_select_free_bet_option_and_enter_stake_amount_manually(self):
        """
        DESCRIPTION: Select free bet option and enter stake amount manually
        EXPECTED: Free bet is selected
        EXPECTED: Entered stake is displayed in the 'Stake' field
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        self.assertEqual(self.stake.amount_form.input.value, str(self.bet_amount),
                         msg=f'"Stake" input field should contain just entered value: {self.bet_amount}. '
                             f'Current value is {self.stake.amount_form.input.value}')

    def test_006_verify_total_est_returns_value(self):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: **'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: if Odds in a fractional format:
        EXPECTED: (free_bet + stake) * (priceNum/priceDen+1) - freebet
        EXPECTED: OR
        EXPECTED: if Odds in a decimal format:
        EXPECTED: (free_bet + stake) * Odds - freebet
        """
        self.verify_estimated_returns(
            est_returns=float(self.get_betslip_content().total_estimate_returns),
            odds=self.odds, bet_amount=self.bet_amount, freebet_amount=float(self.freebet_stake))
