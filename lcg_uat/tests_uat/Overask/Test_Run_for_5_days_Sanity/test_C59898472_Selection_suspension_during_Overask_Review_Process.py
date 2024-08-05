import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.overask
@pytest.mark.betslip
@vtest
class Test_C59898472_Selection_suspension_during_Overask_Review_Process(BaseBetSlipTest):
    """
    TR_ID: C59898472
    NAME: Selection suspension during Overask Review Process
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1
    suggested_max_bet = 1.5
    bir_delay = 30

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
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
        self.__class__.bet_amount = self.max_bet + 1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_openbet_suspend_the_selection(self):
        """
        DESCRIPTION: In Openbet, suspend the Selection
        EXPECTED: Suspension message is seen in betslip
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        self.device.refresh_page()
        self.site.open_betslip()
        sections = self.get_betslip_sections().Singles
        stake = list(sections.values())[0]
        result = wait_for_result(lambda: stake.suspended_stake_label, name='SUSPENDED label to appear',
                                 timeout=self.bir_delay)
        self.assertEqual(result.strip('"'), vec.betslip.SUSPENDED_LABEL,
                         msg=f'"{vec.betslip.SUSPENDED_LABEL}" does not appear Actual content "{result}"')

    def test_003_in_ti_give_a_counter_offer(self):
        """
        DESCRIPTION: In TI, give a counter offer
        EXPECTED: Customer should see a bet not accepted by trader message
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet, bet_status_suspended=True)
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        _, section = list(betreceipt_sections.items())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual overask warning message: "{overask_warning_message}" is not equal '
                             f'to expected: "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')
