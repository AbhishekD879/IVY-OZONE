import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898503_Add_pre_match_and_inplay_selections_and_stake_for_higher_than_the_max_stake(BaseBetSlipTest):
    """
    TR_ID: C59898503
    NAME: Add pre match and inplay selections and stake for higher than the max stake
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True
    max_bet = 1.25
    prices = {'odds_home': '1/12', 'odds_away': '1/13', 'odds_draw': '1/14'}

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load Oxygen/Roxanne Application and login
        PRECONDITIONS: Overask is enabled for logged in user
        """
        event = self.ob_config.add_football_event_to_special_league(is_live=True, lp=self.prices, max_bet=self.max_bet)
        event2 = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet)
        self.__class__.event_name = event.ss_response['event']['name']
        self.__class__.selection_id_1 = event.selection_ids[event.team1]
        self.__class__.selection_id_2 = event2.selection_ids[event2.team2]
        self.site.login(username=tests.settings.user_with_stakefactor_1)

    def test_001_add_inplay_and_preplay_selections_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add inplay and preplay selections to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: No inplay selections should be passed into the OA flow and the user should be returned the max stake messaging and no bet placed
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))
        self.__class__.bet_amount = self.max_bet + 0.3
        self.place_single_bet(number_of_stakes=2)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertFalse(overask, msg='inplay selection is passed into the OA flow')
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        error = stake.wait_for_error_message()
        self.assertEqual(error, vec.betslip.MAX_STAKE.format(self.max_bet),
                         msg=f'Actual message "{error}" is not same as Expected "{vec.betslip.MAX_STAKE.format(self.max_bet)}"')
        self.site.close_betslip()
        self.site.open_my_bets_open_bets()
        self.verify_bet_in_open_bets(event_name=self.event_name,
                                     bet_in_open_bets=False, bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE)
