import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.open_bets
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870292__Any_Counter_Offer_gets_sent_back_and_user_cancels_the_request(BaseBetSlipTest):
    """
    TR_ID: C44870292
    NAME: - Any Counter Offer gets sent back and user cancels the request
    """
    keep_browser_open = True
    max_bet = 0.2
    suggested_max_bet = 0.25
    prices = {0: '1/12', 1: '1/11', 2: '1/9'}

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices, max_bet=self.max_bet)
        self.__class__.runner_name = list(event_params.selection_ids.keys())[0]
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_an_oa_bet_and_give_any_type_of_counter_offer_in_the_ti(self):
        """
        DESCRIPTION: Place an OA bet and give any type of counter offer in the TI
        EXPECTED: The trader should have given a counter offer
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)

    def test_002_in_the_front_end_you_should_see_a_counter_offer(self):
        """
        DESCRIPTION: In the Front End, you should see a counter offer
        EXPECTED: You should see a counter offer
        """
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask is not closed')
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

    def test_003_click_on_the_cancel_button_in_the_counter_offer(self):
        """
        DESCRIPTION: Click on the Cancel button in the counter offer
        EXPECTED: The counter offer should have closed
        """
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()

    def test_004_verify_that_the_bet_has_not_been_placed_by_looking_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Verify that the bet has not been placed by looking in My Bets->Open Bets
        EXPECTED: The bet should not show up in My Bets->Open Bets
        """
        self.site.open_my_bets_open_bets()
        try:
            open_bets = self.site.open_bets.tab_content.accordions_list.get_bet(
                bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.runner_name)
            self.assertFalse(open_bets, msg='Cancelled bet is present in "Open bets" tab')
        except Exception as e:
            self._logger.info(e)
