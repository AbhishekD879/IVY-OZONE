import pytest
import tests
from time import sleep
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C44870252_User_Edited_Acca_Details(BaseBetSlipTest):
    """
    TR_ID: C44870252
    NAME: "User Edited Acca Details
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User have accumulator bets on my bets area
    PRECONDITIONS: and has some EMA bets
    """
    keep_browser_open = True
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User have accumulator bets on my bets area
        PRECONDITIONS: and has some EMA bets
        """
        if tests.settings.backend_env == 'prod':
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'), \
                simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         additional_filters=cashout_filter,
                                                         number_of_events=4)
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

            for i in range(4):
                event = self.ob_config.add_autotest_premier_league_football_event()
                selection_id = event.selection_ids[event.team1]
                self.selection_ids.append(selection_id)

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.site.bet_receipt.footer.click_done()

    def test_001_verify_user_should_able_to_see_the_details_of_an_edited_acca_in_account_history(self):
        """
        DESCRIPTION: Verify user should able to see the details of an edited acca in account history
        EXPECTED: Verify is able to see the details of an edited acca in account history
        """
        self.navigate_to_page('bet-history')
        self.site.wait_content_state('bet-history')
        self.site.wait_content_state_changed()

    def test_002_check_if_the_selection_name_is_displayed_for_all_remaining_selections_and_returns(self):
        """
        DESCRIPTION: Check if the selection name is displayed for all remaining selections and returns
        EXPECTED: Selection name is displayed for all remaining selections and returns
        """
        if self.device_type == 'mobile':
            self.site.open_my_bets_open_bets()
        else:
            self.navigate_to_page('open-bets')
        self.site.close_all_dialogs()
        self.site.wait_content_state('open-bets')

        for i in range(0, 2):
            bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(bets, msg='"Bet types are not displayed"')
            bet_before_EMA = list(bets.values())[0]
            self.assertTrue(bet_before_EMA.edit_my_acca_button.is_displayed(),
                            msg=f'"{vec.ema.EDIT_MY_BET}" Button is not displayed')
            cashout_button = bet_before_EMA.buttons_panel.full_cashout_button.label
            bet_type_before_EMA = bet_before_EMA.bet_type
            edit_my_bet_text = bet_before_EMA.edit_my_acca_button.name
            self.assertEqual(edit_my_bet_text, vec.ema.EDIT_MY_BET,
                             msg=f'Actual :"{edit_my_bet_text}" is not same as'
                                 f'Expected :"{vec.ema.EDIT_MY_BET}"')
            self.assertEqual(cashout_button, vec.bet_history.CASH_OUT_TAB_NAME,
                             msg=f'Actual text: "{cashout_button}" is not same as'
                                 f'Expected text: "{vec.bet_history.CASH_OUT_TAB_NAME}"')
            bet_before_EMA.edit_my_acca_button.click()
            sleep(1)
            cancel_button_text = bet_before_EMA.edit_my_acca_button.name
            self.assertEqual(cancel_button_text, vec.ema.CANCEL,
                             msg=f'Actual text:"{edit_my_bet_text}" is not changed to'
                                 f'Expected text:"{vec.ema.CANCEL}"')
            confirm_button = bet_before_EMA.confirm_button.name
            self.assertEqual(confirm_button, vec.ema.CONFIRM_EDIT.upper(),
                             msg=f'Actual text:"{cashout_button}" is not changed to '
                                 f'Expected text:"{vec.ema.CONFIRM_EDIT.upper()}".')

            selection = list(bet_before_EMA.items_as_ordered_dict.values())[0]
            event_name = selection.event_name
            selection.edit_my_acca_remove_icon.click()
            self.assertTrue(wait_for_result(lambda: selection.edit_my_acca_undo_icon.is_displayed(), timeout=3),
                            msg=f'"{vec.ema.UNDO_LEG_REMOVE}" Button" not displayed')

            bet_before_EMA.confirm_button.click()
            self.site.wait_content_state_changed()
            new_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(new_bets, msg='"New bet" types are not displayed')
            bet_after_EMA = list(new_bets.values())[0]
            bet_type_after_EMA = bet_after_EMA.bet_type
            self.assertNotEqual(bet_type_after_EMA, bet_type_before_EMA,
                                msg='"New bet type" is  not changed')
            new_selection = list(bet_after_EMA.items_as_ordered_dict.values())[- (i + 1)]
            self.assertTrue(new_selection.leg_remove_marker.is_displayed(),
                            msg=f'"{vec.ema.LEG_REMOVED}" text is not displayed')
            actual_event_name = new_selection.event_name
            self.assertEqual(actual_event_name, event_name,
                             msg='"Removed selection" went to last')

    def test_003___verify_user_sees_selections_which_were_removed_have_a_removed_token_displayed_on_open_bets(self):
        """
        DESCRIPTION: - Verify user sees selection(s) which were removed have a Removed token displayed on open bets
        EXPECTED: user sees selection(s) which were removed have a Removed token displayed on open bets
        """
        # covered in step 2

    def test_004___verify_my_bets_show_edit_history_functionality(self):
        """
        DESCRIPTION: - Verify my bets 'SHOW EDIT HISTORY' functionality
        EXPECTED: 'SHOW EDIT HISTORY' functionality displayed
        """
        if self.device_type == 'mobile':
            self.site.open_my_bets_open_bets()
        else:
            self.navigate_to_page('open-bets')
        self.device.refresh_page()
        self.site.wait_content_state('open-bets')
        self.__class__.bets_after_EMB = list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(self.bets_after_EMB.show_edit_history_button.is_displayed(),
                        msg=f'"{vec.ema.HISTORY.show_history}" is not displayed')

    def test_005___verify_show_edit_history_under_my_bets__verify_show_edit_history_shows_edited_history_on_my_bets_on_same_page__verify_user_can_foldunfold_show_edit_history_page_each_acca_bets__verify_user_sees_show_edit_history_under_my_bets_settle_bets_verify_settle_bets_show_edit_history__button_click_opens_show_edit_history__page__verfiy_show_edit_history_summary_details_and_it_should_havetitle__oddsmarketevent__date__time_stamp(self):
        """
        DESCRIPTION: - Verify 'SHOW EDIT HISTORY' under my bets
        DESCRIPTION: - Verify 'SHOW EDIT HISTORY' shows edited history on my bets on same page.
        DESCRIPTION: - Verify user can fold/unfold 'SHOW EDIT HISTORY' page each ACCA bets
        DESCRIPTION: - Verify user sees 'SHOW EDIT HISTORY' under my bets settle bets
        DESCRIPTION: -Verify settle bets 'SHOW EDIT HISTORY'  button click opens 'SHOW EDIT HISTORY'  page
        DESCRIPTION: - Verfiy 'SHOW EDIT HISTORY summary details and it should have
        DESCRIPTION: Title & odds
        DESCRIPTION: Market
        DESCRIPTION: Event , date & time stamp
        EXPECTED: User displayed with
        EXPECTED: 'SHOW EDIT HISTORY' under my bets
        EXPECTED: SHOW EDIT HISTORY' shows edited history on my bets on same page.
        EXPECTED: User can fold/unfold 'SHOW EDIT HISTORY' page each ACCA bets
        EXPECTED: User sees 'SHOW EDIT HISTORY' under my bets settle bets (
        EXPECTED: 'SHOW EDIT HISTORY'  button click opens 'SHOW EDIT HISTORY'  page
        EXPECTED: 'SHOW EDIT HISTORY summary details displays
        EXPECTED: Title & odds
        EXPECTED: Market
        EXPECTED: Event , date & time stamp
        """
        self.bets_after_EMB.show_edit_history_button.click()
        if self.device_type == "mobile":
            self.__class__.handler = self.site.open_bets.edit_acca_history
        else:
            self.__class__.handler = self.site.dialog_manager.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_EDIT_ACCA_HISTORY)
        self.assertIsNotNone(self.handler, msg='Edit Acca History pop-up is not present')
        bets = list(self.handler.content.items_as_ordered_dict.values())
        self.assertTrue(bets, msg='Bets are not displayed')
        for bet in bets:
            bet.click()
            bet_type = bet.content.bet_type
            self.assertTrue(bet_type, msg='bet type is displayed')
            selections = list(bet.content.items_as_ordered_dict.values())
            for selection in selections:
                self.assertTrue(selection.event_name, msg='"Event name " is not displayed')
                self.assertTrue(selection.market_name, msg='"Market name " is not displayed')
                self.assertTrue(selection.outcome_name, msg='"Outcome name " is not displayed')
                self.assertTrue(selection.odds_value, msg='"Price " is not displayed')
                self.assertTrue(selection.event_time, msg='"Time " is not displayed')
            stake = bet.content.stake.value
            returns = bet.content.est_returns.value
            bet_receipt = bet.content.bet_receipt_info.bet_receipt.text
            bet_id = bet.content.bet_receipt_info.bet_id
            bet_date = bet.content.bet_receipt_info.date.text
            co_su = bet.content.cash_out_history.stake_used.value
            co = bet.content.cash_out_history.cash_out.value
            co_msg = bet.content.cash_out_history.cash_out_used_message
            self.assertTrue(stake, msg='"stake " is not displayed')
            self.assertTrue(returns, msg='"returns " is not displayed')
            self.assertTrue(bet_receipt, msg='"bet receipt " is not displayed')
            self.assertTrue(bet_id, msg='"bet id " is not displayed')
            self.assertTrue(bet_date, msg='"bet date " is not displayed')
            self.assertTrue(co_su, msg='"stake used " is not displayed')
            self.assertTrue(co, msg='"cashed out " is not displayed')
            self.assertTrue(co_msg, msg='"cashed out message " is not displayed')
            bet.click()

    def test_006___verify_edit_history_details_for_singlemultiple_edit(self):
        """
        DESCRIPTION: - Verify Edit History details for Single/Multiple edit
        EXPECTED: Edit History details for Single/Multiple edit displays
        EXPECTED: For Each bet:
        EXPECTED: Header
        EXPECTED: the total stake which was used at the time of bet placement
        EXPECTED: Receipt ID is displayed
        EXPECTED: Date and Time of bet placement is displayed
        EXPECTED: Cashout History : Stake Used and Cashed out value
        EXPECTED: For each selection:
        EXPECTED: the selection name
        EXPECTED: the market names
        EXPECTED: the event name is displayed
        EXPECTED: Event Date and Time is displayed
        EXPECTED: Selection Price is displayed when bet was placed
        EXPECTED: the returns status
        """
        # covered in steps 5

    def test_007___verify_edit_history_details_with_won_lost_indicator_settled_bets_and_summary_details_same_as_above_(self):
        """
        DESCRIPTION: - Verify EDIT HISTORY DETAILS with won/ lost indicator (Settled bets) and summary details same as above ."
        EXPECTED: EDIT HISTORY DETAILS displayed with won/ lost indicator (Settled bets) and summary details same as above ."
        """
        if self.device_type == 'mobile':
            self.handler.close_button.click()
        else:
            self.handler.close_dialog()
        self.navigate_to_page('bet-history')
        self.site.wait_content_state('bet-history')

        self.site.close_all_dialogs()
        settled_bets = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        current_tab_name = self.site.bet_history.tab_content.grouping_buttons.current
        if(len(settled_bets)) == 0:
            self._logger.info(f'There are no bets displayed on "{current_tab_name}" of "{vec.bet_history.SETTLED_BETS_TAB_NAME}"')
        else:
            bet_headers = self.site.bet_history.bet_types
            count = 0
            se_bet_name = None
            se_bet = None
            for bet_type in bet_headers:
                if any(subheader in bet_type for subheader in vec.betslip.BETSLIP_BETTYPES):
                    se_bet_name, se_bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=bet_type)
                    count += 1
                self.assertTrue(se_bet_name, msg=f'Bet name is not displayed "{se_bet_name}"')
                self.assertEqual(se_bet.bet_type, bet_type,
                                 msg=f'Bet type: "{se_bet.bet_type}" '
                                     f'is not as expected: "{bet_type}"')
                self.assertTrue(se_bet.date, msg=f'Bet date is not shown for bet type "{bet_type}"')
                odds_sign = se_bet.odds_sign.strip('"')
                bet_odds = f'{odds_sign}{se_bet.odds_value}'
                self.assertTrue(bet_odds, msg=f'odds are not present for bet type "{bet_type}" ')
                self.assertTrue(se_bet.stake.value, msg=f'stake is not present for bet type "{bet_type}"')
                self.assertTrue(se_bet.bet_receipt_info.bet_id, msg=f'bet id is not present for bet type "{bet_type}"')
                status = se_bet.bet_status
                self.assertTrue(status in vec.betslip.BETSLIP_BETSTATUS, msg=f'bets not available for bet type "{bet_type}"')
                if count >= 2:
                    break
