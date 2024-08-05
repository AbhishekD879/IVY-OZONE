import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.open_bets
@pytest.mark.uat
@pytest.mark.p1
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.stg2
@pytest.mark.tst2
@vtest
class Test_C44870211_Preplay_Racing_Bet_placement_(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C44870211
    NAME: Preplay Racing Bet placement "
    DESCRIPTION: "Customer places a single , Forecast and Tricast bet on HR and GH race
    DESCRIPTION: Verify display of forecast/tricast in the betslip
    DESCRIPTION: - selection name
    DESCRIPTION: - 1st/2nd/3rd where appropriate
    DESCRIPTION: - event name"
    PRECONDITIONS: UserName: goldenbuild1 Password: password1
    """
    keep_browser_open = True

    def tricast_forecast_bet_placement(self, racing_type, forecast, tricast, market_name):
        self.navigate_to_edp(event_id=self.eventID, sport_name=racing_type)
        self.place_forecast_tricast_bet_from_event_details_page(sport_name=racing_type, forecast=forecast, tricast=tricast)
        self.site.open_betslip()
        self.__class__.sections = self.get_betslip_sections().Singles
        stake_name, stake = list(self.sections.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        self.test_005_verify_selection_details_in_betslip(market_name=market_name)
        self.test_006_verify_tapping_on_place_bet_bet_is_placed(market_name=market_name)

    def create_or_get_events_with_markets(self, racing_type):
        """
        DESCRIPTION: Create events with markets: Eachway, forecast, tricast.
        EXPECTED: Event is created as required.
        """
        if racing_type == 'horse-racing':
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=6,
                                                              forecast_available=True, tricast_available=True)
        else:
            event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=6,
                                                                        forecast_available=True, tricast_available=True)
        self.__class__.event_start_time = event_params.event_date_time
        self.__class__.selection_ids = event_params.selection_ids
        self.__class__.eventID = event_params.event_id
        start_time_local = self.convert_time_to_local(date_time_str=self.event_start_time)
        if racing_type == 'horse-racing':
            self.__class__.created_event_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time_local}'
        else:
            self.__class__.created_event_name = f'{self.greyhound_autotest_name_pattern} {start_time_local}'
        self.__class__.selection_names = self.selection_ids.keys()
        self.__class__.runner_name = list(event_params.selection_ids.keys())[0]
        self.__class__.event_off_time = event_params.event_off_time
        if racing_type == 'horse-racing':
            self.__class__.event_name = f"{self.event_off_time} {self.horseracing_autotest_uk_name_pattern}"
        else:
            self.__class__.event_name = f"{self.event_off_time} {self.greyhound_autotest_name_pattern}"
        self.__class__.selection_ids = list(event_params.selection_ids.values())[0]

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: HomePage is displayed
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

    def test_002_go_to_hrgh_racing(self, racing_type='horse-racing'):
        """
        DESCRIPTION: Go to HR/GH racing
        EXPECTED: Racing landing page opened
        """
        self.create_or_get_events_with_markets(racing_type)
        self.navigate_to_page(racing_type)
        self.site.wait_content_state(racing_type)

    def test_003_click_on_any_event_meeting(self, racing_type='horse-racing'):
        """
        DESCRIPTION: Click on any event meeting
        EXPECTED: Race card page opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name=racing_type)

    def test_004_make_a_selection_from_win_each_way_market(self):
        """
        DESCRIPTION: Make a selection from Win each way market
        EXPECTED: Selection added to betsip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.sections = self.get_betslip_sections().Singles
        stake_name, stake = list(self.sections.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section[self.runner_name]
        stake.each_way_checkbox.click()
        self.assertTrue(stake.each_way_checkbox.is_displayed(), msg='Each way check box is not displayed')
        # reset betslip counter
        self.__class__.expected_betslip_counter_value = 0

    def test_005_verify_selection_details_in_betslip(self, market_name="Win or Each Way"):
        """
        DESCRIPTION: Verify selection details in betslip
        EXPECTED: Event Name
        EXPECTED: Market Name
        EXPECTED: Meeting time
        EXPECTED: Odds
        EXPECTED: Stake box
        EXPECTED: Potential returns
        EXPECTED: EW box
        EXPECTED: Total stake
        EXPECTED: Total potential returns
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.ordered_collection.values())[0]
        self.assertEqual(stake.market_name, market_name,
                         msg=f'Market name "{stake.market_name}" is not the same as expected "{market_name}"')
        self.assertEqual(stake.event_name, self.event_name,
                         msg=f'Event name "{stake.event_name}" is not the same as expected "{self.event_name}"')
        self.assertTrue(stake.amount_form.has_amount_input(), msg='Amount input is not displayed')
        self.assertEqual(stake.odds, 'SP', msg=f'Stake Odds "{stake.odds}" is not SP')
        self.assertEqual(stake.est_returns, 'N/A', msg=f'Stake Est. Returns "{stake.est_returns}" is not N/A')
        total_stake = self.get_betslip_content().total_stake
        self.assertTrue(total_stake, msg='Total Stake is not displayed')

    def test_006_verify_tapping_on_place_bet_bet_is_placed(self, market_name="Win or Each Way"):
        """
        DESCRIPTION: Verify tapping on 'Place bet' bet is placed
        EXPECTED: Bet is placed
        EXPECTED: Betslip appear with details
        EXPECTED: Single@x/x
        EXPECTED: Receipt No:
        EXPECTED: Meeting name
        EXPECTED: Market name / Meeting time & name
        EXPECTED: Cashout - if applicable
        EXPECTED: Stake for this bet
        EXPECTED: Potential returns
        EXPECTED: Total stake
        EXPECTED: Total potential returns
        EXPECTED: Resure selection & G Betting tab
        """
        betnow_btn = self.get_betslip_content().bet_now_button
        betnow_btn.click()
        self.check_bet_receipt_is_displayed()
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')
        receipt_bet_type_section = receipt_sections.get('Single')
        section_items = receipt_bet_type_section.items_as_ordered_dict
        self.assertTrue(section_items, msg='No bets found in BetReceipt')
        bet_info = list(section_items.values())[0]
        self.assertTrue(bet_info.bet_id, msg="Bet Id not found")
        self.assertIn(market_name, bet_info.event_market_name, msg=f'Market placed "{market_name}" does not match with bet receipt"{bet_info.event_market_name}"')
        self.assertEqual(self.event_name, bet_info.event_name, msg=f'Event placed "{self.event_name}" does not match with bet receipt"{bet_info.event_name}"')
        self.assertTrue(bet_info.estimate_returns, msg=f'"{vec.quickbet.TOTAL_EST_RETURNS_LABEL}" is not displayed')
        self.assertTrue(bet_info.total_stake, msg=f'"{vec.quickbet.TOTAL_STAKE_LABEL_RECEIPT}" not found')

    def test_007_repeat_steps_4_to_8_for_forecast_and_tricast_bets(self, racing_type='horse-racing'):
        """
        DESCRIPTION: Repeat steps #4 to #8 for forecast and tricast bets
        EXPECTED:
        """
        self.tricast_forecast_bet_placement(racing_type=racing_type, forecast=True, tricast=False, market_name="Forecast")
        self.tricast_forecast_bet_placement(racing_type=racing_type, forecast=False, tricast=True, market_name="Tricast")

    def test_008_for_greyhound_racing(self, racing_type='greyhound-racing'):
        self.test_002_go_to_hrgh_racing(racing_type=racing_type)
        self.test_003_click_on_any_event_meeting(racing_type=racing_type)
        self.test_004_make_a_selection_from_win_each_way_market()
        self.test_005_verify_selection_details_in_betslip()
        self.test_006_verify_tapping_on_place_bet_bet_is_placed()
        self.test_007_repeat_steps_4_to_8_for_forecast_and_tricast_bets(racing_type=racing_type)
