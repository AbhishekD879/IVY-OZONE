import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.iphone
@pytest.mark.betslip
@pytest.mark.numeric_keyboard
@pytest.mark.mobile_only
@pytest.mark.liveserv_updates
@pytest.mark.high
@vtest
class Test_C2351461_Verify_displaying_of_numeric_keyboard_while_LS_updates(BaseBetSlipTest):
    """
    TR_ID: C2351461
    VOL_ID: C9698227
    NAME: Verify displaying of numeric keyboard while LS updates
    DESCRIPTION: This test case verifies displaying of numeric keyboard while Live Serve updates
    PRECONDITIONS: - Oxygen application is loaded on Mobile device
    """
    keep_browser_open = True
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create football event in OpenBet
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team1 = event.team1
        self.__class__.selection_ids = event.selection_ids

    def test_001_add_one_selection_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add one selection to the Betslip > Open Betslip
        EXPECTED: Betslip is opened
        EXPECTED: One selection is available within Betslip
        EXPECTED: 'Stake' box is focused
        EXPECTED: Numeric keyboard is displayed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section.get(self.team1)
        self.assertTrue(self.stake, msg='"%s" stake was not found' % self.team1)
        self.stake.amount_form.input.click()

        self.assertTrue(self.stake.amount_form.is_active(), msg='Stake input field was not focused')

        self.assertTrue(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                        msg='Betslip keyboard is not shown')

    def test_002_in_ob_backoffice_trigger_suspension_for_a_selection_from_betslip(self):
        """
        DESCRIPTION: In OB Backoffice trigger suspension for a selection from Betslip
        EXPECTED: Selection is greyed out
        EXPECTED: Appropriate message for suspension is shown
        EXPECTED: Only Ladbrokes: Message for suspension is shown at the top of Betslip for 5s
        EXPECTED: 'Stake' box is NOT focused and 'Stake' is shown within box
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], active=False, displayed=True)

        self.assertFalse(self.stake.amount_form.input.is_enabled(timeout=60, expected_result=False),
                         msg='Amount field is not greyed out after price suspension')

        self.assertFalse(self.stake.amount_form.is_active(expected_result=False), msg='Stake input field was focused')

        self.assertTrue(self.stake.is_suspended(), msg='Stake is not suspended')

        placeholder = self.stake.amount_form.default_value
        self.assertEqual(placeholder, 'Stake', msg='Default input value "%s" != "Stake"' % placeholder)

        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown', timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden after price suspension')

    def test_003_in_ob_backoffice_trigger_return_selection_from_step_2_to_active_state(self):
        """
        DESCRIPTION: In OB Backoffice trigger return selection (from step 2) to active state
        EXPECTED: Selection become active
        EXPECTED: Appropriate message for suspension is NOT shown
        EXPECTED: 'Stake' box becomes focused and '<currency symbol>' is shown within box
        EXPECTED: Numeric keyboard is shown
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], active=True, displayed=True)

        self.assertTrue(self.stake.amount_form.input.is_enabled(timeout=30), msg='Amount field is not active')

        self.assertFalse(self.stake.is_suspended(expected_result=False), msg='Stake is still suspended')

    def test_004_in_ob_backoffice_trigger_price_change_for_a_selection_from_betslip(self):
        """
        DESCRIPTION: In OB Backoffice trigger price change for a selection from Betslip
        EXPECTED: Message for price change is shown above the selection
        EXPECTED: Warning message is shown at the bottom of Betslip
        EXPECTED: Only Ladbrokes: Message for Price change is shown at the top of Betslip for 5s
        EXPECTED: 'Stake' box remains focused and '<currency symbol>' is shown within box
        EXPECTED: Numeric keyboard is shown
        """
        new_price = '7/6'
        odds = self.stake.odds
        outcome_id = self.selection_ids[self.team1]
        self.ob_config.change_price(selection_id=outcome_id, price=new_price)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id, price=new_price)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.team1}" with id "{outcome_id}" is not received')

        general_error_msg = self.get_betslip_content().wait_for_warning_message()
        self.assertEqual(general_error_msg,
                         vec.betslip.PRICE_CHANGE_BANNER_MSG,
                         msg=f'Actual warning message {general_error_msg} does not match expected {vec.betslip.PRICE_CHANGE_BANNER_MSG}')
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.team1)
        error = stake.error_message
        expected_error = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(old=odds, new=new_price)
        self.assertEqual(error, expected_error,
                         msg=f'Received error "{error}" is not the same as expected "{expected_error}"')
        odds = self.stake.odds
        self.assertEqual(odds, new_price, msg='Price still "%s", it\'s not changed to "%s"' % (odds, new_price))

    def test_005_add_other_selections_to_the_betslip_open_betslip(self):
        """
        DESCRIPTION: Add other selections to the Betslip > Open Betslip
        EXPECTED: Betslip is opened
        EXPECTED: Added selections are available within Betslip
        EXPECTED: Numeric keyboard is NOT displayed
        """
        self.get_betslip_content().close_button.click()
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section.get('Draw')
        self.assertTrue(self.stake, msg='Draw" stake was not found')
        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')

    def test_006_set_focus_on_any_stake_field(self):
        """
        DESCRIPTION: Set focus on any 'Stake' field
        EXPECTED: 'Stake' box becomes focused and '<currency symbol>' is shown within box
        EXPECTED: Numeric keyboard is shown above 'BET NOW'/LOG IN & BET' button
        """
        self.stake.amount_form.input.click()
        self.assertTrue(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                        msg='Betslip keyboard is not shown')

    def test_007_in_ob_backoffice_trigger_suspension_for_a_selection_with_focused_stake_field_from_step_6_from_betslip(self):
        """
        DESCRIPTION: In OB Backoffice trigger suspension for a selection with focused 'Stake' field (from step 6) from Betslip
        EXPECTED: Selection is greyed out
        EXPECTED: Appropriate message for suspension is shown
        EXPECTED: Only Ladbrokes: Message for suspension is shown at the top of Betslip for 5s
        EXPECTED: 'Stake' box is NOT focused and 'Stake' is shown within box
        EXPECTED: Numeric keyboard is NOT displayed
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids['Draw'], active=False, displayed=True)

        self.assertFalse(self.stake.amount_form.input.is_enabled(timeout=60, expected_result=False),
                         msg='Amount field is not greyed out after price suspension')
        self.assertFalse(self.stake.amount_form.is_active(expected_result=False), msg='Stake input field was focused')

        self.assertTrue(self.stake.is_suspended(), msg='Stake is not suspended')

        placeholder = self.stake.amount_form.default_value
        self.assertEqual(placeholder, 'Stake', msg='Default input value "%s" != "Stake"' % placeholder)

        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard is not hidden',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')

    def test_008_in_ob_backoffice_trigger_return_selection_from_step_6_to_active_state(self):
        """
        DESCRIPTION: In OB Backoffice trigger return selection (from step 6) to active state
        EXPECTED: Previously selected 'Stake' box is no longer focused
        EXPECTED: Numeric keyboard does not appear
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids['Draw'], active=True, displayed=True)

        self.assertTrue(self.stake.amount_form.input.is_enabled(timeout=30), msg='Amount field is not active')
        self.assertFalse(self.stake.amount_form.is_active(expected_result=False), msg='Stake input field is focused')

        self.assertFalse(self.stake.is_suspended(expected_result=False), msg='Stake is still suspended')

        self.assertFalse(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown',
                                                                          timeout=3, expected_result=False),
                         msg='Betslip keyboard is not hidden')

    def test_009_set_focus_on_any_stake_field(self):
        """
        DESCRIPTION: Set focus on any 'Stake' field
        EXPECTED: 'Stake' box becomes focused and '<currency symbol>' is shown within box
        EXPECTED: Numeric keyboard is shown above 'BET NOW'/LOG IN & BET' button
        """
        self.test_006_set_focus_on_any_stake_field()

    def test_010_in_ob_backoffice_trigger_price_change_for_a_selection_with_focused_stake_box_from_step_9(self):
        """
        DESCRIPTION: In OB Backoffice trigger price change for a selection with focused 'Stake' box (from step 9)
        EXPECTED: Message for price change is shown above the selection
        EXPECTED: Warning message is shown at the bottom of Betslip
        EXPECTED: Only Ladbrokes: Message for Price change is shown at the top of Betslip for 5s
        EXPECTED: 'Stake' box remains focused and '<currency symbol>' is shown within box
        EXPECTED: Numeric keyboard is shown
        """
        new_price = '6/13'
        outcome_id = self.selection_ids['Draw']
        odds = self.stake.odds
        self.ob_config.change_price(selection_id=outcome_id, price=new_price)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id, price=new_price)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "Draw" with id "{outcome_id}" is not received')

        general_error_msg = self.get_betslip_content().wait_for_warning_message()
        self.assertEqual(general_error_msg,
                         vec.betslip.PRICE_CHANGE_BANNER_MSG,
                         msg=f'Actual warning message {general_error_msg} does not match expected {vec.betslip.PRICE_CHANGE_BANNER_MSG}')
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get('Draw')
        error = stake.error_message
        expected_error = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(old=odds, new=new_price)
        self.assertEqual(error, expected_error,
                         msg=f'Received error "{error}" is not the same as expected "{expected_error}"')

        odds = self.stake.odds
        self.assertEqual(odds, new_price, msg='Price still "%s", it\'s not changed to "%s"' % (odds, new_price))

        self.assertTrue(self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                        msg='Betslip keyboard is not shown')
