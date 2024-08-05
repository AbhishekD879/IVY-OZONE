import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898502_Verify_Inplay_selections_are_not_passed_through_the_OA_flow(BaseBetSlipTest):
    """
    TR_ID: C59898502
    NAME: Verify Inplay selections are not passed through the OA flow
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1.25
    prices = {'odds_home': '1/12', 'odds_away': '1/13', 'odds_draw': '1/14'}
    expected_max_bet_msg = vec.betslip.MAX_STAKE.format(max_bet)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load Oxygen/Roxanne Application and login
        PRECONDITIONS: Overask is enabled for logged in user
        """
        event_params = self.ob_config.add_football_event_to_special_league(lp=self.prices, max_bet=self.max_bet, is_live=True)
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.site.login(username=tests.settings.user_with_stakefactor_1)

    def test_001_add_inplay_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add inplay selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: No inplay selections should be passed into the OA flow and the user should be returned the max stake messaging and no bet placed
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.3
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertFalse(overask, msg='inplay selection is passed into the OA flow')
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        error = stake.wait_for_error_message()
        self.assertEqual(error, self.expected_max_bet_msg,
                         msg=f'Actual message "{error}" is not same as Expected "{self.expected_max_bet_msg}"')
        self.site.close_betslip()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
        self.navigate_to_page('bet-history')
        self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
