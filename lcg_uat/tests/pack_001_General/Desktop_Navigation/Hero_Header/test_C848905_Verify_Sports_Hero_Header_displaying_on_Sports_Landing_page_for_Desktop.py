import voltron.environments.constants as vec
import time

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_017_Promotions_Banners_Offers.Offers.BaseOffersTest import BaseOffersTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.medium
@pytest.mark.football
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.navigation
@pytest.mark.offers
@vtest
class Test_C848905_Verify_Sports_Hero_Header_displaying_on_Sports_Landing_page_for_Desktop(BaseSportTest, BaseOffersTest):
    """
    TR_ID: C848905
    VOL_ID: C9698298
    NAME: Verify Sports Hero Header displaying on Sports Landing page for Desktop
    DESCRIPTION: This test case verifies Sports Hero Header displaying on Sports Landing page content.
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Sports Landing page is opened
    PRECONDITIONS: 3. 'Matches'->'Today' tab is opened by default
    PRECONDITIONS: 4. Enhanced Multiples are present
    PRECONDITIONS: 5. Offers are present
    """
    keep_browser_open = True
    outright_name = f'Outright {int(time.time())}'
    coupon = vec.siteserve.EXPECTED_COUPON_NAME
    device_name = tests.desktop_default
    expected_breadcrumbs = ['Home', 'Football', 'Matches']

    def is_breadcrumb_highlighted(self, breadcrumb):
        """
        Verify breadcrumb is highlighted
        :param breadcrumb:
        """
        self.assertTrue(int(breadcrumb.link.css_property_value('font-weight')) == 700,
                        msg='"Matches" hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_000_preconditions(self):
        """
        DESCRIPTION: add offer if it is not present
        DESCRIPTION: add outright and special events, add coupons and check JACKPOT presence
        """
        cms_banners = self.get_initial_data_system_configuration().get('DynamicBanners')
        if not cms_banners:
            cms_banners = self.cms_config.get_system_configuration_item('DynamicBanners')

        use_aem_offer_modules_banners = cms_banners.get('useAemOfferModulesBanners', False)
        if use_aem_offer_modules_banners:
            raise CmsClientException('CMS offers won\'t be shown as AEM offers are enabled')
        all_cms_offer_modules = self.cms_config.get_offer_modules()
        offer_module = next((module for module in all_cms_offer_modules if module.get('name') == f'{self.cms_config.constants.OFFER_MODULE_NAME} C848905'), None)
        if not offer_module:
            offer_module = self.cms_config.create_offer_module(name=f'{self.cms_config.constants.OFFER_MODULE_NAME} C848905')
        offer_module_id = offer_module.get('id')
        self.cms_config.add_offer(offer_module_id=offer_module_id)

        tabs = self.cms_config.get_sport_config(category_id=self.ob_config.football_config.category_id).get('tabs')
        self.__class__.expected_football_tab_names = [i['label'].upper() for i in tabs]

        ss_req_football = SiteServeRequests(env=tests.settings.backend_env,
                                            brand=self.brand,
                                            category_id=self.ob_config.backend.ti.football.category_id)
        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.TYPE, OPERATORS.EQUALS, 'V15')) \
            .add_filter(simple_filter(LEVELS.POOL, ATTRIBUTES.IS_ACTIVE))
        if not ss_req_football.ss_pool(query_builder=query, raise_exceptions=False):
            self.expected_football_tab_names.remove(self.expected_sport_tabs.jackpot)

        self.ob_config.add_autotest_premier_league_football_outright_event(event_name=self.outright_name,
                                                                           selections_number=1)
        self.ob_config.add_autotest_premier_league_football_event(special=True)

        self.ob_config.add_football_event_enhanced_multiples()
        self.ob_config.add_football_event_enhanced_multiples()
        self.ob_config.add_autotest_premier_league_football_outright_event()

        epl_event_id = self.ob_config.add_football_event_to_england_premier_league().event_id
        market_short_name = self.ob_config.football_config. \
            england.premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        epl_match_result_market_id = self.ob_config.market_ids[epl_event_id][market_short_name]
        self.ob_config.add_event_to_coupon(market_id=epl_match_result_market_id, coupon_name=self.coupon)
        self.ob_config.add_football_event_enhanced_multiples()

    def test_001_verify_sports_hero_header_content_on_the_sports_landing_page(self):
        """
        DESCRIPTION: Verify Sports Hero Header content on the Sports Landing page
        EXPECTED: Main View 1 and Main View 2 columns are merged and contain the following element:
        EXPECTED: * Sports header and 'Back' button
        EXPECTED: * Breadcrumbs trail
        EXPECTED: * AEM Banners section and Offer area (depends on screen width)
        EXPECTED: * Enhanced Multiples Caurosel
        EXPECTED: * Sports Sub tabs Menu
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        self.__class__.football = self.site.football

        current_tab = self.football.date_tab.current_date_tab if self.brand in ['bma', 'vanila'] \
            else self.football.date_tab.current_date_tab.upper()
        self.assertEqual(current_tab, self.date_tabs.today, msg=f'"{current_tab}" tab is not the same '
                                                                f'as expected "{self.date_tabs.today}"')

        page_title = self.football.header_line.page_title
        self.assertEqual(page_title.title, vec.siteserve.FOOTBALL_TAB,
                         msg=f'Page title {page_title.title} '
                             f'is not the same as expected {vec.siteserve.FOOTBALL_TAB}')

        self.__class__.title_coordinates = page_title.location.get('y')

    def test_002_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: 'Back' button is displayed on the Sports header
        """
        self.assertTrue(self.football.header_line.back_button, msg='Back button is not present')

    def test_003_verify_breadcrumbs_trail_displaying(self):
        """
        DESCRIPTION: Verify Breadcrumbs trail displaying
        EXPECTED: * Breadcrumbs trail is displayed below Sports header
        EXPECTED: * Breadcrumbs trail is displayed in the next format: 'Home' > 'Sports Name' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        breadcrumbs = self.football.breadcrumbs
        self.assertTrue(breadcrumbs, msg='Breadcrumbs trail is not present')
        self.assertTrue(breadcrumbs.items_as_ordered_dict, msg='No breadcrumbs found')
        actual_breadcrumbs = list(breadcrumbs.items_as_ordered_dict.keys())
        self.assertEqual(actual_breadcrumbs, self.expected_breadcrumbs,
                         msg=f'Breadcrumbs {actual_breadcrumbs} are not the same '
                             f'as expected {self.expected_breadcrumbs}')

        self.assertIn('Matches', breadcrumbs.items_as_ordered_dict.keys(), msg='"Matches" breadcrumb is not present')

        self.is_breadcrumb_highlighted(breadcrumbs.items_as_ordered_dict['Matches'])

        self.assertTrue(breadcrumbs.location.get('y') > self.title_coordinates,
                        msg='Breadcrumbs trail is not displayed below title')

    def test_004_verify_offer_section(self):
        """
        DESCRIPTION: Verify Offer section
        EXPECTED: * Offer section is displayed
        """
        self.assertTrue(self.football.offers_section, msg='Offers section is not present')

    def test_005_verify_aem_banners_section_displaying(self):
        """
        DESCRIPTION: Verify AEM Banners section displaying
        EXPECTED: * AEM banners are displayed below Breadcrumbs trail
        """
        aem_banner_section = self.football.aem_banner_section
        self.assertTrue(aem_banner_section, msg='AEM banner section is not present')

        self.__class__.aem_banner_coordinates = aem_banner_section.location.get('y')

    def test_006_verify_enhanced_multiples_carousel_displaying(self):
        """
        DESCRIPTION: Verify Enhanced Multiples carousel displaying
        EXPECTED: * Enhanced Multiples carousel is displayed below AEM Banners section
        EXPECTED: * Enhanced Multiples carousel contains separated sports cards that are scrolled to right and left side
        """
        em_carousel = self.football.sport_enhanced_multiples_carousel
        self.assertTrue(em_carousel, msg='Enhanced Multiples carousel is not displayed')
        self.assertTrue(self.aem_banner_coordinates < em_carousel.location.get('y'),
                        msg='Enhanced Multiples carousel is not displayed below AEM banners')

    def test_007_verify_sports_subtabs_displaying(self):
        """
        DESCRIPTION: Verify Sports Subtabs displaying
        EXPECTED: The next Sports Subtabs are displayed for Football:
        EXPECTED: - 'In-Play'
        EXPECTED: - 'Matches'
        EXPECTED: - 'Competitions'
        EXPECTED: - 'Coupons'
        EXPECTED: - 'Outrights'
        EXPECTED: - 'Jackpot'
        EXPECTED: - 'Specials'
        EXPECTED: - 'Player Bets'
        EXPECTED: The next Sports Subtabs are displayed for other Sports:
        EXPECTED: - 'In-Play'
        EXPECTED: - 'Matches'
        EXPECTED: - 'Coupons'
        EXPECTED: - 'Outrights'
        """
        self.assertTrue(self.football.tabs_menu.items_as_ordered_dict, msg='No subtabs found')
        subtabs = list(self.football.tabs_menu.items_as_ordered_dict.keys())
        self.assertEqual(sorted(subtabs), sorted(self.expected_football_tab_names),
                         msg=f'Subtabs {sorted(subtabs)} are not the same as '
                             f'expected {sorted(self.expected_football_tab_names)}')
