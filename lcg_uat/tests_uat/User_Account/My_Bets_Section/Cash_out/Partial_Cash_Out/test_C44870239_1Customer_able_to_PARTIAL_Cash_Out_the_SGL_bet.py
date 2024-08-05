import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p1
@pytest.mark.uat
# @pytest.mark.prod
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870239_1Customer_able_to_PARTIAL_Cash_Out_the_SGL_bet(BaseCashOutTest):
    """
    TR_ID: C44870239
    NAME: 1.Customer able to PARTIAL Cash Out the SGL bet
    """
    keep_browser_open = True

    def test_001_place_a_single_on_a_cash_out_market(self):
        """
        DESCRIPTION: Place a single on a Cash Out market
        EXPECTED: You should have placed a single
        """
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
            simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                    all_available_events=True,
                                                    additional_filters=cashout_filter,
                                                    in_play_event=False, number_of_events=1)[0]
        self.__class__.event_name = event['event']['name']
        market = next((market for market in event['event']['children']), None)
        outcomes_resp = market['market']['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                             for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}

        username = tests.settings.betplacement_user
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)
        self.assertTrue(self.site.header.has_freebets(), msg='User does not have Free bets')

        self.open_betslip_with_selections(selection_ids=list(all_selection_ids.values())[0])
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        _, stake = list(singles_section.items())[0]
        self.assertEquals(self.event_name, stake.event_name, msg=f'{self.event_name} not matching '
                                                                 f'with {stake.event_name} in single section')
        stake.amount_form.input.value = self.bet_amount
        if self.brand == 'ladbrokes':
            self.get_betslip_content().bet_now_button.click()
        else:
            self.get_betslip_content().betnow_section.bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_002_go_to_my_bets_open_bets_and_verify_that_your_bet_has_partial_cash_out_available_if_it_does_not_place_more_single_bets_until_you_have_a_bet_with_partial_cash_out(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that your bet has Partial Cash Out available. (If it does not, place more single bets until you have a bet with partial cash out)
        EXPECTED: Your bet should have Partial Cash Out available.
        """
        self.site.open_my_bets_open_bets()
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type='SINGLE', event_names=self.event_name)
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_button(), msg='"Partial Cashout" button is not '
                                                                                 'displayed')

    def test_003_click_on_the_partial_cash_out_button_and_verify_that_you_see_a_slider_where_you_can_vary_the_amount_that_you_can_cash_out(self):
        """
        DESCRIPTION: Click on the Partial Cash Out button and verify that you see a slider where you can vary the amount that you can cash out.
        EXPECTED: You should have clicked on the Partial Cash Out button and see a slider
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.assertTrue(self.bet.buttons_panel.wait_for_cashout_slider(), msg='"Partial Cashout" slider was not '
                                                                              'appeared')

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
