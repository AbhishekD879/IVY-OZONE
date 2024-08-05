import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.medium
@vtest
class Test_C59898485_Customer_logs_out_after_receiving_offer_desktop_only_scenario(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C59898485
    NAME: Customer logs out after receiving offer (desktop only scenario)
    """
    keep_browser_open = True
    max_bet = 1
    bet_amount = 2
    device_name = tests.desktop_default

    def validate_no_bets_on_betslip(self):
        message = self.betslip.no_selections_title
        self.assertEqual(message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'"{message}" is not same as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        """
        event_params = self.ob_config.add_UK_racing_event(max_bet=self.max_bet, number_of_runners=1)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.eventID = event_params.event_id
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(username=self.username, amount=tests.settings.min_deposit_amount)
        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.wait_content_state('Homepage')

    def test_001_add_a_selection_to_bet_slip_and_trigger_overask(self):
        """
        DESCRIPTION: Add a selection to bet slip and trigger Overask
        EXPECTED: You bet should have gone to the Overask flow
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet()
        self.assertTrue(self.get_betslip_content().wait_for_overask_panel(), msg='Overask is not shown')

    def test_002_in_the_ti_give_any_type_of_counter_offer(self):
        """
        DESCRIPTION: In the TI, give any type of counter offer
        EXPECTED: You should have given a counter offer and should see the counter offer on the front end
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')
        self.bet_intercept.offer_max_bet(bet_id=bet_id, betslip_id=betslip_id)
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        actual_stake_value = float(self.stake.offered_stake.name.strip('£'))
        self.assertLess(actual_stake_value, float(self.bet_amount),
                        msg=f'New stake value: "{actual_stake_value}" '
                            f'is not as expected: "{self.bet_amount}"')

    def test_003_log_out_and_verify_that_you_do_not_see_the_counter_offer_anymore(self):
        """
        DESCRIPTION: Log out and verify that you do not see the counter offer anymore
        EXPECTED: You should not see the counter offer anymore and betslip should be cleared
        """
        self.site.logout(timeout=10)
        self.__class__.betslip = self.get_betslip_content()
        self.validate_no_bets_on_betslip()

    def test_004_login_in_back_with_login_button_in_the_header(self):
        """
        DESCRIPTION: Login In back with Login button in the header.
        EXPECTED: User should see empty betslip
        """
        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.wait_content_state('Homepage')
        self.validate_no_bets_on_betslip()
