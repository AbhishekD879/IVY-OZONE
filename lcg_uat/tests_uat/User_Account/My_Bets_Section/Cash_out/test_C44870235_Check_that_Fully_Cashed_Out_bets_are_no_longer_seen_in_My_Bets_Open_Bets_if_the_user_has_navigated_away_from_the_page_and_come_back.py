import datetime
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870235_Check_that_Fully_Cashed_Out_bets_are_no_longer_seen_in_My_Bets_Open_Bets_if_the_user_has_navigated_away_from_the_page_and_come_back(BaseBetSlipTest):
    """
    TR_ID: C44870235
    NAME: Check that Fully Cashed Out bets are no longer seen in My Bets->Open Bets if the user has navigated away from the page and come back
    """
    keep_browser_open = True
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_001_make_a_bet_from_a_cash_out_market(self):
        """
        DESCRIPTION: Make a bet from a cash out market
        EXPECTED: You should have placed a bet from a cash out market
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount=str(20),
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        all_available_events=True,
                                                        additional_filters=cashout_filter,
                                                        in_play_event=False, number_of_events=1)[0]
            self.__class__.event_name = event['event']['name']
            match_result_market = next((market['market'] for market in event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.site.login(username=username, async_close_dialogs=False)
            self.open_betslip_with_selections(selection_ids=list(all_selection_ids.values())[0])
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(cashout=True)
            self.__class__.event_name = event.team1
            all_selection_ids = event.selection_ids[event.team1]
            self.site.login(username=username, async_close_dialogs=False)
            self.open_betslip_with_selections(selection_ids=all_selection_ids)
        self.place_and_validate_single_bet()
        self.site.close_betreceipt()

    def test_002_go_to_my_bets_open_bets_and_fully_cash_out_this_bet(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and fully cash out this bet.
        EXPECTED: You should have fully cashed out this bet
        """
        self.site.open_my_bets_open_bets()
        _, bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type='SINGLE', event_names=self.event_name)
        self.assertTrue(bet.buttons_panel.has_full_cashout_button, msg='"FULL CASHOUT" button is not present')
        bet.buttons_panel.full_cashout_button.click()
        self.assertTrue(bet.buttons_panel.has_confirm_cashout_button(), msg='"Confirm Cashout" button is not displayed')
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.has_cashed_out_mark(timeout=20), msg='"Cash Out" is not successful')
        self.assertTrue(bet.wait_for_message(message=vec.bet_history.FULL_CASH_OUT_SUCCESS),
                        msg=f'Message "{vec.bet_history.FULL_CASH_OUT_SUCCESS}" is not displayed')

    def test_003_go_to_any_other_page_eg_my_bets_open_bets_or_click_on_menu_and_then_come_back_to_my_bets_open_bets_and_verify_that_your_cashed_out_bet_is_no_longer_seen_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Go to any other page e.g. My Bets->Open Bets or click on Menu and then come back to My Bets-Open Bets and verify that your cashed out bet is no longer seen in My Bets->Open Bets
        EXPECTED: Your bet should not be in My Bets-Open Bets
        """
        self.site.header.right_menu_button.click()
        self.site.right_menu.close_icon.click()
        self.site.open_my_bets_open_bets()
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        if len(sections) == 0:
            self._logger.info('*** Currently have no open bets')
        else:
            for section in sections.keys():
                if vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE in section:
                    self.assertFalse(self.event_name in section, msg=f'Cashed out event "{self.event_name}" found in '
                                                                     f'Open Bets tab')
