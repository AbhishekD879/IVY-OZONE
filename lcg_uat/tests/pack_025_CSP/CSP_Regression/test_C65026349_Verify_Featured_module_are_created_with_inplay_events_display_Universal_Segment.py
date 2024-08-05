import pytest
import tests
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C65026349_Verify_Featured_module_are_created_with_inplay_events_display_Universal_Segment(BaseFeaturedTest):
    """
    TR_ID: C65026349
    NAME: Verify Featured module are created with inplay events for Universal/Segment
    DESCRIPTION: This testcase verifies Featured module created with inplay events
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS &gt; Sports pages &gt;home page&gt;HC/Featured tab module
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        if tests.settings.backend_env == 'prod':
            try:
                events = self.get_active_events_for_category(
                    category_id=self.ob_config.football_config.category_id,
                    in_play_event=True, number_of_events=1)
            except Exception:
                events = self.get_active_events_for_category(
                    category_id=self.ob_config.tennis_config.category_id,
                    in_play_event=True, number_of_events=1)
            eventID = events[0]['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            eventID = event.event_id

            self._logger.info(f'*** Created Football eventwith ID "{eventID}"')

        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                             id=eventID,
                                                                             universalSegment=True,
                                                                             events_time_from_hours_delta=-10,
                                                                             module_time_from_hours_delta=-10
                                                                             )['title'].upper()

    def test_002_navigate_to_featured_tab_module(self):
        """
        DESCRIPTION: Navigate to Featured tab module
        EXPECTED: Featured tab module page should be loaded with existing records
        """
        # covered in step 1

    def test_003_create_universal_featured_tab_record_with_same_type_idlive_eventsex_442(self):
        """
        DESCRIPTION: Create universal Featured tab record with same type id(Live events)(ex: 442)
        EXPECTED: Record should be created successfully
        """
        # covered in step 1

    def test_004_launch_oxygen_app(self):
        """
        DESCRIPTION: Launch oxygen app
        EXPECTED: Home page should launch succesfully
        """
        # covered in step 5

    def test_005_home_page_should_launch_succesfully(self):
        """
        DESCRIPTION: Home page should launch succesfully
        EXPECTED: Created record should be displayed under Featured module
        """
        self.site.login()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        module = self.wait_for_featured_module(name=self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')
