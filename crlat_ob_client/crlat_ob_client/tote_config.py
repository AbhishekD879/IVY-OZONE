import re
import logging
from lxml import html

from crlat_ob_client import OBException
from crlat_ob_client.login import OBLogin
from crlat_ob_client.utils.helpers import do_request
from crlat_ob_client import LOGGER_NAME

_logger = logging.getLogger(LOGGER_NAME)


class ToteOBConfig(OBLogin):

    def find_bets(self, customer_username, bet_receipt_id, bet_winnings, set_status='Won'):
        """
        Changing status in bet history 'Win', 'Place', 'Lose'
        """
        status = 1 if set_status == 'Won' else None
        params = 'admin?Customer={customer_username}' \
                 '&UpperCust=Y' \
                 '&Receipt=' \
                 '&TSN=&BetDate1=' \
                 '&BetDate2=' \
                 '&BetPlacedFrom=1&StlDate1=' \
                 '&StlDate2=&Stake1=&Stake2=&UStake1=' \
                 '&UStake2=&Wins1=&Wins2=' \
                 '&Settled=&BetStatus=' \
                 '&PoolTypeOp=&MeetingTypeOp=' \
                 '&ChannelOp=' \
                 '&RepCode=&SubmitName=FindBets' \
                 '&action=ADMIN%3A%3ABET%3A%3ADoBetQuery' \
                 '&QueryType=pools' \
            .format(customer_username=customer_username)
        url = '%s%s' % (self.site[:-2], params)
        self._logger.debug('*** Performing request %s' % url)
        r = do_request(url=url, method='GET', load_response=False, cookies=self.site_cookies)
        page = html.fromstring(r)
        one_customer = page.xpath('//th[@class=contains(text(), \'Manual Settlement\')]')
        few_customers = page.xpath('//td/a[contains(@href, "GoPoolsReceipt")]')
        if one_customer:
            self._logger.info('*** Only one customer is present')
            customer_id = page.xpath('//input[@name="BetId"]')[0].attrib['value']
            self._logger.debug('*** Customer_id: "%s"' % customer_id)
            self.set_bet_status(bet_winnings, status, customer_id)
        elif few_customers:
            self._logger.info('*** Few customers are present')
            for customer in few_customers:
                if customer.text == bet_receipt_id:
                    customer_id = customer.get('href').split('BetId=')[1]
                    self._logger.debug('*** Customer_id: "%s"' % customer_id)
                    self.set_bet_status(bet_winnings, status, customer_id)
                    break
                else:
                    self._logger.info('*** Can not find customer id: %s ' % bet_receipt_id)
        else:
            raise OBException('No pool bets found.')

    def set_bet_status(self, bet_winnings, status, customer_id):
        params = \
            'admin?Manual=' \
            '&BetWinnings={bet_winnings}' \
            '&BetWinningsTax=0' \
            '&BetRefund=0.00' \
            '&BetWinLines={status}' \
            '&BetLoseLines=0' \
            '&BetVoidLines=0' \
            '&BetComment=' \
            '&BetId={customer_id}' \
            '&SubmitName=StlBet' \
            '&action=ADMIN%3A%3ABET%3A%3ADoPoolsManualSettle' \
                .format(bet_winnings=bet_winnings,
                        status=status,
                        customer_id=customer_id,
                        )
        url = '%s%s' % (self.site[:-2], params)
        self._logger.debug('*** Performing request %s' % url)
        do_request(url=url, method='GET', load_response=False, cookies=self.site_cookies)
        self._logger.info('*** Set status "Won"')

    def update_pool_stake_values(self, pool_id, minStakePerLine, maxStakePerLine, minTotalStake, maxTotalStake, stakeIncrement):
        params = 'admin?Status=A' \
                 '&Displayed=Y' \
                 '&DivRec=N' \
                 '&IsVoid=N' \
                 '&MinStake={min_total_stake}' \
                 '&MaxStake={max_total_stake}' \
                 '&MinUnit={min_stake_per_line}' \
                 '&MaxUnit={max_stake_per_line}' \
                 '&StakeIncr={stake_increment}' \
                 '&MaxPayout=' \
                 '&DoSettle=Y' \
                 '&PoolId={pool_id}' \
                 '&action=ADMIN%3A%3APOOLS%3A%3AGoUpdatePool&backup=Y'.format(
            min_total_stake=minTotalStake, max_total_stake=maxTotalStake,
            min_stake_per_line=minStakePerLine, max_stake_per_line=maxStakePerLine,
            stake_increment=stakeIncrement, pool_id=pool_id)
        backoffice = self.site[:-2]  # removing last 2 symbols from site as /office is not needed
        headers = {
            'Referer': '{backoffice}admin?action=ADMIN::POOLS::GoPoolInfo&PoolId={pool_id}'.format(
                backoffice=backoffice,
                pool_id=pool_id)}
        url = backoffice + params
        do_request(url=url, headers=headers, cookies=self.site_cookies, load_response=False)

    def get_selection_ids(self, market_id):
        params = '?action=hierarchy::market::H_get_selections&id=%s&clone=N' % market_id
        url = self.site + params
        resp = do_request(url=url, cookies=self.site_cookies, load_response=False)
        page = html.fromstring(resp)
        selections = page.xpath('//a[not(contains(@href, "result"))]')
        selections_dict = {}
        for i, link in enumerate(selections):
            find = re.search(r'(\d+)', link.attrib['href'])
            sel = find.group(1) if find is not None else None
            self._logger.debug('*** Selection #%s: name %s, id: %s' % (i + 1, link.text, sel))
            selections_dict[link.text] = sel
        return selections_dict
