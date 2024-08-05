import pytest
import voltron.environments.constants as vec
import tests
from voltron.utils.helpers import normalize_name
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C9346556_Verify_Cancel_Pop_up_in_My_Bet_Acca_edit_mode(BaseCashOutTest, BaseBetSlipTest):
    """
    TR_ID: C9346556
    NAME: Verify 'Cancel' Pop up in 'My Bet/Acca' edit mode
    DESCRIPTION: This test case verifies 'Cancel' message in 'My  Bet/Acca' edit mode
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Tap on 'Edit My Bet/Acca' button -> verify that user is in 'My Bet/Acca Edit' mode
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True
    number_of_events = 2
    selection_ids = []
    event_names = []

    @classmethod
    def custom_setUp(cls):
        acca_section_status = cls.get_initial_data_system_configuration().get('EMA', {})
        if not acca_section_status:
            acca_section_status = cls.get_cms_config().get_system_configuration_item('EMA')
        if not acca_section_status.get('enabled'):
            raise CmsClientException('My ACCA section is disabled in CMS')

    def get_bet_with_my_acca_edit(self):
        """
        Get bet with My ACCA edit functionality
        """
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event_names, number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{self.event_names}"')
        return bet

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Create events
        DESCRIPTION: 2. Login into App
        DESCRIPTION: 3. Place Multiple bet
        DESCRIPTION: 4. Navigate to the Bet History
        DESCRIPTION: 5. Go to 'Cash Out' tab -> verify that 'EDIT MY BET/ACCA' button is available
        """
        if tests.settings.backend_env == 'prod':
            event_params = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                               number_of_events=self.number_of_events)
            for event in event_params:
                event_name = normalize_name(event['event']['name'])
                self.event_names.append(event_name)
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
                if event_params[0] == event:
                    self.__class__.selection_name = list(all_selection_ids.keys())[0]
        else:
            event_params = self.create_several_autotest_premier_league_football_events(number_of_events=2)
            self.selection_ids = [event_params[0].selection_ids, event_params[1].selection_ids]
            self.selection_ids = [list(i.values())[0] for i in self.selection_ids]
            self.__class__.selection_name = event_params[0].team1
            self.event_names = event_params[0].event_name
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_open_bets()
        self.device.driver.implicitly_wait(5)
        bet = self.get_bet_with_my_acca_edit()
        self.assertTrue(bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        self.assertEqual(bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'"{vec.ema.EDIT_MY_BET}" button has incorrect name')
        bet.edit_my_acca_button.click()

    def test_001_tap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_acca(self):
        """
        DESCRIPTION: Tap on the 'Selection Removal' button to remove a selection from their original Acca
        EXPECTED: The selection is removed from their original Acca
        """
        bet = self.get_bet_with_my_acca_edit()
        self.device.driver.implicitly_wait(3)
        self.__class__.selection = bet.items[0]
        self.assertTrue(self.selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
        self.selection.edit_my_acca_remove_icon.click()
        self.__class__.edited_bet = self.get_bet_with_my_acca_edit()
        selection = self.edited_bet.items[0]
        self.assertEqual(selection.outcome_name, self.selection_name,
                         msg=f'Selection name for the removed selection "{self.selection_name}" is not displayed')
        self.assertTrue(selection.edit_my_acca_undo_icon.is_displayed(), msg=f'"{vec.EMA.UNDO_LEG_REMOVE}" button is not displayed')

    def test_002_tap_on_cancel_editing_button_and_verify_that_cancel_message_is_not_shown(self):
        """
        DESCRIPTION: Tap on 'Cancel Editing' button and verify that 'Cancel' message is not shown
        EXPECTED: * Cancel message is not shown.
        EXPECTED: * Removed selection is restored.
        EXPECTED: * User is on Openbet /Cashout Tab
        """
        self.assertTrue(self.edited_bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have '
                            f'"{vec.ema.CANCEL}" button on header')
        self.assertEqual(self.edited_bet.edit_my_acca_button.name, vec.ema.CANCEL,
                         msg=f'"{vec.ema.CANCEL}" button is not displayed')
        self.edited_bet.edit_my_acca_button.click()
        self.__class__.bet = self.get_bet_with_my_acca_edit()
        self.__class__.selection = self.bet.items[0]
        self.assertTrue(self.bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')

    def test_003_tap_on_edit_my_betacca_buttontap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_accatry_to_navigate_away_from_the_page_click_back_button_bottom_menu_item_my_bets_tabs_etc(
            self):
        """
        DESCRIPTION: Tap on 'Edit My Bet/Acca' button
        DESCRIPTION: Tap on the 'Selection Removal' button to remove a selection from their original Acca
        DESCRIPTION: Try to navigate away from the page (click Back button, bottom menu item, My Bets tabs, etc)
        EXPECTED: Cancel message is shown
        """
        self.device.driver.implicitly_wait(1)
        self.bet.edit_my_acca_button.click()
        self.selection.edit_my_acca_remove_icon.click()
        self.device.driver.implicitly_wait(3)
        if self.brand == 'bma':
            self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
            self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DO_YOU_WANT_TO_CANCEL_EDITING)
            self.assertEqual(self.dialog.text, vec.EMA.EDIT_CANCEL.caption.upper(),
                             msg=f'Actual message: "{self.dialog.text}" is not the same as Expected message: "{vec.EMA.EDIT_CANCEL.caption.upper()}"')
        else:
            if self.device_type == 'mobile':
                self.site.open_bets.tab_content.grouping_buttons.click_button(vec.bet_history.LOTTO_TAB_NAME)
            else:
                self.site.betslip.tabs_menu.items_as_ordered_dict.get(vec.bet_history.SETTLED_BETS_TAB_NAME).click()
            self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_DO_YOU_WANT_TO_CANCEL_EDITING)
            self.assertEqual(self.dialog.text, vec.EMA.EDIT_CANCEL.caption,
                             msg=f'Actual message: "{self.dialog.text}" is not the same as Expected message: "{vec.EMA.EDIT_CANCEL.caption}"')
        self.assertTrue(self.dialog, msg='Cancel EDIT ACCA dialog is not present on page')

    def test_004_verify_content_of_popup_message(self):
        """
        DESCRIPTION: Verify content of Popup message
        EXPECTED: - Text:
        EXPECTED: 'Do you want to cancel editing?
        EXPECTED: Moving away from this page will cancel changes already made to this bet! Are you sure you want to cancel?'
        EXPECTED: - 'Cancel Edit' button
        EXPECTED: - 'Continue Editing' button
        """
        cancel_edit_popup_msg = self.dialog.description
        self.assertEqual(cancel_edit_popup_msg, vec.EMA.EDIT_CANCEL.text,
                         msg=f'Actual message: "{cancel_edit_popup_msg}" is not the same as Expected message: "{vec.EMA.EDIT_CANCEL.text}"')
        self.assertTrue(self.dialog.cancel_edit_button.is_displayed(), msg='Cancel Edit button is not shown')
        self.assertTrue(self.dialog.continue_edit_button.is_displayed(), msg='Cancel Edit button is not shown')

    def test_005_tap_on_cancel_edit_button_and_verify_that_editing_is_canceled_and_user_is_on_openbet_cashout_tab(self):
        """
        DESCRIPTION: Tap on 'Cancel Edit' button and verify that editing is canceled and user is on Openbet /Cashout Tab
        EXPECTED: Editing is canceled and user is on Openbet /Cashout Tab
        """
        self.dialog.cancel_edit_button.click()
        self.assertTrue(self.bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')

    def test_006_tap_on_continue_editing_button_and_verify_that_popup_is_closed_and_user_continue_editing(self):
        """
        DESCRIPTION: Tap on 'Continue Editing' button and verify that popup is closed and user continue editing
        EXPECTED: 'Continue Editing' should close the pop up and continue editing
        """
        self.test_003_tap_on_edit_my_betacca_buttontap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_accatry_to_navigate_away_from_the_page_click_back_button_bottom_menu_item_my_bets_tabs_etc()
        self.dialog.continue_edit_button.click()
        self.assertTrue(self.bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
