import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import generate_highlights_carousel_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C65581902_Verify_HC_module_are_created_with_inplay_events_display_inplay_checked_Unchecked_for_Universal_Segment(Common):
    """
    TR_ID: C65581902
    NAME: Verify HC module is created with inplay events (display inplay checked/Unchecked) for Universal/Segment
    DESCRIPTION: This testcase verifies Inplay module data when HC are Featured module created with inplay events
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS &gt; Sports pages &gt;home page&gt;HC/Featured tab module
    """
    keep_browser_open = True
    highlights_carousels_title = [generate_highlights_carousel_name(), generate_highlights_carousel_name()]
    sport_id = {'homepage': 0}

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        if tests.settings.backend_env == 'prod':
            try:
                events = self.get_active_events_for_category(
                    category_id=self.ob_config.football_config.category_id,
                    in_play_event=True, number_of_events=2)
            except Exception:
                events = self.get_active_events_for_category(
                    category_id=self.ob_config.tennis_config.category_id,
                    in_play_event=True, number_of_events=2)
            event_id1 = events[0]['event']['id']
            event_id2 = events[1]['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            event_id1 = event.event_id
            event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            event_id2 = event.event_id
            self._logger.info(f'*** Created Football eventwith ID "{event_id1}", "{event_id2}"')

        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0],
                                                   events=[event_id1], inplay=True,
                                                   universalSegment=True)

        self.__class__.highlights_carousel_name_with_inplay_chkbox = self.highlights_carousels_title[0] if not self.brand == 'ladbrokes' \
            else self.highlights_carousels_title[0].upper()

        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[1],
                                                   events=[event_id2],
                                                   universalSegment=True)
        self.__class__.highlights_carousel_name_without_inplay_chkbox = self.highlights_carousels_title[1] if not self.brand == 'ladbrokes' \
            else self.highlights_carousels_title[1].upper()

    def test_002_navigate_to_highlights_carousal_module(self):
        """
        DESCRIPTION: Navigate to Highlights carousal module
        EXPECTED: Highlight carousal module page should be loaded with existing records
        """
        # covered in above step

    def test_003_create_universal_hc_record_with_type_id_live_eventsex_442_with_tick_display_inplay_check_box(self):
        """
        DESCRIPTION: Create universal HC record with type id (Live events)(ex: 442) With tick display inplay check box
        EXPECTED: Record should be created successfully
        """
        # covered in step1

    def test_004_launch_oxygen_app(self):
        """
        DESCRIPTION: Launch oxygen app
        EXPECTED: Home page should launch succesfully
        """
        self.site.wait_content_state('Homepage')

    def test_005_home_page_should_launch_succesfully(self):
        """
        DESCRIPTION: Home page should launch succesfully
        EXPECTED: Created record should be displayed under Highlight carousal
        """
        self.site.login()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_with_inplay_chkbox)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_with_inplay_chkbox}')

    def test_006_verify_above_steps_with_event_id_for_hc_module(self):
        """
        DESCRIPTION: Verify above steps with Event ID for HC module
        EXPECTED: Created record should be displayed under Highlight carousal based on priority.same events should not be display in Featured /Inplay Module
        """
        # covered in step 7

    def test_007_repeat_from_step_2_to_5__by_unchecking_display_inplay_check_box(self):
        """
        DESCRIPTION: Repeat from step 2 to 5 , by unchecking display inplay check box
        EXPECTED: Created record should be displayed under Highlight carousal
        """
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_without_inplay_chkbox)
        self.assertFalse(highlight_carousel,
                         msg=f'displayed Highlights Carousel named {self.highlights_carousel_name_without_inplay_chkbox}')
