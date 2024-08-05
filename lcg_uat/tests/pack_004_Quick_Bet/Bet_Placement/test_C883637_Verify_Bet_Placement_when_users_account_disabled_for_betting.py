import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.medium
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.event_details
@pytest.mark.mobile_only
@pytest.mark.ob_smoke
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C883637_Verify_Bet_Placement_when_Users_Account_disabled_for_betting(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C883637
    VOL_ID: C9697650
    NAME: Verify Bet Placement when Users Account is disabled for betting
    DESCRIPTION: This test case verifies Bet Placement within Quick Bet when Account is disabled for betting
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Quick Bet functionality should be enabled in CMS and user`s settings
        DESCRIPTION: Quick Bet functionality is available for Mobile ONLY
        DESCRIPTION: User is logged in and has positive balance
        """
        self.__class__.football_event_params = self.ob_config.add_football_event_to_england_premier_league()
        self.__class__.tennis_event_params = self.ob_config.add_tennis_event_to_autotest_trophy()
        self.site.login(username=tests.settings.user_disable_football_bet, async_close_dialogs=False)
        user_balance = self.site.header.user_balance
        self.assertGreater(user_balance, 0, msg='User balance is not positive')

    def test_001_select_one_sport_selection(self):
        """
        DESCRIPTION: Tap one <Sport> selection
        EXPECTED: Quick Bet is displayed at the bottom of the page with a message "Sorry, you are not allowed to place bet on this selection."
        EXPECTED: Add to betslip and PLace bet buttons are disabled
        """
        self.navigate_to_edp(event_id=self.football_event_params.event_id)
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.football_event_params.team1)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet panel is not displayed')
        quick_bet_panel = self.site.quick_bet_panel
        error_text = quick_bet_panel.selection_error.text
        self.assertTrue(quick_bet_panel.selection_error,
                        msg=f'"{error_text}" error is not present.')
        self.assertEqual(error_text, vec.quickbet.BET_NOT_PERMITTED,
                         msg=f'Error message "{error_text}" does not equal "{vec.quickbet.BET_NOT_PERMITTED}"')
        self.assertFalse(quick_bet_panel.add_to_betslip_button.is_enabled(expected_result=False),
                         msg='Add to betslip button is not disabled')
        self.assertFalse(quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='Place bet button is not disabled')

    def test_002_tap_x_button(self):
        """
        DESCRIPTION: Tap 'X' button on Quick Bet
        EXPECTED: - Quick bet is closed
        """
        self.site.quick_bet_panel.header.close_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is shown')

    def test_003_add_another_selection_and_try_to_place_bet(self):
        """
        DESCRIPTION: Add another selection from <Sport> which is not disabled for betting and try to place a bet
        EXPECTED: Bet is placed successfully
        """
        self.navigate_to_edp(event_id=self.tennis_event_params.event_id)
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.tennis_event_params.team1,
                                                           market_name=self.expected_market_sections.match_betting)
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(timeout=5),
                        msg='Place bet button is not disabled')
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick bet not closed')

    def test_004_enable_from_step2_for_betting_in_openbet(self):
        """
        DESCRIPTION: Enable <Sport> from step #2 for betting Openbet Ti tool
        """
        # using user with enabled football betting instead
        self.site.logout()
        self.site.login()

    def test_005_repeat_steps_1_2(self):
        """
        DESCRIPTION: Repeat steps  # 1-2
        EXPECTED: Bet is placed successfully
        """
        self.navigate_to_edp(event_id=self.football_event_params.event_id)
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.football_event_params.team1)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet panel is not displayed')
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(timeout=5),
                        msg='Place bet button is not enabled')
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

        self.test_002_tap_x_button()
