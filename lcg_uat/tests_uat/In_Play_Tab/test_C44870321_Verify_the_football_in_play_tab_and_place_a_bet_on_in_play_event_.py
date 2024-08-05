import pytest
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - This script is executed only for QA2 as we cannot suspend any event in prod or beta
@pytest.mark.uat
@pytest.mark.p1
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C44870321_Verify_the_football_in_play_tab_and_place_a_bet_on_in_play_event_(BaseBetSlipTest):
    """
    TR_ID: C44870321
    NAME: "Verify the football in-play tab and place a bet on in-play event "
    DESCRIPTION: this test case verify football inplay tab and bet placement
    """
    keep_browser_open = True
    bir_delay = 30

    def test_000_preconditions(self):
        """
        DESCRIPTION: Sport should be available in inplay
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                          default_market_name='|Draw No Bet|')
        event2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                           default_market_name='|Draw No Bet|')
        self.__class__.teams = [event.team1, event2.team2]
        self.__class__.selection_id_1 = event.selection_ids[event.team1]
        self.__class__.selection_id_2 = event2.selection_ids[event2.team2]

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to In-Play tab
        EXPECTED: In-Play tab opened with all inplay sports
        """
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')

    def test_003_go_to_football_and_add_selections_to_the_betslip(self):
        """
        DESCRIPTION: Go to Football and Add selections to the Betslip
        EXPECTED: Betslip counter is increased
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))

    def test_004_go_to_the_betslip_singles_section(self):
        """
        DESCRIPTION: Go to the Betslip->'Singles' section
        EXPECTED: Betslip is opened
        EXPECTED: Added single selections are present
        """
        singles_section = self.get_betslip_sections().Singles
        for i in range(2):
            self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[i]
            self.assertEqual(self.stake_name, self.teams[i],
                             msg=f'Expected Selection "{self.teams[i]}" is not matching with Actual selection '
                                 f'"{self.stake_name}" on the betslip')

    def test_005_enter__stake_for_selection(self):
        """
        DESCRIPTION: Enter  stake for selection
        EXPECTED: Stake is entered and displayed correctly
        EXPECTED: 'Place Bet' button becomes enabled
        """
        self.enter_stake_amount(stake=(self.stake_name, self.stake))
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(timeout=1.5), msg='"PLACE BET" button is not enabled')

    def test_006_tap_on_place_bet_button_and_trigger_error_occurrence_eg_suspension_price_change(self):
        """
        DESCRIPTION: Tap on place bet button and trigger error occurrence (e.g. suspension, price change)
        EXPECTED: After user will deal with error then** 'Place Bet' button** will be enabled within Betslip
        """
        self.ob_config.change_selection_state(self.selection_id_2, displayed=True, active=False)
        if self.brand == 'ladbrokes':
            self.device.refresh_page()
            self.site.open_betslip()
            result = wait_for_result(lambda: self.get_betslip_content().error == vec.betslip.SELECTION_DISABLED,
                                     name='Betslip error to change', timeout=10)
            self.assertTrue(result, msg=f'Bet Now section warning "{self.get_betslip_content().error}"'
                                        f'is not the same as expected: "{vec.betslip.SELECTION_DISABLED}"')
        else:
            result = wait_for_result(
                lambda: self.get_betslip_content().error == vec.betslip.SINGLE_DISABLED,
                name='Betslip error to change',
                timeout=10)
            self.assertTrue(result, msg=f'Bet Now section warning "{self.get_betslip_content().error}" '
                                        f'is not the same as expected: "{vec.betslip.SINGLE_DISABLED}"')
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertFalse(wait_for_result(lambda: bet_now_button.is_enabled(expected_result=False), timeout=15),
                         msg=f'"{vec.quickbet.BUTTONS.place_bet}" button is not disabled')
        self.ob_config.change_selection_state(self.selection_id_2, displayed=True, active=True)
        self.site.wait_content_state_changed()
        if self.brand == 'ladbrokes':
            self.device.refresh_page()
            self.site.open_betslip()
            self.site.wait_content_state_changed()
            if self.stake_name == vec.bet_finder.FB_BET_FILTER_DOUBLE:
                multiples_section = self.get_betslip_sections(multiples=True).Multiples
                stake_name, stake = list(multiples_section.items())[0]
                self.enter_stake_amount(stake=(stake_name, stake))
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(wait_for_result(lambda: bet_now_button.is_enabled(expected_result=True), timeout=15),
                        msg=f'"{vec.quickbet.BUTTONS.place_bet}" button is disabled')

    def test_007_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: Bet is placed successfully
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_008_repeat_steps_3_to_7_for_multiple_bets(self):
        """
        DESCRIPTION: repeat steps #3 to #7 for multiple bets
        """
        self.__class__.expected_betslip_counter_value = 0
        self.test_003_go_to_football_and_add_selections_to_the_betslip()
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        self.__class__.stake_name, self.__class__.stake = list(multiples_section.items())[0]
        self.assertEqual(self.stake_name, vec.bet_finder.FB_BET_FILTER_DOUBLE,
                         msg=f'Expected Selection "{vec.bet_finder.FB_BET_FILTER_DOUBLE}" is not matching with '
                             f'Actual selection "{self.stake_name}" on the  bet slip')
        self.site.wait_content_state_changed()
        self.test_005_enter__stake_for_selection()
        self.test_006_tap_on_place_bet_button_and_trigger_error_occurrence_eg_suspension_price_change()
        self.test_007_tap_place_bet_button()
