import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot grant odds boost
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.odds_boost
@vtest
class Test_C2983104_Verify_displaying_of_the_boosted_selections_in_the_My_Bets(BaseBetSlipTest):
    """
    TR_ID: C2983104
    NAME: Verify displaying of the boosted selections in the My Bets
    PRECONDITIONS: 1. Login as a user with a valid token added to some sport category
    PRECONDITIONS: 2. Place a bet on some boosted selection
    PRECONDITIONS: 3. Reuse this selection, place a bet without boosting
    PRECONDITIONS: 4. Go to My Bets > Open Bets
    """
    keep_browser_open = True
    bet_with_boost = None
    bet_without_boost = None

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: Login with user and place bet with boosting odds
        """
        username = tests.settings.default_username
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = self.event.selection_ids[self.event.team1]
        self.ob_config.grant_odds_boost_token(username=username)
        self.site.login(username)
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.site.wait_content_state_changed()

        bet_amount = 0.8
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake.name, stake), stake_bet_amounts={self.event.team1: bet_amount})
        self.__class__.est_returns = self.get_betslip_content().total_estimate_returns
        _, team = list(self.get_betslip_sections().Singles.items())[0]
        self.__class__.actual_odds = team.odds
        odds_boost_header = self.get_betslip_content().odds_boost_header
        odds_boost_header.boost_button.click()
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.reuse_selection_button.click()

        self.place_single_bet(stake_bet_amounts={self.event.team1: bet_amount})
        self.site.bet_receipt.close_button.click()
        self.site.open_my_bets_open_bets()
        self.site.wait_content_state_changed()
        self.__class__.bets_list = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.__class__.normal_bet = f'SINGLE - [{self.event.team1}'
        self.__class__.boosted_bet = f'1 SINGLE - [{self.event.team1}'

    def test_001_verify_the_this_bet_has_been_boosted_bar_and_the_appropriate_data_price_and_estimated_returns_are_shown_for_the_boosted_bet(self):
        """
        DESCRIPTION: Verify the "This bet has been boosted!" bar and the appropriate data: price and estimated returns are shown for the boosted bet
        EXPECTED: * The bar with Odds Boost icon and text "This bet has been boosted!" is located in the bottom of the bet
        EXPECTED: * Boosted odds are shown
        EXPECTED: * Boosted Estimated Returns are shown
        """
        for bet_name, bet in list(self.bets_list.items()):
            if self.normal_bet in bet_name and not self.bet_without_boost:
                self.__class__.bet_without_boost = bet
            if self.boosted_bet in bet_name and not self.bet_with_boost:
                self.__class__.bet_with_boost = bet
            if self.bet_without_boost and self.bet_with_boost:
                break

        has_bet_boosted_text = self.bet_with_boost.has_odds_boost_text(expected_result=True)
        self.assertTrue(has_bet_boosted_text, msg='Oddsboost text not displayed')
        bet_boosted_text = self.bet_with_boost.odds_boost_text
        self.assertEqual(bet_boosted_text, vec.betslip.BOOSTED_MSG,
                         msg=f'Actual text:"{bet_boosted_text}" is not same as'
                             f'Expected text: "{vec.betslip.BOOSTED_MSG}".')

        bet_event = list(self.bet_with_boost.items_as_ordered_dict.values())[0]
        self.assertNotEqual(bet_event.odds_value, self.actual_odds,
                            msg=f'Actual odd value:"{bet_event.odds_value}" is same as'
                                f'Expected odd value: "{self.actual_odds}".')
        boosted_est = self.bet_with_boost.est_returns.stake_value
        self.assertNotEqual(boosted_est, self.est_returns,
                            msg=f'Actual est returns value:"{boosted_est}" is same as'
                                f'Expected odd value: "{self.est_returns}".')

    def test_002_verify_the_this_bet_has_been_boosted_bar_isnt_shown_and_the_appropriate_price_and_estimated_returns_are_shown_for_the_not_boosted_bet(self):
        """
        DESCRIPTION: Verify the "This bet has been boosted!" bar isn't shown and the appropriate price and estimated returns are shown for the not-boosted bet
        EXPECTED: Non-boosted bet doesn't contains the bar. Not boosted odds and returns are shown
        """
        has_bet_boosted_text = self.bet_without_boost.has_odds_boost_text(expected_result=False)
        self.assertFalse(has_bet_boosted_text, msg='"Boosted text" is displayed.')
        event_without_boost = list(self.bet_without_boost.items_as_ordered_dict.values())[0]
        self.assertTrue(event_without_boost.odds_value,
                        msg='"Appropriate odds" are not shown.')
        est_returns_without_boost = self.bet_without_boost.est_returns.stake_value
        self.assertTrue(est_returns_without_boost,
                        msg='"Appropriate est returns" are not shown.')

    def test_003_pass_1_2_step_for_the_settled_bets_in_the_bet_history_tab(self):
        """
        DESCRIPTION: Pass 1-2 step for the settled bets in the Bet History tab
        EXPECTED:
        """
        self.__class__.bet_without_boost = self.__class__.bet_with_boost = None
        self.result_event(selection_ids=self.selection_ids, market_id=self.event.default_market_id,
                          event_id=self.event.event_id)
        self.navigate_to_page('bet-history')
        self.site.wait_content_state(state_name='BetHistory')
        wait_for_result(lambda: self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict,
                        name='Settled bets to be displayed', timeout=5)

        self.bets_list = self.site.bet_history.tab_content.accordions_list.items_as_ordered_dict
        self.test_001_verify_the_this_bet_has_been_boosted_bar_and_the_appropriate_data_price_and_estimated_returns_are_shown_for_the_boosted_bet()
        self.test_002_verify_the_this_bet_has_been_boosted_bar_isnt_shown_and_the_appropriate_price_and_estimated_returns_are_shown_for_the_not_boosted_bet()
