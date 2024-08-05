from time import sleep
import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65593376_Verify_sports_pages_Event_hub_should_display_universal_view_as_CSP_is_not_extended_for_Featured_and_Inplay_Modules_other_than_super_button_surface_bet_modules(BaseFeaturedTest):
    """
    TR_ID: C65593376
    NAME: Verify sports pages/Event hub should display universal view as CSP is not extended for Featured and In play modules (other than super button/surface bet modules).
    DESCRIPTION: This test cases verifies sports pages/Event hub should display universal view as CSP is not extended (other than super button/surface bet modules).
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 2)Create a record in Event hub/sports pages for Featured/inplay module in segmented view.
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > HC/QL
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            eventID = event.event_id
        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                             id=eventID,
                                                                             universalSegment=False,
                                                                             inclusionList=[self.segment],
                                                                             events_time_from_hours_delta=-10,
                                                                             module_time_from_hours_delta=-10
                                                                             )['title'].upper()

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

    def test_003_navigate_to_sports_pagesevent_hub_and_verify_featuredinplay_module(self):
        """
        DESCRIPTION: Navigate to Sports pages/Event hub and verify Featured/inplay module.
        EXPECTED: As CSP is not applicable for sports pages /Event hub for HC/QL/Featured/inplay modules,so user should see Unviversal view.
        """
        sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertTrue(sports, msg='No inplay sports found in the module')
        self.__class__.sport = sports[0]
        self.cms_config.update_inplay_sport_module(sport_name=self.sport.title(), universalSegment=False,
                                                   inclusionList=[self.segment])
        self.device.refresh_page()
        self.assertTrue(self.site.home.tab_content.has_in_play_module(timeout=10), msg="Inplay module not found")
        sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertIn(self.sport, sports, msg=f'Segmented record {self.sport} is not displayed among {sports}')
        featured_tab = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab)
        module = self.wait_for_featured_module(name=self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')
        sleep(5)
        self.site.open_sport(self.sport)
        self.assertTrue(self.site.home.tab_content.has_in_play_module(timeout=10), msg="Inplay module not found")
        sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertNotIn(self.sport, sports, msg=f'Segmented record {self.sport} is displayed among {sports}')

    @classmethod
    def custom_tearDown(cls):
        cls.get_cms_config().update_inplay_sport_module(segment_name=cls.segment,
                                                        sport_name=cls.sport.title(), universalSegment=True)
