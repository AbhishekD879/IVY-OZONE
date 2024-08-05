import pytest
import tests
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.acca
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870254_Verify_edited_acca_in_Open_Bets_tabUser_sees_their_acca_as_per_below(BaseCashOutTest):
    """
    TR_ID: C44870254
    NAME: Verify edited  acca in Open Bets tab,User sees their acca as per below
    """
    keep_browser_open = True
    number_of_events = 4
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: EMA is enabled in CMS
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: User have placed a 4 fold or 5 fold accumulator bet.
        """
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=self.number_of_events)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)
            event_params = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.close_button.click()

    def test_001_navigate_to_my_bets__open_bets_tabverify_that_edit_my_bet_button(self):
        """
        DESCRIPTION: Navigate to My Bets > Open bets tab
        DESCRIPTION: Verify that EDIT MY BET button
        EXPECTED: EDIT MY BET button is shown only for Accumulator bets.
        """
        self.site.open_my_bets_open_bets()
        self.__class__.bet_before_EMA = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(self.bet_before_EMA, msg=f'"{self.bet_before_EMA}" is not displayed"')
        self.__class__.stake_before_EMA = self.bet_before_EMA.stake.value
        self.assertTrue(self.bet_before_EMA.edit_my_acca_button.is_displayed(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed')
        self.__class__.cashout_button = self.bet_before_EMA.buttons_panel.full_cashout_button.label
        self.__class__.bet_type_before_EMA = self.bet_before_EMA.bet_type
        self.__class__.actual_potential_returns = self.bet_before_EMA.est_returns.value

    def test_002_tap_edit_my_bet_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_acca_button(self):
        """
        DESCRIPTION: Tap EDIT My BET button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY ACCA' button
        EXPECTED: Edit mode of the ACCA is open
        EXPECTED: 'CANCEL EDITING' button is shown instead of EDIT MY ACCA button
        """
        self.bet_before_EMA.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(5)
        wait_for_result(lambda: self.bet_before_EMA.edit_my_acca_button.name, name=f'"{vec.EMA.CANCEL}" to be displayed', timeout=30)
        cancel_button_text = self.bet_before_EMA.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                         msg=f'Actual text:"{vec.EMA.EDIT_MY_BET}" is not changed to Expected text:"{vec.EMA.CANCEL}".')

    def test_003_select_the_selections_from_acca(self):
        """
        DESCRIPTION: select the selections from ACCA
        EXPECTED: cash out' button change as 'CONFIRM' and text display on the top of 'Confirm' button.
        EXPECTED: Undo button should be displayed when user select the selections.
        """
        selections = list(self.bet_before_EMA.items_as_ordered_dict.values())[0]
        self.assertTrue(selections, msg=f'"{selections}"not displayed')
        self.__class__.expected_event_name = selections.event_name
        selections.edit_my_acca_remove_icon.click()
        self.__class__.confirm_button = self.bet_before_EMA.confirm_button.name
        self.assertEqual(self.confirm_button, vec.EMA.CONFIRM_EDIT.upper(),
                         msg=f'Actual text:"{self.cashout_button}" is not changed to Expected text:"{vec.EMA.CONFIRM_EDIT.upper()}".')
        self.assertTrue(wait_for_result(lambda: selections.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                        msg=f'"{vec.EMA.UNDO_LEG_REMOVE}" not displayed')

    def test_004_tap_on_confirm_button(self):
        """
        DESCRIPTION: Tap on confirm button
        EXPECTED: confirm button changed to timer.
        EXPECTED: user has successfully edited their acca.
        """
        self.bet_before_EMA.confirm_button.click()
        self.assertEqual(self.cashout_button, vec.bet_history.CASH_OUT_TAB_NAME,
                         msg=f'Actual text:"{vec.bet_history.CASH_OUT_TAB_NAME}" is not changed to Expected text:"{vec.bet_history.CASH_OUT_TAB_NAME}".')
        self.__class__.bet_after_EMA = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(self.bet_after_EMA, msg=f'"{vec.EMA.EDIT_MY_BET}" is not displayed')
        sleep(3)
        EMA_success_msg = self.bet_after_EMA.cash_out_successful_message
        self.assertEqual(EMA_success_msg, vec.EMA.EDIT_SUCCESS.caption,
                         msg=f'Actual message: "{EMA_success_msg}" is not the same as Expected message: "{vec.EMA.EDIT_SUCCESS.caption}"')

    def test_005_verify_the_my_betsopen_bets_area_after_remove_the_selections(self):
        """
        DESCRIPTION: verify the my bets(open bets) area after remove the selections
        EXPECTED: The new bet type name is displayed.
        EXPECTED: The selection(s) which were removed have a Removed token displayed
        EXPECTED: Removed selections should appear below Open selections
        EXPECTED: The new stake is displayed
        EXPECTED: Prices are displayed for any selections
        EXPECTED: The new potential returns are displayed
        """
        bet_type_after_EMA = self.bet_after_EMA.bet_type
        self.assertNotEqual(bet_type_after_EMA, self.bet_type_before_EMA,
                            msg=f'Actual  bet type "{bet_type_after_EMA}" is same as Expected bet type "{self.bet_type_before_EMA}"')
        new_selection = list(self.bet_after_EMA.items_as_ordered_dict.values())[-1]
        self.assertTrue(new_selection.leg_remove_marker.is_displayed(),
                        msg=f'"{new_selection.leg_remove_marker}" is not displayed')
        actual_event_name = new_selection.event_name
        self.assertEqual(actual_event_name, self.expected_event_name,
                         msg=f' Actual text "{actual_event_name}" is not same as Expected text "{self.expected_event_name}"')
        self.assertTrue(new_selection.odds_value, msg=f'"{new_selection.odds_value}" not displayed')
        self.site.wait_splash_to_hide(3)
        self.assertNotEqual(self.bet_after_EMA.stake.value, self.stake_before_EMA,
                            msg=f'stake :"{self.bet_after_EMA.stake.value}" is same as New stake:"{self.stake_before_EMA}".')
        new_potential_returns = self.bet_after_EMA.est_returns.value
        self.assertNotEqual(self.actual_potential_returns, new_potential_returns,
                            msg=f'Actual potential returns:"{self.actual_potential_returns}" is same as New potential returns:"{new_potential_returns}".')
