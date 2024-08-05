import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from random import choices
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.acca
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870251_Verify_behaviour_when_editing_ACCA_Verify_selection_removal_buttons_are_displayed_adjacent_to_all_open_selections__After_the_user_clicks_a_Selection_Removal_button_then_the_selection_removal_button_is_no_longer_displayed__the_selection_removal_bu(BaseBetSlipTest):
    """
    TR_ID: C44870251
    NAME: "Verify behaviour when editing ACCA -Verify selection removal buttons are displayed adjacent to all open selections - After the user clicks a Selection Removal button then the selection removal button is no longer displayed - the selection removal bu
    DESCRIPTION: "Verify behaviour when editing ACCA
    DESCRIPTION: -Verify selection removal buttons are displayed adjacent to all open selections
    DESCRIPTION: - After the user clicks a Selection Removal button then the selection removal button is no longer displayed
    DESCRIPTION: - the selection removal button for the last open selection should become non-clickable
    DESCRIPTION: - When the user clicks on Edit My Bet, Confirm button is displayed but it is non-clickable
    DESCRIPTION: - When the user clicks on Selection Removal button, confirm button is displayed and is clickable
    DESCRIPTION: -  When user clicks on confirm button successful confirmation message is displayed
    DESCRIPTION: - Tapping on Cancel Edit should cancel the editing and bring user to the Openbet /Cashout Tab
    """
    keep_browser_open = True
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should be logged in
        PRECONDITIONS: User have placed a 4 fold or 5 fold accumulator bet.
        """
        self.site.login()
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in cms')

            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                               OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter, all_available_events=True,
                                                         in_play_event=False)
            required_events = choices(events, k=4)
            for event in required_events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)

            for i in range(4):
                event = self.ob_config.add_autotest_premier_league_football_event()
                selection_id = event.selection_ids[event.team1]
                self.selection_ids.append(selection_id)

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed(timeout=20, poll_interval=1)
        self.site.bet_receipt.close_button.click()
        self.site.wait_content_state(state_name='HomePage')

    def test_001_navigate_to_my_bets__open_bets_tabverify_edit_my_bet_button(self):
        """
        DESCRIPTION: Navigate to My Bets > Open bets tab
        DESCRIPTION: Verify 'EDIT MY BET' button
        EXPECTED: EDIT MY BET button is displayed.
        """
        self.site.open_my_bets_open_bets()
        sleep(2)
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets are available')
        self.__class__.bet = list(bets.values())[0]
        self.assertTrue(self.bet.edit_my_acca_button.is_displayed(),
                        msg='"Edit my bet" button is not displayed')

    def test_002_tap_edit_my_bet_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_bet_button(self):
        """
        DESCRIPTION: Tap EDIT My BET button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY BET' button
        EXPECTED: Edit mode of the ACCA is open
        EXPECTED: 'CANCEL EDITING' button is shown instead of EDIT MY BET button
        """
        edit_my_bet_text = self.bet.edit_my_acca_button.name
        self.bet.edit_my_acca_button.click()
        wait_for_result(
            lambda: list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0].edit_my_acca_button.name == vec.ema.CANCEL.upper(),
            name='"CANCEL EDITING" text to be displayed', timeout=10)
        cancel_button_text = self.bet.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.ema.CANCEL.upper(),
                         msg=f'actual text:"{edit_my_bet_text}" is not changed to Expected text:"{vec.ema.CANCEL.upper()}".')

    def test_003_verify_selection_removal_buttons_are_displayed_adjacent_to_all_open_selections(self):
        """
        DESCRIPTION: Verify selection removal buttons are displayed adjacent to all open selections
        EXPECTED: Removal buttons should be available for all open selections
        """
        self.__class__.selections = self.bet.items_as_ordered_dict.values()
        for selection in list(self.selections):
            self.assertTrue(selection.edit_my_acca_remove_icon.is_displayed(),
                            msg='"Selection removal icon(X)" is not displayed')

    def test_004_after_the_user_clicks_a_selection_removal_button_and_verify_if_undo_button_is_displayed(self):
        """
        DESCRIPTION: After the user clicks a Selection Removal button and verify if UNDO button is displayed.
        EXPECTED: UNDO button is displayed when the user clicks on the Selection removal button
        """
        for selection in list(self.selections)[:3]:
            selection.edit_my_acca_remove_icon.click()
            sleep(5)
            result = wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(),
                                     name='"UNDO button" to be displayed', timeout=10)
            self.assertTrue(result,
                            msg='"UNDO button" is not displayed when the user clicks on the "Selection removal icon(X)"')

    def test_005_verify_that_the_selection_removal_button_for_the_last_open_selection_should_become_non_clickable(self):
        """
        DESCRIPTION: Verify that the selection removal button for the last open selection should become non-clickable
        EXPECTED: The selection removal button for the last open selection should be non-clickable
        """
        selection = list(self.selections)[3]
        self.assertFalse(selection.edit_my_acca_remove_icon.click(),
                         msg='"Last Open Selection" is still in clickable state')

    def test_006_when_the_user_clicks_on_selection_removal_button_confirm_button_is_displayed_and_is_clickable(self):
        """
        DESCRIPTION: When the user clicks on Selection Removal button, confirm button is displayed and is clickable
        EXPECTED: The confirm button should be displayed and clickable
        """
        selection = list(self.selections)[2]
        selection.edit_my_acca_undo_icon.click()
        self.assertTrue(self.bet.confirm_button.is_enabled(), msg='"Confirm" button is not clickable')
        sleep(2)
        self.bet.confirm_button.click()

    def test_007_when_user_clicks_on_confirm_button_verify_that_the_successful_confirmation_message_is_displayed(self):
        """
        DESCRIPTION: When user clicks on confirm button, verify that the successful confirmation message is displayed
        EXPECTED: The successful confirmation message should be seen
        """
        result = wait_for_result(lambda: list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0].cash_out_successful_message == vec.ema.EDIT_SUCCESS.caption,
                                 name='"Acca Edited Successfully" message to be displayed', timeout=20)
        bets_after_EMB = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets_after_EMB, msg='No bets are available')
        bet_after_EMB = list(bets_after_EMB.values())[0]
        sucse_msg = bet_after_EMB.cash_out_successful_message
        self.assertTrue(result, msg=f'Message "{sucse_msg}" '
                                    f'is not the same as expected "{vec.ema.EDIT_SUCCESS.caption}"')

    def test_008_tapping_on_cancel_edit_should_cancel_the_editing_and_bring_user_to_the_openbet_cashout_tab(self):
        """
        DESCRIPTION: Tapping on Cancel Edit should cancel the editing and bring user to the Openbet /Cashout Tab
        EXPECTED: The edit should be cancelled and the user is on the Openbet/Cashout tab
        """
        bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets are available')
        bet = list(bets.values())[0]
        bet.edit_my_acca_button.click()
        result = wait_for_result(lambda: list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0].edit_my_acca_button.name == vec.ema.CANCEL.upper(),
                                 name='"CANCEL EDITING" text to be displayed', timeout=20)
        cancel_button_text = bet.edit_my_acca_button.name
        self.assertTrue(result, msg=f'Actual Cancel button text: "{cancel_button_text}" is not same as Expected Cancel button text: "{vec.ema.CANCEL.upper()}"')
        bet.edit_my_acca_button.click()

        if self.device_type == 'mobile':
            actual_my_bets_tabs = self.site.open_bets.tabs_menu.items_names
        else:
            actual_my_bets_tabs = self.site.betslip.tabs_menu.items_names
        self.assertEqual(actual_my_bets_tabs[0], vec.BetHistory.CASH_OUT_TAB_NAME,
                         msg=f'Actual Tab: "{actual_my_bets_tabs[0]}" is not same as Expected Tab: "{vec.BetHistory.CASH_OUT_TAB_NAME}"')
        self.site.wait_splash_to_hide(5)
        edit_acca_button_text = bet.edit_my_acca_button.name
        self.assertEqual(edit_acca_button_text, vec.EMA.EDIT_MY_BET,
                         msg='"Editing ACCA" has not been canceled')
