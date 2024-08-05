import re

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod  # can't change bir delay on prod/hl
@pytest.mark.betslip
@pytest.mark.bir_delay
@pytest.mark.bet_placement
@pytest.mark.liveserv_updates
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C861981_Sport_event_market_selection_suspended_while_placing_a_bet_with_delay_on_an_In_Play_event(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C861981
    NAME: Sport event market selection suspended while placing a bet with delay on an In-Play event
    DESCRIPTION: Verify live updates (<Sport> selection suspended) while placing a bet with delay on an In-Play event
    PRECONDITIONS: - 'BIR Delay' may be set on each hierarchy level in OB System (except Selection)
    PRECONDITIONS: - The highest set 'BIR Delay' value (applicable to a <Sport> selection) is used in "confirmationExpectedAt" attribute in "placeBet" response
    PRECONDITIONS: - In-Play events are available in application
    PRECONDITIONS: - Make sure you have a user account with positive balance
    """
    keep_browser_open = True
    bir_delay = 30

    def test_000_preconditions(self):
        """
        DESCRIPTION: Run preconditions
        """
        event = self.ob_config.add_autotest_premier_league_football_event(is_live=True, bir_delay=self.bir_delay)
        self.__class__.team1 = event.team1
        self.__class__.eventID = event.event_id
        self.__class__.selection_id = event.selection_ids[self.team1]

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_002_add_a_selection_with_bir_delay_to_the_betslip_from_any_in_play_sport_event_and_open_the_betslip(self):
        """
        DESCRIPTION: Add a selection with BIR delay to the Betslip from any In-Play <Sport> event and Open the Betslip
        EXPECTED: Added selection is displayed within Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.singles_section = self.get_betslip_sections().Singles
        stake = self.singles_section.get(self.team1)
        self.assertTrue(stake, msg=f'"{self.team1}" stake was not found in the Betslip')

    def test_003_enter_stake_for_selection_with_set_bir_delay(self):
        """
        DESCRIPTION: Enter Stake for selection with set 'BIR Delay'
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        stake_name, self.__class__.stake = list(self.singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, self.stake))

    def test_004_tap_bet_now_buttonfrom_ox99button_namecoral_and_ladbrokes_place_bet(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        DESCRIPTION: **From OX99**
        DESCRIPTION: Button name:
        DESCRIPTION: Coral and Ladbrokes: 'Place Bet'
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Spinner icon with countdown timer in format XX:XX appear on the green button (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value + 1)
        """
        self.get_betslip_content().bet_now_button.click()
        timer = self.get_betslip_content().timer
        actual_message = self.get_betslip_content().count_down_message
        expected_message = vec.betslip.COUNT_DOWN_TIMER_MESSAGE
        self.assertEqual(actual_message, expected_message, msg=f'Actual notification: "{actual_message}" '
                         f'is not as expected: "{expected_message}"')
        self.assertTrue(timer and re.match(r'\d{2}:\d{2}', timer),
                        msg=f'Countdown timer "{timer}" has incorrect format. Expected format: "XX:XX"')

    def test_005_in_ti_suspend_outcome_with_set_bir_delay_while_bet_is_being_processed(self):
        """
        DESCRIPTION: In TI: Suspend outcome with set 'BIR Delay' while bet is being processed
        EXPECTED: Outcome becomes suspended
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)
        result = self.wait_for_event_market_selection_state_update_from_live_serv(event_id=self.eventID)
        self.assertTrue(result, msg=f'Response for event_id "{self.eventID}" is not received in WS')

    def test_006_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: **Before OX99**
        EXPECTED: - Error message 'Sorry, the outcome has been suspended' is shown below corresponding single
        EXPECTED: - 'Stake' field, 'Odds' and 'Estimated returns'  - disabled and greyed out
        EXPECTED: - Count down timer is still displayed on green button
        EXPECTED: - Warning message 'Please beware that 1 of your selections has been suspended' is shown on the yellow background above notification of processing bet
        EXPECTED: **From OX99**
        EXPECTED: Coral:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * Count down timer is still displayed on green button
        EXPECTED: * Message is displayed at the bottom of the betslip: 'Please beware one of your selections have been suspended'
        EXPECTED: Ladbrokes:
        EXPECTED: * All selection box is greyed out
        EXPECTED: * 'SUSPENDED' label is sown at the center of selection'
        EXPECTED: * Count down timer is still displayed on green button
        EXPECTED: * Message is displayed at the bottom of the betslip: 'One of your selections have been suspended'
        EXPECTED: * message is displayed at the top of the betslip 'One of your selections have been suspended' with duration: 5s
        """
        result = wait_for_result(
            lambda: self.get_betslip_content().error == vec.betslip.SINGLE_DISABLED,
            name='Betslip error to change',
            timeout=5)
        self.assertTrue(result, msg=f'Bet Now section warning "{self.get_betslip_content().error} '
                        f'is not the same as expected: "{vec.betslip.SINGLE_DISABLED}"')
        result = wait_for_result(lambda: self.stake.suspended_stake_label,
                                 name='SUSPENDED label to appear',
                                 timeout=self.bir_delay)
        self.assertEqual(result.strip('"'), vec.betslip.SUSPENDED_LABEL, msg=f'{vec.betslip.SUSPENDED_LABEL} does not appear. '
                         f'Actual content "{result}"')

    def test_007_verify_betslip_once_processing_bet_time_is_up(self):
        """
        DESCRIPTION: Verify Betslip once processing bet time is up
        EXPECTED: - Notification "Please wait while your bet is being placed" disappears
        EXPECTED: - Spinner icon with countdown timer is replaced by 'Bet Now' label
        EXPECTED: - 'Bet Now' button is disabled
        EXPECTED: **From OX99**
        EXPECTED: Button name:
        EXPECTED: Coral and Ladbrokes: 'Place Bet'
        """
        result = wait_for_result(lambda: self.get_betslip_content().timer == '',
                                 name='Count down timer to disappear',
                                 timeout=self.bir_delay,
                                 poll_interval=1)
        self.assertTrue(result, msg='Countdown timer disappear')
        betnow_button = self.get_betslip_content().bet_now_button
        expected_bet_now_button_name = vec.betslip.BET_NOW
        self.assertEqual(betnow_button.name, expected_bet_now_button_name,
                         msg=f'Actual button name: {betnow_button.name} '
                         f'is not as expected: {expected_bet_now_button_name}')
        self.assertFalse(betnow_button.is_enabled(expected_result=False), msg='"Bet Now" button is not disabled')
