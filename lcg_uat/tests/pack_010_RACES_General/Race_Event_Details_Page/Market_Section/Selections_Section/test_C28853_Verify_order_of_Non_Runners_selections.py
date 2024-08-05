import voltron.environments.constants as vec
import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # We should confirm and result event
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C28853_Verify_order_of_Non_Runners_selections(BaseRacing):
    """
    TR_ID: C28853
    NAME: Verify order of Non-Runners selections
    DESCRIPTION: This test case verifies order of Non-Runners selections.
    PRECONDITIONS: 1. Make sure you have events with Non-Runners selections:
    PRECONDITIONS: 'Non-Runners' is a selection which contains **'N/R'** text next to it's name
    PRECONDITIONS: For those selections 'outcomeStatusCode'='S' - those selections are always suspended.
    PRECONDITIONS: 2. To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    markets = [('to_finish_second',)]
    number_of_runners = 7
    market_tabs = None
    non_runners_of_win_eachway_market, non_runners_of_to_finish_market = [], []

    def verify_non_runner_selection_within_market(self, market: str) -> None:
        """
        :param market: market name (e.g. 'WIN OR E/W' / 'TOP FINISH' / 'TO FINISH')
        Verifies 'Non-Runners' appearance and order among other runners within defined market
        """
        self.assertIn(market, self.market_tabs.keys(),
                      msg=f'"{market}" market tab is not available in tabs list: \n["{self.market_tabs.keys()}"]')
        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(market)

        event_markets = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(event_markets, msg='No one market section found')
        self.assertIn(market, event_markets, msg=f'No market "{market}" section found in markets list: \n["{event_markets.keys()}"]')

        event_market = event_markets[market]
        market_outcomes_list = event_market.items_as_ordered_dict
        self.assertEqual(len(market_outcomes_list), self.number_of_runners,
                         msg=f'Outcomes quantity "{len(market_outcomes_list)}" is not the same as expected "{self.number_of_runners}"')
        non_runners_order = []
        for horse_name, horse in list(market_outcomes_list.items())[-2:]:
            non_runners_order.append(f'{horse.runner_number} {horse.name}')
            self.assertTrue(horse.is_non_runner, msg=f'"{horse_name}" horse is not greyed-out however it is non runner')
            self.assertFalse(horse.bet_button.is_enabled(expected_result=False),
                             msg=f'\'Price/odds\' button must be disabled for "{horse_name}" market outcome')

        non_runners_order = [item.lstrip(' ') for item in non_runners_order]
        self.assertListEqual(non_runners_order, self.non_runners_of_win_eachway_market if market == vec.racing.RACING_EDP_DEFAULT_MARKET_TAB else self.non_runners_of_to_finish_market,
                             msg=f'Non_runners are not sorted by horse number. \nActual order: "{non_runners_order}" '
                             f'\nExpected: "{self.non_runners_of_win_eachway_market if market == vec.racing.RACING_EDP_DEFAULT_MARKET_TAB else self.non_runners_of_to_finish_market}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create HR event with 2 markets and set some horses as 'Non_Runner'
        """
        event = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=self.number_of_runners, lp=True)
        self.__class__.eventID = event.event_id
        win_or_each_way_market_id = event.market_id

        win_or_each_way_selection_ids = event.selection_ids.get('win_or_each_way')
        to_finish_second_selection_ids = event.selection_ids.get('to_finish_second')

        ss_event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                     query_builder=self.ss_query_builder)
        ss_event_markets = ss_event_details[0]['event']['children']
        market_template_name = \
            list(self.ob_config.horseracing_config.horse_racing_live.autotest_uk.markets.to_finish_second.keys())[0]
        to_finish_second_market_id = None
        for market in ss_event_markets:
            if market['market']['templateMarketName'] == market_template_name.replace('|', ''):
                to_finish_second_market_id = market['market']['id']

        for i in range(2):
            selection_name, selection_id = list(win_or_each_way_selection_ids.items())[i]
            new_selection_name = f'{selection_name} N/R'

            self.ob_config.change_selection_name(selection_id=selection_id, new_selection_name=new_selection_name)
            self.ob_config.result_selection(selection_id=selection_id, market_id=win_or_each_way_market_id,
                                            event_id=self.eventID, result='V')
            self.ob_config.confirm_result(selection_id=selection_id, market_id=win_or_each_way_market_id,
                                          event_id=self.eventID, result='V')
            self.non_runners_of_win_eachway_market.append(selection_name)

            selection_name, selection_id = list(to_finish_second_selection_ids.items())[i]
            new_selection_name = f'{selection_name} N/R'
            self.ob_config.change_selection_name(selection_id=selection_id, new_selection_name=new_selection_name)
            self.ob_config.result_selection(selection_id=selection_id, market_id=to_finish_second_market_id,
                                            event_id=self.eventID, result='V')
            self.ob_config.confirm_result(selection_id=selection_id, market_id=to_finish_second_market_id,
                                          event_id=self.eventID, result='V')
            self.non_runners_of_to_finish_market.append(selection_name)

    def test_001_open_event_details_page(self):
        """
        DESCRIPTION: Open <Race> Event Details page
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        self.__class__.market_tabs = \
            self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(self.market_tabs, msg='No one market tab found')

    def test_002_verify_non_runner_selections_within_win_or_each_way_market(self):
        """
        DESCRIPTION: Verify Non-Runner selections within 'Win or Each Way' market
        EXPECTED: 1.  'Non-Runners' are displayed at the bottom of the outcomes list (below the 'UNNAMED FAVOURITE'/UNNAMED 2nd FAVOURITE' sections)
        EXPECTED: 2.  'Non-Runners' are ordered by Horse/Greyhound Number in ascending
        """
        market = vec.racing.RACING_EDP_DEFAULT_MARKET_TAB
        self.verify_non_runner_selection_within_market(market=market)

    def test_003_verify_non_runner_selections_within_other_markets(self):
        """
        DESCRIPTION: Verify Non-Runner selections within other markets
        EXPECTED: 1.  'Non-Runners' are displayed at the bottom of the outcomes list (below the last selection with a 'Live Price')
        EXPECTED: 2.  'Non-Runners' are ordered by  Horse/Greyhound Number in ascending
        """
        market = vec.racing.TO_FINISH_MARKET_NAME.upper() if self.device_type == 'desktop' and self.brand == 'ladbrokes' else vec.racing.TO_FINISH_MARKET_NAME
        self.verify_non_runner_selection_within_market(market=market)
