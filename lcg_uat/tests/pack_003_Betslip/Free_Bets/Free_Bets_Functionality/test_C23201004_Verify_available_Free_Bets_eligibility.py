import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
# @pytest.mark.prod # Can't be executed, can't create OB event on prod
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C23201004_Verify_available_Free_Bets_eligibility(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C23201004
    NAME: Verify available Free Bets eligibility
    DESCRIPTION: This test case verifies that eligible and NOT eligible Free Bets are displayed to user in Free Bets pop up. User should not be able to use Free Bet in case freebet / lines < 0.01
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has Free Bets available on their account (please add Free Bets with small value for, e.g. 0.10 0.05)
    PRECONDITIONS: User has multiple racing selections with E/W added to the Betslip
    PRECONDITIONS: -----
    PRECONDITIONS: - For DEV/TST env. - https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account
    PRECONDITIONS: - For PROD/HL env.:
    PRECONDITIONS: Coral: https://sports.coral.co.uk/promotions/details/new-customer-offer (Open a new online, mobile or telephone account with Coral. Place a 5+ Win or 5+ Each Way bet on any sport. Coral will give you an instant four x 5 free bets.)
    PRECONDITIONS: Ladbrokes: https://m.ladbrokes.com/en-gb//promotions/0 (Register a new Ladbrokes account on mobile or online using promo code '20FREE'. Place cumulative qualifying stakes to a total of 5 win or 5 each-way at odds totalling 1/2 or greater.)
    """
    keep_browser_open = True
    selection_ids = []
    selection_ids1 = []

    def add_selection_id_and_name(self, index, event):
        if index == 0:
            for index in range(len(event.selection_ids)):
                self.selection_ids.append(list(event.selection_ids.values())[index])
        else:
            self.selection_ids.append(list(event.selection_ids.values())[0])

    def test_000_preconditions(self):
        """
        DESCRIPTION: To disable live updates, please enter and save next string into Host file (File: /etc/hosts). Reload the app.
        DESCRIPTION: PROD - 127.0.0.1 liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com
        DESCRIPTION: TST2 - 127.0.0.1 liveserve-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com
        DESCRIPTION: TI TST2 system - http://backoffice-tst2.coral.co.uk/ti
        DESCRIPTION: Create racing test event
        EXPECTED: Event is created
        """
        for selection in range(5):
            if selection == 0:
                event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=11)
                self.add_selection_id_and_name(selection, event)
            else:
                event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
                self.add_selection_id_and_name(selection, event)
        for selection in range(4):
            event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1)
            self.selection_ids1.append(list(event.selection_ids.values())[0])

        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username, freebet_value=0.10)
        self.site.login(username=username)

    def test_001_open_bet_slip_and_press_on_use_free_bet_link_under_multiple_bet_type_from_preconditioneg_if_you_have_010_free_bet_try_to_use_it_on_5_fold_acca_x11_multiple_bet(
            self, id_selection=selection_ids, acca_bet_name='5 Fold Acca', section_index=0):
        """
        DESCRIPTION: Open Bet Slip and press on "Use Free Bet" link under multiple bet type from precondition.
        DESCRIPTION: E.g. If you have 0.10 free bet try to use it on 5 Fold Acca (x11) multiple bet
        EXPECTED: Free Bet pop up is shown with list of Free Bets available
        """
        self.open_betslip_with_selections(selection_ids=id_selection)
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        self.assertTrue(multiples_section, msg='Multiples section is not displayed.')
        self.__class__.acca_bet = multiples_section.ordered_collection.get(acca_bet_name)
        self.assertTrue(self.acca_bet, msg=f'Accumulator bet is not available')
        stake_name, self.__class__.stake = list(multiples_section.items())[section_index]
        self._logger.info('*** Verifying stake "%s"' % stake_name)

    def test_002_validate_that_not_eligible_free_bets_are_present_on_free_bets_popup(self):
        """
        DESCRIPTION: Validate that NOT eligible free bets are present on Free Bets popup
        EXPECTED: All Free Bets (eligible and not eligible) for selected bet are displayed
        """
        self.stake.use_free_bet_link.click()
        self.select_free_bet()
        self.assertEqual(self.stake.amount_form.input.value, '', msg='"Stake" input field should remain empty')

    def test_003__select_not_eligible_free_bet_tap_add_button(self):
        """
        DESCRIPTION: * Select NOT eligible free bet
        DESCRIPTION: * Tap 'Add' button
        EXPECTED: [From OX100.1]
        EXPECTED: * 'Free Bet Not Eligible' pop-up with 'Sorry, your free bet cannot be added.' text appears
        EXPECTED: * If [freebet value] / [lines number] is < 0.01 then this Free Bet(s) is not eligible
        EXPECTED: (e.g. if user has 0.10 free bet then it will NOT be available for multiple bets with x11 and more lines)
        EXPECTED: Ladbrokes Popup Design:
        EXPECTED: ![](index.php?/attachments/get/38723)
        """
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BET_NOT_ELIGIBLE, timeout=5,
                                                          verify_name=False)
        self.assertEqual(self.dialog.title, vec.dialogs.DIALOG_MANAGER_FREE_BET_NOT_ELIGIBLE,
                         msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BET_NOT_ELIGIBLE}" '
                             f'pop up is not shown')
        self.assertEqual(self.dialog.description, vec.betslip.FREE_BET_CAN_NOT_BE_ADDED,
                         msg=f'Actual description: "{self.dialog.description}" is not same as '
                             f'Expected description: "{vec.betslip.FREE_BET_CAN_NOT_BE_ADDED}"')

    def test_004_close_popup_by_tapping_ok_button(self):
        """
        DESCRIPTION: Close popup by tapping 'Ok' button
        EXPECTED: Pop up is closed
        """
        self.dialog.ok_button.click()
        self.assertFalse(self.dialog.title, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BET_NOT_ELIGIBLE}" '
                                                f' pop up is shown')

    def test_005_select_each_way_checkbox_first_under_multiple_bet_and_after_select_freebet_where_free_bet_value_less_than_001_eg_010_free_bet_for_double_x6_multiple_bet_0106_per_line_and_01062_per_line_for_ew(
            self):
        """
        DESCRIPTION: Select Each Way checkbox first under multiple bet and after select FreeBet where free bet value less than 0.01 (e.g. 0.10 free bet for Double (x6) multiple bet 0.10/6 per line and 0.10/6/2 per line for E/W)
        EXPECTED: [From OX100.1]
        EXPECTED:  'Free Bet Not Eligible' pop-up with 'Sorry, your free bet cannot be added.' text appears
        EXPECTED:  If [freebet value] / [lines number] is < 0.01 then this Free Bet(s) is not eligible
        EXPECTED: (e.g. if user has 0.10 free bet then it will NOT be available for multiple bets with x6 and more lines with E/W option checked)
        EXPECTED: Ladbrokes Popup Design:
        EXPECTED: ![](index.php?/attachments/get/38723)
        """
        self.clear_betslip()
        self.test_001_open_bet_slip_and_press_on_use_free_bet_link_under_multiple_bet_type_from_preconditioneg_if_you_have_010_free_bet_try_to_use_it_on_5_fold_acca_x11_multiple_bet(
            id_selection=self.selection_ids1, acca_bet_name='Double', section_index=1)
        each_way = self.acca_bet.has_each_way_checkbox()
        self.assertTrue(each_way, msg=f'Each Way checkbox is not present on stake "{self.acca_bet.name}"')
        self.acca_bet.each_way_checkbox.click()
        self.assertTrue(self.acca_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        self.test_002_validate_that_not_eligible_free_bets_are_present_on_free_bets_popup()
        self.test_003__select_not_eligible_free_bet_tap_add_button()

    def test_006_close_popup_by_tapping_ok_button(self):
        """
        DESCRIPTION: Close popup by tapping 'Ok' button
        EXPECTED: Pop up is closed
        EXPECTED: EW is checked, and free bet is not selected
        """
        self.test_004_close_popup_by_tapping_ok_button()
        self.assertTrue(self.acca_bet.each_way_checkbox.is_selected(), msg='Each Way is not selected')
        self.assertTrue(self.stake.use_free_bet_link, msg='free bet is selected')

    def test_007_verify_that_free_bet_not_eligible_is_displayed_when_selected_free_bet_becomes_not_eligible_after_ew_option_is_selectedadd_eligible_free_bet_to_multiple_bet_eg_010_on_double_x6_and_after_that_click_on_ew_checkbox(
            self):
        """
        DESCRIPTION: Verify that "Free Bet Not Eligible" is displayed when selected Free Bet becomes not eligible AFTER E/W option is selected.
        DESCRIPTION: Add eligible Free Bet to multiple bet (e.g. 0.10 on Double (x6)) and after that click on E/W checkbox.
        EXPECTED: Popup with message is displayed:
        EXPECTED: Heading: Free Bet Not Eligible
        EXPECTED: Text: Sorry, your free bet cannot be added.
        EXPECTED: Button: OK
        EXPECTED: When user taps on OK, popup is removed and EW is not checked, and free bet remains selected
        """
        self.acca_bet.each_way_checkbox.click()
        wait_for_result(lambda: not self.acca_bet.each_way_checkbox.is_selected(), timeout=10)
        self.assertFalse(self.acca_bet.each_way_checkbox.is_selected(), msg='Each Way is selected')
        self.test_002_validate_that_not_eligible_free_bets_are_present_on_free_bets_popup()
        self.assertTrue(self.stake.remove_free_bet_link, msg='free bet is selected')
        self.acca_bet.each_way_checkbox.click()
        wait_for_result(lambda: self.acca_bet.each_way_checkbox.is_selected(), timeout=10)
        self.test_003__select_not_eligible_free_bet_tap_add_button()
        self.test_004_close_popup_by_tapping_ok_button()
        self.assertFalse(self.acca_bet.each_way_checkbox.is_selected(), msg='Each Way is selected')
        self.assertTrue(self.stake.remove_free_bet_link, msg='free bet is selected')
