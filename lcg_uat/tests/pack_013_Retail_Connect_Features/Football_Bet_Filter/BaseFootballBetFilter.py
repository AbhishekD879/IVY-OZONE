from fractions import Fraction

from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from requests import ReadTimeout
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt

import tests
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import do_request


class BaseFootballBetFilter(Common):
    hostname = ''
    proxy = None

    def change_state_of_selection(self, category_name: str, selection_name: str, expected_result=True):
        """
        :param category_name: str
        :param selection_name: str
        :param expected_result: bool
        :return:
        """
        selections = self.site.football_bet_filter.tab_content.items_as_ordered_dict
        self.assertTrue(selections, msg='Can not find any selection')
        category_name = selections.get(category_name)
        selection_names = category_name.items_as_ordered_dict
        selection = selection_names.get(selection_name)
        selection.click()
        selection.is_selected(expected_result=expected_result)

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(ReadTimeout), reraise=False)
    def get_events_for_coupon(self, coupon_name: str) -> list:
        """
        Get all events related to coupon
        :param coupon_name: Name of Coupon
        :return: List of events
        """
        params = (('locale', 'en-GB'),
                  ('statistics', 'true'),
                  ('api-key', tests.settings.retail_coupon_api_key),
                  ('filter', f'coupon.|{coupon_name}|'))
        response = do_request(method='GET', url=tests.settings.retail_coupon_url, params=params)

        coupon = response.get('coupon')
        if not coupon:
            raise SiteServeException('No Available Coupons found')
        events = coupon[0].get('event')
        if isinstance(events, dict):
            return [events]
        else:
            return events

    def get_coupons(self) -> list:
        """
        Get list of active coupons

        :return: list of coupons
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   category_id=self.ob_config.backend.ti.football.category_id,
                                   brand=self.brand)

        basic_active_events_filter = self.ss_query_builder.add_filter(exists_filter(LEVELS.COUPON, simple_filter(
            LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, self.start_date_minus)))

        active_coupons_query = basic_active_events_filter \
            .add_filter(exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME,
                                                                   OPERATORS.GREATER_THAN_OR_EQUAL, self.start_date))) \
            .add_filter(exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED,
                                                                   OPERATORS.IS_FALSE))) \
            .add_filter(simple_filter(LEVELS.COUPON, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(exists_filter(LEVELS.COUPON, simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID,
                                                                   OPERATORS.INTERSECTS,
                                                                   self.ob_config.backend.ti.football.category_id)))
        return ss_req.ss_coupon(query_builder=active_coupons_query)

    def get_all_selections(self, coupon_name) -> list:
        """
        Get all selections related for coupon
        :param coupon_name: Name of Coupon
        :return: list of selections
        """
        selections = []
        events = self.get_events_for_coupon(coupon_name=coupon_name)
        for event in events:
            for selection in event['selection']:
                if selection['type'] != 'draw':
                    selections.append(selection)
        return selections

    def get_selections(self, filters=None, opposition_filters=None, coupon_name='', **kwargs) -> list:
        """
        Get selections related for coupon that fits specific filters
        :param filters: Any filter on Your teams tab
        :param opposition_filters: Any filter on Opposition tab
        :param coupon_name: Name of Coupon
        :return: list of selections
        """
        if opposition_filters is None:
            opposition_filters = []
        if filters is None:
            filters = []
        filtered_selections, filtered = [], []
        selections = self.get_all_selections(coupon_name=coupon_name)
        selections_number = len(selections)

        if 'opp_last_game' in kwargs.keys() and not kwargs['opp_last_game'] == []:
            for index in range(0, selections_number):
                try:
                    if selections[index]['stats']['lastGame'] in kwargs['opp_last_game']:
                        index_to_add = index + (-1) ** index
                        filtered_selections.append(selections[index_to_add])
                except (TypeError, KeyError):
                    pass
            if not filtered_selections:
                return []

        if 'opp_last_6_games' in kwargs.keys() and not kwargs['opp_last_6_games'] == []:
            points_range = self.get_points_range(filters=kwargs['opp_last_6_games'])
            for index in range(0, selections_number):
                try:
                    for interval in points_range:
                        if min(interval) <= int(selections[index]['stats']['last6Games']) <= max(interval):
                            index_to_add = index + (-1) ** index
                            filtered.append(selections[index_to_add])
                except (TypeError, KeyError):
                    pass
            filtered_selections = self.get_distinct_selections(filtered_selections, filtered)
            if not filtered_selections:
                return []

        if 'conceded 2+ last games' in opposition_filters:
            filtered = []
            for index in range(0, selections_number):
                try:
                    if selections[index]['stats']['keyTrendsLastGame'] == 'conceded2+':
                        index_to_add = index + (-1) ** index
                        filtered.append(selections[index_to_add])
                except (TypeError, KeyError):
                    pass
            filtered_selections = self.get_distinct_selections(filtered_selections, filtered)
            if not filtered_selections:
                return []

        if 'high scoring' in opposition_filters:
            filtered = []
            for index in range(0, selections_number):
                try:
                    if selections[index]['stats']['keyTrendsScoring'] == 'highScoring':
                        index_to_add = index + (-1) ** index
                        filtered.append(selections[index_to_add])
                except (TypeError, KeyError):
                    pass
            filtered_selections = self.get_distinct_selections(filtered_selections, filtered)
            if not filtered_selections:
                return []

        if 'leaky defence' in opposition_filters:
            filtered = []
            for index in range(0, selections_number):
                try:
                    if selections[index]['stats']['keyTrendsDefence'] == 'weakDefence':
                        index_to_add = index + (-1) ** index
                        filtered.append(selections[index_to_add])
                except (TypeError, KeyError):
                    pass
            filtered_selections = self.get_distinct_selections(filtered_selections, filtered)
            if not filtered_selections:
                return []

        if 'top half' in opposition_filters or 'bottom half' in opposition_filters:
            if not ('top half' in opposition_filters and 'bottom half' in opposition_filters):
                filtered = []
                try:
                    if 'top half' in opposition_filters:
                        for index in range(0, selections_number):
                            if int(selections[index]['stats']['teamsInLeague']) / int(
                                    selections[index]['stats']['leaguePosition']) > 1:
                                index_to_add = index + (-1) ** index
                                filtered.append(selections[index_to_add])
                    else:
                        for index in range(0, selections_number):
                            if int(selections[index]['stats']['teamsInLeague']) / int(
                                    selections[index]['stats']['leaguePosition']) == 1:
                                index_to_add = index + (-1) ** index
                                filtered.append(selections[index_to_add])
                except (TypeError, KeyError):
                    pass
                filtered_selections = self.get_distinct_selections(filtered_selections, filtered)
                if not filtered_selections:
                    return []

        if 'above opposition' in filters or 'below opposition' in opposition_filters:
            # These 2 filters duplicate each other
            filtered = []
            for index in range(0, selections_number, 2):
                try:
                    if int(selections[index]['stats']['leaguePosition']) < int(
                            selections[index + 1]['stats']['leaguePosition']):
                        filtered.append(selections[index])
                    else:
                        filtered.append(selections[index + 1])
                except (TypeError, KeyError):
                    pass
            filtered_selections = self.get_distinct_selections(filtered_selections, filtered)
            if not filtered_selections:
                return []

        if 'favourite' in filters or 'outsider' in filters:
            filtered, favorites, outsiders = [], [], []
            for index in range(0, selections_number, 2):
                current_selection_odds = Fraction(selections[index]['odds'].replace('-', '/'))
                next_selection_odds = Fraction(selections[index + 1]['odds'].replace('-', '/'))
                if current_selection_odds < next_selection_odds:
                    favorites.append(selections[index])
                    outsiders.append(selections[index + 1])
                if current_selection_odds > next_selection_odds:
                    favorites.append(selections[index + 1])
                    outsiders.append(selections[index])
            if 'favourite' in filters and 'outsider' in filters:
                filtered = favorites + outsiders
            elif 'favourite' in filters:
                filtered = favorites
            else:
                filtered = outsiders
            filtered_selections = self.get_distinct_selections(filtered_selections, filtered)
            if not filtered_selections:
                return []

        if filtered_selections:
            selections = filtered_selections

        if 'clean sheet last game' in filters:
            filtered_selections = []
            for selection in selections:
                try:
                    if selection['stats']['keyTrendsLastGame'] == 'cleanSheet':
                        filtered_selections.append(selection)
                except (TypeError, KeyError):
                    pass
            if not filtered_selections:
                return []
            selections = filtered_selections

        if 'high scoring' in filters:
            filtered_selections = []
            for selection in selections:
                try:
                    if selection['stats']['keyTrendsScoring'] == 'highScoring':
                        filtered_selections.append(selection)
                except (TypeError, KeyError):
                    pass
            if not filtered_selections:
                return []
            selections = filtered_selections

        if 'mean defence' in filters:
            for selection in selections:
                try:
                    if selection['stats']['keyTrendsDefence'] == 'meanDefence':
                        filtered_selections.append(selection)
                except (TypeError, KeyError):
                    pass
            if not filtered_selections:
                return []
            selections = filtered_selections

        if 'last_6_games' in kwargs.keys() and not kwargs['last_6_games'] == []:
            filtered_selections = []
            points_range = self.get_points_range(filters=kwargs['last_6_games'])
            for index in range(0, len(selections)):
                for interval in points_range:
                    try:
                        if min(interval) <= int(selections[index]['stats']['last6Games']) <= max(interval):
                            filtered_selections.append(selections[index])
                    except (TypeError, KeyError):
                        pass
            if not filtered_selections:
                return []
            selections = filtered_selections

        if 'last_game' in kwargs.keys() and not kwargs['last_game'] == []:
            filtered_selections = []
            for index in range(0, len(selections)):
                try:
                    if selections[index]['stats']['lastGame'] in kwargs['last_game']:
                        filtered_selections.append(selections[index])
                except (TypeError, KeyError):
                    pass
            if not filtered_selections:
                return []
            selections = filtered_selections

        if 'home' in filters or 'away' in filters:
            if not ('home' in filters and 'away' in filters):
                if 'home' in filters:
                    selections = list(filter(lambda selection: selection['type'] == 'home', selections))
                else:
                    selections = list(filter(lambda selection: selection['type'] == 'away', selections))
                if not selections:
                    return []

        if 'top half' in filters or 'bottom half' in filters:
            filtered_selections = []
            if not ('top half' in filters and 'bottom half' in filters):
                if 'top half' in filters:
                    for selection in selections:
                        try:
                            if int(selection['stats']['leaguePosition']) <= int(
                                    selection['stats']['teamsInLeague']) / 2:
                                filtered_selections.append(selection)
                        except (TypeError, KeyError):
                            pass
                else:
                    for selection in selections:
                        try:
                            if int(selection['stats']['leaguePosition']) > int(selection['stats']['teamsInLeague']) / 2:
                                filtered_selections.append(selection)
                        except (TypeError, KeyError):
                            pass
                if not filtered_selections:
                    return []
                selections = filtered_selections

        return selections

    def get_distinct_selections(self, filtered_selections, filtered):
        """returns selections which are present in both filtered list"""
        if filtered_selections:
            filtered_selections = [selection for selection in filtered_selections if selection in filtered]
        else:
            filtered_selections = filtered
        return filtered_selections

    def get_points_range(self, filters):
        points_range = []
        if '0 - 6 points' in filters:
            points_range.append([0, 6])
        if '7 - 12 points' in filters:
            points_range.append([7, 12])
        if '13 - 18 points' in filters:
            points_range.append([13, 18])
        return points_range

    def verify_number_of_bets(self, expected_number_of_bets):
        ui_number_of_bets = self.site.football_bet_filter.read_number_of_bets()
        self.assertEqual(ui_number_of_bets, expected_number_of_bets,
                         msg=f'Incorrect number of bets filtered. Actual is [{ui_number_of_bets}], Expected [{expected_number_of_bets}]')

    def calculate_odds(self, odds):
        calculated_odds = 1.00
        for value in odds:
            calculated_odds *= float(Fraction(value) + 1)
        return calculated_odds

    def accumulator_odds(self, odds):
        odds = self.calculate_odds(odds=odds)
        return format(round(odds - 1, 2), '.2f') + '/1'

    def accumulation_sum(self, odds):
        odds = self.calculate_odds(odds=odds)
        return '£' + format(round(odds * 10, 2), '.2f')

    def open_bet_filter_via_coupon(self) -> str:
        """
        Select any coupon that has **couponSortCode** parameter equal to "MR"
        Open bet filter
        :return: str coupon name
        """
        if not self.is_tab_present(tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
                                   category_id=self.ob_config.football_config.category_id):
            raise CmsClientException(f'{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons} tab disabled in CMS.')
        coupons = self.get_coupons()
        coupon_name = next((coupon['coupon']['name'] for coupon in coupons if coupon['coupon']['couponSortCode'] == 'MR'), None)
        if not coupon_name:
            raise SiteServeException('No Available Coupons found')

        self.navigate_to_page('sport/football/coupons')
        self.site.wait_content_state(state_name='Football')

        coupon_groups = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupon_groups, msg='No event groups found on Coupon page')

        all_coupons = {}
        for coupon_group_name, coupon_group in coupon_groups.items():
            coupons = coupon_group.items_as_ordered_dict
            self.assertTrue(coupons, msg=f'No coupons found in {coupon_group_name} group')
            all_coupons.update(coupons)

        self.assertIn(coupon_name, all_coupons,
                      msg=f'"{coupon_name}" is not found in list of coupons "{all_coupons.keys()}"')
        found_coupon = all_coupons.get(coupon_name)
        self.assertTrue(found_coupon, msg=f'Coupon "{coupon_name}" not found in {all_coupons.keys()}')
        found_coupon.click()
        self.site.wait_content_state(state_name='CouponPage')

        self.assertTrue(self.site.coupon.has_bet_filter_link(), msg='Can not find bet filter button')

        bet_filter_location = self.site.coupon.bet_filter_link.location.get('y')
        change_coupons_switchers_location = self.site.coupon.coupon_selector_link.location.get('y')

        # bet filter , change coupons
        bet_filter_location_status = change_coupons_switchers_location > bet_filter_location
        self.assertTrue(bet_filter_location_status, 'bet filter is not in correct position')

        self.site.coupon.bet_filter_link.click()
        self.site.wait_content_state(state_name='FootballBetFilterPage')
        return coupon_name
