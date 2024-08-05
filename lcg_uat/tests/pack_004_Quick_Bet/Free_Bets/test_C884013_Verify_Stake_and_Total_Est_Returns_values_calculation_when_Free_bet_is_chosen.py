from random import uniform

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't grant freebets
# @pytest.mark.hl
@pytest.mark.freebets
@pytest.mark.horseracing
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C884013_Verify_Stake_and_Total_Est_Returns_values_calculation_when_Free_bet_is_chosen(BaseSportTest, BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C884013
    VOL_ID: C23220558
    NAME: Verify Stake and Total Est Returns values calculation when Free bet is chosen
    DESCRIPTION: This test case verifies 'Stake' and 'Total Est. Returns' values calculation when Free bet is chosen
    PRECONDITIONS: 1.  Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: 2.  Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. The user is logged in and has free bets added
    """
    keep_browser_open = True
    bet_amount = 3.26
    lp = {0: '1/2'}
    freebet_value_1 = f'{uniform(0.5, 1.5):.2f}'
    freebet_value_2 = f'{uniform(1.6, 2.5):.2f}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        DESCRIPTION: Login as a user with Freebets available
        """
        self.__class__.eventID = self.ob_config.add_football_event_to_england_championship().event_id
        self.__class__.racing_event_id = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms,
                                                                            number_of_runners=1,
                                                                            lp_prices=self.lp).event_id
        expected_market = normalize_name(self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)

        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username, freebet_value=self.freebet_value_1)
        self.ob_config.grant_freebet(username=username, freebet_value=self.freebet_value_2)
        self.site.login(username=username)

    def test_001_add_sport_race_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add <Sport>/ <Race> selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of the page
        EXPECTED: "Use Free Bet" link is displayed under event name
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)

        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content
        self.assertTrue(self.quick_bet.has_use_free_bet_link(), msg='"Use Free Bet" link is not present')

    def test_002_tap_use_free_bet_link_and_select_free_bet_from_the_popup(self):
        """
        DESCRIPTION: Tap "Use Free Bet" link and select Free bet from the pop-up
        EXPECTED: Free bet is selected
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.click()  # it's needed to hide pop-up message, don't remove this line
        self.site.quick_bet_panel.selection.content.use_free_bet_link.click()

        freebet_value = self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value_1))
        expected_stake = f'£{freebet_value}'
        stake = self.site.quick_bet_panel.selection.bet_summary.combined_total_stake
        self.assertEqual(stake, expected_stake,
                         msg=f'Actual Total Stake amount value "{stake}" '
                             f'does not match expected "{expected_stake}"')

    def test_003_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is equal to Free bet value chosen
        """
        # verified in previous step

    def test_004_verify_total_est_returns_value(self):
        """
        DESCRIPTION: Verify 'Est. Returns'(Coral)/'Potential Returns'(Ladbrokes) value
        EXPECTED: 'Est. Returns'/'Potential Returns'value is calculated based on the formula:
        EXPECTED: **free_bet * Odds - free_bet** if Odds has a decimal format
        EXPECTED: **free_bet * ((priceNum/priceDen)+1) - free_bet** - if Odds has fractional  format
        """
        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns,
                                      odds=[self.ob_config.event.prices['odds_draw']],
                                      bet_amount=0,
                                      freebet_amount=float(self.freebet_value_1))

    def test_005_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Stake' field is populated with value
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.value = self.bet_amount
        self.assertEqual(quick_bet.amount_form.input.value, str(self.bet_amount),
                         msg=f'Actual amount "{quick_bet.amount_form.input.value}" '
                         f'does not match expected "{self.bet_amount}"')

    def test_006_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is equal to Free bet value chosen + Stake value entered
        EXPECTED: 2 values are displayed in 'Total Stake' : FB £X.XX + £X.XX [value of stake]
        """
        actual_stake = self.site.quick_bet_panel.selection.bet_summary.combined_total_stake
        expected_stake = f'£{self.freebet_value_1} + £{self.bet_amount}'
        self.assertEqual(actual_stake, expected_stake,
                         msg=f'Actual "Total Stake" value "{actual_stake}" != Expected "{expected_stake}"')

    def test_007_verify_est_returns_coral_potential_returns_ladbrokes_value(self):
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
        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns,
                                      odds=[self.ob_config.event.prices['odds_draw']],
                                      bet_amount=self.bet_amount,
                                      freebet_amount=float(self.freebet_value_1))

    def test_008_select_ew_option_for_race_selection(self):
        """
        DESCRIPTION: Select 'E/W' option (for <Race> selection)
        EXPECTED: 'E/W' option is selected
        """
        self.site.quick_bet_panel.close()
        self.navigate_to_edp(event_id=self.racing_event_id, sport_name='horse-racing')

        self.add_selection_to_quick_bet()

        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.each_way_checkbox.click()
        self.assertTrue(quick_bet.each_way_checkbox.is_selected(), msg='Each Way checkbox is not selected')

    def test_009_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: 'Total Stake' value is calculated based on the formula:
        EXPECTED: **free_bet + (stake * 2)**
        EXPECTED: 2 values are displayed in 'Total Stake' : FB £X.XX + £X.XX [stake * 2]
        """
        self.test_005_enter_value_in_stake_field()

        self.site.quick_bet_panel.selection.content.use_free_bet_link.click()
        freebet_value = self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.freebet_value_2))

        actual_stake = self.site.quick_bet_panel.selection.bet_summary.combined_total_stake
        expected_stake = f'£{freebet_value} + £{self.bet_amount * 2}'
        self.assertEqual(actual_stake, expected_stake,
                         msg=f'Actual "Total Stake" value "{actual_stake}" != Expected "{expected_stake}"')

    def test_010_verify_total_est_returns_value(self):
        """
        DESCRIPTION: Verify 'Est. Returns'(Coral)/'Potential Returns'(Ladbrokes) value
        EXPECTED: 'Est. Returns'/'Potential Returns' value is calculated based on the formula:
        EXPECTED: **Est.Returns = Return1 + Return2**
        EXPECTED: **Return1 = (stake + (1/2 * freebet)) * Odds + (stake + (1/2 * free_bet)) - free_bet**
        EXPECTED: **Return2 = (stake + (1/2 * free_bet)) * Odds * (eachnum/eachden) + (stake + (1/2 * free_bet))**
        EXPECTED: 'Est. Returns'/'Potential Returns' value is equal to **N/A** in case of SP priceType selection added to Quick Bet
        """
        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns,
                                      odds=self.lp.values(),
                                      each_way_coef=0.0625,  # 1/16 from self.ew_terms
                                      bet_amount=self.bet_amount,
                                      freebet_amount=float(self.freebet_value_2))

    def test_011_remove_value_from_stake_field(self):
        """
        DESCRIPTION: Remove value from 'Stake' field
        EXPECTED: 'Total Stake' field is empty
        EXPECTED: FB £X.XX is displayed in 'Total Stake'
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        quick_bet.amount_form.input.clear()

        expected_stake = f'£{self.freebet_value_2}'
        stake = self.site.quick_bet_panel.selection.bet_summary.combined_total_stake
        self.assertEqual(stake, expected_stake,
                         msg=f'Actual Total Stake amount value "{stake}" '
                         f'does not match expected "{expected_stake}"')

    def test_012_verify_est_returns_coral_potential_returns_ladbrokes_value(self):
        """
        DESCRIPTION: Verify 'Est. Returns'(Coral)/'Potential Returns'(Ladbrokes) value
        EXPECTED: 'Est. Returns'/'Potential Returns' value is calculated based on the formula:
        EXPECTED: **Est.Returns = Return1 + Return2**
        EXPECTED: **Return1 = (1/2 * freebet) * Odds +(1/2 * free_bet) - freebet**
        EXPECTED: **Return2 = (1/2 * freebet) * Odds * (eachnum/eachden) + (1/2 * freebet)**
        EXPECTED: 'Est. Returns'/'Potential Returns' value is equal to **N/A** in case of SP priceType selection added to Quick Bet
        """
        actual_est_returns = self.site.quick_bet_panel.selection.bet_summary.total_estimate_returns
        self.verify_estimated_returns(est_returns=actual_est_returns,
                                      odds=self.lp.values(),
                                      each_way_coef=0.0625,  # 1/16 from self.ew_terms
                                      bet_amount=0,
                                      freebet_amount=float(self.freebet_value_2))
