
from collections import namedtuple

import logging
import requests

from crlat_ob_client import OBException
from crlat_ob_client import LOGGER_NAME
from crlat_ob_client.login import OBLogin
from crlat_ob_client.utils.helpers import do_request, check_status_code
from crlat_ob_client.utils.waiters import wait_for_result


requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    pass

_logger = logging.getLogger(LOGGER_NAME)


class BetInterceptRequests(OBLogin):
    backend = None
    customer = None

    def _get_cust_id(self, username):
        params = '?action=customer::search::H_search' \
                 '&system=cust' \
                 '&redirect=true' \
                 '&submit_search=&' \
                 'username={username}' \
                 '&option_username=Y' \
                 '&acct_no=' \
                 '&option_acct_no=N' \
                 '&fname=' \
                 '&lname=' \
                 '&ccy_code=' \
                 '&country_code=' \
                 '&option_country_code=N' \
                 '&reg_date_from=' \
                 '&reg_date_to=' \
                 '&min_bet_count=' \
                 '&max_bet_count=' \
                 '&min_stake_scale=' \
                 '&max_stake_scale=' \
                 '&status=' \
                 '&min_balance=' \
                 '&max_balance=' \
                 '&acct_type=' \
                 '&min_sum_ap=' \
                 '&max_sum_ap=' \
                 '&channel=' \
                 '&min_credit_limit=' \
                 '&max_credit_limit=' \
                 '&group_by=0' \
                 '&page_no=0' \
                 '&sort_col=' \
                 '&sort_dir=' \
                 '&sort_type='.format(username=username)
        url = self.site + params
        resp_dict = do_request(url=url, cookies=self.site_cookies)
        customer_id = resp_dict['id']
        self.customer = customer_id
        return self.customer

    def add_account_rules(self, username, **kwargs):
        """
        :param username: User on which account rules to be added
        :param kwargs: stake_factor - Stake factor to be updated at Global level
        :param kwargs: block_bet - Block bet intercept option to be selected in Block bet column
        """
        url = '{0}'.format(self.site)
        cust_id = self._get_cust_id(username=username)
        stake_factor = kwargs.get('stake_factor', '')
        block_bet = kwargs.get('block_bet', '')
        params = (
            ('action', 'customer::cust_rules::H_update'),
            ('new0_dd_level', 'GLOBAL'),
            ('new0_dd_id', -1),
            ('new0_bip_pre', ''),
            ('new0_channel', ''),
            ('new0_cust_bir_async', 1),
            ('new0_gp_control', ''),
            ('new0_comb_control', ''),
            ('new0_stake_factor', stake_factor),
            ('new0_max_bet_amt', ''),
            ('new0_control', block_bet),
            ('rule_ids', 'new0'),
            ('level', 'TOP'),
            ('id', -1),
            ('cust_id', cust_id)
        )
        resp_dict = do_request(url=url, params=params, cookies=self.site_cookies)
        try:
            success_msg = 'Successfully updated rules'
            resp = resp_dict['msg']
            if resp == success_msg:
                pass
            else:
                raise OBException('Cannot update account rules')
        except KeyError as e:
            self._logger.warning('%s' % e)

    def _bet_intercept_search(self, cust_id, event_id):
        url = '{0}'.format(self.site)
        params = '?action=bet_intercept::search::H_search' \
                 '&bir_flag=N' \
                 '&min_stake=' \
                 '&max_stake=' \
                 '&min_stake_scale=' \
                 '&max_stake_scale=' \
                 '&req_status=-'
        if event_id != 'NA':
            params += '&id={event_id}' \
                      '&level=event'.format(event_id=event_id)
        url = url + params
        resp_dict = do_request(url, cookies=self.site_cookies)
        if len(resp_dict['bets']) > 0:
            for bet in resp_dict['bets']:
                if bet['cust_id'] == cust_id:
                    parameters = namedtuple("bet_intercept_parameters", ['acct_id', 'bet_id', 'bet_group_id'])
                    bet_params = parameters(bet['acct_id'], bet['bet_id'], bet['bet_group_id'])
                    return bet_params
                else:
                    continue
        return None

    def find_bet_for_review(self, username, event_id, timeout=15):
        cust_id = self._get_cust_id(username=username)
        result = wait_for_result(lambda: self._bet_intercept_search(cust_id, event_id) is not None,
                                 name='Searching for bet',
                                 timeout=timeout)
        if result:
            return self._bet_intercept_search(cust_id, event_id)
        else:
            raise OBException('Bet was not found')

    def _bets_intercept_search(self, event_id):
        """
        Search for bets that triggered overask for a event
        :param event_id: after creating event get event_id
        :return: returns response data
        """
        url = '{0}'.format(self.site)
        params = (
            ('action', 'bet_intercept::search::H_search'),
            ('bir_flag', 'N'),
            ('min_stake',''),
            ('max_stake', ''),
            ('min_stake_scale', ''),
            ('max_stake_scale', ''),
            ('req_status', '-'),
            ('id', event_id),
            ('level', 'event')
        )

        resp_dict = do_request(url=url, params=params, cookies=self.site_cookies)
        return resp_dict

    def find_bets_for_review(self, events_id, timeout=15):
        """
        Fetch details of bets that triggered overask for a event
        :param events_id: after creating events get event_id
        :return: returns bet details
        """
        bets_details = {}
        for event_id in events_id:
            result = wait_for_result(lambda: self._bets_intercept_search(event_id) is not None,
                                     name='Searching for bet',
                                     timeout=timeout)
            if result:
                resp_dict= self._bets_intercept_search(event_id)
                if len(resp_dict['bets']) > 0:
                    for bet in resp_dict['bets']:
                        bets_details[bet['bet_id']] = bet['bet_type']
                        bets_details['bet_group_id'] = bet['bet_group_id']
                        bets_details['acct_id'] = bet['acct_id']
            else:
                raise OBException('Bet was not found')
        return bets_details

    def accept_bet(self, event_id, bet_id, betslip_id, expected_result: bool=True):
        # TODO add possibility to accept a bet for other sports, categories and types
        """
        :param event_id: after creating event get event_id
        :param bet_id: find_bet_for_review returns bet_id
        :param betslip_id: find_bet_for_review returns betslip_id
        :param expected_result: specifies expected result for accepted/rejected bet
        :return: if expected_result=True it returns None, else: returns request status
        """
        url = '{0}'.format(self.site)
        params = '?action=bet_intercept::search::H_action_all' \
                 '&bi_action=A' \
                 '&level=async_level' \
                 '&level=async_level' \
                 '&level=async_level' \
                 '&level=async_level' \
                 '&partial=Y&partial=Y&partial=Y&partial=N' \
                 '&bir_flag=N&min_stake=&max_stake=&min_stake_scale=&max_stake_scale=' \
                 '&req_status=-&user_id=' \
                 '&bet_id={bet_id}' \
                 '&betslip_id={betslip_id}' \
                 '&reason_text='.format(bet_id=bet_id, betslip_id=betslip_id)
        if event_id != 'NA':
            params += '&id=FOOTBALL' \
                      '&id=16291' \
                      '&id=3756' \
                      '&id={event_id}' \
                      '&parent_id=0' \
                      '&parent_id=FOOTBALL' \
                      '&parent_id=16291' \
                      '&parent_id=3756'.format(event_id=event_id)
        url = url + params
        resp_dict = do_request(url, cookies=self.site_cookies)
        try:
            if expected_result:
                result = None
                if resp_dict['report']['report'][0]['status'] != 'OK':
                    raise OBException('Cannot accept a bet')
            else:
                result = resp_dict['report']['report'][0]['result']
            return result
        except KeyError as e:
            self._logger.warning('%s' % e)

    def decline_bet(self, event_id, bet_id, betslip_id):
        url = '{0}'.format(self.site)
        if self.brand != 'ladbrokes':
            params = (
                ('action', 'bet_intercept::search::H_action_all'),
                ('bi_action', 'D'),
                ('level', 'async_level'),
                ('level', 'async_level'),
                ('level', 'async_level'),
                ('level', 'async_level'),
                ('partial', 'Y'),
                ('partial', 'Y'),
                ('partial', 'Y'),
                ('partial', 'N'),
                ('bir_flag', 'N'),
                ('min_stake', ''),
                ('max_stake', ''),
                ('min_stake_scale', ''),
                ('max_stake_scale', ''),
                ('req_status', '-'),
                ('user_id', ''),
                ('bet_id', bet_id),
                ('betslip_id', betslip_id),
                ('reason_text', ''),
                ('reason_code', '42179')
            )
        else:
            params = (
                ('action', 'bet_intercept::search::H_action_all'),
                ('bi_action', 'D'),
                ('bir_flag', 'N'),
                ('min_stake', ''),
                ('max_stake', ''),
                ('min_stake_scale', ''),
                ('max_stake_scale', ''),
                ('req_status', '-'),
                ('user_id', ''),
                ('bet_id', bet_id),
                ('betslip_id', betslip_id),
                ('reason_text', ''),
                ('reason_code', '4105')
            )
        if event_id != 'NA':
            params += (
                ('id', 'FOOTBALL'),
                ('id', '16291'),
                ('id', '3756'),
                ('id', event_id),
                ('parent_id', '0'),
                ('parent_id', 'FOOTBALL'),
                ('parent_id', '16291'),
                ('parent_id', '3756')
            )
        resp_dict = do_request(url=url, params=params, cookies=self.site_cookies)
        try:
            status = 'OK'
            resp = resp_dict['report']['report'][0]['status']

            if status in resp:
                pass
            else:
                raise OBException('Cannot decline a bet')
        except KeyError as e:
            self._logger.warning('%s' % e)

    def split_bet(self, account_id, event_id, bet_id, betslip_id, linked=False, **kwargs):
        """
        :param account_id: for getting account_id use find_bet_for_review function
        :param event_id: after creating event get event_id
        :param bet_id: accepts a list of bet ids
        :param betslip_id: find_bet_for_review returns betslip_id
        :param linked: linking split bet
        :param kwargs: stake_part1 - Stake Per Line splited stake part 1
        :param kwargs: price_part1 - Stake Per Line splited price part 1
        :param kwargs: stake_part2 - Stake Per Line splited stake part 2
        :param kwargs: price_part2 - Stake Per Line splited price part 2
        :param kwargs: price_type_parent - 'L' for LP 'S' for SP for parent bet
        :param kwargs: price_type_child - 'L' for LP 'S' for SP for child bet
        :param kwargs: leg_type1 - 'E' for eachway 'W' for WIN
        :param kwargs: leg_type2 - 'E' for eachway 'W' for WIN
        :param kwargs: Number_of_selections - it is a list of selections of each bet
        :param kwargs: Number_of_splits - number of splits to be performed by default it is 1
        :return: bet parts with modified values displaying in betslip
        """
        url = '{0}'.format(self.site)
        stake_part1 = kwargs.get('stake_part1', '')
        price_part1 = kwargs.get('price_part1', '')
        stake_part2 = kwargs.get('stake_part2', '')
        price_part2 = kwargs.get('price_part2', '')
        leg_type1 = kwargs.get('leg_type1', 'W')
        leg_type2 = kwargs.get('leg_type2', 'W')
        Number_of_bets = len(bet_id)
        Number_of_selections = kwargs.get('Number_of_selections', [1])
        Number_of_splits = kwargs.get('Number_of_splits', 1)
        params = '?action=bet_intercept::request::H_submit'
        for bet_index in range(0, Number_of_bets):
            params += '&bet_id={bet_id}'.format(bet_id=bet_id[bet_index])
            params += '&bi_action=O'
        params += '&acct_id={account_id}' \
                  '&betslip_id={betslip_id}' \
                  '&channel=M'.format(account_id=account_id, event_id=event_id,
                                      betslip_id=betslip_id)
        for bet_index in range(1, (Number_of_bets) + 1):
            params += '&reason_text_{bet_id}=' \
                      '&reason_code_{bet_id}=' \
                      '&leg_type_{bet_id}={leg_type1}' \
                      '&stake_{bet_id}={stake_part1}'.format(bet_id=bet_id[bet_index - 1], stake_part1=stake_part1,
                                                             leg_type1=leg_type1)
            bet_type = (Number_of_selections[bet_index - 1])
            for selection_index in range(1, (
                    (bet_type) + 1)):  # for changing price type to LP or SP for single or multiple selections
                price_type_parent = kwargs.get('price_type_parent' + str(selection_index), 'L')
                params += '&price_type_{bet_id}_{selection_index}_1={price_type_parent}'.format(
                    bet_id=bet_id[bet_index - 1],
                    selection_index=selection_index,
                    price_type_parent=price_type_parent)
                if price_type_parent == 'L':
                    params += '&price_changed_{bet_id}_{selection_index}_1=N' \
                              '&price_{bet_id}_{selection_index}_1={price_part1}'.format(
                        bet_id=bet_id[bet_index - 1],
                        selection_index=selection_index,
                        price_part1=price_part1)
            params += '&num_split_{bet_id}={Number_of_splits}'.format(bet_id=bet_id[bet_index - 1],
                                                                      Number_of_splits=Number_of_splits)

            depends_on_bet_id = bet_id[bet_index - 1] if linked else ''
            for split_index in range(Number_of_splits):  # for single or multiple splits
                params += '&leg_type_{bet_id}_{split_index}={leg_type2}' \
                          '&stake_{bet_id}_{split_index}={stake_part2}' \
                          '&depends_on_{bet_id}_{split_index}={depends_on_bet_id}'.format(bet_id=bet_id[bet_index - 1],
                                                                               split_index=split_index,
                                                                               leg_type2=leg_type2,
                                                                               stake_part2=stake_part2,
                                                                               depends_on_bet_id=depends_on_bet_id)

                bet_type = (Number_of_selections[bet_index - 1])
                for selection_index in range(1, (
                        (bet_type) + 1)):  # for changing price type to LP or SP for single or multiple selections
                    price_type_child = kwargs.get(
                        'price_type_child_' + str(split_index) + '_' + str(selection_index),
                        'L')
                    params += '&price_type_{bet_id}_{split_index}_{selection_index}_1={price_type_child}'.format(
                        bet_id=bet_id[bet_index - 1], split_index=split_index, selection_index=selection_index,
                        price_type_child=price_type_child)
                    if price_type_child == 'L':
                        params += '&price_changed_{bet_id}_{split_index}_{selection_index}_1=N' \
                                  '&price_{bet_id}_{split_index}_{selection_index}_1={price_part2}'.format(
                            bet_id=bet_id[bet_index - 1],
                            selection_index=selection_index,
                            split_index=split_index,
                            price_part2=price_part2)
        url = url + params
        resp_dict = do_request(url, cookies=self.site_cookies)
        try:
            if resp_dict['report']['report'][0]['status'] != 'OK':
                raise OBException('Cannot accept a bet')
            else:
                pass
        except KeyError as e:
            self._logger.warning('%s' % e)

    def offer_stake(self, account_id, bet_id, betslip_id, max_bet, price_type='L', **kwargs):
        url = '{0}'.format(self.site)
        leg_type = kwargs.get('leg_type', 'W')  # for each way 'E'
        price_changed = kwargs.get('price_changed', 'N')
        new_price = kwargs.get('new_price', '1/1')
        params = '?action=bet_intercept::request::H_submit' \
                 '&bet_id={bet_id}' \
                 '&bi_action=O' \
                 '&betslip_id={betslip_id}' \
                 '&reason_text_{bet_id}=' \
                 '&reason_code_{bet_id}=' \
                 '&stake_{bet_id}={max_bet}' \
                 '&leg_type_{bet_id}={leg_type}' \
                 '&price_type_{bet_id}_1_1={price_type}' \
                 '&price_changed_{bet_id}_1_1={price_changed}' \
                 '&num_split_{bet_id}=0' \
                 '&acct_id={account_id}' \
            .format(bet_id=bet_id, betslip_id=betslip_id,
                    max_bet=max_bet, account_id=account_id,
                    price_type=price_type, leg_type=leg_type,
                    price_changed=price_changed)
        if price_changed == 'Y':
            params += '&price_{bet_id}_1_1={new_price}'.format(bet_id=bet_id, new_price=new_price)
        url = url + params
        self._logger.debug('URL %s' % url)
        resp_dict = do_request(url, cookies=self.site_cookies)
        try:
            if kwargs.get('bet_status_suspended'):
                offered_bet = next((bet for bet in resp_dict['bets'] if bet['offered'] == 'N'), None)
            else:
                offered_bet = next((bet for bet in resp_dict['bets'] if bet['offered'] == 'Y'), None)
            if not offered_bet:
                raise OBException('Cannot offer stake')
            else:
                pass
        except KeyError as e:
            self._logger.warning('%s' % e)

    def offer_max_bet(self, bet_id, betslip_id):
        url = '{0}'.format(self.site)
        params = '?action=bet_intercept::search::H_action_all' \
                 '&bi_action=O' \
                 '&bir_flag=N' \
                 '&min_stake=' \
                 '&max_stake=' \
                 '&min_stake_scale=' \
                 '&max_stake_scale=' \
                 '&req_status=-' \
                 '&user_id=' \
                 '&bet_id={bet_id}' \
                 '&betslip_id={betslip_id}' \
                 '&reason_text='.format(bet_id=bet_id, betslip_id=betslip_id)
        url = url + params
        resp_dict = do_request(url, cookies=self.site_cookies)
        try:
            if resp_dict['report']['report'][0]['status'] != 'OK':
                raise OBException('Cannot offer max bet')
            else:
                pass
        except KeyError as e:
            self._logger.warning('%s' % e)
        max_bet = resp_dict['report']['report'][0]['max_bet']
        return float(max_bet)

    def offer_multiple_prices(self, account_id, bet_id, betslip_id, max_bet, leg_type='W', price_1=False, price_2=False,
                              price_3=False):

        stake = '10.00' if leg_type == 'E' else max_bet

        url = '{0}'.format(self.site)
        params = '?action=bet_intercept::request::H_submit' \
                 '&bet_id={bet_id}' \
                 '&bi_action=O' \
                 '&acct_id={account_id}' \
                 '&betslip_id={betslip_id}' \
                 '&reason_text_{bet_id}=' \
                 '&reason_code_{bet_id}=' \
                 '&leg_type_{bet_id}={leg_type}' \
                 '&stake_{bet_id}={stake}' \
                 '&num_split_{bet_id}=0' \
            .format(bet_id=bet_id, account_id=account_id, betslip_id=betslip_id, leg_type=leg_type, stake=stake)
        if price_1:
            params += '&price_{bet_id}_1_1={price}' \
                      '&price_changed_{bet_id}_1_1=Y' \
                      '&price_type_{bet_id}_1_1=L'.format(bet_id=bet_id, price=price_1)
        else:
            params += '&price_type_{bet_id}_1_1=S'.format(bet_id=bet_id)

        if price_2:
            params += '&price_{bet_id}_2_1={price}' \
                      '&price_changed_{bet_id}_2_1=Y' \
                      '&price_type_{bet_id}_2_1=L'.format(bet_id=bet_id, price=price_2)
        else:
            params += '&price_type_{bet_id}_2_1=S'.format(bet_id=bet_id)

        if price_3:
            params += '&price_{bet_id}_3_1={price}' \
                      '&price_changed_{bet_id}_3_1=Y' \
                      '&price_type_{bet_id}_3_1=L'.format(bet_id=bet_id, price=price_3)
        else:
            params += '&price_type_{bet_id}_3_1=S'.format(bet_id=bet_id)

        url = url + params
        resp_dict = do_request(url, cookies=self.site_cookies)
        try:
            offered_bet = next((bet for bet in resp_dict['bets'] if bet['offered'] == 'Y'), None)
            if not offered_bet:
                raise OBException('Cannot offer price')
            else:
                pass
        except KeyError as e:
            self._logger.warning('%s' % e)

    def multiple_actions_bets(self, acct_id, betslip_id, bets_details, **kwargs):
        """
        Perform multiple actions on different bets.
        :param acct_id: for getting account_id use find_bets_for_review function
        :param betslip_id: find_bets_for_review returns betslip_id
        :param bets_details: provide bet_id, bet_type, action to be performed, bet value, change price/stake details.
                             Use find_bets_for_review to get bet_id, bet_type details
        :return: performs multiple actions on different bets
        """

        url = '{0}'.format(self.site)
        params = (
            ('action', 'bet_intercept::request::H_submit'),
            ('acct_id', acct_id),
            ('betslip_id', betslip_id)
        )
        for bet, betdetails in bets_details.items():
            bet_id = betdetails.get('id')
            params += (
                ('bet_id', bet_id),
                ('bi_action', betdetails.get('action'))
            )
            if betdetails['action'] == 'D':
                reason_code = '42179' if self.brand == 'bma' else '4105'
                params += (
                    (f'reason_text_{bet_id}', 'Decline message'),
                    (f'reason_code_{bet_id}', reason_code)
                )
            elif betdetails['action'] == 'O':
                if betdetails['bettype'] == 'DBL':
                    params += (
                        (f'price_changed_{bet_id}_1_1', betdetails.get('price_changed_1', 'N')),
                        (f'price_changed_{bet_id}_2_1', betdetails.get('price_changed_2', 'N')),
                        (f'price_type_{bet_id}_1_1', betdetails.get('price_type', 'L')),
                        (f'stake_{bet_id}', betdetails['stake']),
                        (f'leg_type_{bet_id}', betdetails.get('leg_type', 'W')),
                        (f'num_split_{bet_id}', '0')
                    )
                elif betdetails.get('split', False):
                    stake_part1 = betdetails.get('stake_part1', '')
                    price_part1 = betdetails.get('price_part1', '')
                    stake_part2 = betdetails.get('stake_part2', '')
                    price_part2 = betdetails.get('price_part2', '')
                    leg_type1 = betdetails.get('leg_type1', 'W')
                    leg_type2 = betdetails.get('leg_type2', 'W')
                    bet_id = betdetails.get('id', '')
                    Number_of_bets = betdetails.get('number_of_bets', 1)
                    Number_of_selections = betdetails.get('Number_of_selections', [1])
                    Number_of_splits = betdetails.get('Number_of_splits', 1)
                    params += (('channel', 'M'),)
                    for bet_index in range(1, (Number_of_bets) + 1):
                        params += ((f'reason_text_{bet_id}', ''),
                                   (f'reason_code_{bet_id}', ''),
                                   (f'leg_type_{bet_id}', leg_type1),
                                   (f'stake_{bet_id}', stake_part1))
                        bet_type = (Number_of_selections[bet_index - 1])
                        for selection_index in range(1, ((bet_type) + 1)):  # for changing price type to LP or SP for single or multiple selections
                            price_type_parent = betdetails.get('price_type_parent' + str(selection_index), 'L')
                            params += ((f'price_type_{bet_id}_{selection_index}_1', price_type_parent),)
                            if price_type_parent == 'L':
                                params += ((f'price_changed_{bet_id}_{selection_index}_1', 'N'),
                                           (f'price_{bet_id}_{selection_index}_1', price_part1))
                        params += ((f'num_split_{bet_id}', Number_of_splits),)
                        for split_index in range(Number_of_splits):  # for single or multiple splits
                            depends_on_bet_id = bet_id if betdetails.get('linked', False) else ''
                            params += ((f'leg_type_{bet_id}_{split_index}',leg_type2),
                                       (f'stake_{bet_id}_{split_index}', stake_part2),
                                       (f'depends_on_{bet_id}_{split_index}', depends_on_bet_id))
                            bet_type = (Number_of_selections[bet_index - 1])
                            for selection_index in range(1, ((bet_type) + 1)):  # for changing price type to LP or SP for single or multiple selections
                                price_type_child = betdetails.get(
                                    'price_type_child_' + str(split_index) + '_' + str(selection_index),
                                    'L')
                                params += ((f'price_type_{bet_id}_{split_index}_{selection_index}_1', price_type_child),)
                                if price_type_child == 'L':
                                    params += ((f'price_changed_{bet_id}_{split_index}_{selection_index}_1', 'N'),
                                               (f'price_{bet_id}_{split_index}_{selection_index}_1', price_part2))
                elif betdetails['bettype'] == 'SGL':
                    params += (
                        (f'price_changed_{bet_id}_1_1', betdetails.get('price_changed', 'N')),
                        (f'price_type_{bet_id}_1_1', betdetails.get('price_type', 'L')),
                        (f'price_{bet_id}_1_1', betdetails['price']),
                        (f'stake_{bet_id}', betdetails['stake']),
                        (f'leg_type_{bet_id}', betdetails.get('leg_type', 'W')),
                        (f'num_split_{bet_id}', '0')
                    )

        resp_dict = do_request(url, params=params, cookies=self.site_cookies)
        try:
            if resp_dict['report']['report'][0]['status'] != 'OK':
                raise OBException('Cannot accept a bet')
        except KeyError as e:
            self._logger.warning('%s' % e)

    def change_bet_to_each_way_or_win(self, account_id: int, bet_id: int, betslip_id: int,
                                      bet_amount: (int, float), leg_type: str):
        """
        :param account_id: for getting account_id use find_bet_for_review function
        :param bet_id: find_bet_for_review returns bet_id
        :param betslip_id: find_bet_for_review returns betslip_id
        :param bet_amount: stake provided by the trader
        :param leg_type: 'W' if win else 'E' for each way
        :return: changes the bet to each way or win
        """
        url = '{0}'.format(self.site)
        params = (
            ('action', 'bet_intercept::request::H_submit'),
            ('bet_id', bet_id),
            ('bi_action', 'O'),
            ('acct_id', account_id),
            ('betslip_id', betslip_id),
            (f'reason_text_{bet_id}', ''),
            (f'reason_code_{bet_id}', ''),
            (f'leg_type_{bet_id}', leg_type),
            (f'stake_{bet_id}', bet_amount),
            (f'price_type_{bet_id}_1_1', 'L'),
            (f'price_changed_{bet_id}_1_1', 'N'),
            (f'num_split_{bet_id}', '0')
        )
        resp_dict = do_request(url=url, params=params, cookies=self.site_cookies)
        try:
            status = 'OK'
            resp = resp_dict['report']['report'][0]['status']

            if status in resp:
                pass
            else:
                raise OBException('Cannot change bet type')
        except KeyError as e:
            self._logger.warning('%s' % e)

    def change_price_type(self, account_id: int, bet_id: int, betslip_id: int,
                          bet_amount: (int, float), price_type: str, price: (int, float) = '1.10',
                          num_of_prices_to_change: int = 1):
        """
        :param account_id: for getting account_id use find_bet_for_review function
        :param bet_id: find_bet_for_review returns bet_id
        :param betslip_id: find_bet_for_review returns betslip_id
        :param bet_amount: bet amount entered by user
        :param price_type: 'S' for sp and 'L' for lp
        :param price: can change price value if needed
        :param num_of_prices_to_change : Number of prices type that required to be changed
        :return: changes the price type to LP or SP
        """
        url = '{0}'.format(self.site)
        params = (
            ('action', 'bet_intercept::request::H_submit'),
            ('bet_id', bet_id),
            ('bi_action', 'O'),
            ('acct_id', account_id),
            ('betslip_id', betslip_id),
            (f'reason_text_{bet_id}', ''),
            (f'reason_code_{bet_id}', ''),
            (f'leg_type_{bet_id}', 'W'),
            (f'stake_{bet_id}', bet_amount),
            (f'num_split_{bet_id}', '0')
        )
        for price_num in range(num_of_prices_to_change):
            price_change = (
                (f'price_type_{bet_id}_{price_num+1}_1', price_type)
            )
            params += (price_change,)

        if price_type == 'L':
            for price_num in range(num_of_prices_to_change):
                LP_url = (
                    (f'price_changed_{bet_id}_{price_num+1}_1', 'Y'),
                    (f'price_{bet_id}_{price_num+1}_1', price)
                )
                params += LP_url
        resp_dict = do_request(url=url, params=params, cookies=self.site_cookies)
        try:
            status = 'OK'
            resp = resp_dict['report']['report'][0]['status']

            if status in resp:
                pass
            else:
                raise OBException('Cannot change price type')
        except KeyError as e:
            self._logger.warning('%s' % e)

    def change_trader_and_offer_timeout(self, channel_id: str, trader_timeout: int = 120, offer_timeout: int = 120):
        """
        :param channel_id: for mobile: 'M', for desktop: 'I'
        :param trader_timeout: timeout for trader(in seconds)
        :param offer_timeout: offer expiry time(in sceonds)
        :return: changes the trader timeout and offer timeout
        """
        url = '{0}'.format(self.site)
        params_to_delete = (
            ('action', 'bet_intercept::settings::H_remove_async_timeout'),
            ('channel_id', channel_id),
            ('time_to_start', '')
        )

        do_request(url=url, params=params_to_delete, cookies=self.site_cookies)

        params_to_update = (
            ('action', 'bet_intercept::settings::H_update_channel'),
            ('channel_id', channel_id),
            ('async_auto_place', 'Y'),
            ('async_betting', 'Y'),
            ('bir_async_bet', 'N'),
            ('time_to_start', ''),
            ('trader_timeout', trader_timeout),
            ('offer_timeout', offer_timeout)
        )

        resp_dict = do_request(url=url, params=params_to_update, cookies=self.site_cookies)
        try:
            status = 'OK'
            resp = resp_dict['report']['report'][0]['status']

            if status in resp:
                pass
            else:
                raise OBException('Cannot change trader and offer time')
        except KeyError as e:
            self._logger.warning('%s' % e)


