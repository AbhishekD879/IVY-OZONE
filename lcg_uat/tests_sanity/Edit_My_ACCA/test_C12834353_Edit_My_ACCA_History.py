import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # As bets needs to be settled, cannot script it on prod.
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sanity
@pytest.mark.slow
@pytest.mark.bet_history_open_bets
@vtest
class Test_C12834353_Edit_My_ACCA_History(BaseBetSlipTest):
    """
    TR_ID: C12834353
    NAME: Edit My ACCA History
    DESCRIPTION: This test case verifies that 'Edit my ACCA' history is shown for edited bet
    DESCRIPTION: AUTOTEST [C13035462]
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 1. Login
    PRECONDITIONS: 2. Place Single line Multiple Bet (e.g. ACCA7)
    PRECONDITIONS: 3. Go to By Bets> Open Bets tap 'EDIT MY ACCA' for placed bet
    PRECONDITIONS: 4. Remove few selections from the bet and save changes
    PRECONDITIONS: 5. Tap 'EDIT MY ACCA' for placed bet
    PRECONDITIONS: 6. Remove few selections from the bet and save changes
    PRECONDITIONS: Note: all data in Step1 and Step2 is based on received data from BPP in Network -> accountHistory?detailLevel=DETAILED&fromDate=<DateFrom>%2000%3A00%3A00&toDate=<DateTo> Request
    """
    keep_browser_open = True
    selection_ids = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Enable My ACCA feature toggle in CMS
        PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
        PRECONDITIONS: 1. Login
        PRECONDITIONS: 2. Place Single line Multiple Bet (e.g. ACCA7)
        PRECONDITIONS: 3. Go to By Bets> Open Bets tap 'EDIT MY ACCA' for placed bet
        PRECONDITIONS: 4. Remove few selections from the bet and save changes
        PRECONDITIONS: 5. Tap 'EDIT MY ACCA' for placed bet
        PRECONDITIONS: 6. Remove few selections from the bet and save changes
        """
        if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)

        event = self.ob_config.add_autotest_premier_league_football_event()
        event2 = self.ob_config.add_autotest_premier_league_football_event()
        event3 = self.ob_config.add_autotest_premier_league_football_event()
        event4 = self.ob_config.add_autotest_premier_league_football_event()
        event5 = self.ob_config.add_autotest_premier_league_football_event()
        self.selection_ids = [event.selection_ids[event.team1],
                              event2.selection_ids[event2.team1],
                              event3.selection_ids[event3.team1],
                              event4.selection_ids[event4.team1],
                              event5.selection_ids[event5.team1]]

        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        self.__class__.event_id = event.event_id
        self.__class__.event_name = '%s v %s' % (event.team1, event.team2)
        self.__class__.market_id = self.ob_config.market_ids[event.event_id][market_short_name]
        self.__class__.selection_id = event.selection_ids[event.team1]

        self.__class__.event2_id = event2.event_id
        self.__class__.market2_id = self.ob_config.market_ids[event2.event_id][market_short_name]
        self.__class__.selection2_id = event2.selection_ids[event2.team1]

        self.__class__.event3_id = event3.event_id
        self.__class__.market3_id = self.ob_config.market_ids[event3.event_id][market_short_name]
        self.__class__.selection3_id = event3.selection_ids[event3.team1]

        self.__class__.event4_id = event4.event_id
        self.__class__.market4_id = self.ob_config.market_ids[event4.event_id][market_short_name]
        self.__class__.selection4_id = event4.selection_ids[event4.team1]

        self.__class__.event5_id = event5.event_id
        self.__class__.market5_id = self.ob_config.market_ids[event5.event_id][market_short_name]
        self.__class__.selection5_id = event5.selection_ids[event5.team1]

        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.__class__.bet_date = self.site.bet_receipt.receipt_header.bet_datetime
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        for i in range(0, 2):
            bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(bets, msg='"Bet types are not displayed"')
            bet_before_EMA = list(bets.values())[0]
            self.assertTrue(bet_before_EMA.edit_my_acca_button.is_displayed(),
                            msg=f'"{vec.ema.EDIT_MY_BET}" Button is not displayed')
            bet_type_before_EMA = bet_before_EMA.bet_type
            bet_before_EMA.edit_my_acca_button.click()
            sleep(1)
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

    def test_001_navigate_to_my_betsopen_bets_tab(self):
        """
        DESCRIPTION: Navigate to My Bets>Open Bets tab
        EXPECTED:
        """
        if self.device_type == 'mobile':
            self.site.open_my_bets_open_bets()
        else:
            self.navigate_to_page('open-bets')
        self.device.refresh_page()
        self.site.wait_content_state('open-bets')

    def test_002_tap_show_edit_history_buttonverify_that_edit_history_listing_overlay_for_the_edited_acca_is_shown_with_all_appropriate_elements(
            self, open_bets=True):
        """
        DESCRIPTION: Tap 'SHOW EDIT HISTORY' button
        DESCRIPTION: Verify that Edit History Listing Overlay for the edited ACCA is shown with all appropriate elements
        EXPECTED: Edit History Listing Overlay is shown with appropriate elements:
        EXPECTED: * "Edit Acca History" title
        EXPECTED: * 'Close' ('X') button
        EXPECTED: * Bet type for all bets
        EXPECTED: * Original Bet box
        EXPECTED: * All Edited Bet boxes
        EXPECTED: * All edited accas are displayed collapsed by default
        EXPECTED: * Date and Time when the bet was placed is displayed
        EXPECTED: NOTE: Edited ACCA should be shown as per Time Order as they were Edited
        """
        if open_bets:
            self.__class__.bets_after_EMB = \
                list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        else:
            self.__class__.bets_after_EMB = \
                list(self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(self.bets_after_EMB.show_edit_history_button.is_displayed(),
                        msg=f'"{vec.ema.HISTORY.show_history}" is not displayed')

        self.bets_after_EMB.show_edit_history_button.click()
        if self.device_type == "mobile":
            self.__class__.handler = self.site.open_bets.edit_acca_history if open_bets else self.site.bet_history.edit_acca_history
        else:
            self.__class__.handler = self.site.dialog_manager.wait_for_dialog(
                vec.dialogs.DIALOG_MANAGER_EDIT_ACCA_HISTORY)
        self.assertIsNotNone(self.handler, msg=f'"{vec.ema.HISTORY.acca_history}" pop-up is not present')
        bet = self.handler.content.headers.get(vec.bet_history._bet_types_ACC4.upper())
        self.assertTrue(bet.is_displayed(), msg=f'{bet} is not displayed')

        if self.device_type == "mobile":
            self.assertEqual(vec.ema.HISTORY.acca_history, self.handler.header_text,
                             msg=f'Actual title "{vec.ema.HISTORY.acca_history}" does not equal '
                                 f'to "{self.handler.header_text}"')
            self.assertTrue(self.handler.close_button.is_displayed(),
                            msg='"Close" ("X") button is not displayed')
        else:
            self.assertTrue(self.handler.header_object.close_button.is_displayed(),
                            msg='"Close" ("X") button is not displayed')

    def test_003_tap_on_original_betverify_that_detailed_information_for_original_acca_is_shown(self):
        """
        DESCRIPTION: Tap on 'Original Bet'
        DESCRIPTION: Verify that detailed information for original ACCA is shown
        EXPECTED: The Original ACCA is shown with appropriate elements:
        EXPECTED: * Bet Type
        EXPECTED: * Date and Time of bet placement is displayed
        EXPECTED: * Selections name
        EXPECTED: * Markets name
        EXPECTED: * Events name
        EXPECTED: * Events Date and Time
        EXPECTED: * Scores result (if available)
        EXPECTED: * Selections Price
        EXPECTED: * Returns status
        EXPECTED: * Total stake which was used at the time of bet placement
        EXPECTED: * Receipt ID is displayed
        EXPECTED: Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: Message <Cashout Value> was used to Edit your bet should be displayed.
        """
        bets = list(self.handler.content.items_as_ordered_dict.values())
        self.assertTrue(bets, msg='Bets are not displayed')
        for self.__class__.bet in bets:
            self.bet.click()
            bet_type = self.bet.content.bet_type
            self.assertTrue(bet_type, msg='bet type is displayed')
            self.__class__.selections = list(self.bet.content.items_as_ordered_dict.values())
            for selection in self.selections:
                self.assertTrue(selection.event_name, msg='"Event name " is not displayed')
                self.assertTrue(selection.market_name, msg='"Market name " is not displayed')
                self.assertTrue(selection.outcome_name, msg='"Outcome name " is not displayed')
                self.assertTrue(selection.odds_value, msg='"Price " is not displayed')
                self.assertTrue(selection.event_time, msg='"Time " is not displayed')
            stake = self.bet.content.stake.value
            returns = self.bet.content.est_returns.value
            bet_receipt = self.bet.content.bet_receipt_info.bet_receipt.text
            bet_id = self.bet.content.bet_receipt_info.bet_id
            bet_date = self.bet.content.bet_receipt_info.date.text
            co_su = self.bet.content.cash_out_history.stake_used.value
            co = self.bet.content.cash_out_history.cash_out.value
            co_msg = self.bet.content.cash_out_history.cash_out_used_message
            self.assertTrue(stake, msg='"stake " is not displayed')
            self.assertTrue(returns, msg='"returns " is not displayed')
            self.assertTrue(bet_receipt, msg='"bet receipt " is not displayed')
            self.assertTrue(bet_id, msg='"bet id " is not displayed')
            self.assertTrue(bet_date, msg='"bet date " is not displayed')
            self.assertTrue(co_su, msg='"stake used " is not displayed')
            self.assertTrue(co, msg='"cashed out " is not displayed')
            self.assertTrue(co_msg, msg='"cashed out message " is not displayed')
            self.bet.click()
        self.bet.click()

    def test_004_tap_on_edited_betverify_that_detailed_information_for_edited_acca_is_shown(self):
        """
        DESCRIPTION: Tap on 'Edited Bet'
        DESCRIPTION: Verify that detailed information for edited ACCA is shown
        EXPECTED: The Edited ACCA is shown with appropriate elements:
        EXPECTED: * Bet Type
        EXPECTED: * Date and Time of bet placement is displayed
        EXPECTED: * Selections name
        EXPECTED: * Markets name
        EXPECTED: * Events name
        EXPECTED: * Events Date and Time
        EXPECTED: * Scores result (if available)
        EXPECTED: * Selections Price
        EXPECTED: * Returns status
        EXPECTED: * Total stake which was used at the time of bet placement
        EXPECTED: * Receipt ID is displayed
        EXPECTED: * Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: * Message <Cashout Value> was used to Edit your bet should be displayed.
        """
        # Covered in step 3

    def test_005_tap_close_x_buttonverify_that_edit_history_listing_overlay_is_closed(self):
        """
        DESCRIPTION: Tap 'Close' ('X') button
        DESCRIPTION: Verify that Edit History Listing Overlay is closed
        EXPECTED: * Edit History Listing Overlay is closed
        """
        if self.device_type == 'mobile':
            self.handler.close_button.click()
        else:
            self.handler.header_object.close_button.click()

    def test_006_make_a_placed_bet_edited_bet_settled_add_and_settle_the_result_for_each_event_in_the_edited_betverify_that_the_new_bet_is_resulted_and_shown_on_by_betsbet_historysettled_bets(
            self):
        """
        DESCRIPTION: Make a placed bet (edited bet) SETTLED (add and settle the result for each event in the edited bet)
        DESCRIPTION: Verify that the new bet is resulted and shown on By Bets>(Bet History)Settled Bets
        EXPECTED: * Edited Bet is resulted
        EXPECTED: * Edited Bet is shown on By Bets>(Bet History)Settled Bets
        """
        self.ob_config.update_selection_result(event_id=self.event2_id, market_id=self.market2_id,
                                               selection_id=self.selection_id, result='L')
        self.ob_config.update_selection_result(event_id=self.event3_id, market_id=self.market3_id,
                                               selection_id=self.selection3_id, result='v')
        self.ob_config.update_selection_result(event_id=self.event4_id, market_id=self.market4_id,
                                               selection_id=self.selection4_id, result='W')
        self.ob_config.update_selection_result(event_id=self.event5_id, market_id=self.market5_id,
                                               selection_id=self.selection5_id, result='L')
        self.device.refresh_page()
        if self.device_type == 'mobile':
            self.navigate_to_page(name='bet-history')
            self.site.wait_content_state(state_name='BetHistory')
        else:
            self.site.open_my_bets_settled_bets()
        self.__class__.bet = list(self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict.values())[1]
        self.site.wait_splash_to_hide(5)
        selection = list(self.bet.items_as_ordered_dict.values())[1]
        self.assertFalse(selection.has_edit_my_acca_remove_icon(),
                         msg='"Selection removal icon(X)" is displayed')

    def test_007_go_to_by_betsbet_historysettled_betran_2_6_steps(self):
        """
        DESCRIPTION: Go to By Bets>(Bet History)Settled Bet
        DESCRIPTION: Ran 2-6 steps
        EXPECTED: Results are the same
        """
        self.test_002_tap_show_edit_history_buttonverify_that_edit_history_listing_overlay_for_the_edited_acca_is_shown_with_all_appropriate_elements(
            open_bets=False)
        self.test_003_tap_on_original_betverify_that_detailed_information_for_original_acca_is_shown()
        self.test_005_tap_close_x_buttonverify_that_edit_history_listing_overlay_is_closed()
        self.test_006_make_a_placed_bet_edited_bet_settled_add_and_settle_the_result_for_each_event_in_the_edited_betverify_that_the_new_bet_is_resulted_and_shown_on_by_betsbet_historysettled_bets()
