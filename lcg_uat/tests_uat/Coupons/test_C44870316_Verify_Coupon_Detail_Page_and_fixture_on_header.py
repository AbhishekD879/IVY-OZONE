import time
import pytest
import tests
import voltron.environments.constants as vec

from tests.base_test import vtest
from collections import namedtuple
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.p1
@pytest.mark.slow
@pytest.mark.desktop
# @pytest.mark.prod # Required markets always not avail in prod, we need to create them
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870316_Verify_Coupon_Detail_Page_and_fixture_on_header(BaseCouponsTest, BaseBetSlipTest):
    """
    TR_ID: C44870316
    NAME: "Verify  Coupon Detail Page and fixture on header"
    DESCRIPTION: -Verify below on the Coupon Detail Page
    DESCRIPTION: -Verifies Fixture Header on Coupon Details page
    PRECONDITIONS: Load Oxygen application - Homepage is opened
    """
    keep_browser_open = True

    event_markets = [
        ('both_teams_to_score', {'cashout': True}),
        ('over_under_total_goals', {'cashout': True}),
        ('match_result_and_both_teams_to_score', {'cashout': True}),
        ('draw_no_bet', {'cashout': True}),
        ('first_half_result', {'cashout': True}),
        ('to_win_to_nil', {'cashout': True}),
        ('score_goal_in_both_halves', {'cashout': True})
    ]

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
        if self.brand == 'bma' or self.device_type == 'desktop':
            self.__class__.league_name = tests.settings.football_autotest_competition_league
        else:
            self.__class__.league_name = tests.settings.football_autotest_competition_league.title()
        if self.brand == 'bma' and self.device_type == 'desktop':
            self.coupon.tab_content.dropdown_market_selector.value = market_name
        else:
            self.coupon.tab_content.dropdown_market_selector.select_value(market_name)
        sections = self.coupon.tab_content.accordions_list.items_as_ordered_dict
        if not sections:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            sections = self.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No event groups found on Coupon page')
        self.assertIn(self.league_name, sections.keys(),
                      msg=f'"{self.league_name}" is not found in competitions list "{", ".join(sections.keys())}"')
        league = sections[self.league_name]
        self.assertTrue(league, msg=f'No league "{self.league_name}" found on Coupon page')
        dategroups = league.items_as_ordered_dict
        self.assertTrue(dategroups, msg=f'No date groups found for competition "{self.league_name}"')
        if self.brand == 'bma' or self.device_type == 'desktop':
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

    def verify_correct_events_displayed_for_coupon(self, coupon_name):
        active_events_query = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                      self.ob_config.backend.ti.football.category_id))
        resp = self.ss_req.ss_coupon_to_outcome_for_coupon(
            coupon_id=self.ob_config.backend.ti.football.coupons[coupon_name], query_builder=active_events_query)
        self.__class__.coupon_events = [x for x in resp[0]['coupon']['children']]
        events_names_from_ss_resp = [x['event']['name'] for x in self.coupon_events]
        events_names_on_page = []
        self.__class__.sections = self.coupon.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in self.sections.items():
            date_groups = section.items_as_ordered_dict
            self.assertTrue(date_groups, msg='No date groups found on Coupon section "%s"' % section_name)
            for name, date_group in date_groups.items():
                events = date_group.items_as_ordered_dict
                self.assertTrue(events, msg='No events found on Coupon details page in date group "%s"' % name)
                for event_name, events in events.items():
                    events_names_on_page.append(event_name)

        self.assertListEqual(sorted(events_names_on_page), sorted(events_names_from_ss_resp))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event with a coupon
        """
        self.__class__.league_name = tests.settings.football_autotest_competition_league
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(markets=self.event_markets)
        self.__class__.event2 = self.ob_config.add_autotest_premier_league_football_event(markets=self.event_markets)

        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.add_event_to_coupon(market_id=self.ob_config.market_ids[self.event.event_id][market_short_name],
                                           coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)
        self.ob_config.add_event_to_coupon(market_id=self.ob_config.market_ids[self.event2.event_id][market_short_name],
                                           coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)
        for market in self.event_markets:
            self.ob_config.add_event_to_coupon(market_id=self.ob_config.market_ids[self.event.event_id][market[0]],
                                               coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)
            self.ob_config.add_event_to_coupon(market_id=self.ob_config.market_ids[self.event2.event_id][market[0]],
                                               coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        self.site.login()
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name=vec.sb.FOOTBALL)
        matches_tab_name = self.get_sport_tab_name(vec.sb.SPORT_TABS_INTERNAL_NAMES.matches,
                                                   self.ob_config.football_config.category_id)
        self.assertEqual(self.site.football.tabs_menu.current, matches_tab_name,
                         msg=f'"{matches_tab_name}" tab is not active by default')

    def test_002_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: 'Coupons' tab is selected and highlighted
        EXPECTED: Coupons Landing page is loaded
        """
        self.__class__.expected_tab = self.expected_sport_tabs.accas
        self.site.football.tabs_menu.click_button(self.expected_tab)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.expected_tab,
                         msg=f'Active tab is "{current_tab}" but "{self.expected_tab}" is expected to be active')

    def test_003_navigate_to_coupon_details_page(self):
        """
        DESCRIPTION: Navigate to Coupon Details page
        EXPECTED: Coupon Details page is loaded
        """
        self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)

    def test_004_verify_coupons_header(self):
        """
        DESCRIPTION: Verify Coupons header
        EXPECTED: The following elements are present on Coupons header:
        EXPECTED: * 'Back' button
        EXPECTED: * 'Coupons' inscription
        """
        self.__class__.coupon = self.site.coupon
        if self.device_type == 'mobile' and self.brand == 'bma':
            self.assertTrue(self.coupon.header_line.has_back_button,
                            msg='There\'s no back button on Coupon page header')
        else:
            self.assertTrue(self.site.has_back_button, msg=' "Back button" is not displayed')
        if self.device_type != 'mobile' and self.brand != 'ladbrokes':
            self.assertEqual(self.coupon.header_line.page_title.text, vec.coupons.COUPONS_TITLE,
                             msg=f'"{vec.coupons.COUPONS_TITLE}" is not displayed')

    def test_005_verify_coupons_sub_header(self):
        """
        DESCRIPTION: Verify Coupons sub-header
        EXPECTED: Coupons sub-header is located below Coupons header
        EXPECTED: "Name of selected coupon" is displayed at the left side of Coupons sub-header
        """
        actual_coupon_name = self.coupon.name
        self.assertEqual(actual_coupon_name, vec.siteserve.EXPECTED_COUPON_NAME,
                         msg=f'Coupon name in subheader "{actual_coupon_name}" '
                             f'is not the same as expected "{vec.siteserve.EXPECTED_COUPON_NAME}"')

    def test_006_verify_coupons_page_content(self):
        """
        DESCRIPTION: Verify Coupons page content
        EXPECTED: Events for appropriate coupon are displayed on Coupons Details page
        EXPECTED: First **three** accordions are expanded by default
        EXPECTED: The remaining sections are collapsed by default
        EXPECTED: It is possible to collapse/expand all of the accordions by tapping the accordion's header
        EXPECTED: If no events to show, the message '**No events found**' is displayed
        """
        self.verify_correct_events_displayed_for_coupon(coupon_name=vec.siteserve.EXPECTED_COUPON_NAME)
        self.__class__.sections = self.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No event groups found on Coupon page')
        if len(self.sections) >= 3:
            for section_name, section in list(self.sections.items())[:3]:
                self.assertTrue(section.is_expanded(), msg=f'Section "{section_name}" is not expanded by default')
            for section_name, section in list(self.sections.items())[3:]:
                self.assertFalse(section.is_expanded(), msg=f'Section "{section_name}" is expanded by default')

    def test_007_select_match_results_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Match Results' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Draw
        EXPECTED: -Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.match_result,
                            expected_fixture_template='home_draw_away')

    def test_008_select_both_teams_to_score_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Both Teams to Score' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Yes
        EXPECTED: -No
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.both_teams_to_score,
                            expected_fixture_template='yes_no')

    def test_009_select_total_goals_over_under_152535_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Total Goals Over/ Under 1.5/2.5/3.5' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Over
        EXPECTED: -Under
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.total_goals_over_under_1_5,
                            expected_fixture_template='over_under')

    def test_010_select_match_result__both_teams_to_score_in_the_market_selector_drop_down_and_verify_values_on_fixture_headerexpected_result(self):
        """
        DESCRIPTION: Select 'Match Result & Both Teams to Score' in the Market selector drop down and verify values on Fixture header
        DESCRIPTION: Expected Result
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Draw
        EXPECTED: -Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.match_result_and_both_teams_to_score,
                            expected_fixture_template='home_draw_away')

    def test_011_select_draw_no_bet_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Draw No Bet' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.draw_no_bet,
                            expected_fixture_template='home_away')

    def test_012_select_1st_half_result_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select '1st Half Result' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Draw
        EXPECTED: -Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.first_half_result,
                            expected_fixture_template='home_draw_away')

    def test_013_select_to_win_to_nil_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'To Win to Nil' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Home
        EXPECTED: -Away
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.to_win_to_nil,
                            expected_fixture_template='home_away')

    def test_014_select_goal_in_both_halves_in_the_market_selector_drop_down_and_verify_values_on_fixture_header(self):
        """
        DESCRIPTION: Select 'Goal in Both Halves' in the Market selector drop down and verify values on Fixture header
        EXPECTED: The following values are displayed on Fixture header:
        EXPECTED: -Yes
        EXPECTED: -No
        """
        self.market_checker(market_name=vec.coupons.EXPECTED_COUPON_MARKET_TEMPLATES_NAMES.score_goal_in_both_halves,
                            expected_fixture_template='yes_no')

    def test_015_verify_all_the_markets__in_the_event_detail_page(self):
        """
        DESCRIPTION: Verify all the markets  in the event detail page
        EXPECTED: same markets is displayed on EDP
        """
        coupons_event_group = list(self.sections.values())[0]
        coupons_event_by_date_group = list(coupons_event_group.items_as_ordered_dict.values())[0]
        event_1 = list(coupons_event_by_date_group.items_as_ordered_dict.values())[0]
        event_1.click()
        actual_markets_in_edp = sorted(list(self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.keys()))
        for market_name in actual_markets_in_edp:
            self.assertIn(market_name.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS,
                          msg=f'Actual Market : "{market_name}" is not available on EDP')
        self.site.back_button.click()

    def test_016_verify_single_and_multiple_bet_placement_for_coupons(self):
        """
        DESCRIPTION: Verify single and multiple bet placement for coupons
        EXPECTED: single and multiple bets are placed successfully
        """
        sections = self.coupon.tab_content.accordions_list.items_as_ordered_dict
        coupons_event_group = list(sections.values())[0]
        coupons_event_by_date_group = list(coupons_event_group.items_as_ordered_dict.values())[0]
        event_1 = list(coupons_event_by_date_group.items_as_ordered_dict.values())[0]
        event_1.template.first_player_bet_button.click()
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
        time.sleep(2)
        event_2 = list(coupons_event_by_date_group.items_as_ordered_dict.values())[1]
        event_2.template.first_player_bet_button.click()
        if self.device_type == 'mobile':
            self.site.header.bet_slip_counter.click()

        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)
        for stake in self.zip_available_stakes(section=multiples_section, number_of_stakes=1).items():
            self.enter_stake_amount(stake=stake)
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(timeout=1.5), msg='"PLACE BET" button is not enabled')
        bet_now_button.click()
        self.check_bet_receipt_is_displayed()

    def test_017_on_mobile_close_the_bet_receipt_and_tap_back_button(self):
        """
        DESCRIPTION: On Mobile close the bet receipt and Tap 'Back' button
        EXPECTED: Coupons Landing page is loaded
        EXPECTED: List of coupons is displayed
        """
        if self.device_type == 'mobile':
            self.site.bet_receipt.close_button.click()
        self.site.back_button.click()
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.expected_tab,
                         msg=f'Active tab is "{current_tab}" but "{self.expected_tab}" is expected to be active')
        coupon_categories = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(coupon_categories, msg='Can not find any coupon category')
