import pytest

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


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
class Test_C3020315_Verify_removing_acca_selections_in_edit_page_in_Cash_Out_Tab(BaseCashOutTest):
    """
    TR_ID: C3020315
    NAME: Verify removing acca selection(s) in edit page in 'Cash Out' Tab
    DESCRIPTION: This test case verifies removing selection(s) in edit acca
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 2. Login into App
    PRECONDITIONS: 3. Place Multiple bet
    PRECONDITIONS: 4. Navigate to the Bet History from Right/User menu
    PRECONDITIONS: 5. Go to 'Cash Out' tab -> verify that 'EDIT MY BET/ACCA' button is available
    PRECONDITIONS: NOTE: 'EDIT MY BET/ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
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
        _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event_params[0].event_name, number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{self.event_params[0].event_name}"')
        return bet

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Create events
        DESCRIPTION: 2. Login into App
        DESCRIPTION: 3. Place Multiple bet
        DESCRIPTION: 4. Navigate to the Bet History
        DESCRIPTION: 5. Go to 'Cash Out' tab -> verify that 'EDIT MY BET/ACCA' button is available
        """
        system_config = self.get_initial_data_system_configuration()
        cashout_cms = system_config.get('CashOut', {})
        if not cashout_cms:
            cashout_cms = self.cms_config.get_system_configuration_item('CashOut')
        if not cashout_cms:
            raise CmsClientException('CashOut section not found in System Configuration')
        if not cashout_cms.get('isCashOutTabEnabled'):
            raise CmsClientException('CashOut tab is not enabled in CMS')

        self.__class__.event_params = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        selection_ids = [self.event_params[0].selection_ids, self.event_params[1].selection_ids]
        self.__class__.selection_name = self.event_params[0].team1
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=[list(i.values())[0] for i in selection_ids])
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()
        self.site.open_my_bets_cashout()
        bet = self.get_bet_with_my_acca_edit()
        self.assertTrue(bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        self.assertEqual(bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'"{vec.ema.EDIT_MY_BET}" button has incorrect name')
        self.__class__.est_returns_value = bet.est_returns.stake_value
        bet.edit_my_acca_button.click()

    def test_001_tap_edit_my_bet_coraledit_my_acca_ladbrokes_button(self):
        """
        DESCRIPTION: Tap 'EDIT MY BET' (Coral)/EDIT MY ACCA' (Ladbrokes) button
        EXPECTED: Edit mode of the Acca is available
        """
        bet = self.get_bet_with_my_acca_edit()
        self.__class__.selection = bet.items[0]
        self.assertTrue(self.selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')

    def test_002_click_on_selections_removal_button_to_remove_selections_from_their_original_acca(self):
        """
        DESCRIPTION: Click on Selection(s) Removal button to remove selection(s) from their original Acca
        EXPECTED: - The selection(s) are no longer displayed
        EXPECTED: - The selection name(s) for the removed selection is displayed
        EXPECTED: - UNDO button is displayed
        """
        self.selection.edit_my_acca_remove_icon.click()
        self.__class__.edited_bet = self.get_bet_with_my_acca_edit()
        selection = self.edited_bet.items[0]
        self.assertEqual(selection.outcome_name, self.selection_name,
                         msg=f'Selection name for the removed selection "{self.selection_name}" is not displayed')
        self.assertTrue(selection.edit_my_acca_undo_icon.is_displayed(), msg='UNDO button is not displayed')

    def test_003_verify_that_potential_returns_are_updated(self):
        """
        DESCRIPTION: Verify that Potential Returns are updated
        EXPECTED: New Potential Returns is displayed
        """
        actual_est_returns_value = self.edited_bet.est_returns.stake_value
        self.assertTrue(actual_est_returns_value < self.est_returns_value,
                        msg=f'New Potential Returns value "{actual_est_returns_value}" is not updated')
        actual_label = self.edited_bet.est_returns.label
        self.assertEqual(actual_label, vec.bet_history.NEW_TOTAL_RETURN,
                         msg=f'Actual label "{actual_label}" != Expected "{vec.bet_history.NEW_TOTAL_RETURN}"')

    def test_004_verify_that_cancel_editing_button_is_displayed(self):
        """
        DESCRIPTION: Verify that 'Cancel Editing' Button is displayed
        EXPECTED: 'Cancel Editing' Button is displayed
        """
        self.assertTrue(self.edited_bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have '
                            f'"{vec.ema.CANCEL}" button on header')
        self.assertEqual(self.edited_bet.edit_my_acca_button.name, vec.ema.CANCEL,
                         msg=f'"{vec.ema.CANCEL}" button is not displayed')

    def test_005_verify_that_confirm_button_is_displayed(self):
        """
        DESCRIPTION: Verify that 'Confirm' Button is displayed
        EXPECTED: 'Confirm' Button is displayed
        """
        self.assertTrue(self.edited_bet.confirm_button.is_displayed(), msg='"Confirm" Button is not displayed')
        self.assertTrue(self.edited_bet.confirm_button.is_enabled(), msg='"Confirm" Button is not active')

    def test_006_verify_that_message_editing_this_bet_changes_the_value_of_cashout_and_odds_is_shown(self):
        """
        DESCRIPTION: Verify that Message "Editing this bet changes the value of Cashout and Odds" is shown
        EXPECTED: Message "Editing this bet changes the value of Cashout and Odds" is shown
        """
        self.assertEqual(self.edited_bet.edit_my_acca_warning_message, vec.ema.EDIT_WARNING,
                         msg=f'Actual warning message: {self.edited_bet.edit_my_acca_warning_message}, '
                             f'expected warning message: {vec.ema.EDIT_WARNING}')
