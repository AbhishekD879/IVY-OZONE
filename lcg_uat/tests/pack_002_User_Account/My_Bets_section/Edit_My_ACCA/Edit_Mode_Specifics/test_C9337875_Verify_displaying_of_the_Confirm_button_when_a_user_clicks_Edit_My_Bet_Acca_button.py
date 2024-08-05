import pytest
import voltron.environments.constants as vec
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.portal_dependant
@vtest
class Test_C9337875_Verify_displaying_of_the_Confirm_button_when_a_user_clicks_Edit_My_Bet_Acca_button(BaseCashOutTest,
                                                                                                       BaseBetSlipTest):
    """
    TR_ID: C9337875
    NAME: Verify displaying of the Confirm button when a user clicks Edit My Bet/Acca button
    DESCRIPTION: This test case verifies displaying of the Confirm button when a user clicks Edit My Acca button
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: NOTE: 'Edit My BET/ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True
    number_of_events = 2
    selection_ids = []
    event_names = []

    def verify_edit_my_acca(self, open_bets=True):
        self.__class__.bet = self.get_bet_with_my_acca_edit(open_bets)
        self.assertTrue(self.bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        self.assertEqual(self.bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'"{vec.ema.EDIT_MY_BET}" button has incorrect name')

    def get_bet_with_my_acca_edit(self, open_bets=True):
        """
        DESCRIPTION: Get bet with My ACCA edit functionality
        """
        if open_bets:
            _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event_names, number_of_bets=1)
        else:
            _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event_names, number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{self.event_names}"')
        return bet

    def test_000_preconditions(self):
        """
        DESCRIPTION: Enable My ACCA feature toggle in CMS
        DESCRIPTION: CMS -> System Configuration -> Structure -> EMA -> Enabled
        DESCRIPTION: 1. Create events
        DESCRIPTION: 2. Login into App
        DESCRIPTION: 3. Place Multiple bet
        DESCRIPTION: 4. Navigate to the Bet History
        DESCRIPTION: 5. Go to 'open bet' tab -> verify that 'EDIT MY BET/ACCA' button is available
        """
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')
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
            if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
                self.cms_config.set_my_acca_section_cms_status(ema_status=True)
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
        self.verify_edit_my_acca(open_bets=True)

    def test_001_tap_on_on_single_line_accumulator_edit_my_betacca_button(self):
        """
        DESCRIPTION: Tap on on Single line accumulator 'Edit My Bet/Acca' button
        EXPECTED: User is navigated to My Bet/Acca Edit mode
        """
        self.bet.edit_my_acca_button.click()
        sleep(3)
        cancel_button_text = self.bet.edit_my_acca_button.name
        self.assertEqual(cancel_button_text, vec.EMA.CANCEL,
                         msg=f'Actual text:"{vec.EMA.EDIT_MY_BET}" is not changed to Expected text:"{vec.EMA.CANCEL}".')
        self.assertTrue(self.bet.edit_my_acca_button.is_enabled(), msg=f'"{vec.EMA.EDIT_MY_BET}" Button is not active')

    def test_002_verify_that_confirm_button_is_displayed_and_non_click_able(self):
        """
        DESCRIPTION: Verify that 'Confirm' button is displayed and non-click-able
        EXPECTED: 'Confirm' button is displayed and non-click-able
        """
        self.assertTrue(self.bet.confirm_button.is_displayed(), msg=f'"{vec.ema.CONFIRM_EDIT}" Button is not displayed')
        self.assertFalse(self.bet.confirm_button.is_enabled(expected_result=False), msg=f'"{vec.ema.CONFIRM_EDIT}" Button is active')

    def test_003_verify_that_cancel_editing_button_is_displayed_and_clickable(self):
        """
        DESCRIPTION: Verify that 'Cancel Editing' button is displayed and clickable
        EXPECTED: 'Cancel Editing' button is displayed and clickable.
        """
        # covered in step1

    def test_004_tap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_acca(self,
                                                                                                    open_bets=True):
        """
        DESCRIPTION: Tap on the 'Selection Removal' button to remove a selection from their original Acca
        EXPECTED: The selection is removed from their original Acca
        """
        selection = self.bet.items[0]
        self.assertTrue(selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
        selection.edit_my_acca_remove_icon.click()
        edited_bet = self.get_bet_with_my_acca_edit(open_bets)
        selection = edited_bet.items[0]
        self.assertEqual(selection.outcome_name, self.selection_name,
                         msg=f'Selection name for the removed selection "{self.selection_name}" is not displayed')
        self.assertTrue(selection.edit_my_acca_undo_icon.is_displayed(), msg='UNDO button is not displayed')
        self.assertTrue(edited_bet.confirm_button.is_displayed(),
                        msg='"{vec.ema.CONFIRM_EDIT.upper()}" Button is not displayed')
        sleep(3)
        self.assertTrue(edited_bet.confirm_button.is_enabled(), msg='"{vec.ema.CONFIRM_EDIT.upper()}" is not active')

    def test_005_verify_that_the_confirm_button_is_displayed_and_click_able(self):
        """
        DESCRIPTION: Verify that the Confirm button is displayed and click-able
        EXPECTED: The 'Confirm' button is displayed and click-able
        """
        # covered in step 4
        # below for cashout tab
        if self.brand == 'bma':
            self.bet.edit_my_acca_button.click()
            self.site.open_my_bets_cashout()
            self.verify_edit_my_acca(open_bets=False)
            self.test_001_tap_on_on_single_line_accumulator_edit_my_betacca_button()
            self.test_002_verify_that_confirm_button_is_displayed_and_non_click_able()
            self.test_004_tap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_acca(open_bets=False)
