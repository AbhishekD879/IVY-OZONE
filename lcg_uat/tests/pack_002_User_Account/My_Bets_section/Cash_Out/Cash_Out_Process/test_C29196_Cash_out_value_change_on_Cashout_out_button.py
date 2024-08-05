import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot perform live updates on prod
# @pytest.mark.hl
@pytest.mark.bet_placement
@pytest.mark.liveserv_updates
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29196_Cash_out_value_change_on_Cashout_out_button(BaseCashOutTest):
    """
    TR_ID: C29196
    NAME: Cash Out value change on 'CASH OUT' button
    DESCRIPTION: This test case verifies price change on 'CASH OUT' button on Cash Out tab
    PRECONDITIONS: In order to get increased Cashed Out value Price/Odds should be decreased. 
    PRECONDITIONS: In order to get decreased Cashed Out value Price/Odds should be increased.
    """
    keep_browser_open = True
    bet_amount = 5
    increased_price = '14/1'
    decreased_price = '1/14'
    initial_multiple_cashout_value, initial_single_cashout_value = None, None
    initial_odds_value = None
    created_event_name2 = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Run Cash Out precondition steps which creates testing data
        EXPECTED: Test event with available Cash Out was created
        """
        events = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.__class__.created_event_name, self.__class__.created_event_name2 = \
            ['%s %s' % (event.event_name, event.local_start_time) for event in events]
        self.__class__.team1, self.__class__.team2 = [event.team1 for event in events]
        self.__class__.selection_ids = {event.team1: event.selection_ids[event.team1] for event in events}

        username = tests.settings.betplacement_user
        self.site.login(username=username)
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values()))
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_001_open_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 'Cash Out' tab is opened
        """
        self.site.open_my_bets_cashout()

    def test_002_trigger_cash_out_value_increasing_for_single_and_multiple_bet(self):
        """
        DESCRIPTION: Trigger cash out value INCREASING for **Single** bet
        DESCRIPTION: Trigger cash out value INCREASING for **Multiple** bet
        EXPECTED: Corresponding 'Price/Odds' data is not changed
        EXPECTED: Corresponding priceNum/priceDen is changed on SiteServer
        EXPECTED: 'CASH OUT' button immediately displays new cash out value
        """
        single_bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=self.created_event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, number_of_bets=10)

        initial_single_cashout_value = single_bet.buttons_panel.full_cashout_button.amount.value
        betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name, betleg = list(betlegs.items())[0]
        initial_odds_value = betleg.odds_value

        multiple_bet_name, multiple_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=[self.created_event_name, self.created_event_name2], number_of_bets=5)

        initial_multiple_cashout_value = multiple_bet.buttons_panel.full_cashout_button.amount.value

        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.increased_price)

        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection_ids[self.team1], price=self.increased_price)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.created_event_name}" with id '
                        f'"{self.selection_ids[self.team1]}" is not received')

        self.assertTrue(single_bet.buttons_panel.full_cashout_button.wait_amount_to_change(initial_amount=initial_single_cashout_value),
                        msg='Cashout amount is not changed')

        new_single_cashout_value = single_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(initial_single_cashout_value) > float(new_single_cashout_value),
                        msg='New cashout value "%s" is not lower than "%s"' %
                            (new_single_cashout_value, initial_single_cashout_value))

        betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name, betleg = list(betlegs.items())[0]
        new_single_odds_value = betleg.odds_value

        self.assertEqual(initial_odds_value, new_single_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (initial_odds_value, new_single_odds_value))

        self.assertTrue(multiple_bet.buttons_panel.full_cashout_button.wait_amount_to_change(initial_amount=initial_multiple_cashout_value),
                        msg='Cashout Amount is not changed')

        new_multiple_cashout_value = multiple_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(initial_multiple_cashout_value) > float(new_multiple_cashout_value),
                        msg='New cashout value "%s" is not lower than "%s"' %
                            (initial_multiple_cashout_value, new_multiple_cashout_value))

        betlegs = multiple_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name = '%s - %s' % (self.team1, self.created_event_name)
        betleg = betlegs.get(betleg_name)
        self.assertTrue(betleg, msg='BetLeg %s is not found' % betleg_name)
        new_multiple_odds_value = betleg.odds_value

        self.assertEqual(initial_odds_value, new_multiple_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (initial_odds_value, new_multiple_odds_value))
        self.__class__.initial_odds_value = initial_odds_value
        self.__class__.initial_multiple_cashout_value = new_multiple_cashout_value
        self.__class__.initial_single_cashout_value = new_single_cashout_value

    def test_003_repeat_steps_1_2_with_decreased_cash_out_value(self):
        """
        DESCRIPTION: Trigger cash out value DECREASING for **Single** bet
        DESCRIPTION: Trigger cash out value DECREASING for **Multiple** bet
        EXPECTED: Corresponding 'Price/Odds' data is not changed
        EXPECTED: Corresponding priceNum/priceDen is changed on SiteServer
        EXPECTED: 'CASH OUT' button immediately displays new cash out value
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.decreased_price)

        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.selection_ids[self.team1],
                                                                 price=self.decreased_price)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.created_event_name}" with id '
                        f'"{self.selection_ids[self.team1]}" is not received')

        single_bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=self.created_event_name, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, number_of_bets=5)

        self.assertTrue(single_bet.buttons_panel.full_cashout_button.wait_amount_to_change(initial_amount=self.initial_single_cashout_value),
                        msg='Cashout Amount is not changed')

        new_single_cashout_value = single_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(self.initial_single_cashout_value) < float(new_single_cashout_value),
                        msg='New cashout value "%s" is not larger than "%s"' %
                            (new_single_cashout_value, self.initial_single_cashout_value))

        betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name, betleg = list(betlegs.items())[0]
        new_single_odds_value = betleg.odds_value

        self.assertEqual(self.initial_odds_value, new_single_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (self.initial_odds_value, new_single_odds_value))

        multiple_bet_name, multiple_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=[self.created_event_name, self.created_event_name2], number_of_bets=5)

        self.assertTrue(multiple_bet.buttons_panel.full_cashout_button.wait_amount_to_change(initial_amount=self.initial_multiple_cashout_value),
                        msg='Cashout Amount is not changed')

        new_multiple_cashout_value = multiple_bet.buttons_panel.full_cashout_button.amount.value
        self.assertTrue(float(self.initial_multiple_cashout_value) < float(new_multiple_cashout_value),
                        msg='New cashout value "%s" is not lower than "%s"' %
                            (self.initial_multiple_cashout_value, new_multiple_cashout_value))

        betlegs = multiple_bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg='No betlegs found')
        betleg_name = '%s - %s' % (self.team1, self.created_event_name)
        betleg = betlegs.get(betleg_name)
        self.assertTrue(betleg, msg='BetLeg %s is not found' % betleg_name)
        new_multiple_odds_value = betleg.odds_value

        self.assertEqual(self.initial_odds_value, new_multiple_odds_value,
                         msg='Odds is changed from "%s" to "%s"' % (self.initial_odds_value, new_multiple_odds_value))
