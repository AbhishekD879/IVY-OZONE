import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.reg156_fix
@pytest.mark.other
@vtest
class Test_C14294008_TO_BE_EDITEDVanilla__Betslip__GVC_iFrame_appearance(BaseBetSlipTest):
    """
    TR_ID: C14294008
    NAME: [TO BE EDITED][Vanilla] - Betslip - GVC iFrame appearance
    DESCRIPTION: This TC will check the appearance of GVC iFrame
    PRECONDITIONS: * User logged in App
    PRECONDITIONS: * **NOTE** Netteller is NOT supported anymore - check this case with other card ( User has payment method set (for Vanilla use  Netteller Card:  Account ID: Any 12 Digit Number, Secure / Authentication Code: Any 6 Digit Number);
    PRECONDITIONS: * User has balance that is > 0
    """
    keep_browser_open = True
    additional_amount = 5

    def test_001_select_any_desired_event(self):
        """
        DESCRIPTION: Select any desired event;
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self._logger.debug(f'*** Found Football event "{event}"')
            self.__class__.eventID = event['event']['id']
        else:
            self.__class__.eventID = self.ob_config.add_autotest_premier_league_football_event().event_id

        self.site.login(username=tests.settings.quick_deposit_user)
        self.site.wait_content_state('homepage')
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_add_1_selection_to_the_betslip_click_on_add_to_the_betslip_on_quick_bet_pop_up_if_accessing_from_mobile(
            self):
        """
        DESCRIPTION: Add 1 selection to the betslip (click on 'Add to the Betslip' on "Quick Bet" pop up if accessing from mobile);
        EXPECTED: Selection is added;
        """
        self.navigate_to_edp(event_id=self.eventID)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg=f'No one market section found')
        if self.device_type == 'desktop' or self.brand == 'ladbrokes':
            market = markets.get(self.expected_market_sections.match_result.title())
        else:
            market = markets.get(self.expected_market_sections.match_result.upper())
        self.assertTrue(market, msg='Can not find Match Result section')
        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section')
        outcome = list(outcomes.values())[0]
        self.__class__.first_selection_name = list(outcomes.keys())[0]
        outcome.click()

        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=15), msg='Quick Bet is not shown')
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
            self.verify_betslip_counter_change(expected_value=1)
            self.site.open_betslip()

    def test_003_navigate_to_betslip_view_via_a_click_on_betslip_button_in_vanilla_header(self):
        """
        DESCRIPTION: Navigate to Betslip view (via a click on 'Betslip' button in Vanilla Header);
        EXPECTED: Betslip is opened;
        """
        result = self.get_betslip_content()
        self.assertTrue(result, msg='Betslip widget not displayed')

    def test_004_make_a_stake_that_is_less_than_user_balance__stake__user_balance_check_that_place_bet__button_is_active(
            self):
        """
        DESCRIPTION: Make a stake that is less than User balance _(stake < User balance)_;
        DESCRIPTION: Check that 'Place Bet'  button is active;
        EXPECTED: 'Place Bet' button is activated (changed color from greyed out to green);
        """
        section = self.get_betslip_sections().Singles
        stake_name, stake = list(section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        self.assertGreater(str(self.user_balance), stake.amount_form.input.value,
                           msg=f'User Balance  "{str(self.user_balance)}" is not greater than stake "{stake.amount_form.input.value}"')
        betnow_btn = self.get_betslip_content().bet_now_button
        self.assertTrue(betnow_btn.is_enabled(expected_result=True), msg='Bet Now button is disabled')
        self.assertEqual(betnow_btn.background_color_value, vec.colors.PLACE_BET_BUTTON,
                         msg=f'Selected price/odds for "{betnow_btn.background_color_value}" is not highlighted in '
                             f'green {vec.colors.PLACE_BET_BUTTON}')

    def test_005_make_stake_bigger_than_user_balance__stake__user_balance_check_that_place_bet__button_is_changed_to_make_a_deposit_button(
            self):
        """
        DESCRIPTION: Make Stake bigger than User balance _(stake > User balance)_;
        DESCRIPTION: Check that 'Place Bet'  button is changed to 'Make a Deposit' button;
        EXPECTED: * __'Place Bet'__ button is changed to 'Make a Deposit' after rising stake to bigger than User balance;
        """
        stake_value = self.user_balance + self.additional_amount
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        stake_bet_amounts = {
            stake_name: stake_value,
        }
        self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts=stake_bet_amounts)
        info_panel_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(self.additional_amount)
        self.assertEqual(info_panel_text, expected_message_text,
                         msg=f'Error message "{info_panel_text}" is not the same as expected "{expected_message_text}"')
        self.assertTrue(self.get_betslip_content().has_make_quick_deposit_button(timeout=20),
                        msg='"Make a Quick Deposit" button is not displayed')
        make_quick_deposit_button_name = self.get_betslip_content().make_quick_deposit_button.name
        self.assertEqual(make_quick_deposit_button_name, vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN,
                         msg=f'Actual message "{make_quick_deposit_button_name}" != '
                             f'Expected "{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}"')
        self.assertTrue(self.get_betslip_content().make_quick_deposit_button.is_enabled(),
                        msg=f'"{vec.betslip.BETSLIP_MAKE_QUICK_DEPOSIT_BTN}" button is disabled')

    def test_006_tap_on_make_a_deposit_buttonobserve_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap on 'Make a Deposit' button;
        DESCRIPTION: Observe 'Make a Deposit' button
        EXPECTED: Spinner and 'Make a Deposit' text is displayed on the 'Make a Deposit' button
        EXPECTED: 'Quick Deposit' iFrame overlay appears with available payment methods set for User;
        """
        self.get_betslip_content().make_quick_deposit_button.click()
        self.site.wait_content_state_changed(timeout=30)
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='Quick Deposit is not displayed')

    def test_007_add_one_more_selection_to_the_betslip_from_step_1(self):
        """
        DESCRIPTION: Add One more selection to the betslip from step 1;
        EXPECTED: One more selection is added and betslip contains 2 selections;
        """
        self.navigate_to_edp(event_id=self.eventID)
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg=f'No one market section found')
        if self.device_type == 'desktop' or self.brand == 'ladbrokes':
            market = markets.get(self.expected_market_sections.match_result.title())
        else:
            market = markets.get(self.expected_market_sections.match_result.upper())
        self.assertTrue(market, msg='Can not find Match Result section')
        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No one outcome was found in section')
        outcome = list(outcomes.values())[1]
        self.__class__.second_selection_name = list(outcomes.keys())[1]
        outcome.click()
        self.verify_betslip_counter_change(expected_value=2)
        self.site.header.bet_slip_counter.click()

    def test_008_place_a_stake_that_is__bigger_than_user_balance_amount_stake__user_balancecheck_that_that_quick_deposit_overlay_is_displayed_for_betslip_with_several_selections(
            self):
        """
        DESCRIPTION: Place a stake that is  bigger than User balance amount (stake > User balance);
        DESCRIPTION: Check that that 'Quick Deposit' overlay is displayed for betslip with several selections;
        EXPECTED: 'Quick Deposit' iFrame overlay is displayed with available payment methods set for User;
        """
        stake_value = self.user_balance + self.additional_amount
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        stake_bet_amounts = {
            stake_name: stake_value,
        }
        self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts=stake_bet_amounts)
        info_panel_text = self.get_betslip_content().bet_amount_warning_message
        expected_message_text = vec.betslip.BETSLIP_DEPOSIT_NOTIFICATION.format(self.additional_amount)
        self.assertEqual(info_panel_text, expected_message_text,
                         msg=f'Error message "{info_panel_text}" is not the same as expected "{expected_message_text}"')
        self.get_betslip_content().make_quick_deposit_button.click()
        self.site.wait_content_state_changed(timeout=30)
        self.assertTrue(self.get_betslip_content().has_deposit_form(), msg='Quick Deposit is not displayed')

    def test_009_check_that_quick_deposit_overlay_can_be_closed_via_x_button(self):
        """
        DESCRIPTION: Check that 'Quick Deposit' overlay can be closed via 'X' button;
        EXPECTED: Overlay is closed and User can see previously opened betslip;
        """
        self.__class__.quick_deposit = self.site.betslip.quick_deposit.stick_to_iframe()
        self.quick_deposit.switch_to_main_page()
        self.site.betslip.quick_deposit.header.close_button.click()

    def test_010_check_that_betslip_contains_all_previously_added_selections_after_closing_the_quick_deposit_overlay__the_warning_message_displayed(
            self):
        """
        DESCRIPTION: Check that betslip contains all previously added selections after closing the "Quick Deposit" overlay & the warning message displayed.
        EXPECTED: All selections are present in the opened betslip & the warning message displayed;
        """
        self.assertTrue(self.get_betslip_content(),
                        msg='Betslip widget was not opened')
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No one added selection found on Betslip')
        singles_section_list = [i.upper() for i in singles_section.keys()]
        self.assertIn(self.first_selection_name,
                      (singles_section_list if self.brand == 'ladbrokes' else singles_section),
                      msg=f'Actual list "{singles_section.keys()}" does not contain Added selection "{self.first_selection_name}"')
        self.assertIn(self.second_selection_name,
                      (singles_section_list if self.brand == 'ladbrokes' else singles_section),
                      msg=f'Actual list "{singles_section.keys()}" does not contain Added selection "{self.second_selection_name}"')

        actual_message = self.get_betslip_content().bet_amount_warning_message
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(self.additional_amount)
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" is not the same as expected "{expected_message}"')

    def test_011_check_that_iframe_overlay_is_resizablenavigate_to_deposit_amount_field_on_quick_deposit_overlayclick_on_deposit_amount_fieldcheck_that_digital_keyboard_is_displayed_only_for_mobile_tablet(
            self):
        """
        DESCRIPTION: Check that iFrame Overlay is resizable:
        DESCRIPTION: Navigate to "Deposit Amount" field on "Quick Deposit" overlay;
        DESCRIPTION: Click on "Deposit Amount" field;
        DESCRIPTION: Check that Digital keyboard is displayed (only for mobile, tablet);
        EXPECTED: Keyboard is displayed;
        EXPECTED: Overlay is resized after Keyboard appeared;
        EXPECTED: No scrollbars were displayed; (for small screens on Android scrollbar is displayed)
        """
        # cannot verify if scroll bar is there or not.
        # QD iFrame Overlay resizable is Only for manual testing
        if self.device_type == 'mobile':
            self.get_betslip_content().make_quick_deposit_button.click()
            self.__class__.quick_deposit = self.site.betslip.quick_deposit.stick_to_iframe()
            self.quick_deposit.amount.input.click()
            self.assertTrue(self.quick_deposit.keyboard.is_enabled(),
                            msg='Numeric keyboard is not opened')
