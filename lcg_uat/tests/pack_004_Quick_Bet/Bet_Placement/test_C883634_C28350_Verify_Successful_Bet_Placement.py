from fractions import Fraction

import pytest
from crlat_ob_client.utils.date_time import get_date_time_as_string
from voltron.utils.helpers import normalize_name
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_journey_new_customer
@pytest.mark.user_journey_promo_1
@pytest.mark.user_journey_single_greyhound_race
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.event_details
@pytest.mark.mobile_only
@pytest.mark.critical
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C883634_C28350_Verify_Successful_Bet_Placement(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C883634
    TR_ID: C28350
    VOL_ID: C9697948
    NAME: Verify Successful Bet Placement
    DESCRIPTION: This test case verifies successful Bet Placement within Quick Bet
    """
    keep_browser_open = True
    event_params = None

    start_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'
    end_date = f'{get_date_time_as_string(days=2)}T00:00:00.000Z'
    start_date_minus = get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S", hours=-3)
    blocked_hosts = ['*spark-br.*']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        DESCRIPTION: Open created event
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            self.__class__.created_event_name = normalize_name(event['event']['name'])
            market_name, outcomes = next(((market['market']['name'], market['market']['children'])
                                          for market in event['event']['children']
                                          if market['market']['templateMarketName'] == 'Match Betting' and
                                          market['market'].get('children')),
                                         ('Match Betting', []))

            self.__class__.selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            team1, price_resp = next(
                ((i['outcome']['name'], i['outcome']['children'][0]['price'])
                 for i in outcomes if
                 'price' in i['outcome']['children'][0].keys()),
                (outcomes[0]['outcome']['name'], ''))
            self.__class__.team1 = team1.replace('  ', ' ').strip()

            self.__class__.odds = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}' if price_resp else 'SP'  # if price response is empty -> SP
            self._logger.info(f'*** Found Football event "{self.eventID}" - "{self.created_event_name}" - "{market_name}" '
                              f'with selection ids {self.selection_ids} selection "{self.team1}" odds "{self.odds}"')

        else:
            self.__class__.event_params = self.ob_config.add_football_event_to_spanish_la_liga(is_live=True)
            self.__class__.eventID = self.event_params.event_id
            self.__class__.team1 = self.event_params.team1
            self.__class__.created_event_name = f"{self.event_params.team1.strip()} v {self.event_params.team2.strip()}"\
                .replace("  ", " ")
            self.__class__.odds = self.ob_config.event.prices['odds_home']
            market_name = self.ob_config.football_config.spain.spanish_la_liga.market_name.replace('|', '')

        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        self.site.login(async_close_dialogs=False)

    def test_001_open_event(self):
        """
        DESCRIPTION: Open created event
        EXPECTED: EDP of event is opened
        """
        self.__class__.user_balance = self.site.header.user_balance
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_log_in_to_oxygen(self):
        """
        DESCRIPTION: Log in to Oxygen application, get user balance
        """
        # covered in step 001

    def test_003_select_one_sport_selection(self):
        """
        DESCRIPTION: Tap one <Sport> selection
        EXPECTED: Quick Bet is displayed at the bottom of the page
        """
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.team1,
                                                           market_name=self.expected_market_name)

    def test_004_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: 'Stake' field is populated with entered value
        """
        self.assertTrue(self.site.quick_bet_panel.selection.content.amount_form.input.is_displayed(timeout=2),
                        msg='Amount input field is not displayed')
        quick_bet = self.site.quick_bet_panel.selection
        quick_bet.content.amount_form.input.value = self.bet_amount
        amount = float(quick_bet.content.amount_form.input.value)
        self.assertEqual(amount, self.bet_amount,
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')

    def test_005_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: - Bet Receipt is displayed with bet ID number
        EXPECTED: - Bet is placed successfully
        EXPECTED: - User balance is decreased by stake entered on step #4
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.__class__.bet_receipt = self.site.quick_bet_panel.bet_receipt
        self.assertTrue(self.bet_receipt.bet_id, msg='Bet ID is not shown on Bet Receipt')

        expected_user_balance = self.user_balance - self.bet_amount
        self.verify_user_balance(expected_user_balance=expected_user_balance)
        self.__class__.user_balance = expected_user_balance

    def test_006_check_placed_bet_info(self, is_decimal=False):
        """
        DESCRIPTION: Check placed bet information
        EXPECTED: All information about bet match with created event in Openbet Ti tool
        """
        self.assertEqual(self.bet_receipt.name, self.team1,
                         msg=f'Actual Outcome Name "{self.bet_receipt.name}" does not match expected "{self.team1}"')
        self.assertEqual(self.bet_receipt.event_market, self.expected_market_name.title(),
                         msg=f'Actual Market Name "{self.bet_receipt.event_market}" does not match expected "{self.expected_market_name}"')
        self.assertEqual(self.bet_receipt.event_name, self.created_event_name,
                         msg=f'Actual Event Name "{self.bet_receipt.event_name}" does not match expected "{self.created_event_name}"')
        if is_decimal:
            self.__class__.odds = '{0:.2f}'.format(float(Fraction(self.odds)) + 1)
            self.assertAlmostEqual(float(self.bet_receipt.odds), float(self.odds), delta=0.011,
                                   msg=f'Actual odds "{float(self.bet_receipt.odds)}" '
                                       f'does not match expected "{float(self.odds)}" within 0.011 delta')
        else:
            self.assertEqual(self.bet_receipt.odds, self.odds,
                             msg=f'Actual odds "{self.bet_receipt.odds}" does not match expected "{self.odds}"')

    def test_007_tap_x_button(self):
        """
        DESCRIPTION: Tap 'X' button
        EXPECTED: - Quick bet is closed
        EXPECTED: - User stays on the same page
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')
        self.site.wait_content_state(state_name='EventDetails')

    def test_008_change_odds_format_to_decimal(self):
        """
        DESCRIPTION: Go to Right Menu -> Setting item and change odds format to decimal
        EXPECTED: Decimal odds format is selected
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')

    def test_009_repeat_steps_3_7(self):
        """
        DESCRIPTION: Repeat steps #3-7
        EXPECTED: All steps validation pass
        """
        self.test_001_open_event()
        self.test_003_select_one_sport_selection()
        self.test_004_enter_value_in_stake_field()
        self.test_005_tap_place_bet_button()
        self.test_006_check_placed_bet_info(is_decimal=True)
        self.test_007_tap_x_button()
