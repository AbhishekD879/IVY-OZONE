import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from datetime import datetime
from faker import Faker
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65593375_Verify_sports_pages_Event_hub_should_display_universal_view_as_CSP_is_not_extended_for_HC_and_QL_Modules_other_than_super_button_surface_bet_modules(BaseFeaturedTest):
    """
    TR_ID: C65593375
    NAME: Verify sports pages/Event hub should display universal view as CSP is not extended for HC and QL modules (other than super button/surface bet modules).
    DESCRIPTION: This test cases verifies sports pages/Event hub should display universal view as CSP is not extended (other than super button/surface bet modules).
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2)Create a record in Event hub/sports pages for HC/QL/Featured/inplay module in segmented view.
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    highlights_carousels_title = [generate_highlights_carousel_name()]
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    quick_link_name = 'Autotest ' + Faker().city()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > HC/QL
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        if tests.settings.backend_env != 'prod':
            event_id = self.ob_config.add_autotest_premier_league_football_event().event_id
        else:
            event_id = self.get_active_events_for_category()[0]['event']['id']
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False, hours=-7,
                                            minutes=-1)[:-3] + 'Z'
        self.__class__.quick_link = self.cms_config.create_quick_link(title=self.quick_link_name,
                                                                      sport_id=self.homepage_id.get('homepage'),
                                                                      destination=self.destination_url,
                                                                      inclusionList=[self.segment],
                                                                      universalSegment=False,
                                                                      date_from=date_from)
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0],
                                                   events=[event_id], inclusionList=[self.segment],
                                                   universalSegment=False)
        self.__class__.highlights_carousel_name = self.highlights_carousels_title[0] if not self.brand == 'ladbrokes' else self.highlights_carousels_title[0].upper()

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_login_with_segmented_user_as_per_precondtion(self):
        """
        DESCRIPTION: Login with segmented user as per precondtion
        EXPECTED: Segmented data should displayed in HOME PAGE
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_003_navigate_to_sports_pagesevent_hub_and_verify_hcqlfeaturedinplay_module(self):
        """
        DESCRIPTION: Navigate to Sports pages/Event hub and verify HC/QL/Featured/inplay module.
        EXPECTED: As CSP is not applicable for sports pages /Event hub for HC/QL/Featured/inplay modules,so user should see Unviversal view.
        """
        self.wait_for_quick_link(name=self.quick_link_name)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(self.quick_link_name)
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_name}" not found')
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')
