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
class Test_C29110_Each_Way_Calculations_for_Singles_Selections_with_Free_Bet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C29110
    NAME: Each Way Calculations for Singles Selections with Free Bet
    DESCRIPTION: This test case verifies each way calculations for singles selections when free bet is selected
    DESCRIPTION: Formula mentioned in TC is same to provided in comment by PO  in ticket https://jira.egalacoral.com/browse/BMA-5351
    PRECONDITIONS: Make sure <RACE> events have each way option available (terms are shown for market)
    PRECONDITIONS: Example of SS response:
    PRECONDITIONS: https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForEvent/xxxxxx?simpleFilter=event.suspendAtTime:greaterThan:xxxx-xx-xxTxx:xx:xx.000Z&priceHistory=true&externalKeys=event&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True
    bet_amount = 1
    prices = {0: '1/2', 1: '1/5'}

    def test_001_load_invictus(self):
        """
        DESCRIPTION: Load Invictus
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

    def test_002_log_in_to_applicaiton(self):
        """
        DESCRIPTION: Log in to applicaiton
        EXPECTED: User is logged in
        """
        # covered in above step

    def test_003_add_several_lp_selections_from_different_race_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add several 'LP' selections from different <Race> events to the Bet Slip
        EXPECTED: Selections are added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids1)

    def test_004_go_to_bet_slip_singles_section(self):
        """
        DESCRIPTION: Go to 'Bet Slip', 'Singles' section
        EXPECTED: 'Singles' section is shown
        """
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertTrue(self.singles_section, msg="'Singles' section is not shown")
        self.__class__.stake_name, self.__class__.stake = list(self.singles_section.items())[0]

    def test_005_select_free_bet_from_the_drop_down_menuleave_the_stake_field_empty(self):
        """
        DESCRIPTION: Select free bet from the drop down menu
        DESCRIPTION: Leave the stake field empty
        EXPECTED: Free bet is selected
        """
        self.stake.use_free_bet_link.click()
        self.__class__.freebet_stake = self.select_free_bet()

    def test_006_select_each_way_option_and_verify_estimated_returns_value(self, SP=False):
        """
        DESCRIPTION: Select each way option and verify 'Estimated Returns' value
        EXPECTED: Est.Returns = Return1 + Return2
        EXPECTED: When Odds have a Fractional Format :
        EXPECTED: Return1 = ((1/2 * freebet) * Odds) + (1/2 * freebet) - freebet
        EXPECTED: Return2 = ((1/2 * freebet) * Odds * (eachnum/eachden)) +  (1/2 * freebet)
        EXPECTED: where eachnum/eachden = eachWayFactorNum/eachWayFactorDen taken from SS response of the event or in TI
        EXPECTED: When Odds have a Decimal Format :
        EXPECTED: Return1 = ((1/2 * freebet) * (Odds-1)) + (1/2 * freebet) - freebet
        EXPECTED: Return2 = ((1/2 * freebet) * (Odds-1) * (eachnum/eachden)) +  (1/2 * freebet)
        """
        self.assertTrue(self.stake.has_each_way_checkbox,
                        msg=f'Stake does not have Each Way checkbox')
        self.stake.each_way_checkbox.click()
        self.assertTrue(self.stake.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        self.__class__.odds = self.stake.odds
        if not SP:
            self.verify_estimated_returns(est_returns=float(self.get_betslip_content().total_estimate_returns), odds=self.odds, each_way_coef=self.each_way_coef, bet_amount=0, freebet_amount=float(self.freebet_stake))
        else:
            estimate_returns = self.get_betslip_content().total_estimate_returns
            self.assertEquals(estimate_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                              msg=f'Actual "Estimated/Potential Returns is not updated as N/A')

    def test_007_select_free_bet_from_the_dropdownenter_some_stake_amount_in_a_stake_field(self):
        """
        DESCRIPTION: Select free bet from the dropdown
        DESCRIPTION: Enter some stake amount in a stake field
        EXPECTED: Free bet is selected
        EXPECTED: 'Stake' field is pre-populated by value entered
        """
        self.stake.amount_form.input.value = self.bet_amount

    def test_008_select_each_way_option_for_selection_and_verify_estimated_returns_filed(self, SP=False):
        """
        DESCRIPTION: Select each way option for selection and verify 'Estimated Returns' filed
        EXPECTED: Est.Returns = Return1 + Return2
        EXPECTED: When Odds have a Fractional Format :
        EXPECTED: Return1 = (stake + (1/2 * freebet)) * Odds + (stake + (1/2 * freebet)) - freebet
        EXPECTED: Return2 = ((stake + (1/2 * freebet)) * Odds * (eachnum/eachden)) + (stake + (1/2 * freebet))
        EXPECTED: When Odds have a Decimal Format :
        EXPECTED: Return1 = (stake + (1/2 * freebet)) * (Odds-1) + (stake + (1/2 * freebet)) - freebet
        EXPECTED: Return2 = ((stake + (1/2 * freebet)) * (Odds-1) * (eachnum/eachden)) + (stake + (1/2 * freebet))
        """
        if not SP:
            self.verify_estimated_returns(est_returns=float(self.get_betslip_content().total_estimate_returns), odds=self.odds, each_way_coef=self.each_way_coef, bet_amount=self.bet_amount, freebet_amount=float(self.freebet_stake))
        else:
            estimate_returns = self.get_betslip_content().total_estimate_returns
            self.assertEquals(estimate_returns, vec.betslip.ESTIMATED_RESULTS_NA,
                              msg=f'Actual "Estimated/Potential Returns is not updated as N/A')

    def test_009_repeat_steps__3___8_for_sp_selections(self):
        """
        DESCRIPTION: Repeat steps # 3 - 8 for 'SP' selections
        EXPECTED: 'Estimated Returns' will always be equal to 'N/A' value
        """
        self.clear_betslip()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids2)
        self.test_004_go_to_bet_slip_singles_section()
        self.test_005_select_free_bet_from_the_drop_down_menuleave_the_stake_field_empty()
        self.test_006_select_each_way_option_and_verify_estimated_returns_value(SP=True)
        self.test_007_select_free_bet_from_the_dropdownenter_some_stake_amount_in_a_stake_field()
        self.test_008_select_each_way_option_for_selection_and_verify_estimated_returns_filed(SP=True)
