import pytest
import voltron.environments.constants as vec
from decimal import Decimal
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.liveserv_updates
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C904907_Reflection_on_Sport_Unsuspension_and_Price_change(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C904907
    VOL_ID: C9697961
    NAME: Reflection on Sport Unsuspension and Price change
    """
    keep_browser_open = True
    new_price_decreased = '7/99'
    new_price_increased = '999/7'

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
        outcome_id = self.selection_ids['Draw']
        self.ob_config.change_price(selection_id=outcome_id, price=self.new_price_increased)

        self.ob_config.change_selection_state(selection_id=outcome_id, displayed=True)

        price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id,
                                                                 price=self.new_price_increased,
                                                                 multi_update=True)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{outcome_id}" is not received')

    def test_003_check_selection_is_suspended_in_quick_bet(self):
        """
        DESCRIPTION: Check selection is suspended in Quick Bet
        EXPECTED: 'Sorry, the selection/market/event has been suspended' warning message is displayed on yellow(#FFF270) background below 'QUICK BET' header
        EXPECTED: Stake field becomes disabled
        EXPECTED: 'LOGIN & PLACE BET' and 'Add to Betslip' buttons are disabled
        """
        self.site.quick_bet_panel.wait_for_quick_bet_info_panel()
        self.assertTrue(self.site.quick_bet_panel.info_panels_text, msg='No info panel texts found')
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.BET_PLACEMENT_ERRORS.outcome_suspended
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')
        self.assertFalse(self.site.quick_bet_panel.selection.content.amount_form.input.is_enabled(timeout=15, expected_result=False),
                         msg='Amount field is not greyed out')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='LOGIN & PLACE BET button is not disabled')
        self.assertFalse(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='Add to Betslip button is not disabled')

    def test_004_unsuspend_selection_in_backoffice_tool_and_change_price_for_selection_at_same_time(self):
        """
        DESCRIPTION: Unsuspend selection in Backoffice tool and change price for selection at same time
        EXPECTED: Changes are saved
        """
        outcome_id = self.selection_ids['Draw']
        self.ob_config.change_selection_state(selection_id=self.selection_ids['Draw'], displayed=True, active=True)
        self.ob_config.change_price(selection_id=outcome_id, price=self.new_price_decreased)

        price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id,
                                                                 price=self.new_price_decreased,
                                                                 multi_update=True)
        self.assertTrue(price_update,
                        msg=f'Price update for selection id "{outcome_id}" is not received')

    def test_005_check_selection_is_unsuspended_and_new_price_is_displayed_in_quick_bet(self, price=new_price_decreased,
                                                                                        new_price=new_price_increased):
        """
        DESCRIPTION: Check selection is unsuspended and new price is displayed in Quick Bet
        EXPECTED: * Old Odds are instantly changed to New Odds :
        EXPECTED: No warning message is displayed
        EXPECTED: * 'LOGIN & PLACE BET' and 'ADD TO BETSLIP' buttons are enabled
        """
        quick_bet = self.site.quick_bet_panel.selection.content
        result = wait_for_result(lambda: price in quick_bet.odds_value,
                                 name='Odd changes',
                                 timeout=5)
        self.assertTrue(result, msg=f'Old Odd "{quick_bet.odds_value}" is not instantly changed to "{price}"')
        actual_message = self.site.quick_bet_panel.info_panels_text[0]
        expected_message = vec.quickbet.PRICE_IS_CHANGED.format(old=new_price, new=price)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" does not match expected "{expected_message}"')

        self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

    def test_006_close_quick_bet(self):
        """
        DESCRIPTION: Close Quick Bet
        EXPECTED: Quick Bet is closed
        EXPECTED: Selection is unselected
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide()

    def test_007_go_to_settings_and_switch_odds_format_to_decimal(self):
        """
        DESCRIPTION: Go to Settings and switch Odds format to Decimal
        """
        self.site.login(async_close_dialogs=False, timeout_close_dialogs=4)
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')

    def test_008_repeat_steps(self):
        """
        DESCRIPTION: Repeat steps
        EXPECTED: Results are the same
        """
        new_price_decreased = '{0:.2f}'.format(Decimal(7 / 99) + 1)
        new_price_increased = '{0:.2f}'.format(Decimal(999 / 7) + 1)
        self.site.open_betslip()
        self.clear_betslip()
        self.test_001_select_one_sport_selection()
        self.test_002_change_price_for_the_selection_and_suspend_it_in_backoffice_tool()
        self.test_003_check_selection_is_suspended_in_quick_bet()
        self.test_004_unsuspend_selection_in_backoffice_tool_and_change_price_for_selection_at_same_time()
        self.test_005_check_selection_is_unsuspended_and_new_price_is_displayed_in_quick_bet(price=new_price_decreased,
                                                                                             new_price=new_price_increased)
