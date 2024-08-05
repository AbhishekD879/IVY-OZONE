import pytest
import tests
from voltron.environments import constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898464_Single_Football_Bet_placed_using_money_and_free_bet_Countered_by_Stake(BaseBetSlipTest):
    """
    TR_ID: C59898464
    NAME: Single Football Bet placed using money and free bet Countered by Stake
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    PRECONDITIONS: Customer should have Freebets in the account
    """
    keep_browser_open = True
    max_bet = 1.5
    suggested_max_bet = 0.94
    prices = {'odds_home': '1/12', 'odds_away': '1/13', 'odds_draw': '1/14'}

    def test_001_add_single_football__selection_to_betslip_and_place_bet_using_money_and_free_bet(self):
        """
        DESCRIPTION: Add Single Football  selection to betslip and place bet using money and free bet
        EXPECTED: Overask flow is triggered
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet)
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.eventID, selection_id = event_params.event_id, list(event_params.selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.ob_config.grant_freebet(self.username)
        self.site.login(self.username)
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.__class__.bet_amount = self.max_bet + 0.42
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" is not added to the betslip')
        stake_name, stake = list(selections.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        self.place_single_bet(number_of_stakes=1, freebet=True)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='"Overask" is not triggered for the User')

    def test_002_counter_by_stake_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter by stake in OB TI tool
        EXPECTED: On FE Customer should see the bet slip with a message saying that free bet cannot be used.
        EXPECTED: No bet is placed and no bet shows in My Bets and Account History.
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='"Overask" is not closed')
        sleep(3)
        overask_warning_message = self.get_betslip_content().overask_warning
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.some_bets_with_freebet,
                         msg=f'Actual message "{overask_warning_message}" does not match '
                         f'expected "{vec.betslip.OVERASK_MESSAGES.some_bets_with_freebet}"')
        self.navigate_to_page('homepage')
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
