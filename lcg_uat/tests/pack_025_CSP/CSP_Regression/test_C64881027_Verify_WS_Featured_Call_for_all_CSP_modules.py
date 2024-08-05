import pytest
import tests
import time
import voltron.environments.constants as vec
from datetime import datetime
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test \
    import generate_highlights_carousel_name
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@pytest.mark.reg157_fix
@vtest
class Test_C64881027_Verify_WS_Featured_Call_for_all_CSP_modules(BaseFeaturedTest):
    """
    TR_ID: C64881027
    NAME: Verify WS-Featured Call for all CSP modules
    DESCRIPTION: This test case verifies Featured data call for all CSP modules
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    highlights_carousels_title = [generate_highlights_carousel_name()]
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}'

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst

        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
            self._logger.info(f'*** Found Football event with id "{self.eventID}"')
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are not available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(selection_ids.values())[0]

        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            eventID = event.event_id
            selection_ids, self.__class__.team1 = event.selection_ids, event.team1
            selection_id = selection_ids[self.team1]

        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.__class__.quick_link_title = 'Autotest_' + 'C64881027'
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=self.quick_link_title,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from,
                                          universalSegment=False,
                                          inclusionList=[self.segment])
        self.__class__.feature_module_name = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                                     id=eventID,
                                                                                     universalSegment=False,
                                                                                     inclusionList=[self.segment],
                                                                                     events_time_from_hours_delta=-10,
                                                                                     module_time_from_hours_delta=-10
                                                                                     )['title'].upper()

        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                                     categoryIDs=[self.homepage_id.get('homepage')],
                                                                     highlightsTabOn=True,
                                                                     inclusionList=[self.segment],
                                                                     universalSegment=False)
        self.__class__.surface_bet_name = self.surface_bet['title'].upper()

        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0],
                                                   events=[eventID], inclusionList=[self.segment],
                                                   universalSegment=False)
        self.__class__.highlights_carousel_name = self.highlights_carousels_title[0] if not self.brand == 'ladbrokes' \
            else self.highlights_carousels_title[0].upper()

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")

    def test_002_login_with_segmented_user_as_per_precondtion_inspect_the_screen_and_verify_calls_in_network_tab_in_ws(
            self):
        """
        DESCRIPTION: Login with segmented user as per precondtion, Inspect the screen and verify calls in network tab in WS
        EXPECTED: In WS,FEATURED_STRUCTURE_CHANGED call should received after 1 min and after refresh for Super button,Footer menu and MRT
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)

    def test_003_(self):
        """
        DESCRIPTION:
        EXPECTED: In WS,FEATURED_STRUCTURE_CHANGED call should received without refresh for all remaining modules (Surfacebet,HC,QL,Featured module)
        """
        self.device.refresh_page()
        self.wait_for_featured_module(name="QUICK LINK MODULE")
        self.wait_for_featured_module(name="SURFACE BET MODULE")
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name.upper(), expected_result=True)
        self.wait_for_featured_module(name=self.highlights_carousel_name.upper())
        self.wait_for_featured_module(name=self.feature_module_name)
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_004_verify_in_fe(self):
        """
        DESCRIPTION: Verify in FE
        EXPECTED: Once we received call,data should reflect in Homepage
        """
        module = self.wait_for_featured_module(name=self.feature_module_name)
        self.assertTrue(module, msg=f'"{self.feature_module_name}" module is not found')
        self.wait_for_highlights_carousels(name=self.highlights_carousel_name.upper(), expected_result=True)
        self.device.refresh_page()
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        HC_name = self.highlights_carousels_title[0].upper() if self.brand == 'ladbrokes' else\
            self.highlights_carousels_title[0]
        self.assertIn(HC_name, list(highlight_carousels.keys()),
                      msg=f'Highlights Carousel named "{HC_name}" was not found in {list(highlight_carousels.keys())}')
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel.is_displayed(),
                        msg=f'Failed to display Highlights Carousel named "{self.highlights_carousel_name}"')

        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_name)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_name}" not found in "{list(surface_bets.keys())}"')

        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertIn(self.quick_link_title, list(quick_links.keys()),
                      msg=f'Can not find "{self.quick_link_title}" in "{list(quick_links.keys())}"')
