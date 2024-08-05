import re

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod  # can't change bir delay on prod/hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.bir_delay
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.slow
@pytest.mark.high
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C858711_Verify_countdown_when_placing_bet_logged_in(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C858711
    NAME: Verify countdown clock when placing a bet on an In-Play event when user is logged in
    DESCRIPTION: Verify countdown clock on 'Bet Now' button while placing a bet on an In-Play event
    """
    keep_browser_open = True
    event1_selection_ids = None
    event2_selection_ids = None
    event1_team1 = None
    event2_team1 = None
    event2_team2 = None
    market1_id = None
    market2_id = None
    eventID_1 = None
    eventID_2 = None
    bir_delay = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event
        """
        start_time = self.get_date_time_formatted_string(seconds=10)
        market_short_name = self.ob_config.football_config.\
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        event1_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time, bir_delay=10)
        self.__class__.eventID_1, self.__class__.event1_team1, self.__class__.event1_selection_ids = \
            event1_params.event_id, event1_params.team1, event1_params.selection_ids
        self.__class__.market1_id = self.ob_config.market_ids[self.eventID_1][market_short_name]

        event2_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time, bir_delay=10)
        self.__class__.eventID_2, self.__class__.event2_team1, self.__class__.event2_team2, self.__class__.event2_selection_ids = \
            event2_params.event_id, event2_params.team1, event2_params.team2, event2_params.selection_ids
        self.__class__.market2_id = self.ob_config.market_ids[self.eventID_2][market_short_name]

    def test_001_login(self):
        """
        DESCRIPTION: Login to application
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

    def test_002_add_selection_via_deep_link(self):
        """
        DESCRIPTION: Add a selection to the Betslip from any In-Play <Sport> event > Open Betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.event1_selection_ids[self.event1_team1]))

    def test_003_enter_stake_for_single(self):
        """
        DESCRIPTION: Enter any Stake value
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)

    def test_004_set_BIR_delay_30(self):
        """
        DESCRIPTION: In TI: Add 'BIR Delay' value applicable to an added In-Play <Sport> selection
        EXPECTED: 'BIR Delay' is added
        """
        self.__class__.bir_delay = 30
        self.ob_config.change_market_bir_delay(event_id=self.eventID_1, market_id=self.market1_id,
                                               bir_delay=self.bir_delay)

    def test_005_click_bet_now_button_and_verify_count_down(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: Bet placement process starts automatically
        EXPECTED: Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: Spinner icon with countdown timer in format XX:XX appear on the green button (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value + 1)
        EXPECTED: Once time is up, the bet is successfully processed
        """
        self.get_betslip_content().bet_now_button.click(timeout=0)
        betnow_button = wait_for_result(lambda: self.get_betslip_content().bet_now_button.is_displayed(),
                                        timeout=5,
                                        name='"Bet Now" button with timer displayed')
        self.assertTrue(betnow_button, msg='Bet Now" button does not appear')
        result = self.get_betslip_content().bet_now_button.has_spinner_icon(expected_result=True, timeout=1)
        self.assertTrue(result, msg='Spinner not found on Bet Now button')
        betslip = self.get_betslip_content()
        timer = betslip.timer
        message = betslip.count_down_message
        self.assertEqual(message, vec.betslip.COUNT_DOWN_TIMER_MESSAGE,
                         msg=f'Notification "{vec.betslip.COUNT_DOWN_TIMER_MESSAGE}" does not appear. Actual "{message}')
        self.assertTrue(re.match(r'\d{2}:\d{2}', timer), msg=f'Countdown timer "{timer}" has incorrect format. '
                        'Expected format: "XX:XX"')

        result = self.get_betslip_content().bet_now_button.has_spinner_icon(expected_result=False, timeout=self.bir_delay + 3)
        self.assertFalse(result, msg='Spinner has not disappeared from Bet Now button')
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_006_add_selections_via_deep_link(self):
        """
        DESCRIPTION: Add several selections to the Betslip from any In-Play <Sport> event > Open Betslip
        EXPECTED: Added selections are displayed within Betslip
        """
        self.site.wait_content_state(state_name='Homepage')
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.event2_selection_ids[self.event2_team1],
                                                         self.event2_selection_ids[self.event2_team2]))

    def test_007_enter_stake_for_all_singles(self):
        """
        DESCRIPTION: Enter Stake value for all single selections
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)

    def test_008_set_BIR_delay_40(self):
        """
        DESCRIPTION: In TI: Add different 'BIR Delay' values applicable to added In-Play <Sport> selections 'BIR Delay' values are added
        EXPECTED: 'BIR Delay' is added
        """
        self.__class__.bir_delay = 40
        self.ob_config.change_market_bir_delay(event_id=self.eventID_2, market_id=self.market2_id,
                                               bir_delay=self.bir_delay)

    def test_009_click_on_bet_now_button(self):
        """
        DESCRIPTION: repeat step 5:  Tap 'Bet Now' button
        """
        self.test_005_click_bet_now_button_and_verify_count_down()

    def test_010_add_selections_via_deep_link(self):
        """
        DESCRIPTION: Add several selections to the Betslip from any In-Play <Sport> event > Open Betslip
        EXPECTED: Added selections are displayed within Betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.event1_selection_ids[self.event1_team1],
                                                         self.event2_selection_ids[self.event2_team1],
                                                         self.event2_selection_ids['Draw']))

    def test_011_enter_stake_for_multiples(self):
        """
        DESCRIPTION: Enter Stake value for multiple selections
        """
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        stake = list(multiples_section.items())[0]
        self.enter_stake_amount(stake=stake)

    def test_012_set_BIR_delay_25(self):
        """
        DESCRIPTION: In TI: Add different 'BIR Delay' values applicable to added In-Play <Sport> selections 'BIR Delay' values are added
        EXPECTED: 'BIR Delay' is added
        """
        self.__class__.bir_delay = 25
        self.ob_config.change_market_bir_delay(event_id=self.eventID_1, market_id=self.market1_id,
                                               bir_delay=self.bir_delay)
        self.ob_config.change_market_bir_delay(event_id=self.eventID_2, market_id=self.market2_id,
                                               bir_delay=self.bir_delay)

    def test_013_click_on_bet_now_button(self):
        """
        DESCRIPTION: repeat step 5: Tap 'Bet Now' button
        """
        self.test_005_click_bet_now_button_and_verify_count_down()
