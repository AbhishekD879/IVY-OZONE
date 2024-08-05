import re
from collections import OrderedDict

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod  # can't change bir delay on prod/hl
@pytest.mark.betslip
@pytest.mark.bir_delay
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C862022_Price_change_while_placing_a_bet_with_delay_on_an_In_Play_event(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C862022
    NAME: Price change while placing a bet with delay on an In-Play event
    DESCRIPTION: - Verify live updates (price change) while placing a bet with delay on an In-Play event
    PRECONDITIONS: - 'BIR Delay' may be set on each hierarchy level in OB System (except Selection)
    PRECONDITIONS: - The highest set 'BIR Delay' value (applicable to a <Sport> selection) is used in "confirmationExpectedAt" attribute in "placeBet" response
    PRECONDITIONS: - In-Play events are available in application
    PRECONDITIONS: - Make sure you have a user account with positive balance
    """
    keep_browser_open = True
    event1_selection_ids = None
    event2_selection_ids = None
    event1_team1 = None
    event2_team2 = None
    market1_id = None
    market2_id = None
    event1_id = None
    event2_id = None
    new_price1 = '9/1'
    old_prices = OrderedDict([('odds_home', '1/2'),
                              ('odds_draw', '1/3'),
                              ('odds_away', '1/4')])

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add test events
        """
        start_time = self.get_date_time_formatted_string(seconds=10)
        market_short_name = self.ob_config.football_config.\
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        event1_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time,
                                                                                  bir_delay=30, lp=self.old_prices)
        self.__class__.event1_id, self.__class__.event1_team1, self.__class__.event1_selection_ids = \
            event1_params.event_id, event1_params.team1, event1_params.selection_ids
        self.__class__.market1_id = self.ob_config.market_ids[self.event1_id][market_short_name]

        event2_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time,
                                                                                  bir_delay=30, lp=self.old_prices)
        self.__class__.event2_id, self.__class__.event2_team2, self.__class__.event2_selection_ids = \
            event2_params.event_id, event2_params.team2, event2_params.selection_ids
        self.__class__.market2_id = self.ob_config.market_ids[self.event2_id][market_short_name]

    def test_001_load_oxygen_application_and_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.__class__.bir_delay = 60 if self.device_type == 'mobile' else 90

    def test_002_add_selections_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add a selection(s) to the Betslip from any In-Play <Sport> event > Open Betslip
        EXPECTED: Added selection(s) is(are) displayed within Betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.event1_selection_ids[self.event1_team1],
                                                         self.event2_selection_ids[self.event2_team2]))

    def test_003_in_ti_add_bir_delay_value_to_the_in_play_sport_selections(self):
        """
        DESCRIPTION: In TI: Add 'BIR Delay' value applicable to an added In-Play <Sport> selection
        EXPECTED: 'BIR Delay' is added
        """
        self.ob_config.change_market_bir_delay(event_id=self.event1_id, market_id=self.market1_id,
                                               bir_delay=self.bir_delay)
        self.ob_config.change_market_bir_delay(event_id=self.event2_id, market_id=self.market2_id,
                                               bir_delay=self.bir_delay)

    def test_004_in_betslip_enter_any_stake_value_for_selections_with_set_bir_delay(self):
        """
        DESCRIPTION: In application/Betslip: Enter any Stake value for selection(s) with set 'BIR Delay'
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        singles_section = self.get_betslip_sections().Singles
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=2).items():
            self.enter_stake_amount(stake=stake)

    def test_005_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Spinner icon with countdown timer in format XX:XX appear on the green button (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value + 1)
        """
        self.get_betslip_content().bet_now_button.click()

        timer = self.get_betslip_content().timer
        message = self.get_betslip_content().count_down_message

        self.assertEqual(message, vec.betslip.COUNT_DOWN_TIMER_MESSAGE,
                         msg=f'Notification "{vec.betslip.COUNT_DOWN_TIMER_MESSAGE}" does not appear')
        self.assertTrue(timer and re.match(r'\d{2}:\d{2}', timer),
                        msg=f'Countdown timer "{timer}" has incorrect format. Expected format: "XX:XX"')

    def test_006_trigger_price_change_for_selection_with_entered_stake_and_verify_betslip(self):
        """
        DESCRIPTION: In TI: Trigger price change for a selection with set 'BIR Delay' while bet is being processed
        DESCRIPTION: In application: Verify Betslip
        EXPECTED: - Price is changed for a selection
        EXPECTED: - Old Odds are crossed out in black color and New Odds are displayed to the right of Old Odds (in Red color with Red colored Down direct arrows if Odds decreased; in Green color with Green colored Up direct arrows if Odds increased)
        EXPECTED: - Count down timer is still displayed on green button
        """
        outcome_id1 = self.event1_selection_ids[self.event1_team1]
        self.ob_config.change_price(selection_id=outcome_id1, price=self.new_price1)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id1, price=self.new_price1)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.event1_team1}" with id "{outcome_id1}" is not received')

        timer = self.get_betslip_content().timer
        self.assertTrue(timer and re.match(r'\d{2}:\d{2}', timer),
                        msg=f'Countdown timer "{timer}" has incorrect format. Expected format: "XX:XX"')

        singles_sections = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_sections.items())[0]
        expected_message = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(old=list(self.old_prices.values())[0],
                                                                     new=self.new_price1)
        self.assertEqual(stake.error_message, expected_message,
                         msg=f'Actual price change message: "{stake.error_message}" '
                             f'is not equal to expected: "{expected_message}"')

    def test_007_verify_betslip_once_processing_bet_time_is_up(self):
        """
        DESCRIPTION: Verify Betslip once processing bet time is up
        EXPECTED: - Notification "Please wait while your bet is being placed" disappears
        EXPECTED: - Warning message 'Please beware that # of your selections had price change' appears
        EXPECTED: - Spinner icon with countdown timer is replaced by 'Accept & Bet (#)' label
        EXPECTED: - 'Accept & Bet (#)' button is enabled
        """
        general_error_msg = self.get_betslip_content().wait_for_warning_message(timeout=self.bir_delay)
        expected_message = vec.betslip.PRICE_CHANGE_BANNER_MSG
        self.assertEqual(general_error_msg, expected_message,
                         msg=f'Actual message: "{general_error_msg}" does not match expected "{expected_message}"')

        betnow_button = self.get_betslip_content().bet_now_button
        self.assertEqual(betnow_button.name, vec.betslip.ACCEPT_BET,
                         msg=f'Actual "{betnow_button.name}" button name, '
                             f'is not as expected "{vec.betslip.ACCEPT_BET}"')

        self.assertTrue(betnow_button.is_enabled(),
                        msg=f'"{vec.betslip.ACCEPT_BET}" button is disabled')

    def test_008_tap_on_accept_and_bet_button(self):
        """
        DESCRIPTION: Tap on 'Accept & Bet (#)' button
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Spinner icon with countdown timer in format XX:XX appear on the green button
        EXPECTED: (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value + 1)
        EXPECTED: - Once time is up the bet is successfully processed
        """
        self.test_005_tap_bet_now_button()

    def test_009_tap_done_on_bet_receipt(self):
        """
        DESCRIPTION: Tap 'Done' on 'Bet Receipt'
        EXPECTED: Betslip is closed
        """
        self.check_bet_receipt_is_displayed(timeout=self.bir_delay)
        self.site.bet_receipt.footer.click_done()

    def test_010_add_selection_to_the_betslip_and_open_betslip(self):
        """
        DESCRIPTION: Add a selections to the Betslip from any In-Play <Sport> event > Open Betslip
        EXPECTED: Added selections are displayed within Betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.event1_selection_ids[self.event1_team1],
                                                         self.event2_selection_ids[self.event2_team2]))

    def test_011_in_ti_add_bir_delay_value_to_the_in_play_sport_selection(self):
        """
        DESCRIPTION: In TI: Add 'BIR Delay' value applicable to any added In-Play <Sport> selection
        EXPECTED: 'BIR Delay' is added
        """
        self.test_003_in_ti_add_bir_delay_value_to_the_in_play_sport_selections()

    def test_012_in_betslip_enter_any_stake_value_for_selection_with_set_bir_delay(self):
        """
        DESCRIPTION: In application: Enter any Stake value for selections with set 'BIR Delay'
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        singles_section = self.get_betslip_sections().Singles
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)

    def test_013_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now'
        EXPECTED: - Bet placement process starts automatically
        EXPECTED: - Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: - Spinner icon with countdown timer in format XX:XX appear on the green button
        EXPECTED: (countdown timer is taken from "placeBet" response: "confirmationExpectedAt" attribute value + 1)
        """
        self.test_005_tap_bet_now_button()

    def test_014_in_ti_trigger_price_change_for_a_selection_with_no_stake_entered_and_verify_betslip(self):
        """
        DESCRIPTION: In TI: Trigger price change for a selection with **NO** Stake entered while bet is being processed
        EXPECTED: Price is changed for a selection
        """
        outcome_id = self.event2_selection_ids[self.event2_team2]
        self.ob_config.change_price(selection_id=outcome_id, price=self.new_price1)
        price_update = self.wait_for_price_update_from_live_serv(selection_id=outcome_id, price=self.new_price1)
        self.assertTrue(price_update,
                        msg=f'Price update for selection "{self.event2_team2}" with id "{outcome_id}" is not received')

        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = self.singles_section.get(self.event2_team2)

    def test_015_verify_betslip_once_processing_bet_time_is_up(self):
        """
        DESCRIPTION: In application: Verify Betslip
        EXPECTED: - Bet placement goes on
        EXPECTED: - Notification box is displayed at the bottom of the betslip
        EXPECTED: - A notification box is displayed at the top of the betslip with animations - this is removed after 5 seconds (Ladbrokes only)
        EXPECTED: - Notification "Please wait while your bet is being placed" is displayed above the footer
        EXPECTED: - Spinner icon with countdown timer remains shown on the green button
        EXPECTED: - Once time is up, the bet is successfully processed
        """
        timer = self.get_betslip_content().timer
        self.assertTrue(timer, msg='Timer counter is not present')

        message = self.get_betslip_content().count_down_message
        self.assertEqual(message, vec.betslip.COUNT_DOWN_TIMER_MESSAGE,
                         msg=f'Notification "{vec.betslip.COUNT_DOWN_TIMER_MESSAGE}"')
        self.assertTrue(timer and re.match(r'\d{2}:\d{2}', timer),
                        msg=f'Countdown timer "{timer}" has incorrect format. Expected format: "XX:XX"')
        self.check_bet_receipt_is_displayed(timeout=self.bir_delay)

    def test_016_tap_done_on_bet_receipt(self):
        """
        DESCRIPTION: Tap 'Done' on 'Bet Receipt'
        EXPECTED: Betslip is closed
        """
        self.test_009_tap_done_on_bet_receipt()
