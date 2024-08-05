import re
import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.insprint_auto
@pytest.mark.bet_history_open_bets
@pytest.mark.value_area
@vtest
class Test_C66130513_Verify_Cashed_out_message_in_open_Cash_out_Settled_tabs_when_a_customer_has_cashed_out_even_though_the_cash_out_value_is_lower_value_than_stake(
    BaseBetSlipTest):
    """
    TR_ID: C66130513
    NAME: Verify Cashed out message in open ,Cash out, Settled tabs when a customer has cashed out even though the cash out value is lower value than stake.
    DESCRIPTION: This testcase verifies cashed out message in open ,Cash out, Settled tabs when a customer has cashed out even for a lower value than stake.
    PRECONDITIONS: User should be login to application
    PRECONDITIONS: Cashout bets should be available
    """
    keep_browser_open = True

    def verify_you_cashed_out_message(self, bet=None, tab_name=None):
        expected_cash_out_message_pattern = r'^YOU CASHED OUT: £\d+\.\d{2}$'
        expected_cash_out_message_background_color = 'rgb(139, 189, 35)' if self.brand != 'bma' else 'rgb(120, 190, 32)'
        expected_cash_out_message_font_weight = '700'
        expected_cash_out_message_font_size = '13px'
        expected_cash_out_message_font_name = 'Roboto Condensed' if self.brand != 'bma' else 'Lato, Arial, Helvetica Neue, Helvetica, sans-serif'

        cash_out_message = bet.you_cashed_out_message.name.replace('\n', '')
        cash_out_message_background_color = \
            bet.you_cashed_out_message.css_property_value('background').split(')')[0] + ')'
        cash_out_message_font_weight = bet.you_cashed_out_message.css_property_value('font-weight')
        cash_out_message_font_size = bet.you_cashed_out_message.css_property_value('font-size')
        cash_out_message_font_name = bet.you_cashed_out_message.css_property_value('font-family').replace('"', '')

        is_cash_out_message_matched = True if re.match(expected_cash_out_message_pattern, cash_out_message) else False
        self.assertTrue(is_cash_out_message_matched,
                        msg=f'Expected cash out success message is {expected_cash_out_message_pattern} but Actual is {cash_out_message}')
        self.assertEqual(expected_cash_out_message_background_color, cash_out_message_background_color,
                         msg=f'expected Cash out message background color is {expected_cash_out_message_background_color} but actual is {cash_out_message_background_color} under {tab_name}')
        self.assertEqual(expected_cash_out_message_font_weight, cash_out_message_font_weight,
                         msg=f'expected Cash out message font weight is {expected_cash_out_message_font_weight} but '
                             f'actual font weight is {cash_out_message_font_weight} under {tab_name}')
        self.assertEqual(expected_cash_out_message_font_size, cash_out_message_font_size,
                         msg=f'expected Cash out message font size is {expected_cash_out_message_font_size} but actual '
                             f'font size is {cash_out_message_font_size} under {tab_name}')
        self.assertEqual(expected_cash_out_message_font_name, cash_out_message_font_name,
                         msg=f'expected Cash out message font name is {expected_cash_out_message_font_name} but actual '
                             f'font name is {cash_out_message_font_name} under {tab_name}')

    def test_000_preconditions(self):
        """
        Get selections to place the bet
        """
        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                           OPERATORS.EQUALS, 'Y')
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                    additional_filters=cashout_filter,
                                                    number_of_events=1)[0]
        match_result_market = next((market['market'] for market in event['event']['children'] if
                                    market.get('market').get('templateMarketName') == 'Match Betting'), None)
        outcomes = match_result_market['children']
        all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
        self.__class__.selection_id = list(all_selection_ids.values())[0]

    def test_001_load_oxygen_application_ladbrokescoral(self):
        """
        DESCRIPTION: Load oxygen application Ladbrokes/Coral
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_002_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application
        EXPECTED: User should login successfully with valid credentials
        """
        # Covered in above step

    def test_003_add_selections_to_bet_and_place_a_single_bet_selections_should_be_available_for_cash_out(self):
        """
        DESCRIPTION: Add selections to bet and place a single bet. Selections should be available for cash out
        EXPECTED: Bet is placed successfully
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        # Covered in test_006_click_on_cash_out_tab_for_the_bet_where_cash_out_value_is_lower_value_than_stake

    def test_005_verify_the_recently_played_bet_in_open_tab(self):
        """
        DESCRIPTION: Verify the recently played bet in open tab
        EXPECTED: Bet should displayed with all the bet details in open tab
        """
        # Covered in test_006_click_on_cash_out_tab_for_the_bet_where_cash_out_value_is_lower_value_than_stake

    def test_006_click_on_cash_out_tab_for_the_bet_where_cash_out_value_is_lower_value_than_stake(self):
        """
        DESCRIPTION: Click on cash out tab for the bet where cash out value is lower value than stake.
        EXPECTED: You cashed out:0.00 message displayed in green back ground below the bet header
        """
        self.site.open_my_bets_cashout()
        cash_out_bet = next(
            iter(list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(cash_out_bet, msg='Bet is not available under Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')
        self.verify_you_cashed_out_message(bet=cash_out_bet, tab_name='Cash Out tab')

        self.site.open_my_bets_settled_bets()
        settled_bet = next(iter(
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(settled_bet, msg='Bet is not available under Settled tab')
        self.verify_you_cashed_out_message(bet=settled_bet, tab_name='Settled tab')

    def test_007_repeat_step_6_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat step 6 in cash out tab
        EXPECTED: Result should be same
        """
        # Covered in above step

    def test_008_now_click_on_settled_tab(self):
        """
        DESCRIPTION: Now click on settled tab
        EXPECTED: Settled tab opened
        """
        # Covered in above step

    def test_009_verify_cashed_out_bets__where_cashed_out_value_is_lower_value_than_stake(self):
        """
        DESCRIPTION: verify cashed out bets  where cashed out value is lower value than stake.
        EXPECTED: You cashed out:0.00 message displayed in green back ground below the bet header
        """
        # Covered in above step
