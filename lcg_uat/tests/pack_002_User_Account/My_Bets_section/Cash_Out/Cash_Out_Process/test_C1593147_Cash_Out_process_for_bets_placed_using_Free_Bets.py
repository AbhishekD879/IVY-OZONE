import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can't grant freebets on prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.bet_placement
@pytest.mark.freebets
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C1593147_Cash_Out_Process_for_bets_placed_using_Free_Bets(BaseCashOutTest):
    """
    TR_ID: C1593147
    NAME: Cash Out Process for bets placed using Free Bets
    DESCRIPTION: This test case verifies Cashout process for bets placed using Free Bets
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event
        DESCRIPTION: Login as user that have Freebets available
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        local_start_time = self.convert_time_to_local(date_time_str=event.event_date_time)

        self.__class__.event_name = f'{event.team1} v {event.team2} {local_start_time}'
        self.__class__.selection_ids = event.selection_ids

        username = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=username)
        self.site.login(username=username)
        self.assertTrue(self.site.header.has_freebets(), msg='User does not have Free bets')

    def test_001_add_selection_to_betslip_and_select_free_bet_from_free_bets_available_drop_down(self):
        """
        DESCRIPTION: Select an event with available Cashout
        DESCRIPTION: Add selection  from this event to the Betslip and select Free Bet from 'Free Bets Available' drop-down
        EXPECTED: Free bet offer is selected
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids['Draw'])

    def test_002_place_bet_using_selected_free_bet(self):
        """
        DESCRIPTION: Place Bet using selected Free Bet
        EXPECTED: Bet is placed successfully
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self._logger.info(f'*** Verifying stake "{stake_name}"')
        self.assertTrue(stake.has_use_free_bet_link(), msg='"Has Use Free Bet" link was not found')

        if stake.freebet_tooltip is not None:
            stake.freebet_tooltip.click()
        stake.use_free_bet_link.click()

        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, verify_name=False)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" has not appeared')

        dialog.select_first_free_bet()
        self.assertTrue(dialog.wait_dialog_closed(), msg=f'{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} was not closed')

        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_003_go_to_cashout_section_and_verify_placed_bet_displaying(self):
        """
        DESCRIPTION: Go to Cashout section and verify placed bet displaying
        EXPECTED: 1. Placed Bet is displayed in Cashout section
        EXPECTED: 2. Only full Cashout is available for the Bet
        """
        self.site.open_my_bets_cashout()
        self.__class__.bet_name, self.__class__.bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
        self.assertTrue(self.bet, msg=f'Bet "{self.bet_name}" is not displayed')
        self.assertFalse(self.bet.buttons_panel.has_partial_cashout_button(expected_result=False),
                         msg='"PARTIAL CASHOUT" button is present')
        self.assertTrue(self.bet.buttons_panel.has_full_cashout_button(), msg='"FULL CASHOUT" button is not present')

    def test_004_tap_cashout_button(self):
        """
        DESCRIPTION: Tap 'Cashout' button.
        DESCRIPTION: Verify that cashout process is successfully completed
        EXPECTED: Cashout process is successfully completed
        """
        self.bet.buttons_panel.full_cashout_button.click()
        self.bet.buttons_panel.cashout_button.click()

        expected_message = vec.bet_history.FULL_CASH_OUT_SUCCESS
        self.assertTrue(self.bet.wait_for_message(message=expected_message, timeout=30),
                        msg=f'Message: "{expected_message}" is not shown')
