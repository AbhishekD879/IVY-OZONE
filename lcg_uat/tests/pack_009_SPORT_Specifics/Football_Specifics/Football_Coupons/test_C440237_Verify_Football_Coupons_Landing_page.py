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
@pytest.mark.high
@vtest
class Test_C440237_Verify_Football_Coupons_Landing_page(BaseCouponsTest):
    """
    TR_ID: C440237
    NAME: Verify Football Coupons Landing page
    DESCRIPTION: This test case verifies Football Coupons Landing page
    PRECONDITIONS: **CMS Configuration:**
    PRECONDITIONS: Football Coupon ->Coupon Segments -> Create New Segment - 'Featured Coupon' section
    PRECONDITIONS: NOTE:  **Popular coupon** section contains all the rest of available coupons EXCEPT coupons are present in *Featured section*
    PRECONDITIONS: 1. In order to create coupons use the following instruction https://confluence.egalacoral.com/display/SPI/How+to+create+a+Coupon+in+OB+and+TI+system
    PRECONDITIONS: 2. List of Coupons depends on TI tool configuration data for Coupons. All available Coupons from OB response will be displayed on the page
    """
    keep_browser_open = True
    segment_name = 'Auto segment ' + Faker().city()
    coupon_resp = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add events to the following coupons: Football Autotest Coupon, Euro Elite Coupon, UK Coupon
        DESCRIPTION: Football Coupon are configured and enabled
        """
        football_coupons = self.get_initial_data_system_configuration().get('FootballCoupons', {})
        if not football_coupons:
            football_coupons = self.cms_config.get_system_configuration_item('FootballCoupons')
        if not football_coupons.get('enabled'):
            raise CmsClientException('"Football Coupons" module is disabled')
        self.cms_config.add_coupon_segment(
            segment_name=self.segment_name,
            coupon_ids=self.ob_config.backend.ti.football.coupons.get('Football Auto Test Coupon'))

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
        EXPECTED: * **Featured Coupons**(CMS configurable) and **Popular Coupons**(all the rest of available coupons) sections are shown on the Coupons Landing page
        EXPECTED: * List of coupons is displayed on the Coupons Landing page according to related section
        EXPECTED: * It is possible to navigate on Coupons Details page by tapping a row from the list
        """
        coupons = self.site.football.tabs_menu.click_button(self.coupon_tab_name)
        self.assertTrue(coupons, msg='Coupons page was not opened')
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.coupon_tab_name,
                         msg=f'Active tab is "{current_tab}" but "{self.coupon_tab_name}" is expected"')

    def test_003_verify_list_of_coupons(self):
        """
        DESCRIPTION: Verify list of coupons
        EXPECTED: List of coupons includes:
        EXPECTED: * UK Coupon
        EXPECTED: * Odds on Coupon
        EXPECTED: * European Coupon
        EXPECTED: * Euro Elite Coupon
        EXPECTED: * Televised Matches
        EXPECTED: * Top Leagues Coupon
        EXPECTED: * International Coupon
        EXPECTED: * Rest of the World Coupon
        EXPECTED: * Goalscorer Coupon
        EXPECTED: ( All available Coupons from OB response will be displayed on the page)
        """
        coupons_list_from_response = self.get_active_coupons_list()

        coupon_list = self.get_coupons_list_in_coupons_section(coupon_section=vec.coupons.POPULAR_COUPONS.upper())
        popular_coupons_on_page = list(coupon_list.keys())

        featured_coupons = self.get_coupons_list_in_coupons_section(coupon_section=self.segment_name.upper())
        popular_coupons_on_page.append(list(featured_coupons.keys())[0])

        self.assertListEqual(sorted(coupons_list_from_response), sorted(popular_coupons_on_page),
                             msg=f'Coupons sorted list from SS: \n{sorted(coupons_list_from_response)} \n'
                             f'is not equal sorted to UI: \n"{sorted(popular_coupons_on_page)}"')
