import pytest
import tests
import voltron.environments.constants as vec
from collections import namedtuple
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.fixture_header
@pytest.mark.market_selector
@pytest.mark.markets
@pytest.mark.ob_smoke
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C493191_Verify_Fixture_Header_on_Coupon_Details_page(BaseCouponsTest):
    """
    TR_ID: C493191
    NAME: Verify Fixture Header on Coupon Details page
    DESCRIPTION: This test case verifies Fixture Header on Coupon Details page
    """
    keep_browser_open = True

    event_markets = [
        ('both_teams_to_score', {'cashout': True}),
        ('over_under_total_goals', {'cashout': True}),
        ('draw_no_bet', {'cashout': True}),
        ('first_half_result', {'cashout': True}),
        ('to_win_to_nil', {'cashout': True}),
        ('score_goal_in_both_halves', {'cashout': True}),
        ('match_result_and_both_teams_to_score', {'cashout': True})
    ]

    event_match_result_name, event_diff_markets_name = None, None

    def get_market_name_and_headers(self, market_name, fixture_header_1=None, fixture_header_2=None, fixture_header_3=None):
        market_name_and_headers_to_return = namedtuple('name_and_headers', ['market_name', 'fixture_header_1',
                                                                            'fixture_header_2', 'fixture_header_3'])
        market_name, market_headers = self.cms_config.get_coupon_market_name_and_headers(market_name)
        if market_headers:
            fixture_header_1 = market_headers[0].upper()
            fixture_header_2 = market_headers[1].upper()
            if len(market_headers) > 2:
                fixture_header_3 = market_headers[2].upper()

        return market_name_and_headers_to_return(market_name=market_name, fixture_header_1=fixture_header_1,
                                                 fixture_header_2=fixture_header_2, fixture_header_3=fixture_header_3)

    def select_market_and_get_event_section(self, market_name):
        if self.brand != 'ladbrokes' or self.device_type == 'desktop':
            self.__class__.league_name = tests.settings.football_autotest_competition_league
        else:
            self.__class__.league_name = tests.settings.football_autotest_competition_league.title()
        try:
            option_item = self.site.coupon.tab_content.dropdown_market_selector.items_as_ordered_dict[market_name]
        except Exception:
            option_item = self.site.coupon.tab_content.dropdown_market_selector.items_as_ordered_dict[market_name]
        option_item.click()
        sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        if not sections:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No event groups found on Coupon page')
        self.assertIn(self.league_name, sections.keys(),
                      msg=f'"{self.league_name}" is not found in competitions list "{", ".join(sections.keys())}"')
        league = sections[self.league_name]
        self.assertTrue(league, msg=f'No league "{self.league_name}" found on Coupon page')
        dategroups = league.items_as_ordered_dict
        self.assertTrue(dategroups, msg=f'No date groups found for competition "{self.league_name}"')
        if self.brand != 'ladbrokes' or self.device_type == 'desktop':
            group_name = vec.coupons.COUPON_TIME_HEADER.title()
        else:
            group_name = vec.coupons.COUPON_TIME_HEADER
        self.assertIn(group_name, dategroups, msg=f'No Today date group in groups "{dategroups.keys()}"')
        events = dategroups[group_name].items_as_ordered_dict
        self.assertTrue(events, msg='No events found in Today date group')
        return dategroups[group_name], events

    def market_checker(self, market_name, expected_fixture_template):
        """
        Helper method created to not repeat same actions for 8 markets
        """
        if expected_fixture_template == 'home_draw_away':
            expected_fixture_header_1 = vec.sb.FIXTURE_HEADER.home
            expected_fixture_header_2 = vec.sb.FIXTURE_HEADER.draw
            expected_fixture_header_3 = vec.sb.FIXTURE_HEADER.away
        elif expected_fixture_template == 'yes_no':
            expected_fixture_header_1 = vec.sb.FIXTURE_HEADER.yes
            expected_fixture_header_2 = vec.sb.FIXTURE_HEADER.no
            expected_fixture_header_3 = None
        elif expected_fixture_template == 'over_under':
            expected_fixture_header_1 = vec.sb.FIXTURE_HEADER.over
            expected_fixture_header_2 = vec.sb.FIXTURE_HEADER.under
            expected_fixture_header_3 = None
        elif expected_fixture_template == 'home_away':
            expected_fixture_header_1 = vec.sb.FIXTURE_HEADER.home
            expected_fixture_header_2 = vec.sb.FIXTURE_HEADER.away
            expected_fixture_header_3 = None
        else:
            expected_fixture_header_1, expected_fixture_header_2, expected_fixture_header_3 = None, None, None

        expected_market_name, self.__class__.expected_fixture_header_1, self.__class__.expected_fixture_header_2, \
            self.__class__.expected_fixture_header_3 = self.get_market_name_and_headers(market_name=market_name,
                                                                                        fixture_header_1=expected_fixture_header_1,
                                                                                        fixture_header_2=expected_fixture_header_2,
                                                                                        fixture_header_3=expected_fixture_header_3)

        today, events = self.select_market_and_get_event_section(market_name=expected_market_name)
        self.verify_section_fixture_header(section=today)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event with a coupon
        """
        self.__class__.league_name = tests.settings.football_autotest_competition_league
        event = self.ob_config.add_autotest_premier_league_football_event(markets=self.event_markets)
        self.__class__.event_diff_markets_name = event.team1 + ' v ' + event.team2
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.add_event_to_coupon(market_id=self.ob_config.market_ids[event.event_id][market_short_name],
                                           coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)
        for market in self.event_markets:
            self.ob_config.add_event_to_coupon(market_id=self.ob_config.market_ids[event.event_id][market[0]],
                                               coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_001_load_oxygen_application_and_navigate_to_football_coupon_details_page(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Football Coupon Details page
        EXPECTED: Coupon Details page is loaded
        EXPECTED: Events for appropriate coupon are displayed on Coupons Details page
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

    def test_003_select_match_results_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select Match Results or Match Betting in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header: Home, Draw, Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.match_result,
                            expected_fixture_template='home_draw_away')

    def test_004_select_both_teams_to_score_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Both Teams to Score' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header: Yes, No
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.both_teams_to_score,
                            expected_fixture_template='yes_no')

    def test_005_select_total_goals_over_under_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Total Goals Over/ Under 1.5/2.5/3.5' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header: Over, Under
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.total_goals_over_under_1_5,
                            expected_fixture_template='over_under')

    def test_006_select_match_result_and_both_teams_to_score_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'To Win & Both Teams to Score' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header: Home, Draw, Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.match_result_and_both_teams_to_score,
                            expected_fixture_template='home_draw_away')

    def test_007_select_draw_no_bet_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Draw No Bet' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header: Home, Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.draw_no_bet,
                            expected_fixture_template='home_away')

    def test_008_select_1st_half_result_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select '1st Half Result' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header: Home, Draw, Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.first_half_result,
                            expected_fixture_template='home_draw_away')

    def test_009_select_to_win_to_nil_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'To Win to Nil' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header: Home, Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.to_win_to_nil,
                            expected_fixture_template='home_away')

    def test_010_select_goal_in_both_halves_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Goal in Both Halves' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header: Yes, No
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.score_goal_in_both_halves,
                            expected_fixture_template='yes_no')
