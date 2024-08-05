import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.csp
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C64881013_User_with_segmentation_but_no_config_in_CMS_universal_view(Common):
    """
    TR_ID: C64881013
    NAME: User with segmentation, but no config in CMS  (universal view)
    DESCRIPTION: This test case verifies user with segmentation, but no config in CMS
    PRECONDITIONS: 1) User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: Â 2) No configuration in CMS for CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True
    highlights_carousels_title = [generate_highlights_carousel_name()]
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > Highlights Carousels
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_autotest_premier_league_football_event()
            event_id = event.event_id
        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            event_id = event['event']['id']
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0], events=[event_id])
        self.__class__.highlights_carousel_name = self.highlights_carousels_title[0] if not self.brand == 'ladbrokes' \
            else self.highlights_carousels_title[0].upper()

    def test_001_launch_coral_and_lads_appmobile_web_and_verify_universal_view(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web and verify universal view
        EXPECTED: Home page should load with as per CMS universal config
        """
        self.site.wait_content_state('homepage')

    def test_002_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Universal view should displayed as there is no congifuration for specific segement
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        featured_tab = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.site.home.module_selection_ribbon.tab_menu.click_button(featured_tab)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')
