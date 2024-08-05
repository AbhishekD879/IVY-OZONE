import pytest
from faker import Faker
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.coupons
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.medium
@vtest
class Test_C451143_Verify_Football_Coupons_ordering_on_Landing_page(BaseCouponsTest):
    """
    TR_ID: C451143
    NAME: Verify Football Coupons ordering on Landing page
    DESCRIPTION: This test case verifies Football Coupons ordering on Landing page
    PRECONDITIONS: **CMS Configuration:**
    PRECONDITIONS: Football Coupon ->Coupon Segments -> Create New Segment -> Featured coupon section
    PRECONDITIONS: NOTE:  **Popular coupon** section contains all the rest of available coupons EXCEPT coupons are present in *Featured section*
    PRECONDITIONS: 1) In order to get a list of coupons use the following link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Coupon?existsFilter=coupon:simpleFilter:event.startTime:greaterThanOrEqual:2017-07-04T21:00:00.000Z&existsFilter=coupon:simpleFilter:event.suspendAtTime:greaterThan:2017-07-05T13:09:30.000Z&existsFilter=coupon:simpleFilter:event.isStarted:isFalse&simpleFilter=coupon.siteChannels:contains:M&existsFilter=coupon:simpleFilter:event.categoryId:intersects:16&existsFilter=coupon:simpleFilter:event.cashoutAvail:equals:Y&translationLang=en
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    """
    keep_browser_open = True
    featured_coupons = 'Auto segment ' + Faker().city()
    football_autotest_coupon_name = 'Football Auto Test Coupon'
    euro_elite_coupon_name = 'Euro Elite Coupon'
    uk_coupon_name = 'UK Coupon'
    coupon_resp = None
    ss_req = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add events to the following coupons: Football Autotest Coupon, Euro Elite Coupon, UK Coupon
        DESCRIPTION: Football Coupon are configured and enabled
        """
        football_autotest_coupon = self.ob_config.backend.ti.football.coupons.get(self.football_autotest_coupon_name)
        euro_elite_coupon = self.ob_config.backend.ti.football.coupons.get(self.euro_elite_coupon_name)
        uk_coupon = self.ob_config.backend.ti.football.coupons.get(self.uk_coupon_name)

        football_coupons = self.get_initial_data_system_configuration().get('FootballCoupons', {})
        if not football_coupons:
            football_coupons = self.cms_config.get_system_configuration_item('FootballCoupons')
        if not football_coupons.get('enabled'):
            raise CmsClientException('"Football Coupons" module is disabled')
        self.cms_config.add_coupon_segment(
            segment_name=self.featured_coupons,
            coupon_ids=f'{football_autotest_coupon},{uk_coupon},{euro_elite_coupon}')

        autotest_event_id = self.ob_config.add_autotest_premier_league_football_event().event_id
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        autotest_match_result_market_id = self.ob_config.market_ids[autotest_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=autotest_match_result_market_id,
                                           coupon_name='Football Auto Test Coupon')

        laliga_event_id = self.ob_config.add_football_event_to_spanish_la_liga().event_id
        market_short_name = self.ob_config.football_config. \
            spain.spanish_la_liga.market_name.replace('|', '').replace(' ', '_').lower()
        laliga_match_result_market_id = self.ob_config.market_ids[laliga_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=laliga_match_result_market_id, coupon_name='Euro Elite Coupon')

        epl_event_id = self.ob_config.add_football_event_to_england_premier_league().event_id
        market_short_name = self.ob_config.football_config. \
            england.premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        epl_match_result_market_id = self.ob_config.market_ids[epl_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=epl_match_result_market_id, coupon_name='UK Coupon')

        self.__class__.coupon_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.coupons,
            self.ob_config.football_config.category_id)

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')
        result = self.site.football.tabs_menu.current
        self.assertTrue(result, msg=f'"{self.expected_sport_tabs.matches}" tab was not opened')

    def test_002_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: * 'Coupons' tab is selected and highlighted
        EXPECTED: * Coupons Landing page is loaded
        EXPECTED: * **Featured Coupons**(CMS configurable) and **Popular Coupons**(all the rest of available coupons) sections are shown on the Coupons Landing page
        EXPECTED: * List of coupons is displayed on the Coupons Landing page according to related section
        """
        coupons = self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        self.assertTrue(coupons, msg='Coupons page was not opened')
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is "{current_tab}" but Coupons is expected '
                             f'to be active: "{self.coupon_tab_name}"')

        # Popular Coupons
        self.get_coupons_list_in_coupons_section(coupon_section=vec.coupons.POPULAR_COUPONS.upper())

        # Featured Coupon
        featured_coupon_list = self.get_coupons_list_in_coupons_section(coupon_section=self.featured_coupons.upper())

        self.__class__.featured_coupon_list_ui = list(featured_coupon_list.keys())
        self.__class__.created_featured_coupons_list = [self.football_autotest_coupon_name, self.uk_coupon_name, self.euro_elite_coupon_name]
        self.assertListEqual(self.created_featured_coupons_list, self.featured_coupon_list_ui,
                             msg=f'Created coupons "{self.created_featured_coupons_list}"'
                             f'not equal to "{self.featured_coupon_list_ui}"')

    def test_003_verify_coupons_order(self):
        """
        DESCRIPTION: Verify coupons order
        EXPECTED: Featured Coupons are ordered according to CMS config
        EXPECTED: Popular Coupons are ordered by 'displayOrder' in ascending
        """
        coupons_list_from_response = self.get_active_coupons_list()
        self._logger.debug('*** Available coupons in SiteServe response %s' % coupons_list_from_response)

        expected_featured_coupons_order = [self.football_autotest_coupon_name, self.uk_coupon_name, self.euro_elite_coupon_name]
        self.assertListEqual(self.featured_coupon_list_ui, expected_featured_coupons_order,
                             msg=f'\n Actual order of coupons on UI: \n"{self.featured_coupon_list_ui}" \n '
                                 f'are not the same as created: \n"{expected_featured_coupons_order}"')
