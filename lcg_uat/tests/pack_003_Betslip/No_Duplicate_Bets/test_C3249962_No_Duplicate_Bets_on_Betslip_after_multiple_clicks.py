import pytest
import datetime
import tests
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
import voltron.environments.constants as vec
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.bet_history
@pytest.mark.bet_placement
@pytest.mark.high
@pytest.mark.login
@vtest
class Test_C3249962_No_Duplicate_Bets_on_Betslip_after_multiple_clicks(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C3249962
    NAME: No Duplicate Bets on Betslip after multiple clicks
    DESCRIPTION: This test case verifies that user is not able to place duplicate bets by multiple clicking on Bet Now button
    """
    keep_browser_open = True
    deposit_amount = 5.00
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event and login
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category()[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.eventID = event['event']['id']

            outcomes = None
            for market in event['event'].get('children'):
                if market['market']['templateMarketName'] == 'Match Betting':
                    outcomes = market['market'].get('children')
            if not outcomes:
                raise SiteServeException('No Outcomes for market present is SS response')

            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}

            self._logger.info(f'*** Found event "{self.event_name}" with ids "{self.selection_ids}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_ids = event_params.selection_ids
            self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'

        self._logger.info(f'*** Found event "{self.event_name}" with ID "{self.eventID}" with selections {self.selection_ids}')

        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount=self.deposit_amount,
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')
        self.site.login(username=username)
        self.__class__.balance_amount = self.site.header.user_balance

    def test_001_add_selection_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        EXPECTED: Open Betslip with selection is shown
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])

    def test_002_enter_stake(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field
        EXPECTED: Bet is placed successfully
        """
        number_of_stakes = None
        stake_bet_amounts = None

        try:
            self.__class__.user_balance = self.get_betslip_content().header.user_balance if self.site.wait_logged_in(
                login_criteria='betslip_balance', timeout=3) else 0
        except NotImplementedError as e:
            self._logger.warning(e)
            self.__class__.user_balance = self.get_balance_by_page('all')
        section = self.get_betslip_sections().Singles
        number_of_stakes = number_of_stakes if number_of_stakes and number_of_stakes < len(section.keys()) else len(
            section.keys())
        available_stakes = list(
            self.zip_available_stakes(section=section, number_of_stakes=number_of_stakes).items())
        for stake in available_stakes:
            self.enter_stake_amount(stake=stake, stake_bet_amounts=stake_bet_amounts, each_way=False)
        wait_for_result(lambda: self.get_betslip_content().bet_now_button.is_enabled(), timeout=0.5, name='Bet Now is enabled')

    def test_003_click_multiple_times_on_bet_now_button(self):
        """
        DESCRIPTION: Click multiple times on 'BET NOW' button
        EXPECTED: Bet is placed only once
        EXPECTED: Bet Receipt is shown with one placed bet
        EXPECTED: Only one placebet request is present in network
        """
        # TODO: EXPECTED: Only one placebet request is present in network'. After implementation VOL-1815
        we = self.get_betslip_content().bet_now_button._we
        try:
            for _ in range(6):
                click(we)
            if 'Accept' in we.text:
                click(we)
        except StaleElementReferenceException as e:
            self._logger.debug(e)

        self.check_bet_receipt_is_displayed()
        bet_receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(bet_receipt_sections, msg='No BetReceipt sections found')
        self.assertEqual(len(bet_receipt_sections), 1,
                         msg=f'Bet receipt section should have one placed bet. Actual section: {bet_receipt_sections}')
        self.site.bet_receipt.footer.done_button.click()

    def test_004_verify_user_balance(self):
        """
        DESCRIPTION: Verify User's balance
        EXPECTED: User's balance is decreased by entered Stake, not more than that
        """
        balance_after_bet = self.balance_amount - self.bet_amount
        self.verify_user_balance(expected_user_balance=balance_after_bet)

    def test_005_verify_open_bets_page(self):
        """
        DESCRIPTION: Verify 'Open Bets' page
        EXPECTED: Only one placed bet is present on 'Open Bets' page, there are no duplicated bets
        """
        event_duplicates = []
        self.site.open_my_bets_open_bets()
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets found on "Open Bets" page')
        self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                                event_names=self.event_name,
                                                                number_of_bets=1)
        for event in bets.keys():
            event_duplicates.append(event)
        self.assertEqual(len(event_duplicates), 1, msg=f'There are duplicated bets in Open Bets": {event_duplicates}')
