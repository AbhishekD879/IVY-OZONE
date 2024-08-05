import pytest
import tests
from time import sleep
from voltron.utils.helpers import normalize_name
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.high
@vtest
class Test_C3020332_Verify_ability_to_cancel_editing_of_my_ACCA(BaseCashOutTest):
    """
    TR_ID: C3020332
    NAME: Verify ability to cancel editing of my ACCA
    DESCRIPTION: This test case verifies that edit my ACCA can be canceled
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Place a bet on DOUBLE
    PRECONDITIONS: All selections in the placed bet are active
    PRECONDITIONS: All selections in the placed bet are open
    """
    keep_browser_open = True
    number_of_events = 2
    selection_ids = []
    event_names = []
    events_time = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=self.number_of_events)
            for event in events:
                event_name = normalize_name(event['event']['name'])
                self.event_names.append(event_name)
                event_time = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                        date_time_str=event['event']['startTime'],
                                                        future_datetime_format=self.event_card_future_time_format_pattern,
                                                        ss_data=True)
                self.events_time.append(event_time)
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
            self.__class__.double_bet_name = f'{vec.betslip.DBL.upper()} - [{(self.event_names[0]) + " " + (self.events_time[0])}, {(self.event_names[1]) + " " + (self.events_time[1])}]'
        else:
            events = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            self.__class__.double_bet_name = f'{vec.betslip.DBL.upper()} - [{(events[0].event_name) + " " + (events[0].local_start_time)}, {(events[1].event_name) + " " + (events[1].local_start_time)}]'
            self.selection_ids = [event.selection_ids[event.team1] for event in events]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.wait_splash_to_hide(3)
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_my_bets__cashout_tabverify_that_edit_my_bet_coraledit_my_acca_ladbrokes_buttonis_shown_for_double_only(self):
        """
        DESCRIPTION: Navigate to My Bets > Cashout tab
        DESCRIPTION: Verify that 'EDIT MY BET' (Coral)/EDIT MY ACCA' (Ladbrokes) button
        DESCRIPTION: is shown for DOUBLE only
        EXPECTED: 'EDIT MY BET' (Coral)/EDIT MY ACCA' (Ladbrokes) button is shown only for DOUBLE bet
        """
        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            _, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(event_names=self.double_bet_name, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
            self.assertTrue(self.bet.has_edit_my_acca_button(),
                            msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed for double bet')

    def test_002_tap_edit_my_betacca_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_betacca_button(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET/ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY BET/ACCA' button
        EXPECTED: - Edit mode of the ACCA is open
        EXPECTED: - CANCEL EDITING' button is shown instead of 'EDIT MY BET/ACCA' button
        """
        if self.brand == 'bma':
            self.bet.edit_my_acca_button.click()
            sleep(3)
            cancel_button_text = self.bet.edit_my_acca_button.name
            self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                             msg=f'Actual text:"{vec.EMA.EDIT_MY_BET}" is not changed to Expected text:"{vec.EMA.CANCEL}".')

    def test_003_tap_cancel_editing_buttonverify_that_user_returned_back_to_the_not_edit_mode(self):
        """
        DESCRIPTION: Tap 'CANCEL EDITING' button
        DESCRIPTION: Verify that user returned back to the not edit mode
        EXPECTED: - Cashout page is opened
        EXPECTED: - Edit mode of the ACCA is closed
        EXPECTED: - 'EDIT MY BET/ACCA' button is shown
        """
        if self.brand == 'bma':
            self.bet.edit_my_acca_button.click()
            self.site.wait_splash_to_hide(3)
            if self.device_type in ['mobile']:
                self.site.wait_content_state(state_name='Cashout')
            self.assertTrue(self.bet.has_edit_my_acca_button(),
                            msg=f'User is not returned back to the not edit mode and "{vec.EMA.EDIT_MY_BET}" button is not shown')

    def test_004_navigate_to_my_bets__open_bets_tabverify_that_edit_my_betacca_button_is_shown_for_double_only(self):
        """
        DESCRIPTION: Navigate to My Bets > Open Bets tab
        DESCRIPTION: Verify that 'EDIT MY BET/ACCA' button is shown for DOUBLE only
        EXPECTED: 'EDIT MY BET/ACCA' button is shown only for DOUBLE bet
        """
        self.site.open_my_bets_open_bets()
        _, self.__class__.bet = self.site.open_bets.tab_content.accordions_list.get_bet(event_names=self.double_bet_name, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'"{vec.EMA.EDIT_MY_BET}" button is not displayed for double bet')

    def test_005_tap_edit_my_betacca_buttonverify_that_edit_mode_of_the_acca_is_open_and_cancel_editing_button_is_shown_instead_of_edit_my_betacca_button(self):
        """
        DESCRIPTION: Tap ''EDIT MY BET/ACCA' button
        DESCRIPTION: Verify that edit mode of the Acca is open and 'CANCEL EDITING' button is shown instead of 'EDIT MY BET/ACCA' button
        EXPECTED: - Edit mode of the ACCA is open
        EXPECTED: - 'CANCEL EDITING' button is shown instead of 'EDIT MY BET/ACCA' button
        """
        self.bet.edit_my_acca_button.click()
        sleep(3)
        cancel_button_text = self.bet.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                         msg=f'Actual text:"{vec.EMA.EDIT_MY_BET}" is not changed to Expected text:"{vec.EMA.CANCEL}".')

    def test_006_tap_cancel_editing_buttonverify_that_user_returned_back_to_the_not_edit_mode(self):
        """
        DESCRIPTION: Tap 'CANCEL EDITING' button
        DESCRIPTION: Verify that user returned back to the not edit mode
        EXPECTED: - Cashout page is opened
        EXPECTED: - Edit mode of the ACCA is closed
        EXPECTED: - ''EDIT MY BET/ACCA' button is shown
        """
        self.bet.edit_my_acca_button.click()
        self.site.wait_splash_to_hide(3)
        if self.device_type in ['mobile']:
            self.site.wait_content_state(state_name='OpenBets')
        self.assertTrue(self.bet.has_edit_my_acca_button(),
                        msg=f'User is not returned back to the not edit mode and "{vec.EMA.EDIT_MY_BET}" button is not shown')
