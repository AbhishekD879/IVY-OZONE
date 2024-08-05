import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
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
class Test_C9337877_Verify_the_flow_after_tapping_the_Confirm_button_in_My_Bet_Acca_Edit_mode(BaseCashOutTest):
    """
    TR_ID: C9337877
    NAME: Verify the flow after tapping the 'Confirm' button in My Bet/Acca Edit mode
    DESCRIPTION: This test case verifies the flow after tapping the 'Confirm' button in My Bet/Acca Edit mode
    DESCRIPTION: Ladbrokes : https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b?seid=5c4f1e8c4def2a015bb81cea
    DESCRIPTION: Coral : https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3?seid=5be15e2ea472811f68583124
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Bet/Acca' button is available
    PRECONDITIONS: Tap on 'Edit My  Bet/Acca' button -> verify that user is in 'My  Bet/Acca Edit' mode
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

    def get_bet_with_my_acca_edit_cashout(self):
        """
        Get bet with My ACCA edit functionality
        """
        _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE', event_names=self.event_params[0].event_name, number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{self.event_params[0].event_name}"')
        return bet

    def get_bet_with_my_acca_edit_open_bet(self):
        """
        Get bet with My ACCA edit functionality
        """
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event.event_name, number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{self.event.event_name}"')
        return bet

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Enable My ACCA feature toggle in CMS
        PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
        PRECONDITIONS: Login into App
        PRECONDITIONS: Place Multiple bet
        PRECONDITIONS: Navigate to the Bet History from Right/User menu
        PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Bet/Acca' button is available
        PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Bet/Acca' button is available
        PRECONDITIONS: Tap on 'Edit My  Bet/Acca' button -> verify that user is in 'My  Bet/Acca Edit' mode
        PRECONDITIONS: NOTE: 'Edit My BET/ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
        """
        self.__class__.event_params = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.__class__.event = self.event_params[0]
        selection_ids = [self.event.selection_ids, self.event_params[1].selection_ids]
        self.__class__.selection_name = self.event.team1
        self.__class__.full_name = ""
        for event in self.event_params:
            start_time_local = self.convert_time_to_local(date_time_str=event.start_time)
            self.__class__.full_name += f'{event.event_name} {start_time_local}, '
        self.__class__.full_name = f'DOUBLE - [{self.__class__.full_name[:-2]}]'
        start_time_local = self.convert_time_to_local(date_time_str=self.event.start_time)
        self.__class__.event_name = f'{self.selection_name} - {self.event.event_name} {start_time_local}'
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=[list(i.values())[0] for i in selection_ids])
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.__class__.account_balance = self.site.header.user_balance
        self.site.bet_receipt.footer.click_done()

        self.site.open_my_bets_open_bets()
        bet = self.get_bet_with_my_acca_edit_open_bet()
        self.assertTrue(bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        self.assertEqual(bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'"{bet.edit_my_acca_button.name}" button has incorrect name, it was expected to be '
                             f'"{vec.ema.EDIT_MY_BET}"')

        self.site.open_my_bets_cashout()
        bet = self.get_bet_with_my_acca_edit_cashout()
        self.assertTrue(bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{self.selection_name}" does not have My ACCA button on header')
        self.assertEqual(bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'"{bet.edit_my_acca_button.name}" button has incorrect name, it was expected to be '
                             f'"{vec.ema.EDIT_MY_BET}"')

        bet.edit_my_acca_button.click()
        bet = self.get_bet_with_my_acca_edit_cashout()
        self.assertEqual(bet.edit_my_acca_warning_message, vec.ema.EDIT_WARNING,
                         msg=f'Actual warning message: "{bet.edit_my_acca_warning_message}", '
                         f'expected warning message: "{vec.ema.EDIT_WARNING}"')

    def test_001_tap_on_the_selection_removal_button_to_remove_a_selection_from_their_original_acca(self):
        """
        DESCRIPTION: Tap on the 'Selection Removal' button to remove a selection from their original Acca
        EXPECTED: The selection is removed from their original Acca
        """
        bet = self.get_bet_with_my_acca_edit_cashout()
        self.assertTrue(bet.items_as_ordered_dict, msg='No events found')
        selection = bet.items_as_ordered_dict.get(self.event_name)
        self.assertTrue(selection.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
        selection.edit_my_acca_remove_icon.click()
        bet = self.get_bet_with_my_acca_edit_cashout()
        self.assertTrue(bet.items_as_ordered_dict, msg='No events found')

    def test_002_verify_that_the_confirm_button_is_displayed_and_click_able(self):
        """
        DESCRIPTION: Verify that the Confirm button is displayed and click-able
        EXPECTED: The 'Confirm' button is displayed and click-able
        """
        self.__class__.bet_to_delete = self.get_bet_with_my_acca_edit_cashout()
        self.assertTrue(self.bet_to_delete.confirm_button.is_enabled(),
                        msg=f'"Confirm" button is not displayed and click-able, but was expected to be')
        self.__class__.est_return_price = \
            self.bet_to_delete.est_returns.currency + self.bet_to_delete.est_returns.stake_value

    def test_003_make_sure_that_there_are_no_price_updates_to_any_open_selections_from_the_original_acca_and_there_are_no_suspended_selections_on_the_original_acca(self):
        """
        DESCRIPTION: Make sure that there are no price updates to any open selections from the original Acca and there are no suspended selections on the original Acca
        """
        _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE', event_names=self.event_params[0].event_name, number_of_bets=1)
        acca_bets = bet.items_as_ordered_dict
        self.assertTrue(acca_bets, msg='No bets found')
        price = self.ob_config.event.prices['odds_home']
        for bet in acca_bets.values():
            self.assertEqual(price, bet.odds_value,
                             msg=f'Bet price was expected to be "{price}", but was changed to "{bet.odds_value}"')

    def test_004_click_the_confirm_button_and_verify_that_the_original_bet_is_cashed_out(self):
        """
        DESCRIPTION: Click the 'Confirm' button and verify that the original bet is cashed out
        EXPECTED: The original bet is cashed out
        """
        self.bet_to_delete.confirm_button.click()
        _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='DOUBLE', event_names=self.event_params[0].event_name, raise_exceptions=False, number_of_bets=1)
        self.assertFalse(bet, msg=f'Bet for "{self.event_params[0].event_name}" still exists')

    def test_005_verify_that_no_funds_are_sent_or_requested_from_the_users_account(self):
        """
        DESCRIPTION: Verify that no funds are sent or requested from the users account
        EXPECTED: No funds are sent or requested from the users account
        """
        self.verify_user_balance(expected_user_balance=self.account_balance)

    def test_006_verify_that_the_successful_confirmation_message_is_shown_under_the_confirm_button(self):
        """
        DESCRIPTION: Verify that the successful confirmation message is shown under the 'Confirm' button
        EXPECTED: Successful confirmation message is shown under the 'Confirm' button
        """
        _, bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_params[1].event_name, raise_exceptions=False, number_of_bets=1)
        self.assertEqual(bet.cash_out_successful_message, vec.ema.EDIT_SUCCESS.caption,
                         msg=f'Message "{bet.cash_out_successful_message}" '
                             f'is not the same as expected "{vec.ema.EDIT_SUCCESS.caption}"')

    def test_007_verify_content_of_confirmation_message(self):
        """
        DESCRIPTION: Verify content of confirmation message
        EXPECTED: Text: 'Acca Edited Successfully' is displayed
        """
        pass  # done in previous step
