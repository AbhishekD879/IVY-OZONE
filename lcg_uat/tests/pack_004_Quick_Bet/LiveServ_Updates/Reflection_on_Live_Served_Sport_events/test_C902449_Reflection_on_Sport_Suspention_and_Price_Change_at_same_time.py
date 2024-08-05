from decimal import Decimal
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.quick_bet
@pytest.mark.liveserv_updates
@pytest.mark.ob_smoke
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C902449_Reflection_on_Sport_Suspension_and_Price_Change_at_same_time(BaseSportTest):
    """
    TR_ID: C902449
    VOL_ID: C9697699
    NAME: Reflection on Sport Suspension and Price Change at same time
    """
    keep_browser_open = True
    new_price_increased = '99/7'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.eventID = event.event_id
        self.__class__.selection_ids = event.selection_ids

    def test_001_select_one_sport_selection(self):
        """
        DESCRIPTION: Open created event
        DESCRIPTION: Select one <Sport> selection
        EXPECTED: Quick Bet is opened
        EXPECTED: Added selection is displayed
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet()

    def test_002_change_price_for_the_selection_and_suspend_it_in_backoffice_tool(self):
        """
        DESCRIPTION: Change price for the selection and suspend it in Backoffice tool
        EXPECTED: Changes are saved
        """
        self.__class__.outcome_id = self.selection_ids['Draw']
        self.ob_config.change_price(selection_id=self.outcome_id, price=self.new_price_increased)

        self.ob_config.change_selection_state(selection_id=self.outcome_id, displayed=True)

    def test_003_check_price_displaying_in_quick_bet(self, price=new_price_increased):
        """
        DESCRIPTION: Check price displaying in Quick Bet
        EXPECTED: * Old Odds are instantly changed to New Odds
        EXPECTED: * Stake field is greyed out(disabled)
        """
        price_update = self.wait_for_price_update_from_live_serv(selection_id=self.outcome_id,
                                                                 price=self.new_price_increased,
                                                                 multi_update=True)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{self.outcome_id}" is not received')

        quick_bet = self.site.quick_bet_panel.selection.content
        self.assertFalse(quick_bet.amount_form.input.is_enabled(timeout=30, expected_result=False),
                         msg='Stake field is not greyed out')

        quick_bet = self.site.quick_bet_panel.selection.content
        result = wait_for_result(lambda: price in quick_bet.odds_value,
                                 name='Odd changes',
                                 timeout=3)
        self.assertTrue(result, msg=f'Old Odd "{quick_bet.odds_value}" is not instantly changed to "{price}"')

    def test_004_verify_warning_message_and_login_place_bet_button_displaying(self):
        """
        DESCRIPTION: Verify warning message and 'LOGIN & PLACE BET' button displaying
        EXPECTED: * Sorry, the selection has been suspended' warning message is displayed on yellow(#FFF270) background below 'QUICK BET' header
        EXPECTED: * 'LOGIN & PLACE BET' button is disabled
        """
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.BET_PLACEMENT_ERRORS.outcome_suspended
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='LOGIN & PLACE BET button is not disabled')

    def test_005_close_quick_bet(self):
        """
        DESCRIPTION: Close Quick Bet
        EXPECTED: * Quick Bet is closed
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

    def test_006_go_to_settings_and_switch_odds_format_to_decimal(self):
        """
        DESCRIPTION: Login and go to Settings and switch Odds format to Decimal
        """
        self.site.login(async_close_dialogs=False)
        self.ob_config.change_selection_state(selection_id=self.outcome_id, active=True, displayed=True)
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')

    def test_007_repeat_step(self):
        """
        DESCRIPTION: Repeat steps
        EXPECTED: Results are the same
        """
        decimal_price = '{0:.2f}'.format(Decimal(99 / 7) + 1)
        self.test_001_select_one_sport_selection()
        self.test_002_change_price_for_the_selection_and_suspend_it_in_backoffice_tool()
        self.test_003_check_price_displaying_in_quick_bet(price=decimal_price)
        self.test_004_verify_warning_message_and_login_place_bet_button_displaying()
