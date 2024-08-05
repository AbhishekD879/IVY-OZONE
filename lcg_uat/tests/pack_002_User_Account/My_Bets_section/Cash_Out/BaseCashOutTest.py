from collections import namedtuple

from crlat_siteserve_client.siteserve_client import SiteServeRequests
from dateutil import parser

import tests
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


class BaseCashOutTest(BaseBetSlipTest):

    bet_amount = 1.0
    new_increased_price = '6/5'

    def parse_date_time_string(self, date_time_string, time_format='%-H:%M, Today'):
        return parser.parse(date_time_string).time().strftime(time_format)

    def create_several_autotest_premier_league_football_events(self, number_of_events=1, start_time=None,
                                                               markets=None, cashout=True, is_live=False,
                                                               is_upcoming=False, wait_for_event=True, **kwargs):
        Event = namedtuple('created_event', ['event_id', 'event_name', 'team1', 'team2',
                                             'selection_ids', 'start_time', 'local_start_time'])
        created_events = []
        for _ in range(0, number_of_events):
            event = self.ob_config.add_autotest_premier_league_football_event(start_time=start_time, markets=markets,
                                                                              cashout=cashout, is_live=is_live,
                                                                              is_upcoming=is_upcoming,
                                                                              wait_for_event=wait_for_event, **kwargs)
            local_start_time = self.convert_time_to_local(date_time_str=event.event_date_time)
            event_params = Event(event.event_id,
                                 event.team1 + ' v ' + event.team2,
                                 event.team1,
                                 event.team2,
                                 event.selection_ids,
                                 event.event_date_time,
                                 local_start_time
                                 )
            created_events.append(event_params)
        self._logger.info('*** Created events: {}'.format(created_events))
        return created_events

    def verify_cashout_currency_symbol(self, currency):
        """
        Verifies if correct currency is displayed within the cashout section
        :param currency: type of currency (currency symbol)
        :return: None
        """
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets found on Cashout page')
        self.assertIn(self.bet_name, bets)
        bet = bets[self.bet_name]
        self.assertEqual(currency, bet.stake.currency,
                         msg='Bet: "%s" stake amount does not contain required currency symbol: %s' %
                             (self.bet_name, currency))
        self.assertEqual(currency, bet.est_returns.currency,
                         msg='Bet: "%s" Est returns amount does not contain required currency symbol: %s' %
                             (self.bet_name, currency))
        self.assertEqual(currency, bet.buttons_panel.full_cashout_button.amount.currency,
                         msg='Bet: "%s" Full Cashout button amount does not contain required currency symbol: %s' %
                             (self.bet_name, currency))
        bet.buttons_panel.full_cashout_button.click()
        self.assertEqual(currency, bet.buttons_panel.cashout_button.amount.currency,
                         msg='Bet: "%s" Cashout button does not contain required currency symbol: %s' %
                             (self.bet_name, currency))

    @classmethod
    def custom_tearDown(cls):
        if tests.settings.backend_env != 'prod' and cls.delete_events:
            ob_config = cls.get_ob_config()
            events = ob_config.CREATED_EVENTS
            ss_req = SiteServeRequests(env=tests.settings.backend_env, brand=tests.settings.brand)
            for event in events:
                resp = ss_req.ss_event_to_outcome_for_event(event_id=event, raise_exceptions=False)
                if not resp:
                    continue
                event_params = resp[0]['event']
                markets = event_params.get('children', [])
                for market in markets:
                    market_id = market['market']['id']
                    selections = market['market'].get('children', [])
                    for selection in selections:
                        selection_id = selection['outcome']['id']
                        ob_config.result_selection(selection_id=selection_id, market_id=market_id, result='L',
                                                   event_id=event_params['id'], wait_for_update=False)
                        ob_config.settle_result(selection_id=selection_id, market_id=market_id, result='L',
                                                event_id=event_params['id'], wait_for_update=False)
                        ob_config.confirm_result(selection_id=selection_id, market_id=market_id, result='L',
                                                 event_id=event_params['id'], wait_for_update=False)
