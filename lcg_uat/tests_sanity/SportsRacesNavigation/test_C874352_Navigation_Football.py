import random
import pytest
import tests
import voltron.environments.constants as vec
from datetime import datetime
from tests.base_test import vtest
from voltron.utils.helpers import normalize_name
from crlat_siteserve_client.constants import LEVELS
from voltron.utils.waiters import wait_for_result
from crlat_siteserve_client.constants import ATTRIBUTES, OPERATORS
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from voltron.pages.shared.contents.competitions_league_page import CompetitionsOutrightsTabContent
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from tests.pack_013_Retail_Connect_Features.Football_Bet_Filter.BaseFootballBetFilter import BaseFootballBetFilter
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.timeout(1200)
@pytest.mark.slow
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@vtest
class Test_C874352_Navigation_Football(BaseCouponsTest, BaseSportTest, BaseFootballBetFilter):
    """
    TR_ID: C874352
    NAME: Navigation Football
    DESCRIPTION: Test case verifies navigation through Football pages is correct:
    DESCRIPTION: Matches
    DESCRIPTION: Coupons
    DESCRIPTION: Outrights
    DESCRIPTION: Specials
    DESCRIPTION: Enhanced Multiples
    DESCRIPTION: Event Details page
    DESCRIPTION: Combined Markets
    DESCRIPTION: if 'Coupons' Tab is not available see instruction how to generate [Coupon](https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system)
    PRECONDITIONS: Open Oxygen app
    """
    keep_browser_open = True
    sport_name = vec.sb.FOOTBALL
    autotest_coupon = vec.siteserve.EXPECTED_COUPON_NAME
    maxDiff = None

    def verify_correct_events_displayed_for_coupon(self, coupon_name):
        coupons = self.get_coupons()
        coupon_id = None
        for coupon in coupons:
            if coupon['coupon']['name'] == coupon_name:
                coupon_id = coupon['coupon']['id']

        self.assertTrue(coupon_id, msg=f'Coupon id not found for coupon name "{coupon_name}"')

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.backend.ti.football.category_id)
        active_events_query = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                      self.ob_config.backend.ti.football.category_id))
        resp = ss_req.ss_coupon_to_outcome_for_coupon(coupon_id=coupon_id, query_builder=active_events_query)
        coupon_events = [x for x in resp[0]['coupon']['children']]
        events_names_from_ss_resp = [normalize_name(x['event']['name']) for x in coupon_events]
        self.assertTrue(events_names_from_ss_resp, msg='Events not found from ss resp')

        events_names_on_page = []
        sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Sections not found on coupon page')
        for section_name, section in sections.items():
            section.expand()
            date_groups = section.items_as_ordered_dict
            self.assertTrue(date_groups, msg=f'No date groups found on Coupon section "{section_name}"')
            for name, date_group in date_groups.items():
                events = date_group.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events found on Coupon details page in date group "{name}"')
                for event_name, event in events.items():
                    events_names_on_page.append(event_name)

        self.assertTrue(events_names_on_page, msg='Events not found on coupon page')
        self.assertListEqual(sorted(events_names_on_page), sorted(events_names_from_ss_resp),
                             msg=f'Actual list \n"{sorted(events_names_on_page)}" \n'
                                 f'!= Expected \n"{sorted(events_names_from_ss_resp)}"')

    def verify_correct_selection_on_coupon_page(self):
        self.site.coupon.scroll_to_top()
        if self.brand == 'bma' and self.device_type == 'desktop':
            markets_in_dropdown = self.site.coupon.dropdown_market_selector.available_options
        else:
            markets_in_dropdown = self.site.coupon.tab_content.dropdown_market_selector.available_options
        markets_to_check = {vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score: [vec.sb.FIXTURE_HEADER.yes, vec.sb.FIXTURE_HEADER.no],
                            vec.siteserve.EXPECTED_MARKETS_NAMES.to_win_to_nil: [vec.sb.FIXTURE_HEADER.home, vec.sb.FIXTURE_HEADER.away],
                            vec.siteserve.EXPECTED_MARKETS_NAMES.total_goals_over_under_2_5: [vec.sb.FIXTURE_HEADER.over, vec.sb.FIXTURE_HEADER.under]}
        for market, selection_names in markets_to_check.items():
            if market in markets_in_dropdown:
                self.site.coupon.scroll_to_top()
                if self.brand == 'bma' and self.device_type == 'desktop':
                    result = wait_for_result(
                        lambda: self.site.coupon.dropdown_market_selector.is_displayed(),
                        name=f'Market selector to be displayed',
                        timeout=3)
                else:
                    result = wait_for_result(
                        lambda: self.site.coupon.tab_content.dropdown_market_selector.is_displayed(),
                        name=f'Market selector to be displayed',
                        timeout=3)
                self.assertTrue(result, msg=f'Market selector does not displayed')
                if self.brand == 'bma' and self.device_type == 'desktop':
                    self.site.coupon.dropdown_market_selector.click()
                    self.site.coupon.dropdown_market_selector.value = market
                else:
                    self.site.coupon.tab_content.dropdown_market_selector.select_value(market)

                if self.device_type == 'mobile':
                    result = wait_for_result(
                        lambda: market == self.site.coupon.tab_content.dropdown_market_selector.value,
                        name=f'"{market}" market to be selected',
                        timeout=3)
                elif self.brand == 'bma' and self.device_type == 'desktop':
                    result = wait_for_result(
                        lambda: market == self.site.coupon.dropdown_market_selector.value,
                        name=f'"{market}" market to be selected',
                        timeout=3)
                else:
                    result = wait_for_result(
                        lambda: market == self.site.coupon.tab_content.selected_market,
                        name=f'"{market}" market to be selected',
                        timeout=3)
                self.assertTrue(result, msg=f'Market does not changed')
                sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg='Sections not found on coupon page')
                for section_name, section in sections.items():
                    section.expand()
                    date_groups = section.items_as_ordered_dict
                    self.assertTrue(date_groups, msg=f'No date groups found on Coupon section "{section_name}"')
                    for name, date_group in date_groups.items():
                        selections_names_on_page = date_group.fixture_header.items_as_ordered_dict
                        self.assertTrue(selections_names_on_page,
                                        msg=f'No selection names groups found on Coupon section "{name}"')
                        self.assertEqual(list(selections_names_on_page.keys()), selection_names,
                                         msg=f'Actual selection names "{list(selections_names_on_page.keys())}" does not match '
                                         f'expected "{selection_names}" for "{market}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get football enhanced multiples events
        """
        #  Get featured coupons title from CMS
        today_date = datetime.today().strftime('%A').upper()
        coupon_segments_url = f'coupon-segment/brand/{self.brand}'
        coupon_segments = self.cms_config.request.get(url=coupon_segments_url)
        self.__class__.featured_coupons_title = None
        for segment in coupon_segments:
            day = segment.get('dayOfWeek')
            if day and day[0] == today_date:
                self.featured_coupons_title = segment['title']
                break
        else:
            self._logger.warning("*** No featured coupons configured for today")

        self.__class__.category_id = self.ob_config.football_config.category_id
        if tests.settings.backend_env != 'prod':
            # enhanced multiples event
            self.__class__.enhanced_multiples_events = self.ob_config.add_football_event_enhanced_multiples()
            # live event
            self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            # outright event
            self.ob_config.add_autotest_premier_league_football_outright_event()
            # matches/competition event
            event_matches_params = self.ob_config.add_autotest_premier_league_football_event()
            # coupons
            market_short_name = self.ob_config.football_config. \
                autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
            event_coupons_id = self.ob_config.market_ids[event_matches_params.event_id][market_short_name]
            self.ob_config.add_event_to_coupon(market_id=event_coupons_id, coupon_name=self.autotest_coupon)
            # specials event
            self.ob_config.add_autotest_premier_league_football_event(special=True)

    def test_001_click_on_football_button_from_the_main_menu(self):
        """
        DESCRIPTION: Click on Football button from the Main Menu
        EXPECTED: 1. Football Page is loaded
        EXPECTED: 2. The Matches tab is selected by default
        EXPECTED: 3. The first 3 Leagues are expanded by default, and the rest of them are collapsed
        EXPECTED: 4. All events which are available are displayed for the League
        EXPECTED: 5. The "Match Result" option is selected in the market selector for all the event types
        EXPECTED: 6. **For Mobile/Tablet:**
        EXPECTED: Enhanced Multiple events section (if available) is displayed on the top of the list and is expanded
        EXPECTED: **For Desktop:**
        EXPECTED: Enhanced Multiple events section (if available) is displayed as carousel above tabs
        EXPECTED: 7. **For Desktop:**
        EXPECTED: 'In-Play' widget is displayed in 3rd column or below main content (depends on screen resolution) with live events in carousel
        """
        self.site.open_sport(name=self.sport_name)
        current_tab_name = self.site.football.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Default tab is not "{self.expected_sport_tabs.matches}", it is "{current_tab_name}"')

        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'No one event section found in for sport: "{self.sport_name}"')
        if vec.racing.ENHANCED_MULTIPLES_NAME in list(sections.keys()):
            expected_expnaded_section = len(sections.items()) if len(sections.items()) < 4 else 4
        else:
            expected_expnaded_section = len(sections.items()) if len(sections.items()) < 3 else 3
        for section_name, section in list(sections.items())[:expected_expnaded_section]:
            self.assertTrue(section.is_expanded(), msg=f'"{section_name}" is not expanded')
        for section_name, section in list(sections.items())[expected_expnaded_section:]:
            self.assertFalse(section.is_expanded(expected_result=False), msg=f'"{section_name}" is not collapsed')

        selected_market = self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item
        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' \
            else vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        self.assertEqual(selected_market, market_name,
                         msg=f'Default market name from market selector "{selected_market}" '
                         f'is not the same as expected "{market_name}"')
        if tests.settings.backend_env != 'prod':
            if self.device_type == 'desktop':
                em_carousel = self.site.football.sport_enhanced_multiples_carousel
                self.assertTrue(em_carousel, msg='Enhanced Multiples carousel is not displayed')
            else:
                self.assertIn(vec.racing.ENHANCED_MULTIPLES_NAME, sections,
                              msg='No "ENHANCED MULTIPLES" section found in list')

    def test_002_select_a_different_option_from_the_market_selector_eg_total_goals_overunder_25(self):
        """
        DESCRIPTION: Select a different option from the market selector (e.g. "Total Goals Over/Under 2.5")
        EXPECTED: The events list is updated automatically
        EXPECTED: The "Total Goals Over/Under 2.5" selections are now displayed in the list for the events from this Event Type
        """
        if self.device_type == 'desktop':
            self.site.football.tab_content.dropdown_market_selector.click()
            result = wait_for_result(
                lambda: self.site.football.tab_content.dropdown_market_selector.is_expanded(),
                name='Wait for market selector to be expanded', timeout=5)
            self.assertTrue(result, msg=f'Market selector is not expanded')

        current_market = self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item
        markets = self.site.football.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(markets, msg='Markets list is empty')
        if len(markets) < 2:
            self._logger.warning("*** Skipping validation of market selector as only one market is present")
            return

        market_names = list(markets.keys())
        name_to_remove = next((market for market in market_names if market.lower() == current_market.lower()))
        markets.pop(name_to_remove)

        market_name = random.choice(list(markets.keys()))
        market = markets.get(market_name)
        self.assertTrue(market, msg=f'Market "{market_name}" is not found in "{markets.keys()}"')
        self.site.football.tab_content.scroll_to()
        market.click()
        result = wait_for_result(
            lambda: self.site.football.tab_content.dropdown_market_selector.selected_market_selector_item.lower() == market_name.lower(),
            name='Wait for market being selected', timeout=5)
        self.assertTrue(result, msg=f'Market name from market selector is not the same as expected "{market_name}"')

    def test_003_click_on_competitions_tab(self):
        """
        DESCRIPTION: Click on Competitions tab
        EXPECTED: 1. The Competition Page is loaded
        EXPECTED: 2. The first Competition from Popular Competitions section is expanded by default (the rest of them are collapsed)
        EXPECTED: 3. All the competitions in A-Z section are collapsed by default on Mobile and the First accordion is expanded by default on Desktop
        """
        expected_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                    self.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'Competition tab is not active, active is "{active_tab}"')

        if self.device_type == 'mobile':
            popular_competitions = self.site.football.tab_content.competitions_categories.items_as_ordered_dict
        else:
            no_events_label = self.site.football.tab_content.has_no_events_label()
            if no_events_label:
                popular_competitions = None
            else:
                popular_competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict

        if popular_competitions:
            first_competition_name, self.__class__.first_competition = list(popular_competitions.items())[0]
            self.assertTrue(self.first_competition.is_expanded(), msg=f'"{first_competition_name}" is not expanded')
            for competition_name, competition in list(popular_competitions.items())[1:]:
                self.assertFalse(competition.is_expanded(expected_result=False),
                                 msg=f'"{competition_name}" is not collapsed')

        if self.device_type == 'mobile':
            all_categories = self.site.football.tab_content.all_competitions_categories.items_as_ordered_dict

        else:
            grouping_buttons = self.site.football.tab_content.grouping_buttons
            grouping_buttons.click_item(vec.sb_desktop.COMPETITIONS_SPORTS)
            result = wait_for_result(lambda: grouping_buttons.current == vec.sb_desktop.COMPETITIONS_SPORTS,
                                     name=f'"{vec.sb_desktop.COMPETITIONS_SPORTS}" to be selected after click',
                                     timeout=1)
            self.assertTrue(result,
                            msg=f'"{vec.sb_desktop.COMPETITIONS_SPORTS}" is not selected by after click. '
                                f'Active button is "{grouping_buttons.current}"')
            all_categories = self.site.football.tab_content.accordions_list.items_as_ordered_dict

        self.assertTrue(all_categories, msg='No A-Z accordions found on Competitions page')

        self.__class__.first_competition_name, self.__class__.first_competition = list(all_categories.items())[0]
        if self.device_type == 'desktop':
            self.assertTrue(self.first_competition.is_expanded(), msg=f'"{self.first_competition_name}" is not expanded')
        else:
            self.assertFalse(self.first_competition.is_expanded(expected_result=False),
                             msg=f'"{self.first_competition_name}" is not collapsed')
        for competition_name, competition in list(all_categories.items())[1:]:
            self.assertFalse(competition.is_expanded(expected_result=False),
                             msg=f'"{competition_name}" is not collapsed')

    def test_004_select_one_event_from_the_competitions_tab(self):
        """
        DESCRIPTION: Select one event from the competitions tab
        EXPECTED: The list of events from that competition is displayed
        """
        self.first_competition.expand()
        events = self.first_competition.items_as_ordered_dict
        self.assertTrue(events, msg=f'Can not find any event in "{self.first_competition_name}" competition')
        first_event_name, event_competition = list(events.items())[0]
        event_competition.click()
        tab_content = self.site.competition_league.tab_content
        current_tab_content = self.site.competition_league.current_tab_content
        if not tab_content.has_no_events_label():
            if current_tab_content is CompetitionsOutrightsTabContent:
                sections = tab_content.event_league
            else:
                sections = tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No events sections are present on page')

    def test_005_click_on_back_button_and_then_click_on_coupons_tab(self):
        """
        DESCRIPTION: Click on Back Button and then click on Coupons Tab
        EXPECTED: List Of Coupons is displayed in 'Popular Coupons' and 'Featured Coupons' sections
        """
        self.site.back_button_click()
        self.navigate_to_page(name='sport/football/coupons')
        self.site.wait_content_state('Football')
        self.__class__.coupon_categories = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.coupon_categories, msg='Can not find any coupon category')
        coupon_categories_names = list(self.coupon_categories.keys())
        self.assertIn(vec.coupons.POPULAR_COUPONS.upper(), coupon_categories_names,
                      msg=f"{vec.coupons.POPULAR_COUPONS.upper()} does not exist in '{coupon_categories_names}'")

        if self.featured_coupons_title:
            self.assertIn(self.featured_coupons_title.upper(), coupon_categories_names,
                          msg=f"{self.featured_coupons_title} does not exist in '{coupon_categories_names}'")

    def test_006_select_any_coupon_from_the_list(self):
        """
        DESCRIPTION: Select any coupon from the list
        EXPECTED: * Selected Coupon name is displayed on Subheader
        EXPECTED: * A list of the events available under the specific coupon is displayed
        EXPECTED: * Check that the "name" of the selections from the header are correct:
        EXPECTED: - Yes/No for "Both Teams to Score" coupon
        EXPECTED: - Over/Under for Over/Under 2.5 Coupon
        EXPECTED: - Home/Away for "To Win to Nil" coupon
        """
        if tests.settings.backend_env == 'prod':
            coupons_list = self.coupon_categories.get(vec.coupons.POPULAR_COUPONS.upper()).items_as_ordered_dict
            self.assertTrue(coupons_list, msg='Can not find any coupon')
            coupon_name, coupon = list(coupons_list.items())[0]
            coupon.click()
            self.site.wait_content_state('CouponPage')
        else:
            coupon_name = self.autotest_coupon
            self.find_coupon_and_open_it(coupon_section=vec.coupons.POPULAR_COUPONS.upper(), coupon_name=coupon_name)

        result = wait_for_result(lambda: self.site.coupon.name == coupon_name,
                                 name=f'"{coupon_name}" to be displayed',
                                 timeout=5)
        self.assertTrue(result, msg=f'Coupon name "{coupon_name}" does not displayed on the page. '
                        f'Actual: "{self.site.coupon.name}"')
        self.verify_correct_events_displayed_for_coupon(coupon_name)
        self.verify_correct_selection_on_coupon_page()

    def test_007_coral_only_tap_on_change_coupon_dropdown_on_subheader_and_select_any_other_coupon(self):
        """
        DESCRIPTION: **CORAL only:** Tap on 'Change Coupon' dropdown on subheader and select any other coupon
        EXPECTED: * Selected Coupon name is displayed on Subheader
        EXPECTED: * A list of the events available under the specific coupon is displayed
        EXPECTED: * Check that the "name" of the selections from the header are correct:
        EXPECTED: - Yes/No for "Both Teams to Score" coupon
        EXPECTED: - Over/Under for Over/Under 2.5 Coupon
        EXPECTED: - Home/Away for "To Win to Nil" coupon
        """
        if self.brand == 'bma':
            self.site.coupon.coupon_selector_link.click()
            coupons_list = self.site.coupon.coupons_list.items_as_ordered_dict
            self.assertTrue(coupons_list,
                            msg='Coupons are not found in list of coupons')
            coupon_from_dropdown = list(coupons_list.keys())[-1]
            coupon = coupons_list.get(coupon_from_dropdown)
            self.assertTrue(coupon, msg='Can not find coupon')
            coupon.click()
            self.site.wait_content_state('CouponPage')

            wait_for_result(lambda: self.site.coupon.name == coupon_from_dropdown,
                            name='Coupon to change',
                            bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                            timeout=5)
            coupon_name_on_page = self.site.coupon.name
            self.assertEqual(coupon_name_on_page, coupon_from_dropdown,
                             msg=f'Coupon name in subheader "{coupon_name_on_page}" '
                             f'is not the same as expected "{coupon_from_dropdown}"')

            self.verify_correct_events_displayed_for_coupon(coupon_from_dropdown)
            self.verify_correct_selection_on_coupon_page()

    def test_008_go_back_to_football_landing_page_and_click_on_outrights_tab(self):
        """
        DESCRIPTION: Go back to Football Landing page and Click on Outrights Tab
        EXPECTED: The Outrights tab is loaded
        EXPECTED: Leagues and Competitions are all collapsed by default
        """
        self.navigate_to_page('/')
        self.site.open_sport(name=self.sport_name)

        if self.is_tab_present(tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                               category_id=self.category_id):
            expected_sport_tab = \
                self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                                        self.category_id)
            self.site.football.tabs_menu.click_button(expected_sport_tab)
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, expected_sport_tab,
                             msg=f'Competition tab is not active, active is "{active_tab}"')
            sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No one event section found in for sport: "{self.sport_name}"')
            for section_name, section in list(sections.items()):
                self.assertFalse(section.is_expanded(expected_result=False), msg=f'"{section_name}" is not collapsed')
            section_name, section = list(sections.items())[0]
            section.expand()
            events = section.items_as_ordered_dict
            self.assertTrue(events, msg=f'No one event section found in section: "{section_name}"')
        else:
            self._logger.warning("*** Skipping validation of Outrights tab as it is not displayed")

    def test_009_expand_one_event_type(self):
        """
        DESCRIPTION: Expand one event type
        EXPECTED: The list of outrights from that event type are displayed
        """
        # verified in step 8
        pass

    def test_010_click_on_specials_tab_if_available(self):
        """
        DESCRIPTION: Click on Specials tab (if available)
        EXPECTED: The Specials tab is loaded
        EXPECTED: The first event type is expanded by default (the rest of them are collapsed)
        """
        if self.is_tab_present(tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials,
                               category_id=self.category_id):
            expected_sport_tab = \
                self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.specials,
                                        self.ob_config.football_config.category_id)
            self.site.football.tabs_menu.click_button(expected_sport_tab)
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, expected_sport_tab,
                             msg=f'Competition tab is not active, active is "{active_tab}"')
            specials = self.site.football.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(specials, msg='No competitions are present on page')
            special_name, special = list(specials.items())[0]
            self.assertTrue(special.is_expanded(), msg=f'"{special_name}" is not expanded')
            for special_name, special in list(specials.items())[1:]:
                self.assertFalse(special.is_expanded(expected_result=False), msg=f'"{special_name}" is not collapsed')
        else:
            self._logger.warning("*** Skipping validation of Special tab as it is not displayed")

    def test_011_click_on_in_play_tab(self):
        """
        DESCRIPTION: Click on In Play Tab
        EXPECTED: The In Play tab is loaded (with Live now, Upcoming sections)
        EXPECTED: The first N leagues are expanded by default (the rest of them are collapsed), N - CMS configurable value
        """
        in_play_competition_section = self.get_initial_data_system_configuration().get('InPlayCompetitionsExpanded', {})
        if not in_play_competition_section:
            in_play_competition_section = self.cms_config.get_system_configuration_item('InPlayCompetitionsExpanded')
        competitions_count = in_play_competition_section.get('competitionsCount')
        if not competitions_count or not competitions_count.isdigit():
            raise CmsClientException('Expanded leagues are not configured in CMS')
        in_play_expand = int(in_play_competition_section.get('competitionsCount'))
        if self.device_type == 'desktop':
            in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                  self.ob_config.football_config.category_id)
            self.site.football.tabs_menu.click_button(in_play_tab)
            active_tab = self.site.football.tabs_menu.current
            self.assertEqual(active_tab, in_play_tab,
                             msg=f'In-Play tab is not active, active is "{active_tab}"')
        else:
            in_play_tab_present = self.is_tab_present(tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                      category_id=self.category_id)
            self.softAssert(self.assertTrue, in_play_tab_present, msg='In Play tab is not configured for Football')
            if in_play_tab_present:
                expected_in_play_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, self.category_id)
                self.site.football.tabs_menu.click_button(expected_in_play_tab)
                active_tab = self.site.football.tabs_menu.current
                self.assertEqual(active_tab, expected_in_play_tab,
                                 msg=f'In-Play tab is not active, active is "{active_tab}"')

        if self.device_type == 'mobile':
            live_now_sections_name = self.site.inplay.tab_content.live_now.name
            self.assertEqual(live_now_sections_name, vec.inplay.LIVE_NOW_EVENTS_SECTION,
                             msg=f"{vec.inplay.LIVE_NOW_EVENTS_SECTION} is not loaded, actual '{live_now_sections_name}'")
            upcoming_sections_name = self.site.inplay.tab_content.upcoming.name
            self.assertEqual(upcoming_sections_name, vec.inplay.UPCOMING_EVENTS_SECTION,
                             msg=f"{vec.inplay.UPCOMING_EVENTS_SECTION} is not loaded, actual '{upcoming_sections_name}'")
        else:
            switchers_on_in_play = self.site.football.tab_content.grouping_buttons.items_as_ordered_dict
            self.assertTrue(switchers_on_in_play, 'No grouping buttons on In play page')
            self.assertEqual(list(switchers_on_in_play.keys()), [vec.inplay.LIVE_NOW_SWITCHER, vec.inplay.UPCOMING_SWITCHER],
                             msg=f'Expected switchers {vec.inplay.LIVE_NOW_SWITCHER, vec.inplay.UPCOMING_SWITCHER} '
                                 f'does not match actual "{switchers_on_in_play.keys()}"')

        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        if sections:
            for section_name, section in list(sections.items())[:in_play_expand]:
                self.assertTrue(section.is_expanded(), msg=f'"{section_name}" is not expanded')
            for section_name, section in list(sections.items())[in_play_expand:]:
                self.assertFalse(section.is_expanded(expected_result=False), msg=f'"{section_name}" is not collapsed')
        else:
            self._logger.warning("*** Skipping validation of In-play as they are not displayed")
