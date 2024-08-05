import pytest
import tests
from time import sleep
from faker import Faker
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.csp
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C65581870_Verify_user_can_able_to_select_and_delete_one_or_more_segments_from_the_Delete_Segment_page_list_and_Verify_in_FE_for_Sb_and_HC_module(Common):
    """
    TR_ID: C65581870
    NAME: Verify user can able to select and delete one or more segments from the 'Delete Segment' page list and Verify in FE for Sb and HC module.
    DESCRIPTION: This testcase verifies delete one or more segments from the 'Delete Segment' page list
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS > delete segment page
    PRECONDITIONS: CMS > Main navigation>Surface bet/SB/Footermenu/HC/MRT/Inplay/Featured/QL/Sports ribbon
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = 'CSP_AUTO_C65581870'
    highlights_carousels_title = ['Autotest ' + Faker().city()]

    def test_000_preconditions(self):
        """"
        PRECONDITIONS: User should have admin access to CMS.
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > SB/HC
        PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            eventID = event.event_id

        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0],
                                                   events=[eventID], inclusionList=[self.segment],
                                                   universalSegment=False)
        self.__class__.highlights_carousel_name = self.highlights_carousels_title[0] if self.brand == 'bma' else \
            self.highlights_carousels_title[0].upper()

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel,
                        msg=f'Highlights Carousel named {self.highlights_carousel_name} is displayed')

    def test_002_navigate_to_delete_segments_page(self):
        """
        DESCRIPTION: Navigate to Delete segments page
        EXPECTED: Delete segment page should be opened with 'Segments list' dropdown
        """
        # covered in below step

    def test_003_verify_segments_list_dropdown(self):
        """
        DESCRIPTION: Verify Segments list dropdown
        EXPECTED: When user expand segments list ,all existing  segments should display with delete option
        """
        # can not validate CMS UI

    def test_004_select_segment_from_the_dropdown(self):
        """
        DESCRIPTION: Select segment from the dropdown
        EXPECTED: User should able to select segments with check boxes.
        """
        # can not validate CMS UI

    def test_005_select_single_segment_from_the_list(self):
        """
        DESCRIPTION: Select single segment from the list
        EXPECTED: 1. user should able to delete segment through delete icon
        EXPECTED: 2. User can able to delete selected segment from the list"
        """

        self.cms_config.delete_segment(segment_name=self.segment)
        sleep(5)

    def test_006_select_multiple_segments_from_the_list(self):
        """
        DESCRIPTION: Select multiple segments from the list
        EXPECTED: User should able to select and delect multiple segments from the list
        """
        # covered in above step

    def test_007_navigate_to_surfacebet_module_and_verify(self):
        """
        DESCRIPTION: Navigate to SB module and verify
        EXPECTED: 1.Deleted segment should not display in segment dropdown list
        EXPECTED: 2.Existing configuration should not display
        EXPECTED: 3.Excluded record also should not  dispaly in Universal
        """
        # can not validate CMS UI

    def test_008_navigate_to_fe_and_login_with_deleted_segmented_user(self):
        """
        DESCRIPTION: Navigate to FE and login with deleted segmented user
        EXPECTED: Universal view should display as segment is deleted
        """
        #   Cannot create more than one Super Button at a time

    def test_009_Repeat_same_steps_for_HC_module(self):
        """
        EXPECTED: Universal view should displayed when delete segment user logged in
        """
        sleep(5)
        self.device.refresh_page()
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertNotIn(highlight_carousel, highlight_carousels, msg='highlight carousel displaying')
