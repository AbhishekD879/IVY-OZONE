import pytest
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod  # can't modify coupons on prod/hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.desktop
@pytest.mark.coupons
@pytest.mark.safari
@vtest
class Test_C28461_Verify_Event_Data_on_Coupon_page(BaseCouponsTest):
    """
    TR_ID: C28461
    NAME: Verify Event Data on Coupon page
    DESCRIPTION: This test case verifies event data
    PRECONDITIONS: 1. In order to get a list with **Coupon IDs **use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon/
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: 2. For each Coupon retrieve a list of **Events and Outcomes**
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/XX.XX/CouponToOutcomeForCoupon/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - **Coupon **ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: Sport icon is CMS configurable - https://CMS_ENDPOINT/keystone/sport-categories (check CMS_ENDPOINT via *devlog *function)
    """
    keep_browser_open = True
    current_date_tab = vec.sb.TABS_NAME_TODAY
    uk_coupon_name = 'UK Coupon'
    league_name = tests.settings.football_autotest_competition_league

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.__class__.current_date_tab = self.current_date_tab.title()
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_id = event_params.event_id
        self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2
        self.__class__.event_time = event_params.event_date_time
        self.__class__.selection_ids = event_params.selection_ids
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        autotest_match_result_market_id = self.ob_config.market_ids[event_params.event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=autotest_match_result_market_id, coupon_name=self.uk_coupon_name)
        self.__class__.ss_req_football = SiteServeRequests(env=tests.settings.backend_env,
                                                           brand=self.brand,
                                                           category_id=self.ob_config.backend.ti.football.category_id)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_for_mobile_tablet_navigate_to_sport_landing_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_sport_landing_page_from_the_left_navigation_menu(
            self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Sport' Landing page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Sport' Landing page from the 'Left Navigation' menu
        EXPECTED: **For Desktop:**
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Matches'->'Today' tab is opened by default
        EXPECTED: **For Mobile:**
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Matches' tab is opened by default
        """
        self.site.open_sport(name='FOOTBALL')
        current_tab_name = self.site.football.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Default tab is not "{self.expected_sport_tabs.matches}", it is "{current_tab_name}"')
        if self.device_type == 'desktop':
            actual_date_tab_name = self.site.football.date_tab.current_date_tab
            self.assertEqual(actual_date_tab_name, vec.sb.SPORT_DAY_TABS.today,
                             msg=f'Actual date tab is "{actual_date_tab_name}" not "{vec.sb.SPORT_DAY_TABS.today}"')

    def test_003_click_tap_coupons_tab(self):
        """
        DESCRIPTION: Click/Tap 'Coupons' tab
        EXPECTED: 'Coupons' tab is opened
        """
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
                                                     self.ob_config.football_config.category_id)
        tab = self.site.football.tabs_menu.click_button(expected_sport_tab)
        self.assertTrue(tab, msg=f'{expected_sport_tab} page was not opened')

    def test_004_go_to_event_section(self):
        """
        DESCRIPTION: Go to Event section
        """
        self.find_coupon_and_open_it(coupon_name=self.uk_coupon_name)

        leagues = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(leagues, msg='Leagues are not found')
        if self.brand == 'ladbrokes' and self.device_type == 'mobile':
            self.__class__.league_name = self.league_name.title()
        auto_test_league = leagues.get(self.league_name)
        self.assertTrue(auto_test_league, msg=f'"{self.league_name}" is not found in "{list(leagues.keys())}"')
        dates = auto_test_league.items_as_ordered_dict
        self.assertTrue(dates, msg='Event dates list is empty')
        today_section = dates.get(self.current_date_tab)
        self.assertTrue(today_section, msg=f'Section "{self.current_date_tab}" is not found in "{list(dates.keys())}"')
        events = today_section.items_as_ordered_dict
        self.assertTrue(events, msg=f'There\'s no events on "{self.current_date_tab}" section')
        self.__class__.event = events.get(self.event_name)
        self.assertTrue(self.event, msg=f'Event "{self.event_name}" is not found')

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: *   Event name corresponds to '**name**' attribute
        EXPECTED: *   Event name is displayed in format: '<Team1/Player1>** v/vs** <Team2/Player2>'
        """
        self.__class__.event_resp = self.ss_req_football.ss_event_to_outcome_for_event(event_id=self.event_id,
                                                                                       query_builder=self.ss_query_builder)
        event_name_resp = self.event_resp[0]['event']['name']
        event_name_ui = self.event.event_name
        self.assertEqual(event_name_ui, event_name_resp,
                         msg=f'Event name "{event_name_ui}" doesn\'t corresponds to "**name**"" '
                         f'attribute "{event_name_resp}"')
        self.assertEqual(event_name_ui, self.event_name,
                         msg=f'Event name "{event_name_ui}" is not displayed in format "{self.event_name}"')

    def test_006_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: *   Event start time corresponds to **startTime** attribute
        EXPECTED: *   Event Start Time is shown below event name
        EXPECTED: *   For events that occur Today date format is 24 hours: for Coral: HH:MM, Today (e.g. "14:00 or 05:00, Today"), for Ladbrokes: HH:MM Today (e.g. "14:00 or 05:00 Today")
        EXPECTED: *   For events that occur in the Future (including tomorrow) date format is 24 hours: for Coral: HH:MM, DD MMM (e.g. 14:00 or 05:00, 24 Nov or 02 Nov), for Ladbrokes: HH:MM DD MMM (e.g. 14:00 or 05:00 24 Nov or 02 Nov)
        """
        event_time_ui = self.event.event_time
        event_time_resp = self.event_resp[0]['event']['startTime']
        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               ui_format_pattern=self.event_card_today_time_format_pattern,
                                                               ss_data=True
                                                               )
        self.assertEqual(event_time_ui, event_time_resp_converted,
                         msg=f'Event time on UI "{event_time_ui}" is not the same as got '
                         f'from response "{event_time_resp_converted}"')

    def test_007_click_tap_anywhere_on_event_section_except_priceodds_button(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event section (except 'Price/Odds' button)
        EXPECTED: Event Details Page is opened
        """
        self.event.click()
        self.site.wait_content_state(state_name='EventDetails')
