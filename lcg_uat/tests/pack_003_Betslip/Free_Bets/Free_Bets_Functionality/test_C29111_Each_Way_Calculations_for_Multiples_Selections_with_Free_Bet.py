import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't grant freebet on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C29111_Each_Way_Calculations_for_Multiples_Selections_with_Free_Bet(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C29111
    NAME: Each Way Calculations for Multiples Selections with Free Bet
    DESCRIPTION: This test case verifies each way calculations for Multiple selections when free bet is selected
    PRECONDITIONS: Make sure <RACE> events have each way option available (terms are shown for market)
    PRECONDITIONS: NOTE, for STG environment UAT assistance is needed in order to get free bet tokens available
    PRECONDITIONS: User has to be logged in
    """
    keep_browser_open = True
    bet_amount = 1
    prices = {0: '1/2', 1: '1/5'}

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        username = tests.settings.betplacement_user
        for i in range(2):
            self.ob_config.grant_freebet(username=username)
        self.__class__.expected_ew_terms = self.ew_terms

        # events for lp selections
        event_1 = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms, lp_prices=self.prices)
        self.__class__.each_way_coef = int(self.expected_ew_terms['ew_fac_num']) / int(self.expected_ew_terms['ew_fac_den'])
        event_2 = self.ob_config.add_UK_racing_event(number_of_runners=1, ew_terms=self.ew_terms, lp_prices=self.prices)
        self.__class__.selection_ids1 = (list(event_1.selection_ids.values())[0],
                                         list(event_2.selection_ids.values())[0])

        # events for sp selections
        event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2)
        event_params2 = self.ob_config.add_UK_racing_event(number_of_runners=2)
        self.__class__.selection_ids2 = (list(event_params1.selection_ids.values())[0],
                                         list(event_params2.selection_ids.values())[0])
        self.site.login(username)

    def test_002_add_a_few_lp_selections_from_different_race_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add a few 'LP' selections from different <Race> events to the Bet Slip
        EXPECTED: Selections are added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids1)

    def test_003_go_to_bet_slip_multiples_section(self):
        """
        DESCRIPTION: Go to 'Bet Slip', 'Multiples' section
        EXPECTED: 'Multiples' section is shown
        """
        sections = self.get_betslip_sections(multiples=True)
        multiples_section = sections.Multiples
        self.assertTrue(multiples_section, msg="'Multiple' section is not shown")
        self.__class__.stake_name, self.__class__.stake = list(multiples_section.items())[0]

    def test_004_chose_free_bet_from_the_dropdown_and_select_each_way_option(self):
        """
        DESCRIPTION: Chose free bet from the dropdown and select 'Each way' option
        EXPECTED: *   Free bet is chosen
        EXPECTED: *   'Each way' option is checked
        EXPECTED: *   'Stake' field is empty
        """
        self.stake.use_free_bet_link.click()
        self.__class__.freebet_stake = self.select_free_bet()
        self.assertTrue(self.stake.has_each_way_checkbox,
                        msg=f'Stake does not have Each Way checkbox')
        self.stake.each_way_checkbox.click()
        self.assertTrue(self.stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')

    def test_005_verify_total_est_returns_value(self, SP=False):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: **'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: **free\_bet/(lines*2) * bets[i].payout.potential - free\_bet **
        EXPECTED: *   **bets[i].payout.potential **attribute** **is taken** **from **'builtBet' **responce;
        EXPECTED: *   '**i**' - number of corresponding mutiple bet;
        EXPECTED: *   id = 'symbol of bet type' (e.g. id  = 'DBL' - double, 'TBL' - treble).
        EXPECTED: * lines - number of lines returned in buildBet response
        EXPECTED: * payout.potential = 'potential with legType: "W"' + 'potential with legType: "P"'
        EXPECTED: NOTE: for each multiple bet type there are two identical lines with id. One of them is calculated with 'Each way' option, second - without. Take into consideration line where is id calculated with 'Each way' option
        """
        self.__class__.odds = self.stake.odds
        if not SP:
            self.verify_estimated_returns(est_returns=float(self.get_betslip_content().total_estimate_returns), odds=self.odds, each_way_coef=self.each_way_coef, bet_amount=0, freebet_amount=float(self.freebet_stake))
        else:
            estimate_returns = self.get_betslip_content().total_estimate_returns
            self.assertEquals(estimate_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                              msg=f'Actual "Estimated/Potential Returns is not updated as N/A')

    def test_006_enter_amount_in_stake_field(self):
        """
        DESCRIPTION: Enter amount in 'Stake' field
        EXPECTED: *   'Stake' field is auto-populated with entered value
        EXPECTED: *   Free bet is chosen
        EXPECTED: *   'Each way' option is checked
        """
        self.stake.amount_form.input.value = self.bet_amount

    def test_007_verify_total_est_returns_value(self, SP=False):
        """
        DESCRIPTION: Verify **'Total Est. Returns'** value
        EXPECTED: **'Total Est. Returns'** value is calculated based on formula:
        EXPECTED: **(stake + free\_bet/(lines*2)) * bets[i].payout.potential - free\_bet **
        """
        if not SP:
            self.verify_estimated_returns(est_returns=float(self.get_betslip_content().total_estimate_returns), odds=self.odds, each_way_coef=self.each_way_coef, bet_amount=self.bet_amount, freebet_amount=float(self.freebet_stake))
        else:
            estimate_returns = self.get_betslip_content().total_estimate_returns
            self.assertEquals(estimate_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                              msg=f'Actual "Estimated/Potential Returns is not updated as N/A')

    def test_008_repeat_steps__3___7_for_sp_selections(self):
        """
        DESCRIPTION: Repeat steps # 3 - 7 for 'SP' selections
        EXPECTED: **'Total Est.Returns'** value will always be equal to 'N/A'
        """
        self.clear_betslip()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids2)
        self.test_003_go_to_bet_slip_multiples_section()
        self.test_004_chose_free_bet_from_the_dropdown_and_select_each_way_option()
        self.test_005_verify_total_est_returns_value(SP=True)
        self.test_006_enter_amount_in_stake_field()
        self.test_007_verify_total_est_returns_value(SP=True)
