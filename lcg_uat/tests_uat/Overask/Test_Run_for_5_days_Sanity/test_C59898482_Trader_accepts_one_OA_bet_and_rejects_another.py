import pytest
import voltron.environments.constants as vec
from collections import defaultdict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898482_Trader_accepts_one_OA_bet_and_rejects_another(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C59898482
    NAME: Trader accepts one OA bet and rejects another
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 0.2
    max_mult_bet = 0.3
    prices = {0: '1/20'}
    selections = []
    events = []

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp_prices=self.prices, max_bet=self.max_bet,
                                                                                 max_mult_bet=self.max_mult_bet)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'
        event_params1 = self.ob_config.add_autotest_premier_league_football_event(lp_prices=self.prices, max_bet=self.max_bet,
                                                                                  max_mult_bet=self.max_mult_bet)
        self.__class__.eventID1, selection_ids1 = event_params1.event_id, event_params1.selection_ids
        self.__class__.selection_id1 = list(selection_ids1.values())[0]
        self.__class__.event_name1 = f'{event_params1.team1} v {event_params1.team2}'
        self.selections.append(self.selection_id)
        self.selections.append(self.selection_id1)
        self.events.append(self.eventID)
        self.events.append(self.eventID1)
        self.site.login()

    def test_001_add_two_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.open_betslip_with_selections(selection_ids=self.selections)
        self.__class__.bet_amount = self.max_mult_bet + 0.1
        self.place_single_bet(number_of_stakes=2)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_accepts_one_oa_bet_and_reject_another_in_ob_ti(self):
        """
        DESCRIPTION: Accepts one OA bet and reject another in OB TI
        EXPECTED: Customer should see bet receipt showing that one bet was placed and the other was not - message showing "Trader did not accept the bet".
        EXPECTED: Only the accepted bet should be seen in both My Bets and Account History.
        """
        bets_details = \
            self.bet_intercept.find_bets_for_review(events_id=self.events)
        acct_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        flag = False
        data = defaultdict(dict)
        for bet_id, bet_type in bets_details.items():
            if not flag and bet_type == 'SGL':
                data['bet1']['id'] = bet_id
                data['bet1']['action'] = 'A'
                data['bet1']['bettype'] = bet_type
                flag = True
            elif bet_type == 'SGL' and flag:
                data['bet2']['id'] = bet_id
                data['bet2']['action'] = 'D'
                data['bet2']['bettype'] = bet_type
        self.bet_intercept.multiple_actions_bets(acct_id=acct_id, betslip_id=betslip_id, bets_details=data)
        self.check_bet_receipt_is_displayed()
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        _, section = list(betreceipt_sections.items())[0]
        overask_warning_message = section.declined_bet.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual overask warning message: "{overask_warning_message}" is not equal '
                             f'to expected: "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                     event_name=self.event_name)
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                     event_name=self.event_name1, bet_in_open_bets=False)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                     event_name=self.event_name)
        self.verify_bet_in_open_bets(bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE,
                                     event_name=self.event_name1, bet_in_open_bets=False)
