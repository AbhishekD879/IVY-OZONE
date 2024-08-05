import pytest
import tests
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from tests.base_test import vtest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.reg157_fix
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C58668015_Verify_the_view_of_Virtual_Sports_EDP(BaseVirtualsTest):
    """
    TR_ID: C58668015
    NAME: Verify the view of Virtual Sports EDP
    DESCRIPTION: This test case verifies the view of Virtual Sports EDP
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        if '287' not in virtuals_cms_class_ids:
            raise SiteServeException('virtual football was not configured in CMS')
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')

    def test_001_navigate_to_the_virtual_sport_page(self):
        """
        DESCRIPTION: Navigate to the Virtual sport page
        EXPECTED: Page loads in order:
        EXPECTED: First Sport > First child sport > Next available event
        EXPECTED: EDP template automatically chosen according to sport and displayed with the below
        EXPECTED: details:
        EXPECTED: -  The event being displayed should be highlighted
        EXPECTED: -  Time of the event with the name of the event
        EXPECTED: -  Count down timer if the event hasn't started yet
        EXPECTED: -  List of the markets
        EXPECTED: -  CTA at the bottom of the page
        EXPECTED: Design:
        EXPECTED: https://app.zeplin.io/project/5d64f0e582415f9b2a7045aa/screen/5dee3f51be0bb316723dcf29
        virtual sports hub is configured to a new page and from virtual sports hub we navigate to virtual sports page.
        """
        self.site.open_sport(name=self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            virtual_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() != 'NEXT EVENTS'), None)
            next(iter(list(virtual_section.items_as_ordered_dict.values()))).click()
        expected_url = f'https://{tests.HOSTNAME}/virtual-sports'.replace('beta2', 'beta')
        wait_for_result(lambda: expected_url in self.device.get_current_url(), name='Page to be loaded', timeout=20)
        sport_corousal = self.site.virtual_sports.sport_carousel
        if 'Football' in sport_corousal.items_names:
            sport_corousal.open_tab('Football')
            self.__class__.flag = True

        tab_content = self.site.virtual_sports.tab_content
        event_time = tab_content.sport_event_time
        self.assertTrue(event_time.is_displayed(), msg=f'Event time: "{event_time.name} is not displayed')
        event_name = tab_content.sport_event_name
        self.assertTrue(event_name, msg=f'Event name: "{event_name} is not displayed')
        try:
            self.assertTrue(tab_content.has_timer(), msg=f'Timer is not displayed for the event: "{event_time}"')
            event_name, event = list(tab_content.event_off_times_list.items_as_ordered_dict.items())[0]
            self.assertTrue(event.is_selected(), msg=f'The event: "{event_name}" being displayed is not highlighted')
        except Exception:
            self._logger.info(f'Event: "{event_name}" is went to live')
        if self.flag:
            events = self.site.virtual_sports.tab_content.event_off_times_list.items_as_ordered_dict
            list(events.values())[len(events) - 1].click()
            markets = self.site.virtual_sports.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(markets.keys(), msg='List of the markets are not displayed')
        else:
            self.assertTrue(self.site.virtual_sports.tab_content.event_markets_list.market_tabs_list.is_displayed(),
                            msg='List of the markets are not displayed')
        page_url = self.device.get_current_url()
        url_parts = page_url.split('/')
        child_sports = tab_content.child_sport_carousel.items_as_ordered_dict
        for child_sport_name, child_sport in child_sports.items():
            if child_sport.is_selected():
                name = child_sport_name.replace(' ', '-').lower()
                break
        self.assertEqual(name, url_parts[-1],
                         msg=f'Expected event: "{name}" is not same as Expected: "{url_parts[-1]}"')
        child_sport = self.site.virtual_sports.sport_carousel.current.replace(' ', '-').lower()
        self.assertEqual(child_sport, url_parts[-2],
                         msg=f'Expected child sport: "{child_sport}" is not same as Expected: "{url_parts[-2]}"')
        self.assertEqual('virtual-sports', url_parts[-4],
                         msg=f'Expected child sport: "{"virtual-sports"}" is not same as Expected: "{url_parts[-2]}"')
        self.assertTrue(tab_content.cta_button.is_displayed(),
                        msg='CTA button at the bottom of the page is not displayed')

    def test_002_verify_markets_on_edp(self):
        """
        DESCRIPTION: Verify markets on EDP
        EXPECTED: List of the markets with the name of the market as the collapsible header and the first market expanded sorted by SiteServer display order
        """
        if self.flag:
            markets = self.site.virtual_sports.tab_content.accordions_list.items_as_ordered_dict
            for i in range(len(markets.values())):
                if i == 0:
                    self.assertTrue(list(markets.values())[i].is_expanded(),
                                    msg='First Market was not expanded by default')
                else:
                    self.assertFalse(list(markets.values())[i].is_expanded(),
                                     msg=f'Market: "{i}" was expanded which is not expected')
        else:
            self._logger.info('Can not verify whether markets are collapsed or not as virtual football is not available')

    def test_003_tap_on_cta_at_the_bottom(self):
        """
        DESCRIPTION: Tap on CTA at the bottom
        EXPECTED: - User redirected to another site URL
        EXPECTED: - Button text and link configured in CMS > Virtual Sports > [createdSport] > 'Button text', 'Cross-sell URL' fields
        """
        self.site.virtual_sports.tab_content.cta_button.click()
        if self.flag:
            try:
                self.site.wait_content_state('Football')
            except:
                wait_for_haul(2)
                self.site.wait_content_state('Football')
        else:
            self.site.wait_content_state_changed()
