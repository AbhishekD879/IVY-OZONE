import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.acca
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.portal_dependant
@vtest
class Test_C9240648_Verify_Undo_multiple_removals(BaseCashOutTest, BaseBetSlipTest):
    """
    TR_ID: C9240648
    NAME: Verify Undo multiple removals
    DESCRIPTION: This test case verifies Undo multiple removals
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet (Treble or more)
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Verify that 'Edit My Bet/Edit My ACCA' button is available on both Cashout and My Bets (Open Bets)
    PRECONDITIONS: Tap on 'Edit My Bet/Edit My ACCA' button
    PRECONDITIONS: NOTE: 'Edit My BET/ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True
    number_of_events = 3
    selection_ids = []
    event_names = []

    def get_bet_with_my_acca_edit(self, open_bets=True):
        """
        Get bet with My ACCA edit functionality
        """
        if open_bets:
            _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE, event_names=self.event_names, number_of_bets=1)
        else:
            _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_TREBLE_STAKE_TITLE, event_names=self.event_names,
                number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{self.event_names}"')
        return bet

    def selection_undo(self):
        for betleg in list(self.selections)[:2]:
            actual_est_returns = self.bet.est_returns.stake_value
            self.assertTrue(betleg.edit_my_acca_undo_icon.is_displayed(), msg='undo icon is not displayed')
            betleg.edit_my_acca_undo_icon.click()
            self.assertTrue(betleg.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
            self.assertNotEquals(actual_est_returns, self.bet.est_returns.stake_value,
                                 msg='potential returns are not updated')

        actual_est_returns_value = self.bet.est_returns.stake_value
        self.assertEquals(actual_est_returns_value, 'N/A',
                          msg='updated potentials returns are not displayed')

    def test_000_preconditions(self):
        """
        Description: Enable My ACCA feature toggle in CMS
        Description: CMS -> System Configuration -> Structure -> EMA -> Enabled
        Description: Login into App
        Description: Place Multiple bet (Treble or more)
        """
        if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)
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
            event_params = self.create_several_autotest_premier_league_football_events(
                number_of_events=self.number_of_events)
            self.selection_ids = [event_params[0].selection_ids, event_params[1].selection_ids,
                                  event_params[2].selection_ids]
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
        bet = self.get_bet_with_my_acca_edit(open_bets=True)
        self.assertTrue(bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        self.assertEqual(bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'"{vec.ema.EDIT_MY_BET}" button has incorrect name')
        bet.edit_my_acca_button.click()
        self.__class__.bet = self.get_bet_with_my_acca_edit(open_bets=True)

    def test_001_tap_on_a_selection_removal_button_for_2_or_more_selections(self):
        """
        DESCRIPTION: Tap on a Selection Removal button for 2 (or more) selections
        EXPECTED: The Selection 'Undo' button is displayed for each tapped Selection
        """
        self.__class__.selections = self.bet.items_as_ordered_dict.values()
        for betleg in list(self.selections)[:2]:
            actual_est_returns = self.bet.est_returns.stake_value
            self.assertTrue(betleg.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
            betleg.edit_my_acca_remove_icon.click()
            self.assertTrue(betleg.edit_my_acca_undo_icon.is_displayed(), msg='undo icon is not displayed')
            self.assertNotEquals(actual_est_returns, self.bet.est_returns.stake_value,
                                 msg='potential returns are not updated')

    def test_002_click_on_the_selections_undo_buttons(self):
        """
        DESCRIPTION: Сlick on the Selections 'Undo' buttons
        EXPECTED: The respective removed selection is re-displayed
        """
        self.selection_undo()
        if self.brand == 'bma':
            if self.device_type == 'desktop':
                self.bet.edit_my_acca_button.click()
            self.site.open_my_bets_cashout()
            bet = self.get_bet_with_my_acca_edit(open_bets=False)
            self.assertTrue(bet.edit_my_acca_button.is_displayed(),
                            msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
            self.assertEqual(bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                             msg=f'"{vec.ema.EDIT_MY_BET}" button has incorrect name')
            bet.edit_my_acca_button.click()
            self.__class__.bet = self.get_bet_with_my_acca_edit(open_bets=False)
            self.test_001_tap_on_a_selection_removal_button_for_2_or_more_selections()
            self.selection_undo()

    def test_003_verify_that_the_selection_removal_button_is_re_displayed_adjacent_to_the_selection(self):
        """
        DESCRIPTION: Verify that the Selection Removal button is re-displayed adjacent to the selection
        EXPECTED: The Selection Removal button is re-displayed adjacent to the selection
        """
        # covered in step 2

    def test_004_verify_that_the_updated_potential_returns_are_displayed(self):
        """
        DESCRIPTION: Verify that the updated potential returns are displayed
        EXPECTED: The updated potential returns are displayed
        """
        # covered in step 2
