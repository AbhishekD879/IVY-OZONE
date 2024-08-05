import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898469_Multiple_HR_bet_rejected_by_the_trader(BaseBetSlipTest):
    """
    TR_ID: C59898469
    NAME: Multiple HR bet rejected by the trader
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1
    max_mult_bet = 0.3
    prices = [{0: '1/12'}, {0: '1/11'}]
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events for HR
        """
        for i in range(2):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices[i],
                                                              max_bet=self.max_bet, max_mult_bet=self.max_mult_bet)
            self.__class__.event_name = event_params.ss_response['event']['name']
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_add_mutliple_hr_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add mutliple HR selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_multiple_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_reject_the_multiple_bet_in_ob_ti_tool(self):
        """
        DESCRIPTION: Reject the multiple bet in OB TI Tool
        EXPECTED: Customer sees a Trader has not accepted the bet message in betslip. No bet should be seen in My Bets and Account History
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self.bet_intercept.decline_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.site.wait_content_state_changed(timeout=15)
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        section = list(betreceipt_sections.values())[0]
        overask_warning_message = section.multiple_declined_bet.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual message "{overask_warning_message}" is not same as'
                             f'Expected message "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

        if self.device_type == 'mobile':
            self.navigate_to_page('homepage')
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE)
