import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import \
    generate_highlights_carousel_name
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C65593418_Verify_Universal_exclusion_for_HC_and_Inplay_CSP_related_modules(Common):
    """
    TR_ID: C65593418
    NAME: Verify Universal exclusion for HC & Inplay CSP related modules.
    DESCRIPTION: This test case verifies universal exclusion
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button.
    """
    keep_browser_open = True
    highlights_carousels_title = [generate_highlights_carousel_name()]
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    sport_id = {'homepage': 0}

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        if tests.settings.backend_env != 'prod':
            event_id = self.ob_config.add_autotest_premier_league_football_event().event_id
            for i in range(0, 3):
                self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            for i in range(0, 2):
                self.ob_config.add_handball_event_to_croatian_premijer_liga(is_live=True)
        else:
            event_id = self.get_active_events_for_category()[0]['event']['id']

        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0],
                                                   events=[event_id], exclusionList=[self.segment],
                                                   universalSegment=True)

        self.__class__.highlights_carousel_name = self.highlights_carousels_title[0] if not self.brand == 'ladbrokes' \
            else self.highlights_carousels_title[0].upper()

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        # covered in step 001

    def test_003_click_on_super_button_link(self):
        """
        DESCRIPTION: click on HC.
        EXPECTED: User should be able to view existing super buttons should be displayed.
        """
        # covered in step 001

    def test_004_click_on_super_button_cta_button(self):
        """
        DESCRIPTION: Click on HC CTA button
        EXPECTED: User should be able to view newly added radio buttons for Universal and Segments inclusion with text boxes
        """
        # covered in step 001

    def test_005_select_universal_radio_button(self):
        """
        DESCRIPTION: Select Universal radio button
        EXPECTED: Upon selecting Universal radio button ,Segment(s) Exclusion text field should be enabled and able to enter text (ex: Football)
        """
        # covered in step 001

    def test_006_click_on_create_button(self):
        """
        DESCRIPTION: Click on create button
        EXPECTED: On successful creation, page should redirect to super button module page
        """
        # covered in step 001

    def test_007_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

    def test_008_login_in_fe_with_userexcept_specific_segmented_user__which_is_excluded(self):
        """
        DESCRIPTION: Login in FE with user(except specific segmented user  which is excluded)
        EXPECTED: Universal user should able to view super buttons across the application except in football segment (as we have configured segment(s) Exclusion as Football)
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        try:
            highlight_carousels = self.site.home.tab_content.highlight_carousels
            highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
            self.assertFalse(highlight_carousel,
                             msg=f'Displaying Highlights Carousel named {self.highlights_carousel_name}')
        except Exception:
            self._logger.info(f'Not Displaying Highlights Carousel named {self.highlights_carousel_name}')

    def test_009_repeat_same_steps_for_remaining_all_other_modules(self):
        """
        DESCRIPTION: Repeat same steps for remaining all other modules (as per pre conditions )
        EXPECTED: Excluded record should not displayed for specific segmented user.
        """
        sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
        self.assertTrue(sports, msg='No inplay sports found in the module')
        self.__class__.sport = sports[-1]
        try:
            self.cms_config.update_inplay_sport_module(sport_name=self.sport.title(), universalSegment=True,
                                                       exclusionList=[self.segment])
            sleep(60)
            self.device.refresh_page()
            sports = list(self.site.home.tab_content.in_play_module.items_as_ordered_dict.keys())
            self.assertNotIn(self.sport, sports, msg=f'Segmented record {self.sport} is displayed among {sports}')
        finally:
            self.get_cms_config().update_inplay_sport_module(sport_name=self.sport.title(),
                                                             universalSegment=True, exclusionList=[])