class ChangeOBCfg(object):
    def __init__(self, ob_config):
        self.site = ob_config.ob_url
        self.site_cookies = ob_config.site_cookies
        self._logger = ob_config._logger

    def change_COMB_tolerance_value(self, old_value, new_value):
        url = '{0}/admin?NumCfgs=7&CfgGrpName=Cashout' \
              '&CfgName_0=CASHOUT_AVAIL&CfgValue_old_0=Y' \
              '&CfgACtion_0=ManageOpenbetCfg&CfgValue_0=Y' \
              '&CfgName_1=CASHOUT_MULTI_DELAY&CfgValue_old_1=2' \
              '&CfgACtion_1=ManageOpenbetCfg&CfgValue_1=2' \
              '&CfgName_2=CASHOUT_SINGLE_DELAY' \
              '&CfgValue_old_2=4' \
              '&CfgACtion_2=ManageOpenbetCfg' \
              '&CfgValue_2=4' \
              '&CfgName_3=CASHOUT_WEIGHTING' \
              '&CfgValue_old_3=0.02' \
              '&CfgACtion_3=ManageOpenbetCfg' \
              '&CfgValue_3=0.02' \
              '&CfgName_4=COMB_TOLERANCE_VALUE&CfgValue_old_4={1}&CfgACtion_4=ManageOpenbetCfg&CfgValue_4={2}' \
              '&CfgName_5=ENABLE_COMB_TOLERANCE&CfgValue_old_5=Y' \
              '&CfgACtion_5=ManageOpenbetCfg&CfgValue_5=Y' \
              '&CfgName_6=PARTIAL_CASHOUT_AVAIL' \
              '&CfgValue_old_6=Y&CfgACtion_6=ManageOpenbetCfg' \
              '&CfgValue_6=Y' \
              '&action=ADMIN%3A%3AOPENBET_CFG%3A%3ADoOpenbetCfg'.format(self.site, old_value, new_value)
        r = requests.get(url, cookies=self.site_cookies)
        check_status_code(r)


