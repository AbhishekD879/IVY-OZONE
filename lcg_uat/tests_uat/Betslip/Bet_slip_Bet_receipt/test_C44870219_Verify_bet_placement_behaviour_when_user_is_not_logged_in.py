import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.pages.shared.components.base import ComponentBase


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.p1
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C44870219_Verify_bet_placement_behaviour_when_user_is_not_logged_in(BaseBetSlipTest, ComponentBase):
    """
    TR_ID: C44870219
    NAME: Verify bet placement behaviour when user is not logged in.
    DESCRIPTION: Check  this journey for both Quick bet and bet slip
    PRECONDITIONS: - Quick bet applicable for mobiles only
    """
    keep_browser_open = True
    selection_list = []

    def selections(self, selection):
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')
        for index in range(0, selection):
            selection_btn = bet_buttons_list[index]
            if selection_btn in self.selection_list:
                continue
            self.scroll_to_we(selection_btn)
            selection_btn.click()
            self.selection_list.append(selection_btn)

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        EXPECTED: User can able to launch the app
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_on_any_selection(self):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: User must be displayed Quick bet Pop up
        EXPECTED: -User sees Add to bet slip and Login and place a bet buttons
        """
        self.selections(1)
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
            self.assertTrue(self.site.quick_bet_panel.add_to_betslip_button.is_displayed(),
                            msg='"ADD TO BETSLIP" button is not displayed')
            self.assertTrue(self.site.quick_bet_panel.place_bet.is_displayed(),
                            msg=f'"{vec.Betslip.LOGIN_AND_PLACE_BET_QUICK_BET}" button is not displayed')

    def test_003_enter_stake_and_click_on_login_and_place_a_bet_button(self):
        """
        DESCRIPTION: Enter stake and click on login And place a bet button
        EXPECTED: User should see "Login/register" overlay displayed
        EXPECTED: Close the overlay
        """
        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel
            quick_bet.selection.content.amount_form.input.value = str(self.bet_amount)
            quick_bet.place_bet.click()
            dialog = self.site.wait_for_dialog(vec.Dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
            self.assertTrue(dialog, msg='Log In dialog is not present on page')
            dialog.close_dialog()
            self.assertTrue(dialog.wait_dialog_closed(), msg='Log In dialog is not closed')
            quick_bet.add_to_betslip_button.click()
            self.site.wait_content_state('Homepage')

    def test_004_check_the_same_behaviour_for_bet_slip_journey(self):
        """
        DESCRIPTION: Check the same behaviour for bet slip journey
        """
        self.selections(2)
        self.site.header.bet_slip_counter.click()
        singles_section = self.get_betslip_sections().Singles
        for stake in singles_section.values():
            stake.amount_form.input.clear()
            stake.amount_form.input.value = self.bet_amount
        self.assertTrue(self.get_betslip_content().bet_now_button.is_displayed(),
                        msg=f'"{vec.Betslip.LOGIN_AND_BET_BUTTON_CAPTION}" button is not displayed')
        self.get_betslip_content().bet_now_button.click()
        dialog = self.site.wait_for_dialog(vec.Dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        self.assertTrue(dialog, msg='Log In dialog is not present on page')
        dialog.close_dialog()
        self.assertTrue(dialog.wait_dialog_closed(), msg='Log In dialog is not closed')

    def test_005_add_two_or_three_selections_to_bet_slip(self):
        """
        DESCRIPTION: Add two or three selections to bet slip
        EXPECTED: User sees "Login and place a bet" button on bet slip.
        """
        # This test step is covered in step 4

    def test_006_click_on_login_and_place_a_bet_button(self):
        """
        DESCRIPTION: Click on "Login and place a bet" button
        EXPECTED: User should see "Login/register" overlay displayed
        """
        # This test step is covered in step 4
