import pytest
import tests
import voltron.environments.constants as vec
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from tests.base_test import vtest
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.desktop
@vtest
class Test_C9608213_Verify_that_CASH_OUT_button_is_NOT_shown_when_cash_out_is_unavailable_for_the_bet(BaseCashOutTest):
    """
    TR_ID: C9608213
    NAME: Verify that 'CASH OUT'  button is NOT shown when cash out is unavailable for the bet
    DESCRIPTION: This test case verifies that 'CASH OUT' button is NOT shown when cash out is unavailable for the bet
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a SINGLE and MULTIPLE bets where one of the events in the bet with CASH OUT unavailable (In AccountHistory?DetailLevel... response: cashoutValue: "CASHOUT_SELN_NO_CASHOUT")
    """
    keep_browser_open = True
    number_of_events = 1

    def test_000_pre_conditions(self):
        """
            PRECONDITIONS: Login with User1
            PRECONDITIONS: Place a SINGLE and MULTIPLE bets where one of the events in the bet with CASH OUT unavailable (In AccountHistory?DetailLevel... response: cashoutValue: "CASHOUT_SELN_NO_CASHOUT")
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')

            cashout_filter_false = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'N'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'N')

            event1 = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)[0]
            outcomes = next(((market['market']['children']) for market in event1['event']['children']), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id1 = list(all_selection_ids.values())[0]

            event2 = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter_false,
                                                         number_of_events=self.number_of_events)[0]

            outcomes = next(((market['market']['children']) for market in event2['event']['children']), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id2 = list(all_selection_ids.values())[0]
            self.__class__.event_name = normalize_name(event2['event']['name'])

        else:
            event1 = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
            event2 = self.ob_config.add_autotest_premier_league_football_event(cashout=False)
            selection_id1 = list(event1.selection_ids.values())[0]
            selection_id2 = list(event2.selection_ids.values())[0]
            self.__class__.event_name = event2[7]['event']['name']

        self.navigate_to_page('Homepage')
        self.site.wait_content_state('homepage')
        self.site.login(username=tests.settings.betplacement_user)

        self.open_betslip_with_selections(selection_ids=(selection_id1, selection_id2))
        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()

        self.__class__.expected_betslip_counter_value = 0

        self.open_betslip_with_selections(selection_ids=selection_id2)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_my_betsopen_betsverify_that_cash_out_button_is_not_shown_for_the_bets_from_preconditions(
            self):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets
        DESCRIPTION: Verify that 'CASH OUT' button is NOT shown for the bets from preconditions
        EXPECTED: 'CASH OUT' button is NOT shown
        """
        self.site.open_my_bets_open_bets()
        self.__class__.open_bets = self.site.open_bets.tab_content.accordions_list
        bet_name, single_bet = self.open_bets.get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                                      event_names=self.event_name)
        self.assertFalse(single_bet.buttons_panel.has_full_cashout_button(expected_result=False, timeout=5),
                         msg=f'CASHOUT button is present for "{bet_name}" under Single bet. It should not.')

        bet_name, double_bet = self.open_bets.get_bet(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE,
                                                      event_names=self.event_name)
        self.assertFalse(double_bet.buttons_panel.has_full_cashout_button(expected_result=False, timeout=5),
                         msg=f'CASHOUT button is present for "{bet_name}" under Double bet. It should not.')

    def test_002_coral_onlynavigate_to_my_betscash_outverify_that_cash_out_button_is_not_shown_for_the_bets_from_preconditions(
            self):
        """
        DESCRIPTION: (Coral only)
        DESCRIPTION: Navigate to My Bets>Cash Out
        DESCRIPTION: Verify that 'CASH OUT' button is NOT shown for the bets from preconditions
        EXPECTED: 'CASH OUT' button is NOT shown
        """
        if tests.settings.brand == 'bma':
            self.site.open_my_bets_cashout()
            bet_name, single_bet = self.site.cashout.tab_content.accordions_list. \
                get_bet(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name,
                        raise_exceptions=False)
            self.assertFalse(single_bet,
                             msg=f'CASHOUT button is present for "{bet_name} under Double Single". It should not.')

            bet_name, double_bet = self.site.cashout.tab_content.accordions_list. \
                get_bet(bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event_name,
                        raise_exceptions=False)
            self.assertFalse(double_bet,
                             msg=f'CASHOUT button is present for "{bet_name} under Double Single". It should not.')
