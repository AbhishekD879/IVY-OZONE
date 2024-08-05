import pytest
import tests
import voltron.environments.constants as vec
from fractions import Fraction
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod       cannot script it for prod as we need to change the price and stake
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870285__Double_and_Singles_on_Football_Countered_by_Stake_for_Double_and_a_Price_for_one_of_the_Single(BaseBetSlipTest):
    """
    TR_ID: C44870285
    NAME: - Double and Singles on Football Countered by Stake for Double and a Price for one of the Single
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    suggested_max_bet = 0.25
    prices = [{0: '1/12', 1: '1/10', 2: '1/9'},
              {0: '1/13', 1: '1/11', 2: '1/11'}]
    new_price = '1/6'
    selection_ids = []
    event_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(default_market_name='|Draw No Bet|', lp=self.prices[i],
                                                                                     max_bet=self.max_bet,
                                                                                     max_mult_bet=self.max_mult_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(self.eventID)
        if self.site.wait_logged_out():
            self.__class__.username = tests.settings.betplacement_user
            self.site.login(self.username)

    def test_001_place_2_single_football_oa_bets_and_one_oa_double_football_bet(self, single=True):
        """
        DESCRIPTION: Place 2 single Football OA bets and one OA double Football bet
        EXPECTED: The bets should go through to the OA flow
        """
        # Cannot provide price offer and stake offer at a time, so done one after one
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 0.5
        sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        singles_section, multiples_section = sections.Singles, sections.Multiples
        if single:
            for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=2).items():
                self.enter_stake_amount(stake=stake)
        else:
            for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=1).items():
                self.enter_stake_amount(stake=stake)
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(), msg=f'"{bet_now_button.name}" button is disabled')
        bet_now_button.click()
        overask = self.get_betslip_content().wait_for_overask_panel()
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_the_ti_change_the_prices_for_the_singles(self):
        """
        DESCRIPTION: In the TI, change the prices for the singles
        EXPECTED: On the front end, you should see the counter offer with the original prices crossed out and the new prices next to them for the singles. The new prices should be highlighted.
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.event_ids[0])
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id,
                                                 price_1=self.new_price, max_bet=self.bet_amount)
        overask_trader_message = wait_for_result(lambda: self.get_betslip_content().overask_trader_section.trader_message, timeout=10)
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = wait_for_result(lambda: self.get_betslip_content().overask_trader_section.expires_message, timeout=10)
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        sections = self.get_betslip_sections().Singles
        self.assertTrue(sections.keys(), msg=f'"{sections}" is not added to the betslip')
        odd_value = sections.overask_trader_offer.stake_content.odd_value.value.strip(' x')
        self.assertEqual(odd_value, self.new_price,
                         msg=f'Actual price :{odd_value} is not same as'f'Expected price :{self.new_price}')
        stakes = sections.overask_trader_offer.stake_content.odd_value
        new_odds = stakes.value.strip(' x')
        self.assertTrue(stakes.is_displayed(), msg=f'original odds "{stakes.name}" is not crossed out and new '
                                                   f'odds "{new_odds}" are not displayed')
        price_color = sections.overask_trader_offer.stake_content.odd_value.value_color
        self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for stake is not highlighted in yellow')

    def test_003_check_that_the_new_potential_returns_are_correct_for_the_singles_and_the_double(self, single=True):
        """
        DESCRIPTION: Check that the new Potential Returns are correct for the singles and the double.
        EXPECTED: The new Potential Returns should be correct
        """
        new_potential_returns = self.get_betslip_content().total_estimate_returns
        if single:
            self.verify_estimated_returns(est_returns=new_potential_returns, bet_amount=self.bet_amount,
                                          odds=self.new_price)
        else:
            self.verify_estimated_returns(est_returns=new_potential_returns, bet_amount=self.suggested_max_bet,
                                          is_double=True, odds=[self.new_price, self.prices[1][0]])

    def test_004_place_the_bets(self, single=True):
        """
        DESCRIPTION: Place the bets
        EXPECTED: You should see the bet receipt, with the new prices for the singles and the new stake for the double
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        if single:
            singles = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict['Single']
            odd_values = list(singles.items_as_ordered_dict.values())[0]
            actual_price = odd_values.odds
            self.assertEqual(actual_price, self.new_price,
                             msg=f'Actual price "{actual_price}" is not same as '
                                 f'New price "{self.new_price}" for single bet')
        else:
            actual_stake = float(self.site.bet_receipt.footer.total_stake)
            suggested_stake = float(self.suggested_max_bet)
            self.assertEqual(actual_stake, suggested_stake,
                             msg=f'Actual stake "{actual_stake}" is not same as '
                                 f'Suggested stake "{suggested_stake}" for '
                                 f'the double bet')
        self.site.bet_receipt.close_button.click()

    def test_005_check_the_bets_in_my_bets_open_bets_make_sure_that_the_bets_have_the_correct_prices_and_stake_and_correct_potential_returns(self, single=True):
        """
        DESCRIPTION: Check the bets in My Bets->Open Bets. Make sure that the bets have the correct prices and stake and correct Potential Returns
        EXPECTED: The bets should show in My Bets->Open Bets and they should have the correct prices, stake and Potential Returns.
        """
        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets,
                        msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        actual_stake = bet.stake.stake_value
        actual_est_returns = round(float(bet.est_returns.stake_value), 1)
        if single:
            actual_odd = bet.odds_value
            self.assertEqual(actual_odd, self.new_price,
                             msg=f'Actual price: "{actual_odd}" is not same as '
                                 f'Expected price:"{self.new_price}"')
            self.assertEqual(float(actual_stake), float(self.bet_amount),
                             msg=f'Actual stake: "{float(actual_stake)}" is not same as '
                                 f'Expected stake:"{float(self.bet_amount)}"')
            expected_returns = round(((float(Fraction(self.new_price)) + 1) * (self.bet_amount)), 1)
            self.assertEqual(actual_est_returns, expected_returns,
                             msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                                 f'Expected Returns:"{expected_returns}"')
        else:
            selections = list(bet.items_as_ordered_dict.values())
            self.assertTrue(selections, msg="No selections found")
            for i in range(len(selections)):
                actual_odd = selections[i].odds_value
                expected_odd = self.prices[i][0]
                self.assertEqual(actual_odd, expected_odd,
                                 msg=f'Actual price "{actual_odd}" is not same as '
                                     f'Expected price "{expected_odd}"')
            self.assertEqual(float(actual_stake), float(self.suggested_max_bet),
                             msg=f'Actual stake: "{float(actual_stake)}" is not same as '
                                 f'Expected stake:"{float(self.suggested_max_bet)}"')
            expected_returns = round(((self.suggested_max_bet) * (float(Fraction(self.prices[0][0])) + 1) * (float(Fraction(self.prices[0][1])) + 1)), 1)
            self.assertEqual(actual_est_returns, expected_returns,
                             msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                                 f'Expected Returns:"{expected_returns}"')

    def test_006_in_the_tichange_the_stake_of_the_double_and_click_on_submit(self):
        """
        DESCRIPTION: In the TI,change the stake of the double and click on Submit
        EXPECTED: On the front end,
        EXPECTED: For the double, the new stake should be highlighted.
        """
        self.event_ids.clear()
        self.selection_ids.clear()
        self.test_000_preconditions()
        self.test_001_place_2_single_football_oa_bets_and_one_oa_double_football_bet(single=False)
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        overask_trader_message = wait_for_result(lambda: self.get_betslip_content().overask_trader_section.trader_message, timeout=10)
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = wait_for_result(lambda: self.get_betslip_content().overask_trader_section.expires_message, timeout=10)
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(sections.keys(), msg=f'"{sections}" is not added to the betslip')
        stake = sections.overask_trader_offer.stake_content.stake_value.name
        actual_stake = float(stake[1:])
        expected_stake = float(self.suggested_max_bet)
        self.assertEqual(actual_stake, expected_stake,
                         msg=f'Actual stake "{actual_stake}" is not same as Expected stake "{expected_stake}"')
        stake_color = sections.overask_trader_offer.stake_content.stake_value.value_color
        self.assertEqual(stake_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified stake is not highlighted in yellow')

    def test_007_repeat_step_1_5(self):
        """
        DESCRIPTION: Repeat step 1-5
        """
        self.test_003_check_that_the_new_potential_returns_are_correct_for_the_singles_and_the_double(single=False)
        self.test_004_place_the_bets(single=False)
        self.test_005_check_the_bets_in_my_bets_open_bets_make_sure_that_the_bets_have_the_correct_prices_and_stake_and_correct_potential_returns(single=False)
