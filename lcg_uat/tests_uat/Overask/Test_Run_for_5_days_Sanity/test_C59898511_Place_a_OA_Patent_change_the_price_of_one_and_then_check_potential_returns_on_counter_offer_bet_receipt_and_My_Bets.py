import pytest
import tests
from fractions import Fraction
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@vtest
class Test_C59898511_Place_a_OA_Patent_change_the_price_of_one_and_then_check_potential_returns_on_counter_offer_bet_receipt_and_My_Bets(BaseBetSlipTest):
    """
    TR_ID: C59898511
    NAME: Place a OA Patent, change the price of one and then check potential returns on counter offer, bet receipt and My Bets
    """
    keep_browser_open = True
    max_bet = 0.5
    prices = [{0: '1/5', 1: '1/3', 2: '1/4'},
              {0: '1/4', 1: '1/6', 2: '1/7'},
              {0: '1/8', 1: '1/9', 2: '1/10'}]
    new_price = '1/2'
    new_price2 = '1/4'
    new_price3 = '1/8'
    eventIDs = []
    selectionIDs = []

    def verify_est_returns(self, est_returns, odd1, odd2, odd3, bet_amount):
        S1 = (float(Fraction(odd1)) * float(bet_amount)) + float(bet_amount)
        S2 = (float(Fraction(odd2)) * float(bet_amount)) + float(bet_amount)
        S3 = (float(Fraction(odd3)) * float(bet_amount)) + float(bet_amount)
        D1, D2, D3 = S1 * S2, S2 * S3, S3 * S1
        T1 = S1 * S2 * S3
        expected_est_returns = round(float((S1 + S2 + S3) + (D1 + D2 + D3) + T1), 2)
        self.assertAlmostEqual(float(est_returns), float(expected_est_returns),
                               msg=f'Actual estimated returns "{est_returns}" doesn\'t match expected '
                                   f'"{expected_est_returns}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        for i in range(0, 3):
            event = self.ob_config.add_autotest_premier_league_football_event(default_market_name='|Draw No Bet|',
                                                                              lp=self.prices[i], max_bet=self.max_bet)
            self.eventIDs.append(event.event_id)
            self.selectionIDs.append(event.selection_ids[event.team1])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_a_patent_bet_that_triggers_overask(self):
        """
        DESCRIPTION: Place a Patent bet that triggers Overask
        EXPECTED: You should have placed a Patent bet that goes through to the Overask flow
        """
        self.open_betslip_with_selections(selection_ids=self.selectionIDs)
        self.__class__.bet_amount = self.max_bet + 0.5
        sections = self.get_betslip_sections(multiples=True).Multiples.get('Patent')
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        sections.amount_form.input.value = 1
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(), msg=f'"{bet_now_button.name}" button is disabled')
        bet_now_button.click()
        self.site.wait_content_state_changed(timeout=5)
        overask = self.get_betslip_content().wait_for_overask_panel()
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_ti_counter_offer_by_changing_the_price_of_one_of_the_selections(self):
        """
        DESCRIPTION: In TI, counter offer by changing the price of one of the selections.
        EXPECTED: You should have counter offered by changing the price of one selections.
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventIDs[0])
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id,
                                                 price_1=self.new_price, price_2=self.new_price2,
                                                 price_3=self.new_price3, max_bet=self.bet_amount)
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message, timeout=10)
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.expires_message, timeout=10)
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain "{cms_overask_expires_message}" from CMS')

        self.__class__.multiples_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(self.multiples_section, msg=f'sections are not added to the betslip')
        stake_name1, self.__class__.stake1 = list(self.multiples_section.items())[0]
        actual_price = self.stake1.offered_price.name
        self.assertEqual(actual_price, self.new_price,
                         msg=f'Actual price "{actual_price}" is not same as Expected price "{self.new_price}"')

    def test_003_in_the_counter_offer_verify_that_the_new_price_is_highlighted_in_yellow_for_the_selection_and_the_old_price_should_be_shown_with_a_strike_through(self):
        """
        DESCRIPTION: In the counter offer, verify that the new price is highlighted in yellow for the selection and the old price should be shown with a strike through.
        EXPECTED: The new price should be highlighted in yellow and the old price should be struck through.
        """
        self.assertTrue(self.stake1.previous_price, msg=f'previous price "{self.prices[0][0]}" are not crossed out')

    def test_004_verify_that_the_new_potential_returns_are_correct_ie_they_are_calculated_using_the_new_price(self):
        """
        DESCRIPTION: Verify that the new potential returns are correct i.e. they are calculated using the new price
        EXPECTED: The new potential returns should be correct.
        """
        actual_est_returns = round(float(self.get_betslip_content().total_estimate_returns), 2)
        self.verify_est_returns(est_returns=actual_est_returns, bet_amount=self.bet_amount,
                                odd1=self.new_price, odd2=self.new_price2, odd3=self.new_price3)

    def test_005_place_the_bet_and_verify_that_the_bet_receipt_also_shows_the_correct_new_potential_returns(self):
        """
        DESCRIPTION: Place the bet and verify that the bet receipt also shows the correct new potential returns.
        EXPECTED: The bet receipt should show the correct new potential returns.
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        actual_est_returns = round(float(self.site.bet_receipt.footer.total_estimate_returns), 2)
        self.verify_est_returns(est_returns=actual_est_returns, bet_amount=self.bet_amount,
                                odd1=self.new_price, odd2=self.new_price2, odd3=self.new_price3)
        self.site.bet_receipt.close_button.click()

    def test_006_go_to_my_bets_open_bets_and_verify_that_the_new_potential_returns_are_correct_and_the_selection_for_which_you_changed_the_price_shows_the_new_price(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that the new potential returns are correct and the selection for which you changed the price shows the new price.
        EXPECTED: My Bets->Open Bets should show the new price and the correct new potential returns
        """
        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets,
                        msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        actual_est_returns = round(float(bet.est_returns.stake_value), 2)
        self.verify_est_returns(est_returns=actual_est_returns, bet_amount=self.bet_amount,
                                odd1=self.new_price, odd2=self.new_price2, odd3=self.new_price3)
        selections = list(bet.items_as_ordered_dict.values())[0]
        self.assertTrue(selections, msg="No selections found")
        actual_odd = selections.odds_value
        self.assertEqual(actual_odd, self.new_price,
                         msg=f'Actual price "{actual_odd}" is not same as Expected price "{self.new_price}"')
