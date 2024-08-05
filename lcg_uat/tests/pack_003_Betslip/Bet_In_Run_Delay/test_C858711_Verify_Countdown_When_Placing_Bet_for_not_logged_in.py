import re

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod  # can't change bir delay on prod/hl
@pytest.mark.betslip
@pytest.mark.bir_delay
@pytest.mark.ob_smoke
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C858711_Verify_countdown_when_placing_bet_not_logged_in(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C858711
    NAME: Verify countdown clock when placing a bet on an In-Play event when user is not logged in
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

    @classmethod
    def custom_setUp(cls):
        cms_config = cls.get_cms_config()
        odds_boost = cms_config.get_initial_data().get('oddsBoost')
        if odds_boost is not None:
            cms_config.update_odds_boost_config(enabled=False)

    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        odds_boost = cms_config.get_initial_data().get('oddsBoost')
        if odds_boost is None:
            cms_config.update_odds_boost_config(enabled=True)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Football event
        DESCRIPTION: Login and Logout
        """
        self.__class__.username = tests.settings.betplacement_user

        start_time = self.get_date_time_formatted_string(seconds=10)
        market_short_name = self.ob_config.football_config.\
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

        event1_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time,
                                                                                  bir_delay=10)
        self.__class__.eventID_1, self.__class__.event1_team1, self.__class__.event1_selection_ids = \
            event1_params.event_id, event1_params.team1, event1_params.selection_ids
        self.__class__.market1_id = self.ob_config.market_ids[self.eventID_1][market_short_name]

        event2_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time,
                                                                                  bir_delay=10)
        self.__class__.eventID_2, self.__class__.event2_team1, self.__class__.event2_team2, self.__class__.\
            event2_selection_ids = event2_params.event_id, event2_params.team1, event2_params.\
            team2, event2_params.selection_ids
        self.__class__.market2_id = self.ob_config.market_ids[self.eventID_2][market_short_name]

        self.site.login(username=self.username, async_close_dialogs=False)
        self.site.logout()

    def test_001_add_selection_via_deep_link(self):
        """
        DESCRIPTION: Add a selection to the Betslip from any In-Play <Sport> event > Open Betslip
        """
        self.open_betslip_with_selections(selection_ids=(self.event1_selection_ids[self.event1_team1]))

    def test_002_enter_stake_for_single(self):
        """
        DESCRIPTION: Enter any Stake value using
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(self.zip_available_stakes(section=singles_section, number_of_stakes=1).items())[0]
        self.enter_stake_amount(stake=stake)

    def test_003_set_BIR_delay_20(self):
        """
        DESCRIPTION: In TI: Add 'BIR Delay' value applicable to an added In-Play <Sport> selection
        EXPECTED: 'BIR Delay' is added
        """
        self.__class__.bir_delay = 40
        self.ob_config.change_market_bir_delay(event_id=self.eventID_1, market_id=self.market1_id,
                                               bir_delay=self.bir_delay)

    def test_004_login_and_verify_count_down(self):
        """
        DESCRIPTION: Tap 'Log In & Bet' button
        DESCRIPTION: Login as a user that has sufficient funds to place a bet
        EXPECTED: Bet placement process starts automatically
        EXPECTED: Notification "Please wait while your bet is being placed" appears on the yellow background above the Betslip footer
        EXPECTED: Spinner icon with countdown timer in format XX:XX appear on the green button (countdown timer is taken rom "placeBet" response: "confirmationExpectedAt" attribute value + 1)
        EXPECTED: Once time is up, the bet is successfully processed
        """
        betnow_button = self.get_betslip_content().bet_now_button
        betnow_button.click(timeout=0)
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='Log In dialog was not found')
        dialog.username = self.username
        dialog.password = tests.settings.default_password
        dialog.click_login()
        dialog.wait_dialog_closed()
        self.site.close_all_dialogs(async_close=False)
        betnow_button = self.get_betslip_content().bet_now_button
        if betnow_button.is_enabled():
            betnow_button.click(timeout=0)
        result = self.get_betslip_content().bet_now_button.has_spinner_icon(expected_result=True, timeout=3)
        self.assertTrue(result, msg='Spinner not found on Bet Now button')
        timer = self.get_betslip_content().timer
        message = self.get_betslip_content().count_down_message
        self.assertEqual(message, vec.betslip.COUNT_DOWN_TIMER_MESSAGE,
                         msg=f'Notification "{vec.betslip.COUNT_DOWN_TIMER_MESSAGE}" does not appear')
        self.assertTrue(re.match(r'\d{2}:\d{2}', timer), msg=f'Countdown timer "{timer}" has incorrect format. '
                                                             'Expected format: "XX:XX"')
        result = betnow_button.has_spinner_icon(expected_result=False, timeout=self.bir_delay + 3)
        self.assertFalse(result, msg='Spinner has not disappeared from Bet Now button')
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

    def test_005_log_out_from_oxygen_application(self):
        """
        DESCRIPTION: Log out from Oxygen application
        EXPECTED: User is logged out
        """
        self.site.logout()

    def test_006_add_selections_via_deep_link(self):
        """
        DESCRIPTION: Add several selections to the Betslip from any In-Play <Sport> event > Open Betslip
        EXPECTED: Added selections are displayed within Betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.event2_selection_ids[self.event2_team1],
                                                         self.event2_selection_ids[self.event2_team2]))

    def test_007_enter_stake_for_all_singles(self):
        """
        DESCRIPTION: Enter Stake value for all single selections
        EXPECTED: Entered value is displayed in 'Stake' field
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(self.zip_available_stakes(section=singles_section, number_of_stakes=1).items())[0]
        self.enter_stake_amount(stake=stake)

    def test_008_set_BIR_delay_30(self):
        """
        DESCRIPTION: In TI: Add different 'BIR Delay' values applicable to added In-Play <Sport> selections 'BIR Delay' values are added
        EXPECTED: 'BIR Delay' is added
        """
        self.__class__.bir_delay = 30
        self.ob_config.change_market_bir_delay(event_id=self.eventID_2, market_id=self.market2_id,
                                               bir_delay=self.bir_delay)

    def test_009_repeat_step_4(self):
        """
        DESCRIPTION: repeat step 4: Tap 'Log In & Bet' button and login
        """
        self.test_004_login_and_verify_count_down()

    def test_010_logout(self):
        """
        DESCRIPTION: Log out from Oxygen application
        EXPECTED: User is logged out
        """
        self.test_005_log_out_from_oxygen_application()

    def test_011_add_selections_via_deep_link(self):
        """
        DESCRIPTION: Add several selections to the Betslip from any In-Play <Sport> event > Open Betslip
        EXPECTED: Added selections are displayed within Betslip
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(self.event1_selection_ids[self.event1_team1],
                                                         self.event2_selection_ids[self.event2_team1],
                                                         self.event2_selection_ids['Draw']))

    def test_012_enter_stake_for_multiples(self):
        """
        DESCRIPTION: Enter Stake value for multiples selection
        """
        multiples_section = self.get_betslip_sections(multiples=True).Multiples
        stake = list(self.zip_available_stakes(section=multiples_section, number_of_stakes=1).items())[0]
        self.enter_stake_amount(stake=stake)

    def test_013_set_BIR_delay_15(self):
        """
        DESCRIPTION: In TI: Add different 'BIR Delay' values applicable to added In-Play <Sport> selections 'BIR Delay' values are added
        EXPECTED: 'BIR Delay' is added
        """
        self.__class__.bir_delay = 20

        self.ob_config.change_market_bir_delay(event_id=self.eventID_1, market_id=self.market1_id,
                                               bir_delay=self.bir_delay)
        self.ob_config.change_market_bir_delay(event_id=self.eventID_2, market_id=self.market2_id,
                                               bir_delay=self.bir_delay)

    def test_014_repeat_step_4(self):
        """
        DESCRIPTION: repeat step 4: Tap 'Log In & Bet' button and login
        """
        self.test_004_login_and_verify_count_down()
