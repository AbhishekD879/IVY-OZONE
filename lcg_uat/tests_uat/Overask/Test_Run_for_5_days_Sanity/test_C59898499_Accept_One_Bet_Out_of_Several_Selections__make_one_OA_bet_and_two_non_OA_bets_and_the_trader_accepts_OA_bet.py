import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898499_Accept_One_Bet_Out_of_Several_Selections__make_one_OA_bet_and_two_non_OA_bets_and_the_trader_accepts_OA_bet(BaseBetSlipTest):
    """
    TR_ID: C59898499
    NAME: Accept One Bet Out of Several Selections - make one OA bet and two non OA bets and the trader accepts OA bet
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1.5
    event_names = []
    selection_ids = []
    prices = {'odds_home': '1/12', 'odds_away': '1/13', 'odds_draw': '1/14'}

    def test_000_preconditions(self):
        """
         PRECONDITIONS: Load Oxygen/Roxanne Application and login
         PRECONDITIONS: Overask is enabled for logged in user
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet)
        self.__class__.eventID = event_params.event_id
        self.event_names.append(event_params.ss_response['event']['name'])
        self.selection_ids.append(list(event_params.selection_ids.values())[0])
        for i in range(0, 2):
            event = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices)
            self.event_names.append(event.ss_response['event']['name'])
            self.selection_ids.append(list(event.selection_ids.values())[0])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_make_one_oa_bet_and_two_non_oa_betstrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Make one OA bet and two non OA bets
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 0.3
        self.place_single_bet(number_of_stakes=3)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the user')

    def test_002_if_trader_accepts_overask_bet(self):
        """
        DESCRIPTION: If trader accepts Overask bet
        EXPECTED: Customer should see the bet receipt with all 3 bets showing as being placed.
        EXPECTED: My Bets and Account History should reflect these bets.
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()
        for event in self.event_names:
            self.site.open_my_bets_open_bets()
            self.verify_bet_in_open_bets(event_name=event,
                                         bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
            self.navigate_to_page('bet-history')
            self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
            self.verify_bet_in_open_bets(event_name=event,
                                         bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
