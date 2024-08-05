import re
import pytest
from crlat_ob_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.prod_incident
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.sports
@pytest.mark.high
@pytest.mark.desktop
@vtest
class Test_C440338_Verify_Coupons_Details_Page_and_Change_Coupon_Selector(BaseCouponsTest):
    """
    TR_ID: C440338
    VOL_ID: C11495669
    NAME: This test case verifies Coupons Details page
    PRECONDITIONS: 1) In order to get an information about particular coupon use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/CouponToOutcomeForCoupon/XXX?simpleFilter=event.startTime:lessThan:2017-07-15T09:01:00.000Z&simpleFilter=event.categoryId:intersects:16&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.isStarted:isFalse&simpleFilter=event.startTime:greaterThanOrEqual:2017-07-09T21:00:00.000Z&simpleFilter=event.suspendAtTime:greaterThan:2017-07-10T09:01:00.000Z&translationLang=en
    PRECONDITIONS: XXX - coupon's id
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    """
    keep_browser_open = True
    autotest_coupon = 'Football Auto Test Coupon'
    uk_coupon = 'UK Coupon'

    start_date = f'{get_date_time_as_string(days=-1)}T22:00:00.000Z'
    end_date = f'{get_date_time_as_string(days=5)}T00:00:00.000Z'
    ss_req_football = None

    def verify_correct_events_displayed_for_coupon(self, coupon_name):
        active_events_query = self.basic_active_events_filter() \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_STATUS_CODE, OPERATORS.EQUALS, 'A')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                      self.ob_config.backend.ti.football.category_id))
        resp = self.ss_req_football.ss_coupon_to_outcome_for_coupon(
            coupon_id=self.ob_config.backend.ti.football.coupons[coupon_name], query_builder=active_events_query)
        self.__class__.coupon_events = [x for x in resp[0]['coupon']['children']]
        events_names_from_ss_resp = [x['event']['name'] for x in self.coupon_events]
        events_names_on_page = []
        self.__class__.sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in self.sections.items():
            date_groups = section.items_as_ordered_dict
            self.assertTrue(date_groups, msg='No date groups found on Coupon section "%s"' % section_name)
            for name, date_group in date_groups.items():
                events = date_group.items_as_ordered_dict
                self.assertTrue(events, msg='No events found on Coupon details page in date group "%s"' % name)
                for event_name, events in events.items():
                    events_names_on_page.append(event_name)

        self.assertListEqual(sorted(events_names_on_page), sorted(events_names_from_ss_resp),
                             msg=f'Incorrect events names order.\nActual is:\n{sorted(events_names_on_page)}\n'
                             f'Expected is:\n{sorted(events_names_from_ss_resp)}')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add events to the following coupons: Football Autotest Coupon and Football Auto Test Coupon No Cashout
        """
        self.__class__.coupon_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
                                                                 self.ob_config.football_config.category_id)

        autotest_event_id = self.ob_config.add_autotest_premier_league_football_event().event_id
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        autotest_match_result_market_id = self.ob_config.market_ids[autotest_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=autotest_match_result_market_id,
                                           coupon_name=self.autotest_coupon)

        epl_event_id = self.ob_config.add_football_event_to_england_premier_league().event_id
        market_short_name = self.ob_config.football_config. \
            england.premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        epl_match_result_market_id = self.ob_config.market_ids[epl_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=epl_match_result_market_id,
                                           coupon_name=self.uk_coupon)

        self.__class__.ss_req_football = SiteServeRequests(env=tests.settings.backend_env,
                                                           brand=self.brand,
                                                           category_id=self.ob_config.backend.ti.football.category_id)

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: Football Landing page is opened
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')

    def test_002_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'COUPONS' tab
        EXPECTED: * 'Coupons' tab is selected and highlighted
        EXPECTED: * 'Coupons Landing page is loaded
        """
        coupons = self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        self.assertTrue(coupons, msg='Coupons page was not opened')
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is {current_tab} but Coupons is expected to be active')

    def test_003_navigate_to_coupon_details_page(self, expected_coupon_name=autotest_coupon):
        """
        DESCRIPTION: Navigate to Coupon Details page
        EXPECTED: Coupon Details page is loaded
        """
        self.find_coupon_and_open_it(coupon_name=expected_coupon_name)

    def test_004_verify_url_when_navigating_to_coupon_details_page(self, expected_coupon_name=autotest_coupon):
        """
        DESCRIPTION: Verify URL when navigating to Coupon Details page
        EXPECTED: https://{websitename}.coral.co.uk/football/coupons/couponname/id is displayed in URL for selected coupon
        """
        if self.brand != 'ladbrokes':
            page_title = self.site.coupon.header_line.page_title.title
            self.assertEqual(page_title, vec.coupons.COUPONS_TITLE,
                             msg=f'Page title {page_title} is not the same as expected {vec.coupons.COUPONS_TITLE}')
        current_url = self.device.get_current_url()
        url_pattern = r'^http[s]?:\/\/.+\/coupons\/football\/([\w-]+)\/([\d]+)'
        self.assertRegexpMatches(current_url, url_pattern,
                                 msg=f'Current url {current_url} not matching expected pattern {url_pattern}')
        match_groups = re.search(url_pattern, current_url).groups()
        coupon_name_in_url = match_groups[0]
        coupon_id_in_url = match_groups[1]
        self._logger.info(f'*** Coupon name is {coupon_name_in_url}, id is {coupon_id_in_url}')
        expected_coupon_name_in_url = expected_coupon_name.lower().replace(' ', '-')
        self.assertEqual(
            coupon_name_in_url, expected_coupon_name_in_url,
            msg=f'Coupon name in url {coupon_name_in_url} is not the same as expected {expected_coupon_name}')
        self.assertEqual(coupon_id_in_url, str(self.ob_config.backend.ti.football.coupons.get(expected_coupon_name)),
                         msg=f'Coupon id in url {coupon_id_in_url} is not the same as expected '
                         f'{self.ob_config.backend.ti.football.coupons.get(expected_coupon_name)}')

    def test_005_verify_coupons_header(self):
        """
        DESCRIPTION: Verify Coupons header
        EXPECTED: The following elements are present on Coupons header:
        EXPECTED: * 'Back' button
        EXPECTED: * 'Coupons' inscription
        """
        if self.device_type != 'desktop':
            if self.brand != 'ladbrokes':
                self.assertTrue(self.site.coupon.header_line.has_back_button,
                                msg='There\'s no back button on Coupon page header')
            else:
                self.assertTrue(self.site.header.has_back_button, msg='Back button is not displayed')

    def test_006_verify_coupons_sub_header(self, expected_coupon_name=autotest_coupon):
        """
        DESCRIPTION: Verify Coupons sub-header
        EXPECTED: * Coupons sub-header is located below Coupons header
        EXPECTED: * "Name of selected coupon" is displayed at the left side of Coupons sub-header
        EXPECTED: * "Change Coupon" link and image is displayed at the right side of Coupons sub-header
        """
        coupon_name = self.site.coupon.name
        self.assertEqual(coupon_name, expected_coupon_name,
                         msg=f'Coupon name in subheader {coupon_name} '
                             f'is not the same as expected {expected_coupon_name}')
        if self.brand != 'ladbrokes':
            self.assertTrue(self.site.coupon.has_coupon_selector, msg='Coupon subheader doesn\'t have coupon selector')

    def test_007_verify_coupons_page_content(self, expected_coupon_name=autotest_coupon):
        """
        DESCRIPTION: Verify Coupons page content
        EXPECTED: * Events for appropriate coupon are displayed on Coupons Details page
        EXPECTED: * Events are grouped by **classId** and **typeId**
        EXPECTED: * First **three** accordions are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the accordions by tapping the accordion's header
        EXPECTED: * If no events to show, the message '**No events found**' is displayed
        """
        self.verify_correct_events_displayed_for_coupon(coupon_name=expected_coupon_name)
        self.__class__.sections = self.site.coupon.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No event groups found on Coupon page')
        if len(self.sections) >= 3:
            for section_name, section in list(self.sections.items())[:3]:
                self.assertTrue(section.is_expanded(), msg='Section "%s" is not expanded by default' % section_name)

    def test_008_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: * Coupons Landing page is loaded
        EXPECTED: * List of coupons is displayed
        """
        self.site.back_button_click()
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is {current_tab} but Coupons is expected to be active')

    def test_009_repeat_steps_4_9_for_all_coupons_on_the_page(self, coupon_name=uk_coupon):
        """
        DESCRIPTION: Repeat steps 4-9 for all coupons on the page
        """
        self.test_003_navigate_to_coupon_details_page(expected_coupon_name=coupon_name)
        self.test_004_verify_url_when_navigating_to_coupon_details_page(expected_coupon_name=coupon_name)
        self.test_005_verify_coupons_header()
        self.test_006_verify_coupons_sub_header(expected_coupon_name=coupon_name)
        self.test_007_verify_coupons_page_content(expected_coupon_name=coupon_name)
        self.test_008_tap_back_button()
