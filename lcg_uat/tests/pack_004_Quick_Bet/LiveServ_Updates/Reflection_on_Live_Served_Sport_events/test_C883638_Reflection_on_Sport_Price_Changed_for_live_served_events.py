import pytest
import tests
from decimal import Decimal
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed, can't create OB event on prod, can't trigger LiveServe updates on prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.quick_bet
@pytest.mark.liveserv_updates
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C883638_Reflection_on_Sport_Price_Changed_for_live_served_events(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C883638
    VOL_ID: C9698454
    NAME: Reflection on Sport Price Changed for live served events
    DESCRIPTION: This test case verifies Quick Bet reflection on Sports Price Changed
    """
    keep_browser_open = True
    start_price = '99/7'
    new_price_decreased = '7/99'
    new_price_increased = '999/7'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = event.selection_ids

        market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        self.__class__.new_price_increased_fract = self.new_price_increased
        self.__class__.new_price_decreased_fract = self.new_price_decreased

    def test_001_select_one_sport_selection(self):
        """
        DESCRIPTION: Open created event
        DESCRIPTION: Select one <Sport> selection
        EXPECTED: Quick Bet is opened
        EXPECTED: Added selection is displayed
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

    def test_002_change_price_for_the_selection_in_backoffice_tool(self):
        """
        DESCRIPTION: Change price for the selection in Backoffice tool
        """
        self.ob_config.change_price(selection_id=self.selection_ids['Draw'], price=self.start_price)
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_bet_info_panel(expected_result=True),
                        msg='Quick Bet Info Panel is not present')
        start_text = self.site.quick_bet_panel.info_panels_text[0]

        outcome_id = self.selection_ids['Draw']
        self.ob_config.change_price(selection_id=outcome_id, price=self.new_price_increased)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id,
                                                                 price=self.new_price_increased_fract)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{outcome_id}" is not received')
        self.site.quick_bet_panel.wait_for_message_to_change(previous_message=start_text)

    def test_003_check_that_price_is_updated_in_quick_bet(self):
        """
        DESCRIPTION: Check that price is updated in Quick Bet
        EXPECTED: Old Odds are instantly changed to New Odds
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        result = wait_for_result(lambda: self.new_price_increased in quick_bet.odds_value,
                                 name='Odd changes',
                                 timeout=2)
        self.assertTrue(result, msg=f'Old Odd "{quick_bet.odds_value}" is not instantly changed to "{self.new_price_increased}"')

    def test_004_verify_warning_message_and_login_place_bet_button_displaying(self):
        """
        DESCRIPTION: Verify warning message and  'LOGIN & PLACE BET' button displaying
        EXPECTED: 'Price changed from 'n' to 'n'' warning message is displayed on yellow(#FFF270) background below 'QUICK BET' header
        EXPECTED: * 'LOGIN & PLACE BET' button is disabled
        """
        texts = wait_for_result(lambda: self.site.quick_bet_panel.info_panels_text,
                                name='Waiting for warning message',
                                timeout=5)
        self.assertTrue(texts, msg='No info panel texts found')  # TODO: VOL-3301

        actual_message = texts[0]
        expected_message = vec.quickbet.PRICE_IS_CHANGED. \
            format(old=self.start_price, new=self.new_price_increased)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')

        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='"LOGIN & PLACE BET" button is not disabled')

    def test_005_enter_stake_in_stake_field_and_trigger_price_change(self):
        """
        DESCRIPTION: Enter stake in 'Stake' field and trigger price change
        EXPECTED: Old Odds are instantly changed to New Odds
        EXPECTED: Warning Message should remain during the input of at least 1 number into the stake field and re-appears after the price change trigger
        EXPECTED: Est. Returns and Total Est. Returns should be recalculated
        EXPECTED: 'LOGIN & PLACE BET' button becomes enabled
        """
        outcome_id = self.selection_ids['Draw']
        old_message = self.site.quick_bet_panel.info_panels_text[0]
        self.ob_config.change_price(selection_id=outcome_id, price=self.new_price_decreased)

        self.site.quick_bet_panel.selection.content.amount_form.input.value = '0.01'
        self.assertTrue(self.site.quick_bet_panel.wait_for_quick_bet_info_panel(),
                        msg='Quick Bet Info Panel is not present')

        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='"ADD TO BETSLIP" button is not enabled')

        price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id,
                                                                 price=self.new_price_decreased_fract)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{outcome_id}" is not received')
        self.site.quick_bet_panel.wait_for_message_to_change(previous_message=old_message)

        quick_bet = self.site.quick_bet_panel.selection.content
        result = wait_for_result(lambda: self.new_price_decreased in quick_bet.odds_value,
                                 name='Odd changes',
                                 timeout=2)
        self.assertTrue(result, msg=f'Old Odd "{quick_bet.odds_value}" is not instantly changed to "{self.new_price_decreased}"')

        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.PRICE_IS_CHANGED. \
            format(old=self.new_price_increased, new=self.new_price_decreased)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')

    def test_006_login_with_user_account_with_positive_balance(self):
        """
        DESCRIPTION: Login with user account with positive balance
        EXPECTED: User is logged in
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.site.login(async_close_dialogs=False)

    def test_007_go_to_settings_and_switch_odds_format_to_decimal(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Decimal
        EXPECTED: Odds format successfully changed to Decimal
        """
        change_odds_format = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(change_odds_format, msg=f'Odds format was not changed to {vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC}')

    def test_008_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps #2-5
        EXPECTED: Results are the same
        """
        self.new_price_decreased = '{0:.2f}'.format(Decimal(7 / 99) + 1)
        self.new_price_increased = '{0:.2f}'.format(Decimal(999 / 7) + 1)
        self.start_price = '{0:.2f}'.format(Decimal(99 / 7) + 1)
        self.new_price_increased_fract = '14271/100'
        self.new_price_decreased_fract = '7/100'
        self.site.open_betslip()
        self.clear_betslip()
        self.test_001_select_one_sport_selection()
        self.test_002_change_price_for_the_selection_in_backoffice_tool()
        self.test_003_check_that_price_is_updated_in_quick_bet()
        self.test_004_verify_warning_message_and_login_place_bet_button_displaying()
        self.test_005_enter_stake_in_stake_field_and_trigger_price_change()
