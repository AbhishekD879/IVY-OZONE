import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
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
class Test_C9240630_Verify_the_Undo_button_when_a_user_removes_a_selection_from_their_original_acca(BaseCashOutTest):
    """
     TR_ID: C9240630
     NAME: Verify the 'Undo' button when a user removes a selection from their original acca
     DESCRIPTION: This test case verifies displaying of the Selection 'Undo' button when a user removes a selection from their original acca
     DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
     DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
     PRECONDITIONS: Enable My ACCA feature toggle in CMS
     PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
     PRECONDITIONS: Login into App
     PRECONDITIONS: Place Multiple bet
     PRECONDITIONS: Navigate to the Bet History from Right/User menu
     PRECONDITIONS: Verify that 'Edit My Bet/Edit My ACCA' button is available on both Cashout and My Bets (Open Bets)
     PRECONDITIONS: Tap on 'Edit My Bet/Edit My ACCA' button: need to verify on both Cashout and My Bets (Open Bets)
     PRECONDITIONS: NOTE: 'Edit My ACCA/BET' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
     """

    keep_browser_open = True
    number_of_events = 2
    selection_ids = []
    event_names = []

    def get_bet_with_my_acca_edit(self, open_bets=True):
        """
        Get bet with My ACCA edit functionality
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
        Description: Enable My ACCA feature toggle in CMS
        Description: CMS -> System Configuration -> Structure -> EMA -> Enabled
        Description: Login into App
        Description: Place Multiple bet (Treble or more)
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
            event_params = self.create_several_autotest_premier_league_football_events(
                number_of_events=self.number_of_events)
            self.selection_ids = [event_params[0].selection_ids, event_params[1].selection_ids]
            self.selection_ids = [list(i.values())[0] for i in self.selection_ids]
            self.__class__.selection_name = event_params[0].team1
            self.event_names = event_params[0].event_name
        self.site.login()
        self.open_betslip_with_selections(self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        if self.device_type == 'mobile':
            self.site.bet_receipt.footer.click_done()

        if self.brand == 'bma':
            self.site.open_my_bets_cashout()
            self.__class__.bet = self.get_bet_with_my_acca_edit(open_bets=False)

    def test_001_tap_on_edit_my_betedit_my_acca_button_on_cashout_tab(self, brand='bma'):
        """
         DESCRIPTION: Tap on 'Edit My Bet/Edit My ACCA' button on Cashout tab
         EXPECTED: The Selection Removal sign "X" appears next to all selections of ACCA
         """
        if self.brand in brand:
            self.bet.edit_my_acca_button.click()
            selections = self.bet.items_as_ordered_dict.values()
            for betleg in list(selections)[:2]:
                self.assertTrue(betleg.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')

    def test_002_tap_on_a_selection_removal_button_xto_remove_the_selection_from_the_original_acca_on_cashout(self, open_bets=False, brand='bma'):
        """
         DESCRIPTION: Tap on a Selection Removal button ('X')to remove the selection from the original Acca on Cashout
         EXPECTED: The selection is removed from ACCA and the "Undo" button is displayed next to it
         """
        if self.brand in brand:
            self.__class__.selection = self.bet.items[0]
            self.selection.edit_my_acca_remove_icon.click()
            self.assertTrue(self.selection.edit_my_acca_undo_icon.is_displayed(), msg='undo icon is not displayed')
            self.assertEqual(self.selection.outcome_name, self.selection_name,
                             msg=f'Selection name for the removed selection "{self.selection_name}" is not displayed')
            self.assertTrue(self.selection.leg_remove_marker.is_displayed(), msg='REMOVED text is not displayed')

    def test_003_verify_the_name_of_the_removed_selection(self):
        """
         DESCRIPTION: Verify the name of the removed selection
         EXPECTED: The removed selection is marked as "Removed" next to selection name
         """
        # covered in 2

    def test_004_tap_on_the_undo_button(self, open_bets=False, brand='bma'):
        """
         DESCRIPTION: Tap on the 'UNDO' button
         EXPECTED: The selection is added back to the ACCA and the Selection Removal sign "X" appears next to it
         """
        if self.brand in brand:
            self.selection.edit_my_acca_undo_icon.click()
            self.assertTrue(self.selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')

    def test_005_repeat_steps_2_4_on_my_bets_open_bets(self):
        """
         DESCRIPTION: Repeat steps 2-4 on My Bets (Open Bets)
         EXPECTED: The "UNDO" button works accordingly
         """
        if self.brand == 'bma':
            self.bet.edit_my_acca_button.click()
        self.site.open_my_bets_open_bets()
        self.__class__.bet = self.get_bet_with_my_acca_edit(open_bets=True)
        self.test_001_tap_on_edit_my_betedit_my_acca_button_on_cashout_tab(brand='bma,ladbrokes')
        self.test_002_tap_on_a_selection_removal_button_xto_remove_the_selection_from_the_original_acca_on_cashout(
            open_bets=True, brand='bma,ladbrokes')
        self.test_004_tap_on_the_undo_button(open_bets=True, brand='bma,ladbrokes')
