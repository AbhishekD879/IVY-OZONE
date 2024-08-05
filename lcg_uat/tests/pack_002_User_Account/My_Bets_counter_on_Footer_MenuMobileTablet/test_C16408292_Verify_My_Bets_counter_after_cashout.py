import pytest
import datetime
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.lad_prod
@pytest.mark.lad_hl
# @pytest.mark.lad_tst2  # disabled Partial Cashout tests on TST2/STG2 endpoints
# @pytest.mark.lad_stg2  # due to offers constantly granted to user that prevents partial cashout appearance
@pytest.mark.high
@pytest.mark.other
@pytest.mark.footer
@pytest.mark.mobile_only
@vtest
class Test_C16408292_Verify_My_Bets_counter_after_cashout(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C16408292
    VOL_ID: C29855321
    NAME: Verify My Bets counter after cashout
    DESCRIPTION: This test case verifies that correct My Bets counter is displayed after successful cash-out
    PRECONDITIONS: - Load Oxygen/Roxanne Application
    PRECONDITIONS: - Make sure user has open (unsettled) bets with cash out available
    PRECONDITIONS: - Make sure 'BetsCounter' config is turned on in CMS > System configurations
    PRECONDITIONS: - My Bets' option is present and active in the top 5 list in Menus > Footer menus in CMS https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: - Should be tested for Sports/Races singles and multiple bets
    """
    keep_browser_open = True
    bet_amount = 2
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def get_bet_by_name(self, bet_name):
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg=f'Bets are not found on "Open Bets" page')
        bet = bets.get(bet_name)
        self.assertTrue(bet, msg=f'Bet {bet_name} is not found in {bets.keys()}')
        return bet

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        DESCRIPTION: Make bets for user
        """
        self.check_my_bets_counter_enabled_in_cms()
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')

            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        additional_filters=cashout_filter)[0]
            outcomes = next(((market['market']['children']) for market in event['event']['children']), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.event_name = normalize_name(event['event']['name'])
            self._logger.info(f'*** Found Football event with selection ids: "{self.selection_ids}"')
            event_start_time_local = self.convert_time_to_local(
                date_time_str=event['event']['startTime'],
                ob_format_pattern=self.ob_format_pattern,
                ss_data=True,
                future_datetime_format=self.event_card_future_time_format_pattern)
            self.__class__.first_bet_name = f'SINGLE - [{self.event_name} {event_start_time_local}]'
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
            self.__class__.selection_ids = event.selection_ids
            self.__class__.event_name = event.team1 + ' v ' + event.team2
            start_time = event.event_date_time
            start_time_local = self.convert_time_to_local(date_time_str=start_time,
                                                          future_datetime_format=self.event_card_future_time_format_pattern)
            self.__class__.first_bet_name = f'SINGLE - [{event.team1} v {event.team2} {start_time_local}]'

        self.__class__.second_bet_name = f'1 {self.first_bet_name}'

        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount=str(tests.settings.min_deposit_amount),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year, cvv='111')
        self.site.login(username=username)

        for selection in list(self.selection_ids.values())[:2]:
            self.open_betslip_with_selections(selection_ids=selection)
            self.place_single_bet()
            self.site.bet_receipt.close_button.click()
            self.__class__.expected_betslip_counter_value = 0

    def test_001_navigate_to_cash_out_tab_on_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page
        EXPECTED: 'Cash Out' tab is opened
        """
        self.site.open_my_bets_cashout()

    def test_002_make_a_full_cashout_for_a_bet(self):
        """
        DESCRIPTION: Make a full cashout for a bet
        EXPECTED: Bet is cashed out
        """
        bet = self.get_bet_by_name(self.first_bet_name)
        self.__class__.counter_before_cashout = int(self.get_my_bets_counter_value_from_footer())

        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.has_cashed_out_mark(timeout=20), msg='Cash Out is not successful')

    def test_003_verify_my_bets_counter_displaying_on_the_footer(self):
        """
        DESCRIPTION: Verify My Bets counter displaying on the Footer
        EXPECTED: My Bets counter is decreased by one
        """
        actual_indicator = int(self.get_my_bets_counter_value_from_footer())
        expected_indicator = self.counter_before_cashout - 1
        self.assertEqual(actual_indicator, expected_indicator,
                         msg=f'Actual value indicator "{actual_indicator}" != Expected "{expected_indicator}"')

        self.__class__.expected_indicator = actual_indicator

    def test_004_make_a_partial_cashout_for_another_bet(self):
        """
        DESCRIPTION: Make a partial cashout for another bet
        EXPECTED: Bet is partially cashed out
        """
        self.__class__.bet = self.get_bet_by_name(self.second_bet_name)
        self.__class__.counter_before_cashout = int(self.get_my_bets_counter_value_from_footer())

        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        expected_message = vec.bet_history.PARTIAL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=expected_message, timeout=30),
                        msg=f'Message "{expected_message}" is not shown')

    def test_005_verify_my_bets_counter_displaying_on_the_footer(self):
        """
        DESCRIPTION: Verify My Bets counter displaying on the Footer
        EXPECTED: My Bets counter remains the same
        """
        actual_indicator = int(self.get_my_bets_counter_value_from_footer())

        self.assertEqual(actual_indicator, self.expected_indicator,
                         msg=f'Actual value indicator "{actual_indicator}" != Expected "{self.expected_indicator}"')

    def test_006_make_a_full_cash_out_for_a_bet_from_step_4(self):
        """
        DESCRIPTION: Make a full cash out for a bet from step #4
        EXPECTED: Bet is cashed out
        """
        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.bet.has_cashed_out_mark(timeout=20), msg='Cash Out is not successful')

    def test_007_verify_my_bets_counter_displaying_on_the_footer(self):
        """
        DESCRIPTION: Verify My Bets counter displaying on the Footer
        EXPECTED: My Bets counter is decreased by one
        """
        self.__class__.expected_indicator = self.expected_indicator - 1
        actual_indicator = int(self.get_my_bets_counter_value_from_footer())

        self.assertEqual(actual_indicator, self.expected_indicator,
                         msg=f'Actual value indicator "{actual_indicator}" != Expected "{self.expected_indicator}"')
