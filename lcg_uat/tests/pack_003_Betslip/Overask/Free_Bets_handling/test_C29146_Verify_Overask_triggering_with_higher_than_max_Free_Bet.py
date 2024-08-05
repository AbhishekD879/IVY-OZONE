import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from random import uniform


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.freebets
@pytest.mark.max_min_bet
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29146_Verify_Overask_triggering_with_higher_than_max_Free_Bet(BaseBetSlipTest):
    """
    TR_ID: C29146
    NAME: Verify Overask triggering with higher than max Free Bet
    DESCRIPTION: This test case verifies that freebet gets unselected if it was selected before Overask was triggered
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with bet limit 0.5
        """
        self.__class__.username = tests.settings.freebet_user
        free_bet_value = f'{uniform(1, 2):.2f}'
        self.ob_config.grant_freebet(username=self.username, freebet_value=free_bet_value)
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=0.5)
        self.__class__.eventID, self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event_params.event_id, event_params.team1, event_params.team2, event_params.selection_ids

        self.__class__.created_event_name = self.team1 + ' v ' + self.team2

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.site.login(username=self.username)
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_002_select_free_bet_with_value_which_is_higher_then_maximum_limit_for_added_selection(self):
        """
        DESCRIPTION: Select Free bet with value which is higher then maximum limit for added selection
        """
        # covered in next step

    def test_003_tap_bet_nowplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now'/'Place bet' (From OX 99) button
        EXPECTED: Overask is triggered for the User
        EXPECTED: The bet review notification/(overlay from OX 99)is shown to the User
        """
        self.place_single_bet(number_of_stakes=1, freebet=True)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask excedds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

    def test_004_trigger_stake_modification_by_trader_and_verify_betslip_displaying(self):
        """
        DESCRIPTION: Trigger Stake modification by Trader and verify betslip displaying
        EXPECTED: Info message is displayed above 'Bet Now' button with text: 'Freebet cannot be used with this bet.'
        EXPECTED: Stake field is cleared.
        EXPECTED: Free Bet value is unselected in dropdown.
        EXPECTED: 'Bet Now' button is enabled and displayed.
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(
            username=self.username,
            event_id=self.eventID
        )
        self._logger.debug(f'*** Bet id {bet_id}, betslip id {betslip_id}')
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id, betslip_id=betslip_id, max_bet='0.5')

        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False)
        self.assertFalse(overask, msg='Overask panel is not hidden')

        singles_section = self.get_betslip_sections().Singles
        for stake_name, stake in singles_section.items():
            self.assertEqual(stake.amount_form.input.value, '', msg='"Stake" input field should remain empty')
            self.assertTrue(stake.has_use_free_bet_link(), msg='Freebet selector is not present')

        self.get_betslip_content().wait_for_overask_message_to_change()
        overask_warning_message = self.get_betslip_content().overask_warning
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.some_bets_with_freebet,
                         msg=f'Actual message "{overask_warning_message}" does not match expected "{vec.betslip.OVERASK_MESSAGES.some_bets_with_freebet}"')
        betnow_btn = self.get_betslip_content().bet_now_button
        self.assertFalse(betnow_btn.is_enabled(expected_result=False), msg='Bet Now button is not disabled')

    def test_005_enter_some_stake_value_less_than_max_allowed_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter some stake value less than max allowed
        EXPECTED: Stake appears in stake box
        EXPECTED: Tap 'Bet Now' button
        EXPECTED: The bet is placed as per normal process
        """
        self.__class__.bet_amount = 0.01
        self.place_single_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

    def test_006_add_few_selections_to_the_betslip_and_for_one_of_them_select_free_bet_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them select free bet value which will trigger Overask for the selection
        EXPECTED:
        """
        self.site.bet_receipt.footer.click_done()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1], self.selection_ids[self.team2]))

    def test_007_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps 2-5
        EXPECTED: Bets can not be placed using higher than max allowed free bet value.
        """
        self.test_002_select_free_bet_with_value_which_is_higher_then_maximum_limit_for_added_selection()
        self.test_003_tap_bet_nowplace_bet_from_ox_99_button()
        self.test_004_trigger_stake_modification_by_trader_and_verify_betslip_displaying()
        self.test_005_enter_some_stake_value_less_than_max_allowed_and_tap_bet_now_button()
