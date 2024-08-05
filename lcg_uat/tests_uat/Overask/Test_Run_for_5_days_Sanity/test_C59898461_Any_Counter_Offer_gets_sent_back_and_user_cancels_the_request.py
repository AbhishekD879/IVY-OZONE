import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C59898461_Any_Counter_Offer_gets_sent_back_and_user_cancels_the_request(BaseBetSlipTest):
    """
    TR_ID: C59898461
    NAME: Any Counter Offer gets sent back and user cancels the request
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1
    suggested_max_bet = 0.25
    prices = {0: '1/12'}

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

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
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

    def test_002_counter_offer_by_stakeprice(self):
        """
        DESCRIPTION: Counter Offer by Stake/Price
        EXPECTED: Counter offer gets sent back
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

    def test_003_cancel_the_offer(self):
        """
        DESCRIPTION: Cancel the Offer
        EXPECTED: Counter offer is completely exited(Selection shouldn't be seen and betslip should be empty)
        """
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.site.open_betslip()
        self.assertEqual(self.get_betslip_content().no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual message: "{self.get_betslip_content().no_selections_title}" is not same as '
                             f'Expected message: "{vec.betslip.NO_SELECTIONS_TITLE}"')
