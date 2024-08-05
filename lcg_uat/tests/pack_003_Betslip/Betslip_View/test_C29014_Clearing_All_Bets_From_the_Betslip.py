import pytest

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C29014_Clearing_All_Bets_From_the_Betslip(BaseBetSlipTest):
    """
    TR_ID: C29014
    NAME: Clearing All Bets From the Betslip
    DESCRIPTION: This test case verifies how all bets can be removed from the BetSlip.
    PRECONDITIONS: User is logged in / logged out
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True
    remove_all_button = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/select two different sport events
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'*** Found Football event with selections  "{self.selection_ids}"')
            self.__class__.team1_1 = list(self.selection_ids.keys())[0]

            self.__class__.selection_ids_2 = self.get_active_event_selections_for_category(category_id=self.ob_config.tennis_config.category_id)
            self.__class__.team1_2 = list(self.selection_ids_2.keys())[0]
            self._logger.info(f'*** Found Tennis event with selections "{self.selection_ids_2}"')

        else:
            event_params1 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1_1, self.__class__.selection_ids = event_params1.team1, event_params1.selection_ids
            event_params2 = self.ob_config.add_tennis_event_to_autotest_trophy()
            self.__class__.team1_2, self.__class__.selection_ids_2 = event_params2.team1, event_params2.selection_ids

    def test_001_add_single_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add single selection to the Betslip
        EXPECTED:
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1_1])

    def test_002_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: * Selection is present in the Bet Slip
        EXPECTED: * 'REMOVE ALL' button is displayed within Betslip header on the right from Your Selections section
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.team1_1, singles_section.keys())

        self.__class__.remove_all_button = self.get_betslip_content().remove_all_button
        name = self.remove_all_button.name
        self.assertEqual(name, vec.betslip.REMOVE_ALL_SELECTIONS,
                         msg=f'Button name "{name}" is not as expected "{vec.betslip.REMOVE_ALL_SELECTIONS}"')
        self.assertTrue(self.remove_all_button.is_displayed(), msg='REMOVE ALL button is not displayed')

    def test_003_tap_remove_all_button(self):
        """
        DESCRIPTION: Tap 'REMOVE ALL' button
        EXPECTED: * Remove All pop-up is shown
        """
        self.remove_all_button.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_REMOVE_ALL}" dialog is not shown')

    def test_004_verify_view_of_remove_all_pop_up(self):
        """
        DESCRIPTION: Verify view of Remove All pop-up
        EXPECTED: Pop-up contains header title, question text and two buttons: Cancel and Continue
        EXPECTED: Coral: pop up name is "REMOVE ALL?", Ladbrokes: pop up name is "Remove All" # is verified in previous step
        """
        text = self.dialog.text
        self.assertTrue(text, msg='Text is not shown on Pop-up')
        self.assertEqual(text, vec.betslip.CONFIRM_CLEAR_OF_BET_SLIP,
                         msg=f'Pop-up text "{text}" is not as expected "{vec.betslip.CONFIRM_CLEAR_OF_BET_SLIP}"')

        self.assertTrue(self.dialog.has_continue_button(), msg='Continue button is not shown')
        continue_button_name = self.dialog.continue_button.name
        self.assertEqual(continue_button_name, vec.betslip.CLEAR_BETSLIP_CONTINUE,
                         msg=f'Button name "{continue_button_name}" is not as expected "{vec.betslip.CLEAR_BETSLIP_CONTINUE}"')

        self.assertTrue(self.dialog.has_cancel_button(), msg='Cancel button is not shown')
        cancel_button_name = self.dialog.cancel_button.name
        self.assertEqual(cancel_button_name, vec.betslip.CLEAR_BETSLIP_CANCEL,
                         msg=f'Button name "{cancel_button_name}" is not as expected "{vec.betslip.CLEAR_BETSLIP_CANCEL}"')

    def test_005_press_cancel_button(self):
        """
        DESCRIPTION: Press Cancel button
        EXPECTED: * Remove All pop-up is closed
        EXPECTED: * User stays on Betslip, placed bets are present in Betslip
        """
        self.dialog.cancel_button.click()
        self.dialog.wait_dialog_closed()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL, timeout=1)
        self.assertFalse(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_REMOVE_ALL}" dialog is still shown after click on Cancel button')

        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip is not opened')
        singles_section = self.get_betslip_sections().Singles
        self.assertIn(self.team1_1, singles_section.keys())

    def test_006_tap_remove_all_button_and_press_continue_button(self):
        """
        DESCRIPTION: Tap 'REMOVE ALL' button and press Continue button
        EXPECTED: *  Bets is removed from the Bet Slip after confirming
        EXPECTED: *  The Bet Slip counter is reset to 0
        EXPECTED: *  For Mobile: Betslip is automatically closed after selections removal
        EXPECTED: *  For Tablet and Desktop: User sees 'You have no selections in the slip.' message
        EXPECTED: *  For Mobile: 'GO BETTING' button is displayed for empty Betslip
        """
        self.test_003_tap_remove_all_button()
        self.dialog.continue_button.click()
        self.assertTrue(self.dialog.wait_dialog_closed(), msg=f'"{vec.dialogs.DIALOG_MANAGER_REMOVE_ALL}" popup not closed')
        self.__class__.expected_betslip_counter_value = 0

        if self.device_type == 'mobile':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is not closed')

            self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)
        else:
            betslip = self.get_betslip_content()
            no_selections_title = betslip.no_selections_title
            self.assertTrue(no_selections_title, msg=f'"{vec.betslip.NO_SELECTIONS_TITLE}" title is not shown')
            self.assertEqual(no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'Title "{no_selections_title}" is not as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

    def test_007_mobile_go_to_any_other_page_except_of_homepagetap_go_betting_button_in_betslip_widget(self):
        """
        DESCRIPTION: Mobile:
        DESCRIPTION: Go to any other page except of Homepage
        DESCRIPTION: Tap 'GO BETTING' button in Betslip widget
        EXPECTED: - Homepage is opened in the main view
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='sport/football')
            self.site.wait_content_state('football')
            self.site.open_betslip()
            result = self.site.has_betslip_opened()
            self.assertTrue(result, msg='Betslip is not opened')
            self.assertTrue(self.get_betslip_content().has_start_betting_button(), msg=f'"{vec.bet_history.START_BETTING}" button is not shown')
            self.get_betslip_content().start_betting_button.click()
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is not closed')
            self.site.wait_content_state('HomePage')

    def test_008_mobile_tap_go_betting_button_in_betslip_widget_again_when_user_is_already_navigated_to_the_homepage(self):
        """
        DESCRIPTION: Mobile:
        DESCRIPTION: Tap 'GO BETTING' button in Betslip widget again when user is already navigated to the Homepage
        EXPECTED: Homepage continues to display in the main view without any additional redirection
        """
        if self.device_type == 'mobile':
            self.site.open_betslip()
            result = self.site.has_betslip_opened()
            self.assertTrue(result, msg='Betslip is not opened')
            self.assertTrue(self.get_betslip_content().has_start_betting_button(), msg=f'"{vec.bet_history.START_BETTING}" button is not shown')
            self.get_betslip_content().start_betting_button.click()
            self.assertFalse(self.site.has_betslip_opened(expected_result=False), msg='Betslip is not closed')
            self.site.wait_content_state('HomePage')

    def test_009_add_several_selections_from_the_different_events(self):
        """
        DESCRIPTION: Add several selections from the different events
        EXPECTED:
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1_1], self.selection_ids_2[self.team1_2]))

    def test_010_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: *   Selections are present in the Bet Slip
        EXPECTED: * 'REMOVE ALL' button is displayed within Betslip header on the right from Your Selections section
        """
        singles_section = self.get_betslip_sections(multiples=True).Singles

        self.assertIn(self.team1_1, singles_section.keys())
        self.assertIn(self.team1_2, singles_section.keys())

        self.__class__.remove_all_button = self.get_betslip_content().remove_all_button
        self.assertEqual(self.remove_all_button.name, vec.betslip.REMOVE_ALL_SELECTIONS)
        self.assertTrue(self.remove_all_button.is_displayed(), msg='REMOVE ALL button is not displayed')

    def test_011_tap_remove_all_button(self):
        """
        DESCRIPTION: Tap 'REMOVE ALL' button
        EXPECTED: *  Remove All pop-up is shown
        """
        self.test_003_tap_remove_all_button()

    def test_012_verify_view_of_remove_all_pop_up(self):
        """
        DESCRIPTION: Verify view of Remove All pop-up
        EXPECTED: Pop-up contains header title, question text and two buttons: Cancel and Continue
        """
        self.test_004_verify_view_of_remove_all_pop_up()

    def test_013_press_cancel_button(self):
        """
        DESCRIPTION: Press Cancel button
        EXPECTED: * Remove All pop-up is closed
        EXPECTED: * User stays on Betslip, placed bets are present in Betslip
        """
        self.dialog.cancel_button.click()
        self.dialog.wait_dialog_closed()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL, timeout=1)
        self.assertFalse(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_REMOVE_ALL}" dialog is shown after click on Cancel button')

        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip is not opened')
        singles_section = self.get_betslip_sections(multiples=True).Singles

        self.assertIn(self.team1_1, singles_section.keys())
        self.assertIn(self.team1_2, singles_section.keys())

    def test_014_tap_remove_all_button_and_press_continue_button(self):
        """
        DESCRIPTION: Tap 'REMOVE ALL' button and press Continue button
        EXPECTED: *  All Bets are removed from the Bet Slip after confirming (Singles, Multiples)
        EXPECTED: *  The Bet Slip counter is reset to 0
        EXPECTED: *  For Mobile: Betslip is automatically closed after selections removal
        EXPECTED: *  For Tablet and Desktop: User sees 'You have no selections in the slip.' message
        EXPECTED: *  For Tablet and Desktop: 'GO BETTING' button is displayed for empty Betlsip
        """
        self.test_006_tap_remove_all_button_and_press_continue_button()
