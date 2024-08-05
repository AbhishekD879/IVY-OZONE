import datetime
import pytest

import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.acca
@pytest.mark.slow
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C9618068_Verify_displaying_Edit_History_Listing_Page(BaseCashOutTest):
    """
    TR_ID: C9618068
    NAME: Verify displaying Edit History Listing Page
    DESCRIPTION: This test case verifies the view of Edit History Listing page of Settled Bet
    PRECONDITIONS: 1. Login with User1
    PRECONDITIONS: 2. Place Single line Multiple Bet (e.g. ACCA5)
    PRECONDITIONS: 3. Go to By Bets> Open Bets tap 'EDIT MY ACCA' for placed bet
    PRECONDITIONS: 4. Remove few selections from the bet and save changes
    PRECONDITIONS: 5. Tap 'SHOW EDIT HISTORY' button
    PRECONDITIONS: Note: all data in Step1 and Step2 is based on received data from BPP in Network -> accountHistory?detailLevel=DETAILED&fromDate=<DateFrom>%2000%3A00%3A00&toDate=<DateTo> Request
    """
    keep_browser_open = True
    ema_history = None
    acca_betslip_section = '5 Fold Acca'
    acca_5 = 'ACCA (5)'
    acca_4 = 'ACCA (4)'
    original_bet = 'Original Bet'
    edited_bet = 'Edited Bet'
    match_result = 'won'
    events_finished = False

    def get_bet_with_my_acca_edit_open_bet(self, bet_type: str, event_name: str):
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(bet_type=bet_type,
                                                                         event_names=event_name)
        self.assertTrue(bet, msg=f'Cannot find bet for "{event_name}"')
        return bet

    def get_my_acca_bet_from_settled_bets(self, bet_type: str, event_name: str):
        _, bet = self.site.bet_history.tab_content.accordions_list.get_bet(bet_type=bet_type,
                                                                           event_names=event_name)
        self.assertTrue(bet, msg=f'Cannot find bet for "{event_name}"')
        return bet

    def get_edit_acca_history_handler(self, open_bets=True):
        if self.device_type == "mobile":
            handler = self.site.open_bets.edit_acca_history if open_bets else self.site.bet_history.edit_acca_history
        else:
            handler = self.site.dialog_manager.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_EDIT_ACCA_HISTORY)

        self.assertIsNotNone(handler, msg='Edit Acca History pop-up is not present')
        return handler

    def get_api_event_name(self, api_event):
        start_time_local = self.convert_time_to_local(date_time_str=api_event.start_time,
                                                      ob_format_pattern='%Y-%m-%d %H:%M:%S',
                                                      future_datetime_format=self.event_card_future_time_format_pattern,
                                                      ui_format_pattern='%H:%M, Today')
        return f'{api_event.team1} - {api_event.event_name} FT' \
            if self.events_finished and api_event in self.remaining_events \
            else f'{api_event.team1} - {api_event.event_name} {start_time_local}'

    def assert_header_time_date(self, change_date, bet):
        expected_date_time = datetime.datetime.strptime(change_date, '%d/%m/%Y, %H:%M')
        expected_date_time = expected_date_time.replace(year=1900)
        actual_date_time = datetime.datetime.strptime(bet.date, '%H:%M - %d %b')
        if tests.location in ['AWS_GRID', 'AWS']:
            # This hack is needed for CI in order to handle time difference between UI and actual API London time
            # actual_date_time += datetime.timedelta(hours=1)
            # On 28.05.2020 this code caused test failure:
            #       "expected to be "1900-05-28 06:57:00", but actual it is "1900-05-28 07:57:00"
            # This might be related with daylight saving time. Leave this comment to check in future

            pass
        self.assertAlmostEqual(expected_date_time, actual_date_time, delta=datetime.timedelta(minutes=1),
                               msg=f'Date and Time of bet placement was expected to be "{expected_date_time}", '
                               f'but actual it is "{actual_date_time}"')

    def verify_bet_leg_info(self, api_event, ui_event):
        ui_event_outcome_name = ui_event.outcome_name
        self.assertEqual(api_event.team1, ui_event_outcome_name,
                         msg=f'Actual event selection name "{api_event.team1}" does not equal '
                         f'to expected "{ui_event_outcome_name}"')

        ui_event_market_name = ui_event.market_name
        expected_market = 'Match Betting' if self.brand == 'ladbrokes' else 'Match Result'
        self.assertEqual(expected_market, ui_event_market_name,
                         msg=f'Market name is not displayed, but displayed "{expected_market}"')

        ui_event_event_name = ui_event.event_name
        self.assertEqual(api_event.event_name, ui_event_event_name,
                         msg=f'Actual event name "{api_event.event_name}" does not equal '
                         f'to expected "{ui_event_event_name}"')

        api_event_time = self.convert_time_to_local(date_time_str=api_event.start_time,
                                                    ob_format_pattern='%Y-%m-%d %H:%M:%S',
                                                    ui_format_pattern='%H:%M, Today')
        expected_time = "FT" if self.events_finished and api_event in self.remaining_events else api_event_time
        ui_event_event_time = ui_event.event_time
        self.assertEqual(expected_time, ui_event_event_time,
                         msg=f'Actual event date and time "{expected_time}" does not equal '
                         f'to expected "{ui_event_event_time}"')

    def assert_event_price(self, api_price, ui_event):
        ui_event_odds_value = ui_event.odds_value
        self.assertEqual(api_price, ui_event_odds_value,
                         msg=f'Actual event selection price "{api_price}" does not equal '
                         f'to expected "{ui_event_odds_value}"')

    def verify_original_bet(self):
        self.assertTrue(self.ema_history.content.headers, msg=f'Histories not found')
        original_bet = self.ema_history.content.headers.get(self.acca_5)
        self.assertTrue(original_bet, msg=f'Original Bet history was not found')
        original_bet.click()

        original_bet_type = original_bet.type
        self.assertEqual(original_bet_type, self.original_bet,
                         msg=f'Original bet type was expected to be {self.original_bet} but it is {original_bet_type}')

        self.assert_header_time_date(self.bet_date, original_bet)

        ui_events = original_bet.content.items_as_ordered_dict
        self.assertTrue(ui_events, msg=f'UI events for {self.original_bet} are not found')
        self.assertEqual(len(self.event_params), len(ui_events),
                         msg=f'Events count is not equal, '
                         f'expected to have {len(self.event_params)} but it has {len(ui_events)}')

        for api_event in self.event_params:
            api_event_name = self.get_api_event_name(api_event)
            ui_event = ui_events.get(api_event_name)
            self.assertTrue(ui_event,
                            msg=f'Event "{api_event_name}" is not found between events "{list(ui_events.keys())}"')

            self.verify_bet_leg_info(api_event, ui_event)
            if self.events_finished and api_event in self.remaining_events:
                ui_event_icon_status = ui_event.icon.status
                self.assertEqual(self.match_result, ui_event_icon_status,
                                 msg=f'Match result for event "{api_event_name}" was expected to be as'
                                 f' "{self.match_result}" but it is "{ui_event_icon_status}"')
            price = self.ob_config.event.prices['odds_home']
            self.assert_event_price(price, ui_event)

        est_returns_value = original_bet.content.est_returns.value
        self.assertEqual(self.first_new_stake, est_returns_value,
                         msg=f'Returns amount was expected to be "{self.first_new_stake}" but it is '
                         f'"{est_returns_value}"')
        stake_value = original_bet.content.stake.stake_value
        self.assertEqual(self.bet_amount, float(stake_value),
                         msg=f'Actual stake "{float(self.bet_amount)}" does not equal to '
                         f'expected stake "{float(stake_value)}"')
        actual_bet_receipt = original_bet.content.bet_receipt_info.bet_receipt.value
        self.assertEqual(self.bet_receipt_id, actual_bet_receipt,
                         msg=f'Bet Receipt ID was expected to be "{self.bet_receipt_id} but it '
                         f'is "{self.bet_receipt_id}"')
        ui_message = original_bet.content.cash_out_history.stake_used.message
        self.assertEqual(vec.ema.CASHOUT_HISTORY.stake_used, ui_message,
                         msg=f'Expected message "{vec.ema.CASHOUT_HISTORY.stake_used}" does not equal '
                         f'to actual "{ui_message}"')
        stake_used = original_bet.content.cash_out_history.stake_used.value
        self.assertEqual(float(self.bet_amount), float(stake_used),
                         msg=f'Stake used value was expected to be "{float(self.bet_amount)}" but '
                         f'it is "{float(stake_used)}"')

        cash_out_message = original_bet.content.cash_out_history.cash_out.message
        self.assertEqual(vec.ema.CASHOUT_HISTORY.cashed_out, cash_out_message,
                         msg=f'Expected message "{vec.ema.CASHOUT_HISTORY.cashed_out}" does not equal '
                         f'to actual "{cash_out_message}"')
        stake = original_bet.content.cash_out_history.cash_out.currency + \
            original_bet.content.cash_out_history.cash_out.value
        self.assertEqual(self.first_new_stake, stake,
                         msg=f'Stake used value was expected to be "{self.first_new_stake}" but '
                         f'it is "{stake}"')

        expected_msg = vec.ema.CASHOUT_HISTORY.cashout_used.format(
            float(original_bet.content.cash_out_history.cash_out.value))
        cash_out_used_message = original_bet.content.cash_out_history.cash_out_used_message
        self.assertEqual(expected_msg, cash_out_used_message,
                         msg=f'Actual message "{expected_msg}" does not equal to actual '
                         f'"{cash_out_used_message}"')

    def verify_edited_bet(self):
        self.assertTrue(self.ema_history.content.headers, msg=f'Histories not found')
        edited_bet = self.ema_history.content.headers.get(self.acca_4)
        self.assertTrue(edited_bet, msg='Edited Bet history was not found')
        edited_bet.click()

        edited_bet_type = edited_bet.type
        self.assertEqual(edited_bet_type, self.edited_bet,
                         msg=f'Original bet type was expected to be {self.edited_bet} but it is {edited_bet_type}')

        self.assertIsNotNone(edited_bet.date, msg='Edited bet time is not displayed')

        ui_events = edited_bet.content.items_as_ordered_dict
        self.assertTrue(ui_events, msg=f'UI events for {self.edited_bet} are not found')
        self.assertEqual(len(self.event_params) - 1, len(ui_events),
                         msg=f'Events count is not equal, '
                         f'expected to have {len(self.event_params) - 1} but it has {len(ui_events)}')

        for api_event in self.event_params:
            if api_event.event_name == self.event_delete_first.event_name:
                continue
            api_event_name = self.get_api_event_name(api_event)
            ui_event = ui_events.get(api_event_name)
            self.assertTrue(ui_event,
                            msg=f'Event "{api_event_name}" is not found between events "{list(ui_events.keys())}"')

            self.verify_bet_leg_info(api_event, ui_event)
            if self.events_finished and api_event in self.remaining_events:
                ui_event_icon_status = ui_event.icon.status
                self.assertEqual(self.match_result, ui_event_icon_status,
                                 msg=f'Match result for event "{api_event_name}" was expected to be as'
                                 f' "{self.match_result}" but it is "{ui_event_icon_status}"')

            price = self.ob_config.event.prices['odds_home']
            self.assert_event_price(price, ui_event)

        est_returns_value = edited_bet.content.est_returns.value
        self.assertEqual(self.second_new_stake, est_returns_value,
                         msg=f'Returns amount was expected to be "{self.second_new_stake}" but it is '
                         f'"{est_returns_value}"')

        stake_value = edited_bet.content.stake.value
        self.assertEqual(self.first_new_stake, stake_value,
                         msg=f'Actual stake "{self.first_new_stake}" does not equal to '
                         f'expected stake "{stake_value}"')

        actual_bet_receipt = edited_bet.content.bet_receipt_info.bet_receipt.value
        self.assertIsNotNone(actual_bet_receipt, msg=f'Bet Receipt ID was not displayed')

        stake_used_message = edited_bet.content.cash_out_history.stake_used.message
        self.assertEqual(vec.ema.CASHOUT_HISTORY.stake_used, stake_used_message,
                         msg=f'Expected message "{vec.ema.CASHOUT_HISTORY.stake_used}" does not equal '
                         f'to actual "{stake_used_message}"')
        stake = edited_bet.content.cash_out_history.stake_used.currency + \
            edited_bet.content.cash_out_history.stake_used.value
        self.assertEqual(self.first_new_stake, stake,
                         msg=f'Stake used value was expected to be "{self.first_new_stake}" but '
                         f'it is "{stake}"')

        cash_out_message = edited_bet.content.cash_out_history.cash_out.message
        self.assertEqual(vec.ema.CASHOUT_HISTORY.cashed_out,
                         cash_out_message,
                         msg=f'Expected message "{vec.ema.CASHOUT_HISTORY.cashed_out}" does not equal '
                         f'to actual "{cash_out_message}"')
        stake = edited_bet.content.cash_out_history.cash_out.currency + edited_bet.content.cash_out_history.cash_out.value
        self.assertEqual(self.second_new_stake, stake,
                         msg=f'Stake used value was expected to be "{self.second_new_stake}" but '
                         f'it is "{stake}"')

        expected_msg = vec.ema.CASHOUT_HISTORY.cashout_used.format(
            float(edited_bet.content.cash_out_history.cash_out.value))
        cash_out_used_message = edited_bet.content.cash_out_history.cash_out_used_message
        self.assertEqual(expected_msg, cash_out_used_message,
                         msg=f'Actual message "{expected_msg}" does not equal to actual '
                         f'"{cash_out_used_message}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Login with User1
        DESCRIPTION: 2. Place Single line Multiple Bet (e.g. ACCA5)
        DESCRIPTION: 3. Go to By Bets> Open Bets tap 'EDIT MY ACCA' for placed bet
        DESCRIPTION: 4. Remove few selections from the bet and save changes
        DESCRIPTION: 5. Tap 'Edit My ACCA' one more time and remove one more selection from the bet and save changes
        DESCRIPTION: 6. Tap 'SHOW EDIT HISTORY' button
        DESCRIPTION: Note: all data in Step1 and Step2 is based on received data from BPP in Network -> accountHistory?detailLevel=DETAILED&fromDate=<DateFrom>%2000%3A00%3A00&toDate=<DateTo> Request
        """
        self.__class__.event_params = self.create_several_autotest_premier_league_football_events(number_of_events=5)

        self.__class__.event_delete_first = self.event_params[0]
        self.__class__.event_delete_second = self.event_params[1]
        self.__class__.remaining_events = self.event_params[2:]
        self.__class__.event_name = self.event_params[2].event_name
        selection_ids = [event.selection_ids for event in self.event_params]

        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=[list(i.values())[0] for i in selection_ids])
        self.place_multiple_bet(stake_name=self.acca_betslip_section)
        self.check_bet_receipt_is_displayed()

        self.__class__.bet_date = self.site.bet_receipt.receipt_header.bet_datetime

        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = betreceipt_sections.get(self.acca_betslip_section)
        self.__class__.bet_receipt_id = section.bet_id

        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_open_bets()

        # Remove first bet
        bet = self.get_bet_with_my_acca_edit_open_bet(self.acca_5, self.event_delete_first.event_name)
        bet.edit_my_acca_button.click()
        self.assertTrue(bet.items_as_ordered_dict, msg='No events found')
        api_event_name = self.get_api_event_name(self.event_delete_first)
        bet.items_as_ordered_dict.get(api_event_name).edit_my_acca_remove_icon.click()
        bet = self.get_bet_with_my_acca_edit_open_bet(self.acca_5, self.event_delete_first.event_name)
        self.__class__.first_new_stake = bet.stake.value
        bet.confirm_button.click()

        if self.device_type == 'mobile':
            self.site.wait_content_state('OpenBets')

        # Remove second bet
        bet = self.get_bet_with_my_acca_edit_open_bet(self.acca_4, self.event_delete_second.event_name)
        bet.edit_my_acca_button.click()

        self.assertTrue(bet.items_as_ordered_dict, msg='No events found')
        api_event_name = self.get_api_event_name(self.event_delete_second)
        bet.items_as_ordered_dict.get(api_event_name).edit_my_acca_remove_icon.click()
        bet = self.get_bet_with_my_acca_edit_open_bet(self.acca_4, self.event_delete_second.event_name)
        self.__class__.second_new_stake = bet.stake.value
        bet.confirm_button.click()

        # Open My Acca Edit History
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        if self.device_type == 'desktop':
            self.site.open_my_bets_open_bets()
        if self.site.cookie_banner:  # lad tst2 env
            self.site.cookie_banner.ok_button.click()
        bet = self.get_bet_with_my_acca_edit_open_bet(vec.betslip.TBL.upper(), self.event_name)
        bet.show_edit_history_button.click()

    def test_001_tap_on_original_betverify_that_detailed_information_for_original_acca_is_shown(self):
        """
        DESCRIPTION: Tap on 'Original Bet'
        DESCRIPTION: Verify that detailed information for original ACCA is shown
        EXPECTED: The Original ACCA is shown with appropriate elements:
        EXPECTED: - Original Bet Type
        EXPECTED: - Date and Time of bet placement is displayed
        EXPECTED: - Selections name
        EXPECTED: - Markets name
        EXPECTED: - Events name
        EXPECTED: - Events Date and Time
        EXPECTED: - Scores result (if available)
        EXPECTED: - Selections Price
        EXPECTED: - Returns status
        EXPECTED: - Total stake which was used at the time of bet placement
        EXPECTED: - Receipt ID is displayed
        EXPECTED: - Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: - Message <Cashout Value> was used to Edit your bet should be displayed.
        """
        self.__class__.ema_history = self.get_edit_acca_history_handler()
        self.verify_original_bet()

    def test_002_tap_on_edited_betverify_that_detailed_information_for_edited_acca_is_shown(self):
        """
        DESCRIPTION: Tap on 'Edited Bet'
        DESCRIPTION: Verify that detailed information for edited ACCA is shown
        EXPECTED: The Edited ACCA is shown with appropriate elements:
        EXPECTED: - Original Bet Type
        EXPECTED: - Date and Time of bet placement is displayed
        EXPECTED: - Selections name
        EXPECTED: - Markets name
        EXPECTED: - Events name
        EXPECTED: - Events Date and Time
        EXPECTED: - Scores result (if available)
        EXPECTED: - Selections Price
        EXPECTED: - Returns status
        EXPECTED: - Total stake which was used at the time of bet placement
        EXPECTED: - Receipt ID is displayed
        EXPECTED: - Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: - Message <Cashout Value> was used to Edit your bet should be displayed.
        """
        self.__class__.ema_history = self.get_edit_acca_history_handler()
        self.verify_edited_bet()

    def test_003_make_a_placed_bet_edited_bet_settled_add_and_settle_the_result_for_each_event_in_the_edited_betverify_that_the_new_bet_is_resulted_and_shown_on_by_betsbet_historysettled_bets(
            self):
        """
        DESCRIPTION: Make a placed bet (edited bet) SETTLED (add and settle the result for each event in the edited bet)
        DESCRIPTION: Verify that the new bet is resulted and shown on By Bets>(Bet History)Settled Bets
        EXPECTED: - Edited Bet is resulted
        EXPECTED: - Edited Bet is shown on By Bets>(Bet History)Settled Bets
        """
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        for event in self.remaining_events:
            market_id = self.ob_config.market_ids[event.event_id][market_short_name]
            self.result_event(selection_ids=list(event.selection_ids.values()),
                              market_id=market_id,
                              event_id=event.event_id)

        self.__class__.events_finished = True

        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state(state_name='BetHistory')

        bet = self.get_my_acca_bet_from_settled_bets(vec.betslip.TBL.upper(), self.event_name)
        self.assertTrue(bet.items_as_ordered_dict, msg='No events found')

        for event in self.remaining_events:
            api_event_name = self.get_api_event_name(event)
            ui_event = bet.items_as_ordered_dict.get(api_event_name)
            self.assertTrue(ui_event, msg=f'Event "{api_event_name}" is not found between '
                                          f'events "{list(bet.items_as_ordered_dict.keys())}"')
            ui_event_icon_status = ui_event.icon.status
            self.assertEqual(self.match_result, ui_event_icon_status,
                             msg=f'Match result for event "{api_event_name}" was expected to be as'
                             f' "{self.match_result}" but it is "{ui_event_icon_status}"')

    def test_004_go_to_by_betsbet_historysettled_bettap_show_edit_history_buttonverify_that_edit_history_listing_overlay_for_the_edited_acca_is_shown_with_all_appropriate_elements(
            self):
        """
        DESCRIPTION: Go to By Bets>(Bet History)Settled Bet
        DESCRIPTION: Tap 'SHOW EDIT HISTORY' button
        DESCRIPTION: Verify that Edit History Listing Overlay for the edited ACCA is shown with all appropriate elements
        EXPECTED: Edit History Listing Overlay is shown with appropriate elements:
        EXPECTED: - "Edit Acca History" title
        EXPECTED: - 'Close' ('X') button
        EXPECTED: - Bet type for all bets
        EXPECTED: - Original Bet box
        EXPECTED: - Edited Bet box
        EXPECTED: - Date and Time when the bet was placed is displayed
        """
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state(state_name='BetHistory')
        bet = self.get_my_acca_bet_from_settled_bets(vec.betslip.TBL.upper(), self.event_name)
        bet.show_edit_history_button.click()

        ema_history = self.get_edit_acca_history_handler(open_bets=False)
        if self.device_type == "mobile":
            self.assertEqual(vec.ema.HISTORY.acca_history, ema_history.header_text,
                             msg=f'Actual title "{vec.ema.HISTORY.acca_history}" does not equal '
                             f'to "{ema_history.header_text}"')
            self.assertTrue(ema_history.close_button.is_displayed(),
                            msg='"Close" ("X") button is not displayed')
        else:
            self.assertTrue(ema_history.header_object.close_button.is_displayed(),
                            msg='"Close" ("X") button is not displayed')

        self.assertTrue(ema_history.content.headers, msg=f'Histories not found')

        original_bet = ema_history.content.headers.get(self.acca_5)
        self.assertTrue(original_bet, msg=f'Original Bet history "{self.acca_5}" was not found')
        self.assert_header_time_date(self.bet_date, original_bet)

        edited_bet = ema_history.content.headers.get(self.acca_4)
        self.assertTrue(edited_bet, msg=f'Edited Bet history "{self.acca_4}" was not found')

    def test_005_tap_on_original_betverify_that_detailed_information_for_original_acca_is_shown(self):
        """
        DESCRIPTION: Tap on 'Original Bet'
        DESCRIPTION: Verify that detailed information for original ACCA is shown
        EXPECTED: The Original ACCA is shown with appropriate elements:
        EXPECTED: - Original Bet Type
        EXPECTED: - Date and Time of bet placement is displayed
        EXPECTED: - Selections name
        EXPECTED: - Markets name
        EXPECTED: - Events name
        EXPECTED: - Events Date and Time
        EXPECTED: - Scores result (if available)
        EXPECTED: - Selections Price
        EXPECTED: - Returns status
        EXPECTED: - Total stake which was used at the time of bet placement
        EXPECTED: - Receipt ID is displayed
        EXPECTED: - Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: - Message <Cashout Value> was used to Edit your bet should be displayed.
        """
        self.__class__.ema_history = self.get_edit_acca_history_handler(open_bets=False)
        self.verify_original_bet()

    def test_006_tap_on_edited_betverify_that_detailed_information_for_edited_acca_is_shown(self):
        """
        DESCRIPTION: Tap on 'Edited Bet'
        DESCRIPTION: Verify that detailed information for edited ACCA is shown
        EXPECTED: The Edited ACCA is shown with appropriate elements:
        EXPECTED: - Original Bet Type
        EXPECTED: - Date and Time of bet placement is displayed
        EXPECTED: - Selections name
        EXPECTED: - Markets name
        EXPECTED: - Events name
        EXPECTED: - Events Date and Time
        EXPECTED: - Scores result (if available)
        EXPECTED: - Selections Price
        EXPECTED: - Returns status
        EXPECTED: - Total stake which was used at the time of bet placement
        EXPECTED: - Receipt ID is displayed
        EXPECTED: - Cashout History is displayed along with Stake Used and Cashed out value
        EXPECTED: - Message <Cashout Value> was used to Edit your bet should be displayed.
        """
        self.__class__.ema_history = self.get_edit_acca_history_handler(open_bets=False)
        self.verify_edited_bet()
