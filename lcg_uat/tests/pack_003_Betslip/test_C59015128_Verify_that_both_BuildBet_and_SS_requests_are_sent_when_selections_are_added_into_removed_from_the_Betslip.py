import json
import pytest
import tests
from random import choice
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can not create events in prod/beta
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59015128_Verify_that_both_BuildBet_and_SS_requests_are_sent_when_selections_are_added_into_removed_from_the_Betslip(BaseSportTest, BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C59015128
    NAME: Verify that both BuildBet and SS requests are sent when selections are added into/removed from the Betslip
    DESCRIPTION: Test case verifies presence(usage) of both SS and BPP requests when selection-oriented actions such as selections 'adding into/removing from' Betslip are executed for certain pages(sports/races).
    PRECONDITIONS: * 'Virtual' sport with at least 2 upcoming events should be present
    PRECONDITIONS: * 'Scorecast' market should be present for the upcoming Football event
    PRECONDITIONS: * 'Forecast'/'Tricast' market should be present for the upcoming <Race> event
    PRECONDITIONS: * Upcoming <Sport>/<Race> event with at least 2 active selections should be present
    PRECONDITIONS: * Oxygen app should be opened
    PRECONDITIONS: * User should be logged in
    PRECONDITIONS: * QuickBet should be disabled for mobile responsive mode
    PRECONDITIONS: DevTools should be opened (Click on 'Inspect') -> 'Network' tab -> 'XHR' filter
    """
    keep_browser_open = True
    headers = {'Content-Type': 'application/json'}
    team_result = '1'
    prices = {0: '1/2', 1: '1/3'}

    def get_build_bet_request_data(self):

        url = f'{tests.settings.BETTINGMS}v1/buildBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
        post_data = placebet_request.get('postData')
        self.assertTrue(post_data, msg='Post Data is not found in placeBet request')
        legs = post_data.get('leg')
        self.assertTrue(legs, msg='No Legs found in placeBet request')
        for leg in legs:
            sports_leg = leg.get('sportsLeg')
            self.assertTrue(sports_leg, msg='No sportsLeg found in placeBet request')
            price = sports_leg.get('price')
            self.assertTrue(price, msg='No price found in placeBet request')
            price_type_ref = price.get('priceTypeRef')
            self.assertTrue(price_type_ref, msg='No priceTypeRef found in placeBet request')
        data = json.dumps(post_data)
        req = do_request(url=url, data=data, headers=self.headers)
        self.__class__.event_ids = []
        self.__class__.outcome_details = req['outcomeDetails']
        for outcome in self.outcome_details:
            ss_request = self.ss_req.ss_event_to_outcome_for_event(event_id=outcome['eventId'])
            ss_event = ss_request[0]['event']
            self.event_ids.append(ss_event['id'])

    def test_001_navigate_to_virtuals_page(self):
        """
        DESCRIPTION: Navigate to 'Virtuals' page
        EXPECTED: Page contains event(s)/list(s) of markets with selections
        """
        events = self.get_active_event_for_class(class_id=self.ob_config.virtuals_config.virtual_football.class_id,
                                                 raise_exceptions=False)
        if events is None:
            self.__class__.bet_amount = 0.10
            events = self.get_active_event_for_class(
                class_id=self.ob_config.virtuals_config.pt_virtual_football.class_id)
        event = choice(events)
        selections = next(((market['market']['children']) for market in event['event']['children'] if
                           market['market'].get('children')), None)
        if not selections:
            raise SiteServeException('There are no available selections')

        selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in selections}

        selections2 = next(((market['market']['children']) for market in events[1]['event']['children'] if
                            market['market'].get('children')), None)
        if not selections2:
            raise SiteServeException(f'Can not find any selection')

        selection_ids2 = {i['outcome']['name']: i['outcome']['id'] for i in selections2}
        self.__class__.selection_ids_all_events_football = [list(selection_ids.values())[0],
                                                            list(selection_ids2.values())[1]]
        self._logger.info(f'*** Found Virtual Football outcomes "{self.selection_ids_all_events_football}"')

        # creating event with Scorecast market
        event1 = self.ob_config.add_autotest_premier_league_football_event(markets=[('scorecast', {'cashout': True})])
        self.__class__.eventID = event1.event_id
        self.__class__.team1 = event1.team1
        self.__class__.team2 = event1.team2
        list(event1.selection_ids['first_goalscorer'].values())
        self.__class__.home_selection_id = list(event1.selection_ids['first_goalscorer'].values())[0]
        self.__class__.away_selection_id = list(event1.selection_ids['first_goalscorer'].values())[1]
        self.__class__.draw_selection_id = list(event1.selection_ids['first_goalscorer'].values())[2]

        # creating event with forecast market
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=self.prices,
                                                          forecast_available=True)
        event_start_time = event_params.event_date_time
        start_time_local = self.convert_time_to_local(date_time_str=event_start_time)
        event_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time_local}'
        self.__class__.event_id2 = event_params.event_id
        self.__class__.selection_ids = list(event_params.selection_ids.values())
        self._logger.info(
            f'*** Created Horse Racing Forecast/Tricast event "{event_name}" with id "{self.event_id2}"')

    def test_002_add_2_selections_into_betslip(self):
        """
        DESCRIPTION: Add 2 selections into Betslip
        EXPECTED: * BuildBet requests are sent to BPP
        EXPECTED: * Second request contains bet data regarding the price, status, etc. of both selections
        EXPECTED: * SS requests (filtered by 'Simple') with event IDs that contain added selections are also sent
        EXPECTED: ![](index.php?/attachments/get/113549250)
        EXPECTED: ![](index.php?/attachments/get/113549247)
        EXPECTED: ![](index.php?/attachments/get/113549251)
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids_all_events_football)
        self.get_build_bet_request_data()

    def test_003_click_on_x_button_to_remove_any_selection(self):
        """
        DESCRIPTION: Click on 'X' button to remove any selection
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains remaining selection is also sent
        EXPECTED: ![](index.php?/attachments/get/113549253)
        EXPECTED: ![](index.php?/attachments/get/113549252)
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='*** No stakes found')
        self.stake = list(singles_section.values())[0]
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip was not opened')
        self.stake.remove_button.click()
        self.get_build_bet_request_data()
        self.assertNotIn(self.selection_ids_all_events_football, self.event_ids,
                         msg='removed selection is present in SS request')

    def test_004_open_edp_of_the_football_event_that_has_a_configured_scorecast_market_with_active_selections(self):
        """
        DESCRIPTION: Open EDP of the Football event that has a configured 'Scorecast' market with active selections
        EXPECTED: * Page contains market dropdowns with selections
        EXPECTED: * 'Scorecast' market dropdown is present under 'ALL MARKETS' tab
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state(state_name='EventDetails')
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No markets are shown')
        self.__class__.scorecast = self.markets.get(self.expected_market_sections.scorecast)
        self.assertTrue(self.scorecast, msg='SCORECAST section is not found')
        self.scorecast.expand()

    def test_005_form_a_scorecast_selection_and_tap_on_its_buttonadd_it_to_betslip(self):
        """
        DESCRIPTION: Form a 'Scorecast' selection and tap on its button(add it to Betslip)
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * BuildBet request contains bet data regarding the price, status, etc. of the selections
        EXPECTED: * SS request (filtered by 'Simple') with event ID that contains added selection is also sent
        EXPECTED: ![](index.php?/attachments/get/113549259)
        EXPECTED: ![](index.php?/attachments/get/113549267)
        """
        self.scorecast.home_team_results_dropdown.select_value(self.team_result)
        self.scorecast.away_team_results_dropdown.select_value(self.team_result)
        self.scorecast.player_scorers_list.select_player_by_index(index=2)
        player = self.scorecast.player_scorers_list.selected_item

        self.__class__.expected_outcome_name = f'{player}, Draw {self.team_result}-{self.team_result}'
        self.__class__.output_price = self.scorecast.output_price
        self._logger.debug(f'*** Output price for player "{player}" is: "{self.output_price}"')
        sleep(2)
        self.assertTrue(self.scorecast.add_to_betslip.is_enabled(expected_result=True),
                        msg='"Odds calculation" button is not active')
        self.scorecast.add_to_betslip.click()
        self.assertTrue(self.scorecast.add_to_betslip.is_selected(),
                        msg='"Odds calculation" button is not highlighted in green')
        self.get_build_bet_request_data()

    def test_006_open_edp_of_the_event_that_has_at_least_2_active_selections(self):
        """
        DESCRIPTION: Open EDP of the event that has at least 2 active selections
        EXPECTED: Page contains market dropdown(s) with selections
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_007_add_1st_active_selection_into_betslip_and_suspend_it_through_ti(self):
        """
        DESCRIPTION: Add 1st active selection into Betslip and suspend it through TI
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Request contains bet data regarding the price, status, etc. of the remaining selection
        EXPECTED: * SS request(filtered by 'Simple') with event ID that contains removed selection is NOT sent
        EXPECTED: ![](index.php?/attachments/get/113549279)
        """
        sleep(2)
        self.open_betslip_with_selections(selection_ids=(self.home_selection_id, self.away_selection_id))
        self.ob_config.change_selection_state(selection_id=self.home_selection_id, displayed=False)
        self.get_build_bet_request_data()
        self.assertNotIn(self.home_selection_id, self.event_ids,
                         msg='removed selection is present in SS request')
        self.assertIn(self.eventID, self.event_ids,
                      msg='added selection is not present in SS request')

    def test_008_add_2nd_active_selection_into_betslip(self):
        """
        DESCRIPTION: Add 2nd active selection into Betslip
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * Second request contains bet data regarding the price, status, etc. of both selections
        EXPECTED: * SS request (filtered by 'SS') with event IDs that contain added selections is also sent
        EXPECTED: ![](index.php?/attachments/get/113549286)
        EXPECTED: ![](index.php?/attachments/get/113549288)
        """
        # covered in step 007

    def test_009_open_edp_of_the_race_event_that_has_a_configured_forecasttricast_market_with_active_selections(self):
        """
        DESCRIPTION: Open EDP of the <Race> event that has a configured 'Forecast'/'Tricast' market with active selections
        EXPECTED: * Page contains market tab(s) with selections list(s)
        EXPECTED: * 'Forecast'/'Tricast' market tab is present in the markets lane(tabs lane)
        """
        self.navigate_to_edp(event_id=self.event_id2, sport_name='horse-racing')
        self.site.wait_content_state('RacingEventDetails')
        self.__class__.sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='*** No one section was found')

    def test_010_form_a_forecasttricast_selection_and_tapclick_on_add_to_betslip_button(self):
        """
        DESCRIPTION: Form a 'Forecast'/'Tricast' selection and tap/click on 'Add to Betslip' button
        EXPECTED: * BuildBet request is sent to BPP
        EXPECTED: * BuildBet request contains bet data regarding the price, status, etc. of the selections
        EXPECTED: * SS request (filtered by 'Simple') with event ID that contains added selection is also sent
        EXPECTED: ![](index.php?/attachments/get/113549305)
        EXPECTED: ![](index.php?/attachments/get/113549300)
        """
        self.place_forecast_tricast_bet_from_event_details_page(forecast=True,
                                                                any_button=True)
        self.site.open_betslip()
        self.get_build_bet_request_data()
