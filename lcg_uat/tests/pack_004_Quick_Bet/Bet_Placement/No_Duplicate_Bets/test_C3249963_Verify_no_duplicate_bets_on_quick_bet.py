import re
import datetime
import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.betslip
@pytest.mark.bet_history
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C3249963_No_Duplicate_Bets_on_Quick_Bet(BaseSportTest, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C3249963
    VOL_ID: C9697979
    NAME: Verify No Duplicate Bets on Quick Bet
    DESCRIPTION: This test case verifies that user is not able to place duplicate bets by multiple clicking on Bet Now button
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event and login
        """
        category_id = self.ob_config.football_config.category_id
        if tests.settings.backend_env == 'prod':
            self.__class__.card = tests.settings.master_card
            event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.eventID = event['event']['id']
            market_name = next((market['market']['name'] for market in event['event']['children']
                                if market.get('market').get('templateMarketName') == 'Match Betting'), None)
        else:
            self.__class__.card = tests.settings.visa_card
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            self.__class__.event_name = '%s v %s' % (event_params.team1, event_params.team2)
            market_name = self.ob_config.football_config.\
                autotest_class.autotest_premier_league.market_name.replace('|', '')

        self._logger.info(f'*** Found event "{self.event_name}" with ID "{self.eventID}"')

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount=str(tests.settings.min_deposit_amount),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')

        self.site.login(username=username)
        self.__class__.balance_amount = self.site.header.user_balance

    def test_001_add_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add selection to the Quick Bet
        EXPECTED: Selection is successfully added
        """
        self.navigate_to_edp(self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

    def test_002_enter_stake(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field
        EXPECTED: Bet is placed successfully
        """
        quick_bet = self.site.quick_bet_panel.selection
        self.assertTrue(quick_bet.content.amount_form.is_displayed(), msg='"Stake" box is not displayed')
        quick_bet.content.amount_form.input.value = self.bet_amount
        amount = float(quick_bet.content.amount_form.input.value)
        self.assertEqual(amount, self.bet_amount,
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')

    def test_003_click_multiple_times_on_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: Bet is placed only once
        EXPECTED: Bet Receipt is shown with one placed bet
        EXPECTED: Only one request 30011 is present in remote betslip websocket
        """
        responses = []
        response_id = 30011
        # Place 'PLACE BET' button multiple times
        we = self.site.quick_bet_panel.place_bet._we
        for attempt in range(6):
            click(we)

        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        if bet_receipt_displayed:
            bet_receipt_selection_name = self.site.quick_bet_panel.bet_receipt.name
            self.assertTrue(bet_receipt_selection_name, msg=f'Selection "{vec.sb.DRAW}" is not found on BetReceipt')
            self.assertEqual(bet_receipt_selection_name, vec.sb.DRAW.title(),
                             msg=f'Selection name on bet receipt "{bet_receipt_selection_name}" is not the same'
                                 f' as added {vec.sb.DRAW.title()}')
            self.site.quick_bet_panel.header.close_button.click()
        else:
            user_balance = self.get_balance_by_page('all')
            self.assertFalse(float(user_balance) == float(self.balance_amount - self.bet_amount),
                             msg='Bet was not placed as user balance has not changed')
            self.site.quick_bet_panel.header.close_button.click()
        # Parse log with responses
        logs = self.device.get_performance_log()
        for log in list(reversed(logs)):
            try:
                data_dict = log[1]['message']['message']['params']['response']['payloadData'].split('[')
                if data_dict[0] == str(42):
                    request = re.findall(r"^(.+?),", data_dict[1])[0].strip('"')
                    if request == str(response_id):
                        responses.append(data_dict)
            except (KeyError, TypeError, IndexError):
                continue
        self.assertEqual(len(responses), 1,
                         msg=f'Number of request present in remote betslip websocket "{len(responses)}" is not the same as expected "1"')

    def test_004_verify_user_balance(self):
        """
        DESCRIPTION: Verify User's balance
        EXPECTED: User's balance is decreased by entered Stake, not more than that
        """
        self.verify_user_balance(expected_user_balance=(self.balance_amount - self.bet_amount))

    def test_005_verify_open_bets_page(self):
        """
        DESCRIPTION: Verify 'Open Bets' page
        EXPECTED: Only one placed bet is present on 'Open Bets' page, there are no duplicated bets
        """
        bet_duplicates = []
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict,
                        name='No bets found on "Open Bets" page', expected_result=True,
                        timeout=20)
        self.assertTrue(bets, msg='No bets found on "Open Bets" page')
        self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                event_names=self.event_name,
                                                                number_of_bets=1)
        for event in bets.keys():
            bet_duplicates.append(event)
        self.assertEqual(len(bet_duplicates), 1, msg=f'There are duplicated bets in Open Bets": {bet_duplicates}')
