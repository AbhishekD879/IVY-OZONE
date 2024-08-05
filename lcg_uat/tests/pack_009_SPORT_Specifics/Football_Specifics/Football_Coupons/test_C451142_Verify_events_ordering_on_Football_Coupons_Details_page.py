from datetime import datetime

import pytest
from crlat_siteserve_client.constants import ATTRIBUTES, OPERATORS, LEVELS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.sports
@pytest.mark.low
@pytest.mark.desktop
@vtest
class Test_C451142_Verify_events_ordering_on_Football_Coupons_Details_page(BaseCouponsTest):
    """
    TR_ID: C451142
    NAME: Verify events ordering on Football Coupons Details page
    DESCRIPTION: This test case verifies events ordering on Football Coupons Details page
    PRECONDITIONS: 1) 2) In order to get an information about particular coupon use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?simpleFilter=event.startTime:lessThan:2017-07-15T09:01:00.000Z&simpleFilter=event.categoryId:intersects:16&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.startTime:greaterThanOrEqual:2017-07-09T21:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2017-07-10T09:01:00.000Z&translationLang=en
    PRECONDITIONS: XXX - coupon's id
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    """
    keep_browser_open = True
    coupon_name = 'UK Coupon'
    active_events_query = None

    def get_event_start_time(self, events: list, competitions: list) -> dict:
        """
        Gets events start times
        :param events: list of events (event is a dictionary with all event attributes)
        :return: return dictionary where key is name and value is event startTime
        """
        if isinstance(competitions, str):
            competitions = (competitions,)
        return {x['event']['name']: x['event']['startTime'] for x in events if x['event']['typeName'] in competitions}

    def get_order_of_events(self, events: list, competitions: list) -> list:
        """
        Having response gets the expected order of events in coupon
        :param events: coupon events
        :param competitions: coupon competitions
        :return: expected order of events in coupon
        """
        event_start_times = self.get_event_start_time(events=events, competitions=competitions)
        event_start_times_converted = []
        for name, start_time in event_start_times.items():
            date_time_obj = datetime.strptime(start_time.split(',')[0], self.ob_format_pattern)
            event_start_times_converted.append((name, date_time_obj.timetuple()))

        expected_order_tuple = sorted(event_start_times_converted, key=lambda x: (x[1], x[0]))
        return [x for x, _ in expected_order_tuple]

    def get_coupons_competitions_display_order(self, coupon_id: (str, int), raise_exceptions: bool = False,
                                               **kwargs) -> list:
        """
        Gets competition display order within given coupon
        :param coupon_id: id of coupon either string or numeric
        :param raise_exceptions: True or False
        :param kwargs:
        :return: sorted by classDisplayOrder and typeDisplayOrder list of competitions
        """
        resp = self.ss_req_football.ss_coupon_to_outcome_for_coupon(
            coupon_id=coupon_id,
            query_builder=self.active_events_query)

        coupon_events = [x for x in resp[0]['coupon']['children']]

        leagues = []
        for coupon in coupon_events:
            if coupon['event']['typeName'] not in leagues:
                leagues.append((coupon['event']['typeName'],
                                coupon['event']['classDisplayOrder'],
                                coupon['event']['typeDisplayOrder']))

        leagues = list(set(leagues))

        ordered = []
        for league in reversed(sorted(leagues, key=lambda sub: (sub[1], sub[2]))):
            ordered.append(league[0])

        return ordered

    def test_001_add_events_to_uk_coupon(self):
        """
        DESCRIPTION: Add events to UK Coupon
        """
        epl_event_id = self.ob_config.add_football_event_to_england_premier_league().event_id
        market_short_name = self.ob_config.football_config. \
            england.premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        epl_match_result_market_id = self.ob_config.market_ids[epl_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=epl_match_result_market_id, coupon_name=self.coupon_name)

        start_time = self.get_date_time_formatted_string(hours=2)
        epl_event_id2 = self.ob_config.add_football_event_to_england_premier_league(start_time=start_time).event_id
        epl_match_result_market_id2 = self.ob_config.market_ids[epl_event_id2][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=epl_match_result_market_id2, coupon_name=self.coupon_name)

        championship_event_id = self.ob_config.add_football_event_to_england_championship().event_id
        market_short_name = self.ob_config.football_config. \
            england.championship.market_name.replace('|', '').replace(' ', '_').lower()
        championship_match_result_market_id = self.ob_config.market_ids[championship_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=championship_match_result_market_id, coupon_name=self.coupon_name)

        self.__class__.active_events_query = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID,
                                      OPERATORS.INTERSECTS, self.ob_config.backend.ti.football.category_id))

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_002_tap_football_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: 'MATCHES' tab is opened by default and highlighted
        """
        self.site.open_sport(name='FOOTBALL')

    def test_003_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'COUPONS' tab
        EXPECTED: * 'COUPONS' tab is selected and highlighted
        EXPECTED: * Coupons Landing page is loaded
        EXPECTED: * List of coupons is displayed on the Coupons Landing page
        """
        self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is "{current_tab}" but "{self.coupon_tab_name}" is expected to be active')

    def test_004_navigate_to_uk_coupon(self):
        """
        DESCRIPTION: Navigate to UK Coupon
        EXPECTED: Events for selected coupon are displayed on Coupons Details page
        """
        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=self.coupon_name)

    def test_005_verify_competition_accordions_order(self):
        """
        DESCRIPTION: Verify competition accordions order
        EXPECTED: Accordions are ordered by coupons **classDisplayOrder** and **typeDisplayOrder** in ascending
        """
        self.__class__.sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No event groups found on Coupon page')
        competitions_list = list(self.sections.keys())

        self.__class__.ss_req_football = SiteServeRequests(env=tests.settings.backend_env,
                                                           brand=self.brand,
                                                           category_id=self.ob_config.backend.ti.football.category_id)
        if self.brand != 'ladbrokes' or self.device_type == 'desktop':
            competitions_disp_order = [competition.upper() for competition in
                                       self.get_coupons_competitions_display_order(
                                           coupon_id=self.ob_config.backend.ti.football.coupons[self.coupon_name])]
        else:
            competitions_disp_order = [competition for competition in
                                       self.get_coupons_competitions_display_order(
                                           coupon_id=self.ob_config.backend.ti.football.coupons[self.coupon_name])]

        self.assertEqual(competitions_list, competitions_disp_order,
                         msg=f'Competition order "{competitions_list}" '
                         f'is not the same as expected "{competitions_disp_order}"')

    def test_006_verify_events_order_in_the_accordions(self):
        """
        DESCRIPTION: Verify events order in the accordions
        EXPECTED: Events are ordered in the following way:
        EXPECTED: * startTime - chronological order in the first instance
        EXPECTED: * Event displayOrder in ascending
        EXPECTED: * Alphabetical order in ascending (in case of the same 'startTime')
        """
        premier_league = 'PREMIER LEAGUE' if self.brand != 'ladbrokes' or self.device_type == 'desktop' else 'Premier League'

        resp = self.ss_req_football.ss_coupon_to_outcome_for_coupon(
            coupon_id=self.ob_config.backend.ti.football.coupons[self.coupon_name],
            query_builder=self.active_events_query)
        coupon_events = [x for x in resp[0]['coupon']['children']]
        expected_order = self.get_order_of_events(events=coupon_events, competitions='Premier League')
        order_of_events_on_page = []
        self.assertTrue(self.sections, msg='No Competitions found on Coupon details page')
        self.assertIn(premier_league, self.sections,
                      msg=f'"{premier_league}" is not found in competitions list "{self.sections.keys()}"')
        date_groups = self.sections.get(premier_league).items_as_ordered_dict
        self.assertTrue(date_groups, msg='No date groups found in section')
        for date_name, date_group in date_groups.items():
            events = date_group.items_as_ordered_dict
            self.assertTrue(self.sections, msg='No Competitions found on Coupon details page')
            for event_name, events in events.items():
                order_of_events_on_page.append(event_name)
        self._logger.debug(f'*** Order of events on page "{order_of_events_on_page}"')
        self._logger.debug(f'*** Expected order of events on page "{expected_order}"')
        self.assertListEqual(order_of_events_on_page, expected_order)
