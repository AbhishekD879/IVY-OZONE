import pytest
import tests
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import exists_filter, simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.desktop
@vtest
class Test_C2512945_Verify_Bet_Slip_where_Forecast_Tricast_bets_are_NOT_available(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C2512945
    NAME: Verify Bet Slip where 'Forecast'/'Tricast' bets are NOT available
    DESCRIPTION: This test case verifies in what conditions forecast/tricast options will not be available on the Bet Slip
    """
    keep_browser_open = True
    selection_ids, selection_ids_2, selection_ids_3, selection_ids_4 = [], [], [], []
    markets = [('to_finish_second',), ('top_2_finish',)]

    def check_forecast_tricast_bets_are_not_available(self):
        """
        This method retrieves all sections from BetSlip, verifies that it is not empty and fails the test in case
        'FORECASTS/TRICASTS' section is available.
        """
        betslip_sections = self.get_betslip_content().betslip_sections_list
        self.assertTrue(len(betslip_sections) > 0, msg='BetSlip is empty, no sections found')
        name = 'FORECASTS/TRICASTS'
        self.assertNotIn(name, betslip_sections.keys(),
                         msg=f'"{name}" section is available')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        # Selections from the same Race but from different markets

        if tests.settings.backend_env == 'prod':
            additional_filter = exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                                                          ATTRIBUTES.NCAST_TYPE_CODES,
                                                                          OPERATORS.INTERSECTS,
                                                                          'CF,TC')), \
                exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                                          ATTRIBUTES.IS_EACH_WAY_AVAILABLE,
                                                          OPERATORS.IS_TRUE))

            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         expected_template_market='Win or Each Way', number_of_events=3,
                                                         additional_filter=additional_filter)

            for market in events[0]['event']['children']:
                if market['market']['templateMarketName'] == 'Win or Each Way' and market['market'].get('children'):
                    outcomes = market['market']['children']

            self.__class__.selection_ids = list(i['outcome']['id'] for i in outcomes)[0]

            for market in events[1]['event']['children']:
                if market['market']['templateMarketName'] == 'Win or Each Way' and market['market'].get('children'):
                    outcomes2 = market['market']['children']

            self.__class__.selection_ids_2 = list(i['outcome']['id'] for i in outcomes2)[:3]

            for market in events[2]['event']['children']:
                if market['market']['templateMarketName'] == 'Win or Each Way' and market['market'].get('children'):
                    outcomes3 = market['market']['children']

            self.__class__.selection_ids_3 = list(i['outcome']['id'] for i in outcomes3)[:3]

            self.__class__.selection_ids_4 = list(self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id).values())[0]
        else:

            event = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=3,
                                                       forecast_available=True, tricast_available=True)
            self.__class__.selection_ids = [list(selection.values())[0] for selection in list(event.selection_ids.values())]

            # Selections from the same Race and the same market
            event = self.ob_config.add_UK_racing_event(number_of_runners=3, forecast_available=True, tricast_available=True)
            self.__class__.selection_ids_2 = list(event.selection_ids.values())

            for _ in range(3):
                # Selections from different Races
                event = self.ob_config.add_UK_racing_event(number_of_runners=3,
                                                           forecast_available=True, tricast_available=True)
                self.__class__.selection_ids_3.append(list(event.selection_ids.values())[0])

                # Selections from the same Sport market
                event = self.ob_config.add_autotest_premier_league_football_event()
                self.__class__.selection_ids_4.append(list(event.selection_ids.values())[0])

    def test_001_add_two_or_three_selections_from_the_same_race_but_each_from_different_market(self):
        """
        DESCRIPTION: Add two or three selections from the same <Race> but each from different market
        EXPECTED: Selections are added
        """
        self.open_betslip_with_selections(self.selection_ids)

    def test_002_open_bet_slip_and_verify_forecast_tricast_bets(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' bets
        EXPECTED: 'Forecast'/'Tricast' bets are NOT available if selections from different markets are added
        """
        self.check_forecast_tricast_bets_are_not_available()

    def test_003_clear_the_betslip_and_add_two_or_more_selections_from_different_races_to_the_bet_slip(self):
        """
        DESCRIPTION: Clear the Betslip and add two or more selections from different <Races> to the Bet Slip
        EXPECTED: Selections are added to the Bet Slip
        """
        self.clear_betslip()
        self.open_betslip_with_selections(self.selection_ids_3)

    def test_004_open_bet_slip_and_verify_forecast_tricast_bets(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' bets
        EXPECTED: 'Forecast'/'Tricast' bets are NOT available if selections from different events are added
        """
        self.check_forecast_tricast_bets_are_not_available()

    def test_005_clear_the_betslip_and_add_two_or_more_sport_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Clear the Betslip and add two or more <Sport> selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        self.clear_betslip()
        self.open_betslip_with_selections(self.selection_ids_4)

    def test_006_verify_forecast_tricast_bets(self):
        """
        DESCRIPTION: Verify 'Forecast/Tricast' bets
        EXPECTED: 'Forecast/Tricast' bets are NOT available for <Sport> events
        """
        self.check_forecast_tricast_bets_are_not_available()

    def test_007_clear_the_betslip_and_add_two_or_more_sport_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or three selections from the same <Race> from the same market
        EXPECTED: Selections are added
        """
        self.clear_betslip()
        self.open_betslip_with_selections(self.selection_ids_2)

    def test_008_verify_forecast_tricast_bets(self):
        """
        DESCRIPTION: Open Bet Slip and verify 'Forecast'/'Tricast' bets
        EXPECTED: 'Forecast'/'Tricast' bets are NOT available if selections from same markets are added
        """
        self.check_forecast_tricast_bets_are_not_available()
