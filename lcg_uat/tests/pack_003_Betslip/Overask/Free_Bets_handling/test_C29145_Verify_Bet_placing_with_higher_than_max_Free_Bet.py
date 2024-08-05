import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from random import uniform


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.max_min_bet
@pytest.mark.freebets
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29145_Verify_Bet_placing_with_higher_than_max_Free_Bet(BaseBetSlipTest):
    """
    TR_ID: C29145
    NAME: Verify Bet placing with higher than max Free Bet
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event with bet limit 0.5
        """
        free_bet_value_1, free_bet_value_2 = f'{uniform(1, 2):.2f}', f'{uniform(2, 3):.2f}'
        self.__class__.username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=self.username, freebet_value=free_bet_value_1)
        self.ob_config.grant_freebet(username=self.username, freebet_value=free_bet_value_2)
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=0.5)
        self.__class__.eventID, self.__class__.team1, self.__class__.selection_ids \
            = event_params.event_id, event_params.team1, event_params.selection_ids

    def test_001_add_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip
        EXPECTED: Selection is successfully added. Free bet dropdown is available and active.
        """
        self.site.login(username=self.username)
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_002_select_free_bet_which_is_higher_than_max_allowed_and_tap_place_a_bet_button(self):
        """
        DESCRIPTION: Select free bet which is higher than max allowed
        """
        self.place_single_bet(freebet=True)

    def test_003_tap_bet_nowplace_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now'/'Place bet' (From OX 99) button
        EXPECTED: Overask is triggered for the User
        EXPECTED: The bet review notification is shown to the User
        """
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask exceeds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

    def test_004_trigger_stake_confirmation_by_trader_and_verify_betslip_displaying(self):
        """
        DESCRIPTION: Trigger Stake confirmation by Trader and verify Betslip displaying
        EXPECTED: Bet is placed
        EXPECTED: Bet receipt is shown to user
        EXPECTED: 'Go Betting' button is present and enabled
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)

        self.check_bet_receipt_is_displayed(timeout=20)

        bet_receipt_footer = self.site.bet_receipt.footer
        self.assertTrue(bet_receipt_footer.done_button.is_displayed(), msg='"Done" button is not displayed')
        self.assertTrue(bet_receipt_footer.done_button.is_enabled(), msg='"Done" button is not enabled')

    def test_005_tap__go_betting(self):
        """
        DESCRIPTION: Tap 'Done'/'Go Betting'(From OX 99) button
        EXPECTED: Betslip is cleared and closed
        """
        self.site.bet_receipt.footer.click_done()

    def test_006_add_few_selections_to_the_betslip_and_for_one_of_them_select_free_bet_with_stake_value_which_will_trigger_overask_for_the_selection(self):
        """
        DESCRIPTION: Add few selections to the Betslip and for one of them select free bet with stake value which will trigger Overask for the selection
        EXPECTED:
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values()))

    def test_007_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 'Go Betting' button is present and enabled
        """
        self.place_single_bet(number_of_stakes=1, freebet=True)

        self.test_003_tap_bet_nowplace_bet_from_ox_99_button()

        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)

        self.check_bet_receipt_is_displayed()

        self.assertTrue(self.site.bet_receipt.footer.done_button.is_displayed(), msg='"Done" button is not displayed')
