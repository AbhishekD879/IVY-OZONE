import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870243__Verify_partial_cash_out_button_with_the_potential_returns_amount_on_the_cash_out__Open_Bets_tab_Verify_the_partial_cash_out_button_and_also_the_slider_with_proposed_cash_out_values_default_position_of_slider_in_middle_as_per_production__Verify(BaseBetSlipTest):
    """
    TR_ID: C44870243
    NAME: "-Verify partial cash-out button with the potential returns amount on the cash-out  /Open Bets tab -Verify the partial cash-out button and also the slider with proposed cash out values (default position of slider in middle as per production) - Verify
    DESCRIPTION: "-Verify partial cash-out button with the potential returns amount on the cash-out  /Open Bets tab
    DESCRIPTION: -Verify the partial cash-out button and also the slider with proposed cash out values (default position of slider in middle as per production)
    DESCRIPTION: - Verify by adjusting the slider up or down and the partial cashout value changes absed on slider .
    """
    keep_browser_open = True
    bet_amount = 1
    event_list = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Used should be logged in
        """
        self.site.login()

    def test_001_place_a_single_on_a_cash_out_market(self):
        """
        DESCRIPTION: Place a single on a Cash Out market
        EXPECTED: You should have placed a single
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         in_play_event=False,
                                                         all_available_events=True,
                                                         additional_filters=cashout_filter)
            for event in events:
                self.event_name = event['event']['name']
                if self.event_name not in self.event_list:
                    self.event_list.append(self.event_name)
                    match_result_market = next((market['market'] for market in event['event']['children'] if
                                                market.get('market').get('templateMarketName') == 'Match Betting'), None)
                    outcomes = match_result_market['children']
                    self.__class__.all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                    break
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(in_play_event=False)
            self.__class__.all_selection_ids = event.selection_ids
        self.open_betslip_with_selections(selection_ids=list(self.all_selection_ids.values())[0])
        self.place_and_validate_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_002_go_to_my_bets_open_bets_and_verify_that_your_bet_has_partial_cash_out_available_if_it_does_not_place_more_single_bets_until_you_have_a_bet_with_partial_cash_out(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that your bet has Partial Cash Out available. (If it does not, place more single bets until you have a bet with partial cash out)
        EXPECTED: Your bet should have Partial Cash Out available.
        """
        self.site.open_my_bets_open_bets()
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list. \
            get_bet(bet_type='SINGLE', selection_ids=list(self.all_selection_ids.values())[0])
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button, msg=F'"{vec.bet_history.CASHOUT}" button is not present')
        if not self.bet.buttons_panel.has_partial_cashout_button():
            self.expected_betslip_counter_value = 1
            self.device.go_back()
            self.test_001_place_a_single_on_a_cash_out_market()
            self.test_002_go_to_my_bets_open_bets_and_verify_that_your_bet_has_partial_cash_out_available_if_it_does_not_place_more_single_bets_until_you_have_a_bet_with_partial_cash_out()

    def test_003_click_on_the_partial_cash_out_button_and_verify_the_slider_with_proposed_cash_out_values_default_position_of_slider_in_middle_as_per_production(self):
        """
        DESCRIPTION: Click on the Partial Cash Out button and verify the slider with proposed cash out values (default position of slider in middle as per production)
        EXPECTED: You should see the slider with proposed cash out values (default position of slider in middle as per production)
        """
        full_cashout_value = float(self.bet.buttons_panel.partial_cashout_button.amount.value)
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        self.assertTrue(self.bet.buttons_panel.has_partial_cashout_slider,
                        msg='PARTIAL CASHOUT slider was not appeared')
        self.__class__.partial_cashout_value = float(self.bet.buttons_panel.partial_cashout_button.amount.value)
        expected_mid_slider_value = round(float(full_cashout_value / 2.0), 2)
        self.assertEqual(self.partial_cashout_value, expected_mid_slider_value,
                         msg=f'Actual mid slider value "{self.partial_cashout_value}" is not same as "{expected_mid_slider_value}"')

    def test_004_verify_that_sliding_to_the_left_decreases_you_cash_out_value_and_sliding_to_the_right_increases_it(self):
        """
        DESCRIPTION: Verify that sliding to the left decreases you cash out value and sliding to the right increases it
        EXPECTED: Sliding to the left should decrease the cash out value and sliding to the right should increase it
        """
        wait_for_result(lambda: self.bet.buttons_panel.move_partial_cashout_slider(direction='left'), timeout=5)
        left_slider_value = float(self.bet.buttons_panel.partial_cashout_button.amount.value)
        self.assertTrue(left_slider_value < self.partial_cashout_value,
                        msg=f'left slided value "{left_slider_value}" is not less than the previous cashout value "{self.partial_cashout_value}"')
        self.bet.buttons_panel.partial_cashout_close_button.click()
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        wait_for_result(lambda: self.bet.buttons_panel.move_partial_cashout_slider(direction='right'), timeout=5)
        right_slider_value = float(self.bet.buttons_panel.partial_cashout_button.amount.value)
        self.assertTrue(right_slider_value > left_slider_value,
                        msg=f'right slided value "{right_slider_value}" is not greater than the previous cashout value "{left_slider_value}"')

    def test_005_verify_that_clicking_on_the_x_closes_partial_cash_out_slider(self):
        """
        DESCRIPTION: Verify that clicking on the X closes Partial Cash Out slider
        EXPECTED: Clicking on the X should close Partial Cash Out slider
        """
        self.bet.buttons_panel.partial_cashout_close_button.click()
        self.assertFalse(self.bet.buttons_panel.wait_for_cashout_slider(expected_result=False),
                         msg='PARTIAL CASHOUT slider is present')

    def test_006_verify_that_clicking_on_the_cash_out_value_shows_you_the_confirm_cash_out_button_which_when_clicked_partially_cashes_out_the_bet(self):
        """
        DESCRIPTION: Verify that clicking on the Cash Out Value shows you the Confirm Cash Out button which when clicked partially cashes out the bet
        EXPECTED: You should see the Confirm Cash Out Button and clicking it should partially cash out your bet
        """
        self.bet.buttons_panel.partial_cashout_button.click()
        self.bet.buttons_panel.wait_for_cashout_slider()
        cashout_amount = self.bet.buttons_panel.partial_cashout_button.amount.value
        self.bet.buttons_panel.partial_cashout_button.click()
        confirmation_text = self.bet.buttons_panel.cashout_button.name
        currency_symbol = self.site.header.user_balance_section.currency_symbol
        expected_confirmation = vec.BetHistory.CASHOUT_BET.confirm_cash_out + ' ' + currency_symbol + cashout_amount
        self.assertEqual(expected_confirmation, confirmation_text,
                         msg=f'Expected confirmation text: "{expected_confirmation}" '
                             f'is not equal to actual: "{confirmation_text}"')
        self.bet.buttons_panel.cashout_button.click()
        self.assertTrue(self.bet.wait_for_message(message=vec.BetHistory.PARTIAL_CASH_OUT_SUCCESS, timeout=30),
                        msg=f'Message "{vec.BetHistory.PARTIAL_CASH_OUT_SUCCESS}" is not shown')
