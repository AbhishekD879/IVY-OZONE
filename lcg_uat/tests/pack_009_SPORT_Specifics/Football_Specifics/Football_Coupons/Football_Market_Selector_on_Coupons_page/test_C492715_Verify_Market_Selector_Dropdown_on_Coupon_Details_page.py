import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.market_selector
@pytest.mark.markets
@pytest.mark.ob_smoke
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C492715_Verify_Market_Selector_Dropdown_on_Coupon_Details_page(BaseCouponsTest, BaseSportTest):
    """
    TR_ID: C492715
    NAME: Verify Market Selector Dropdown on Coupon Details page
    DESCRIPTION: This test case verifies Market selector drop down on Coupon Details page
    """
    keep_browser_open = True

    first_event_markets = [
        ('both_teams_to_score', {'cashout': True}),
        ('match_result_and_both_teams_to_score', {'cashout': True}),
        ('over_under_total_goals', {'cashout': True})]

    second_event_markets = [
        ('draw_no_bet', {'cashout': True}),
        ('first_half_result', {'cashout': True}),
        ('to_win_to_nil', {'cashout': True}),
        ('score_goal_in_both_halves', {'cashout': True})]

    event_match_result_name, event_diff_markets_name = None, None

    def get_market_name_and_headers(self, market_name, fixture_header_1=None, fixture_header_2=None, fixture_header_3=None):
        cms_markets = self.cms_config.get_coupon_market_selector_markets()
        for item in cms_markets:
            if market_name == item['templateMarketName']:
                if item['header']:
                    for header in item['header']:
                        fixture_header_1 = header[0]
                        fixture_header_2 = header[1]
                        if len(header) > 2:
                            fixture_header_3 = header[2]
                market_name = item['title']
                break
        return market_name, fixture_header_1, fixture_header_2, fixture_header_3

    def test_000_preconditions(self):
        """
        DESCRIPTION: Adds football event with a coupon
        """
        # Event with 'Match Betting', 'Both Teams to Score', 'To Win not to Nil' and 'Over Under Total Goals' markets
        first_event = self.ob_config.add_autotest_premier_league_football_event(markets=self.first_event_markets)
        self.__class__.eventID = first_event.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.first_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.add_event_to_coupon(market_id=self.ob_config.market_ids[self.eventID][market_short_name],
                                           coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)
        for market in self.first_event_markets:
            self.ob_config.add_event_to_coupon(
                market_id=self.ob_config.market_ids[self.eventID][market[0]],
                coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)

        # Event with 'Draw no Bet', 'First Half Result', 'To Win to Nil', 'Score Goal in both Halves'
        # and 'Both Teams to Score' markets
        second_event = self.ob_config.add_autotest_premier_league_football_event(
            markets=self.second_event_markets)
        self.__class__.eventID2 = second_event.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID2,
                                                               query_builder=self.ss_query_builder)
        self.__class__.second_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        for market in self.second_event_markets:
            self.ob_config.add_event_to_coupon(
                market_id=self.ob_config.market_ids[self.eventID2][market[0]],
                coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)

        self.__class__.markets_selections = []
        self.__class__.all_markets = self.first_event_markets + self.second_event_markets
        for market in self.all_markets:
            if market[0] == 'first_half_result':
                self.__class__.markets_selections.append(
                    {'market_name': getattr(vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES, market[0]),
                     'expected_odds': 3,
                     'expected_event_id': self.eventID2})
            elif market[0] == 'match_result_and_both_teams_to_score':
                self.__class__.markets_selections.append(
                    {'market_name': getattr(vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES, market[0]),
                     'expected_odds': 3,
                     'expected_event_id': self.eventID})
                self.first_event_markets.remove(market)
            elif market in self.first_event_markets:
                self.__class__.markets_selections.append(
                    {'market_name': getattr(vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES, market[0]),
                     'expected_odds': 2,
                     'expected_event_id': self.eventID})
            else:
                self.__class__.markets_selections.append(
                    {'market_name': getattr(vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES, market[0]),
                     'expected_odds': 2,
                     'expected_event_id': self.eventID2})

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_001_load_oxygen_application_and_navigate_to_football_coupon_details_page(self):
        """
        DESCRIPTION: Navigate to UK Coupon
        EXPECTED: Events for selected coupon are displayed on Coupons Details page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')
        self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is "{current_tab}" but "{self.coupon_tab_name}" is expected to be active')
        self.find_coupon_and_open_it(coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)

    def test_002_verify_displaying_of_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify displaying of the Market selector drop down
        EXPECTED: * The Market Selector displayed below the Coupon sub-header and above the First accordion on the page
        EXPECTED: * Match Result is selected by default in Market selector drop down
        EXPECTED: * Market: is shown in front of market name
        """
        self.assertTrue(self.site.coupon.tab_content.has_dropdown_market_selector(), msg='Coupon doesn\'t have market selector')

    def test_003_verify_options_available_for_football_in_the_market_selector_drop_down(self):
        """
        DESCRIPTION: Verify options available for Football in the Market selector drop down:
        EXPECTED: The following markets are shown in the Market selector drop down in the order listed below:*
        EXPECTED: * Match Result
        EXPECTED: * Both Teams to Score
        EXPECTED: * Total Goals Over/ Under 1.5
        EXPECTED: * To Win & Both Teams to Score
        EXPECTED: * Draw No Bet
        EXPECTED: * 1st Half Result
        EXPECTED: * To Win To Nil
        EXPECTED: * Goal in Both Halves
        """
        markets_in_dropdown = self.site.coupon.tab_content.dropdown_market_selector.available_options

        expected_market_names = [self.cms_config.get_coupon_market_name_and_headers(
            vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.match_result).market_name]
        for market in self.all_markets:
            market_template = getattr(vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES, market[0])
            expected_market_names.append(self.cms_config.get_coupon_market_name_and_headers(market_template).market_name)

        for market in expected_market_names:
            self.assertIn(market, markets_in_dropdown,
                          msg=f'"{market}" market cannot be found in {markets_in_dropdown} markets list')

    def test_004_select_match_results_in_the_market_selector_drop_down(self, market_template=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.match_result,
                                                                       expected_odds_quantity=3,
                                                                       expected_event_id=None):
        """
        DESCRIPTION: Select 'Match Results' in the Market selector drop down
        EXPECTED: The events for selected market are shown
        EXPECTED: Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        expected_event_id = self.eventID if expected_event_id is None else expected_event_id
        market_name = self.cms_config.get_coupon_market_name_and_headers(market_template).market_name
        try:
            option_item = self.site.coupon.tab_content.dropdown_market_selector.items_as_ordered_dict[market_name]
        except Exception:
            option_item = self.site.coupon.tab_content.dropdown_market_selector.items_as_ordered_dict[market_name]
        option_item.click()
        event = self.get_event_from_league(event_id=expected_event_id,
                                           section_name=self.section_name,
                                           raise_exceptions=False)
        self.assertTrue(event, msg=f'"{expected_event_id}" cannot be found with selected "{market_name}" market')

        quantity_of_selections = len(list(filter(lambda x: x, event.get_active_prices().values())))
        self.softAssert(self.assertEqual, quantity_of_selections, expected_odds_quantity,
                        msg=f'Actual quantity of selections: "{quantity_of_selections}" '
                        f'is not equal to expected: "{expected_odds_quantity}" for "{market_name}" market')

    def test_005_repeat_previous_step_for_next_markets(self):
        """
        DESCRIPTION: Repeat previous step for next markets:
        DESCRIPTION: Both Teams to Score, Total Goals Over/ Under 1.5, To Win & Both Teams to Score, Draw No Bet
        DESCRIPTION: 1st Half Result, To Win To Nil, Goal in Both Halves
        """
        for market in self.markets_selections:
            self.test_004_select_match_results_in_the_market_selector_drop_down(market_template=market['market_name'],
                                                                                expected_odds_quantity=market['expected_odds'],
                                                                                expected_event_id=market['expected_event_id'])
