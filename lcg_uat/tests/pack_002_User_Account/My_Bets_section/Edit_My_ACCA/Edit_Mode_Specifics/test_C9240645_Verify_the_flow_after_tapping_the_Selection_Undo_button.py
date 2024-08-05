import pytest

import tests
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.acca
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9240645_Verify_the_flow_after_tapping_the_Selection_Undo_button(BaseCashOutTest):
    """
    TR_ID: C9240645
    NAME: Verify the flow after tapping the Selection 'Undo' button
    DESCRIPTION: This test case verifies the flow after tapping the Selection 'Undo' button
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Bet' button is available
    PRECONDITIONS: Tap on 'Edit My Bet' button
    PRECONDITIONS: NOTE: 'Edit My BET/ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True

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
            bet_type='DOUBLE', event_names=self.event.event_name, number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{self.event.event_name}"')
        return bet

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Create events
        DESCRIPTION: 2. Login into App
        DESCRIPTION: 3. Place Multiple bet
        DESCRIPTION: 4. Navigate to the Bet History
        DESCRIPTION: 5. Go to 'Open Bets' Tab -> verify that 'Edit My Bet' button is available
        DESCRIPTION: 6. Tap on 'Edit My Bet' button
        """
        event_params = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.__class__.event = event_params[0]
        selection_ids = [self.event.selection_ids, event_params[1].selection_ids]
        self.__class__.selection_name = self.event.team1
        self.__class__.event_name = f'{self.selection_name} - {self.event.event_name} {self.event.local_start_time}'
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=[list(i.values())[0] for i in selection_ids])
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_open_bets()
        bet = self.get_bet_with_my_acca_edit()
        self.assertTrue(bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        self.assertEqual(bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'Actual button name: "{bet.edit_my_acca_button.name}", '
                             f'expected button name: "{vec.ema.EDIT_MY_BET}"')
        self.__class__.est_returns_value = bet.est_returns.stake_value
        bet.edit_my_acca_button.click()

    def test_001_tap_on_a_selection_removal_button(self):
        """
        DESCRIPTION: Tap on a Selection Removal button
        EXPECTED: Chosen selection is removed from the original Acca
        EXPECTED: The Selection 'Undo' button is displayed
        """
        bet = self.get_bet_with_my_acca_edit()
        self.__class__.selection = bet.items_as_ordered_dict.get(self.event_name)
        self.assertTrue(self.selection,
                        msg=f'Selection "{self.event_name}" is not found')
        self.assertTrue(self.selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
        self.selection.edit_my_acca_remove_icon.click()
        self.assertTrue(self.selection.edit_my_acca_undo_icon.is_displayed(), msg='UNDO button is not displayed')

    def test_002_click_on_the_selection_undo_button(self):
        """
        DESCRIPTION: Click on the Selection 'Undo' button
        EXPECTED: The removed selection is re-displayed
        """
        self.selection.edit_my_acca_undo_icon.click()
        self.__class__.edited_bet = self.get_bet_with_my_acca_edit()
        self.__class__.selection = self.edited_bet.items_as_ordered_dict.get(self.event_name)
        self.assertEqual(self.selection.outcome_name, self.selection_name,
                         msg=f'Selection name for the removed selection "{self.selection_name}" is not displayed')

    def test_003_verify_that_the_selection_removal_button_is_re_displayed_adjacent_to_the_selection(self):
        """
        DESCRIPTION: Verify that the Selection Removal button is re-displayed adjacent to the selection
        EXPECTED: The Selection Removal button is re-displayed adjacent to the selection
        """
        self.assertTrue(self.selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')

    def test_004_verify_that_the_updated_potential_returns_are_displayed(self):
        """
        DESCRIPTION: Verify that the updated potential returns are displayed
        EXPECTED: The updated potential returns are displayed
        """
        self.assertEqual(self.edited_bet.est_returns.label, vec.bet_history.TOTAL_RETURN,
                         msg=f'Wrong updated potential returns label displayed. '
                             f'\nActual: "{self.edited_bet.est_returns.label}" \nExpected: "{vec.bet_history.TOTAL_RETURN}"')
