import pytest
import tests
from tests.Common import Common
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
class Test_C65026278_Verify_content_field_is_displayed_on_surface_bet_module_screen_table_verify_in_FE(Common):
    """
    TR_ID: C65026278
    NAME: Verify content field is displayed on surface bet module screen table verify in FE.
    DESCRIPTION: This test case verifies content field is displayed on surface bet module screen
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: 2)CMS configuration:
    PRECONDITIONS: CMS > Sports pages >home page>Surface bet.
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]
            eventID = event.event_id
        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                      categoryIDs=[0, 16],
                                                      eventIDs=[eventID])
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should able to see the Surfacebet module page with existing Universal records
        EXPECTED: Newly added 'Content' column should be added in Module screen
        EXPECTED: Application should be loaded successfully
        EXPECTED: Content text should be reflected in FE
        """
        # covered in step1

    def test_003_verify_module_page_for_surfacebet(self):
        """
        DESCRIPTION: Verify module page for surfacebet
        EXPECTED: Newly added 'Content' column should be added in Module screen
        """
        # covered in step1

    def test_004_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: Application should be loaded successfully
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')

    def test_005_verify_context_text_for_sb_record(self):
        """
        DESCRIPTION: Verify context text for sb record
        EXPECTED: Content text should be reflected in FE
        """
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
