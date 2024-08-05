import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C64881024_Verify_HC_when_inplay_check_box_is_checked(BaseFeaturedTest):
    """
    TR_ID: C64881024
    NAME: Verify HC when inplay check box is checked
    DESCRIPTION: This Test case verifies HC for live events
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS > Sports pages >home page>HC
    """
    keep_browser_open = True
    highlights_carousels_title = [generate_highlights_carousel_name(), generate_highlights_carousel_name()]
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
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
                                                   events=[event_id1], inplay=True, inclusionList=[self.segment],
                                                   universalSegment=False)

        self.__class__.highlights_carousel_name_with_inplay_chkbox = self.highlights_carousels_title[0] if not self.brand == 'ladbrokes' \
            else self.highlights_carousels_title[0].upper()

        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[1],
                                                   events=[event_id2], inclusionList=[self.segment],
                                                   universalSegment=False)
        self.__class__.highlights_carousel_name_without_inplay_chkbox = self.highlights_carousels_title[1] if not self.brand == 'ladbrokes' \
            else self.highlights_carousels_title[1].upper()

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be able to see the HC module page with existing Universal HC records
        """
        # covered in step 001

    def test_003_click_on_create_highlight_carousel_cta(self):
        """
        DESCRIPTION: Click on Create highlight carousel CTA
        EXPECTED: User should able view detail page
        """
        # covered in step 001

    def test_004_create_hc_with_display_inplay_check_box_is_checked(self):
        """
        DESCRIPTION: Create HC with display inplay check box is checked
        EXPECTED: HC should able to create successfully
        """
        # covered in step 001

    def test_005_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_006_verify_hc__in_home_page(self):
        """
        DESCRIPTION: Verify HC  in Home page
        EXPECTED: Inplay events should display in HC ,as display inplay check box is checked in CMS
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_with_inplay_chkbox)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_with_inplay_chkbox}')

    def test_007_create_hc_with_display_inplay_check_box_is_unchecked(self):
        """
        DESCRIPTION: Create HC with display inplay check box is unchecked
        EXPECTED: HC should able to create successfully
        """
        # covered in step 001

    def test_008_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        # covered in step 005

    def test_009_verify_hc__in_home_page(self):
        """
        DESCRIPTION: Verify HC  in Home page
        EXPECTED: Pre events should only display in HC ,as display inplay check box is unchecked in CMS
        """
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name_without_inplay_chkbox)
        self.assertFalse(highlight_carousel,
                         msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name_without_inplay_chkbox}')
