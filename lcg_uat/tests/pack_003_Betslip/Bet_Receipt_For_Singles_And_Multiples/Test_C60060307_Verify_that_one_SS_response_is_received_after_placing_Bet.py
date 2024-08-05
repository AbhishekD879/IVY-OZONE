import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C60060307_Verify_that_one_SS_response_is_received_after_placing_Bet(BaseCashOutTest, BaseBetSlipTest):
    """
    TR_ID: C60060307
    NAME: Verify that one SS response is received after placing Bet
    DESCRIPTION: Test case verifies that EventToOutomeForEvent is replaced with EventToOutcomeForOutcome in SS responce after Betslip receipt
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Make sure the user is logged into their account
    PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
    PRECONDITIONS: 4. Make bet placement
    PRECONDITIONS: 5. Make sure Bet is placed successfully
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    selection_ids = []
    number_of_events = 4

    def get_number_of_EventToOutomeForEvent__requests(self,event_id) -> int:
        """
        Method is used only to get number of buildBet requests
        :return: Number of buildBet requests in performance log
        """
        sleep(1.5)
        log = self.device.get_performance_log()
        base_url = f'{self.ss_req.site}openbet-ssviewer/Drilldown/{self.ss_req.version}/'
        expected_url = f'{base_url}EventToOutcomeForOutcome/{event_id}?'
        number_of_build_bet_requests = 0
        for entry in log:
            for entry_field in entry:
                for entry_type, entry_value in entry_field.items():
                    if entry_type == 'message':
                        url = entry_value.\
                            get('message', {}).\
                            get('params', {}).\
                            get('request', {}).\
                            get('url', '')
                        number_of_build_bet_requests += 1 if url == expected_url else 0
        return number_of_build_bet_requests

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load Oxygen app
        PRECONDITIONS: 2. Make sure the user is logged into their account
        PRECONDITIONS: 3. The User's account balance is sufficient to cover a bet stake
        PRECONDITIONS: 4. Make bet placement for several single selections (at least 4)
        PRECONDITIONS: 5. Make sure Bet is placed successfully
        PRECONDITIONS: For <Sport>  it is possible to place a bet from:
        PRECONDITIONS: - event landing page
        PRECONDITIONS: - event details page
        PRECONDITIONS: For <Races> it is possible to place a bet from:
        PRECONDITIONS: - 'Next 4' module
        PRECONDITIONS: - event details page
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=self.number_of_events)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.__class__.eventID = event['event']['id']
                self.selection_ids.append(selection_id)
        else:
            events = self.create_several_autotest_premier_league_football_events(number_of_events=self.number_of_events)
            self.selection_ids = [event.selection_ids[event.team1] for event in events]
            self.__class__.eventID = events[0].event_id
        self.site.login()
        self.__class__.expected_betslip_counter_value = 0
        self.__class__.selection_id = self.selection_ids[0]
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_single_bet(number_of_stakes=1)

    def test_001_check_ss_response__for_bet_receipt__in_devtools__network__xhr___search_outcome(self):
        """
        DESCRIPTION: Check SS response  for Bet receipt  in devTools-> Network ->XHR -> search 'outcome'
        EXPECTED: Verify betslip receipt with EventToOutomeForOutcome, example of request: EventToOutcomeForOutcome/582071908?
        EXPECTED: no EventToOutcomeForEvent requests should be made from betslip receipt
        """
        initial_number = self.get_number_of_EventToOutomeForEvent__requests(self.eventID)
        self.assertEqual(initial_number, 0, msg=f'Actual SS response entry count {initial_number} != expected count 0')

    def test_002_make_multiply_stakecheck_ss_response_for_bet_receipt_in_devtools__network__xhr___search_outcome(self):
        """
        DESCRIPTION: Make multiply Stake
        DESCRIPTION: Check SS response for Bet receipt in devTools-> Network ->XHR -> search 'outcome'
        EXPECTED: Verify betslip receipt with EventToOutomeForOutcome, example of request: EventToOutcomeForOutcome/582071908?
        EXPECTED: no EventToOutomeForEvent requests should be made from betslip receipt
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_multiple_bet(number_of_stakes=1)
        initial_number = self.get_number_of_EventToOutomeForEvent__requests(self.eventID)
        self.assertEqual(initial_number, 0, msg=f'Actual SS response entry count {initial_number} != expected count 0')
