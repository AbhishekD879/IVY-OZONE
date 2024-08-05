import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
# @pytest.mark.prod - This test case is limited to QA2 only as we cannot suspend markets on prod
@pytest.mark.open_bets
@pytest.mark.sports
@pytest.mark.medium
@vtest
class Test_C44870215_Customer_Bet_placements_fails_on_an_in_play_event_where_betting_is_not_allowed_once_event_starts_and_event_suspended_error_message_displays(BaseBetSlipTest):
    """
    TR_ID: C44870215
    NAME: Customer Bet placements fails on an in play event where betting is not allowed once event starts and event suspended error message displays
    DESCRIPTION: This test case verify suspended error message on Quick bet / Betslip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.selection_ids = event.selection_ids
        market_short_name = self.ob_config.football_config.autotest_class.autotest_premier_league. \
            market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.eventID = event.event_id
        self.__class__.team1 = event.team1
        self.__class__.marketID = self.ob_config.market_ids[self.eventID][market_short_name]

    def test_001_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: HomePage opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_go_to_in_play_on_sport_ribbon(self):
        """
        DESCRIPTION: Go to In-Play on sport ribbon
        EXPECTED: In-Play landing page opened
        """
        self.navigate_to_page('in-play')
        self.site.wait_content_state(state_name='InPlay')

    def test_003_make_a_selection_from_any_inplay_sport_and_add_to_betslip(self):
        """
        DESCRIPTION: Make a selection from any inplay sport and add to betslip
        EXPECTED: Selection added to betslip
        """
        self.open_betslip_with_selections(self.selection_ids[self.team1])

    def test_004_enter_the_stake_to_place_a_bet(self):
        """
        DESCRIPTION: Enter the stake to place a bet
        EXPECTED: Stake entered
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.assertEqual(stake_name, self.team1,
                         msg=f'Selection "{self.team1}" should be present in betslip')
        self.enter_stake_amount(stake=(stake_name, self.stake))
        self.assertEqual(self.stake.amount_form.input.value, str(self.bet_amount),
                         msg=f'"Stake" input field should contain just entered value: "{self.bet_amount}"'
                             f'Current value is "{self.stake.amount_form.input.value}"')

    def test_005_verify_that_selection_suspended_in_betslip(self):
        """
        DESCRIPTION: Verify that selection suspended in betslip
        EXPECTED: Some of the selections are suspended message display on top of betslip
        EXPECTED: Selections are greyed out
        EXPECTED: Place bet button is grey out
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True)
        self.verify_betslip_is_suspended(stakes=[self.stake])
