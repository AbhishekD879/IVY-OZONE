import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from random import choices
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870241_3Customer_able_to_PARTIAL_Cash_Out_the_TRX_bet(BaseCashOutTest):
    """
    TR_ID: C44870241
    NAME: 3.Customer able to PARTIAL Cash Out the TRX bet
    """
    keep_browser_open = True

    def test_001_place_a_trixie_on_cash_out_markets(self):
        """
        DESCRIPTION: Place a Trixie on Cash Out markets
        EXPECTED: You should have placed a Trixie
        """
        selection_ids = []
        self.__class__.event_names = []
        self.site.login()
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True, additional_filters=cashout_filter,
                                                         in_play_event=False)
            event1 = choices(events, k=3)
            for event in event1:
                match_result_market = next((market for market in event['event']['children']), None)
                outcomes = match_result_market['market']['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                selection_ids.append(selection_id)
                self.event_names.append(event['event']['name'])
        else:
            events_params = self.create_several_autotest_premier_league_football_events(number_of_events=3, cashout=True)
            selection_ids = [event_params.selection_ids[event_params.team1] for event_params in events_params]
            event_names = [events_name.team1 for events_name in events_params]
            self.event_names.append(event_names)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_002_go_to_my_bets_open_bets_and_verify_that_your_bet_has_partial_cash_out_available_if_it_does_not_place_more_trixie_bets_until_you_have_a_bet_with_partial_cash_out(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that your bet has Partial Cash Out available. (If it does not, place more Trixie bets until you have a bet with partial cash out)
        EXPECTED: Your bet should have Partial Cash Out available.
        """
        self.site.open_my_bets_open_bets()
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type='TREBLE', event_names=self.event_names[0])
        if self.bet.buttons_panel.has_partial_cashout_button():
            self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(),
                            msg=f'"{vec.bet_history.PARTIAL_CASH_OUT_BTN_TEXT}" button is not displayed')
        else:
            self.test_001_place_a_trixie_on_cash_out_markets()
            self.site.open_my_bets_open_bets()
            _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type='TREBLE', event_names=self.event_names[0])

    def test_003_click_on_the_partial_cash_out_button_and_verify_that_you_see_a_slider_where_you_can_vary_the_amount_that_you_can_cash_out(self):
        """
        DESCRIPTION: Click on the Partial Cash Out button and verify that you see a slider where you can vary the amount that you can cash out.
        EXPECTED: You should have clicked on the Partial Cash Out button and see a slider
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.wait_for_cashout_slider(), msg=f'"{vec.bet_history.PARTIAL_CASH_OUT_BTN_TEXT}"slider was not appeared')

    def test_004_move_the_slider_in_any_direction_and_cash_out_the_bet(self):
        """
        DESCRIPTION: Move the slider in any direction and cash out the bet
        EXPECTED: You should have cashed out
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.bet.buttons_panel.move_partial_cashout_slider(direction='right')
        sleep(2)
        self.__class__.cashout_amount = self.bet.buttons_panel.partial_cashout_button.amount.value
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

    def test_005_verify_that_you_see_the_partial_cash_out_successful_message_and_that_you_header_balance_has_updated(self):
        """
        DESCRIPTION: Verify that you see the Partial Cash Out Successful message and that you header balance has updated
        EXPECTED: You should see a Partial Cash Out Successful message and your header should have updated
        """
        self.assertTrue(self.bet.wait_for_message(message=vec.bet_history.PARTIAL_CASH_OUT_SUCCESS, timeout=30),
                        msg=f'Message "{vec.bet_history.PARTIAL_CASH_OUT_SUCCESS}" is not shown')
        self.device.refresh_page()
        self.verify_user_balance(expected_user_balance=float(self.user_balance) + float(self.cashout_amount))
