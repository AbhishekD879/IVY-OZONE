import pytest
import tests
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry_if_exception_type, wait_fixed, stop_after_attempt, retry
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.reg156_fix
@pytest.mark.mobile_only
@vtest
class Test_C64881012_Verify_Surface_bet_with_show_on_sports_event_hub_for_Universal_Segmented_record_and_verify_in_CMS_and_FE(BaseFeaturedTest):
    """
    TR_ID: C64881012
    NAME: Verify Surface bet with show on sports/event hub for Universal/Segmented record and verify in CMS and FE
    DESCRIPTION: This test case verifies Surface bet with show on sports/event hub for Universal/Segment record
    PRECONDITIONS: 1)User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button/Surface bet
    PRECONDITIONS: 2)User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    PRECONDITIONS: 3) Create or Edit super button/Surface bet with Universal without excluded.
    PRECONDITIONS: 4) Select one or multiple sports pages(Football, Cricket) in show on sports/Event hub, Make sure super button/Surface bet should be in valid date range and all other proper config and save
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def navigate_to_the_configured_module_and_event_inside_the_module(self):
        """
        DESCRIPTION: navigate to the configured module and Event inside the module
        EXPECTED: Configured Event is shown inside the created module.
        """
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should able to login successfully
        """
        # can't automate CMS UI

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should able to see the Surfacebet module page with existing Universal records
        """
        # can't automate CMS UI

    def test_003_create_new_record_with_show_on_sportsevent_hub_for_universal_record(self):
        """
        DESCRIPTION: Create new record with show on sports/event hub for Universal record
        EXPECTED: Record should be created properly
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(event_selection.values())[0]
            self.__class__.eventhub_selection_id = list(event_selection.values())[1]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event.event_id
            self.__class__.selection_id = event.selection_ids[event.team1]

        surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_id,
                                                      categoryIDs=[self.ob_config.football_config.category_id,
                                                                   self.ob_config.cricket_config.category_id])

        self.__class__.sport_surface_bet_title = surface_bet.get('title').upper()

    def test_004_navigate_to_sports_category_in_cms_and_click_on_sport_which_was_included_in_created_record(self):
        """
        DESCRIPTION: Navigate to sports category in CMS and click on sport which was included in created record
        EXPECTED: Newly created record should be displayed in sport pages in CMS.
        """
        cms_surface_bets = self.cms_config.get_surface_bets_for_page(
            reference_id=self.ob_config.football_config.category_id, related_to='sport')
        surface_bets = [s_bets['title'] for s_bets in cms_surface_bets]
        self.assertIn(self.sport_surface_bet_title.title(), surface_bets,
                      msg=f'"created {self.sport_surface_bet_title}" is not in CMS {surface_bets}')

    def test_005_navigate_to_event_hub_in_cms_and_click_on_event_hub_which_was_included_in_created_record(self):
        """
        DESCRIPTION: Navigate to event hub in CMS and click on event hub which was included in created record
        EXPECTED: Newly created record should be displayed in event hub in CMS.
        """
        # Create Event Hub module
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]

        # need a unique non-existing index for new Event hub
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)

        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='SURFACE_BET')

        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=self.eventhub_selection_id,
                                                                     priceNum=1,
                                                                     priceDen=2,
                                                                     eventIDs=self.eventID,
                                                                     categoryIDs=[
                                                                         self.ob_config.football_config.category_id,
                                                                         self.ob_config.cricket_config.category_id],
                                                                     event_hub_id=index_number,
                                                                     edpOn=True,
                                                                     highlightsTabOn=True)
        self.__class__.event_hub_surface_bet_title = self.surface_bet.get('title').upper()

        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

    def test_006_launch_oxygen_application(self):
        """
        DESCRIPTION: Launch oxygen application
        EXPECTED: Home page launch successfully
        """
        self.navigate_to_page("Homepage")

    def test_007_navigate_to_home_page_and_verify_created_record(self):
        """
        DESCRIPTION: Navigate to home page and verify created record
        EXPECTED: surface bet should be displayed in home page.
        """
        self.navigate_to_the_configured_module_and_event_inside_the_module()

    def test_008_navigate_to_sports_pages_which_was_included_in_cms_and_verify(self):
        """
        DESCRIPTION: Navigate to sports pages (which was included in CMS) and verify
        EXPECTED: All surface bets which have been configured on ‘Show on Sports’ field shall be displayed for all segments on the selected sports page
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

        result = self.wait_for_surface_bets(name=self.sport_surface_bet_title, timeout=5, poll_interval=1,
                                            raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            # # this method is not applicable as the feature structure call is off.
            # self.wait_for_surface_bets(name=self.sport_surface_bet_title, timeout=15, poll_interval=1)

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.sport_surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.sport_surface_bet_title}" not found in "{list(surface_bets.keys())}"')

        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state('cricket')

        result = self.wait_for_surface_bets(name=self.sport_surface_bet_title, timeout=5, poll_interval=1,
                                            raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            # this method is not applicable as the feature structure call is off.
            # self.wait_for_surface_bets(name=self.sport_surface_bet_title, timeout=15, poll_interval=1)

        surface_bets = self.site.cricket.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.sport_surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.sport_surface_bet_title}" not found in "{list(surface_bets.keys())}"')

    def test_009_navigate_to_event_hubwhich_was_included_in_cms_and_verify(self):
        """
        DESCRIPTION: Navigate to event hub(which was included in CMS) and verify
        EXPECTED: All surface bets which have been configured on ‘Show on Event hub’ field shall be displayed for all segments on the selected sports page /event hub
        """
        # Can't automate CMS UI

    def test_010_repeat_same_steps_for_segmented_recordlogin_with_segment_user_from_pre_conditions(self):
        """
        DESCRIPTION: Repeat same steps for segmented record,Login with segment user from pre conditions.
        EXPECTED: All surface bets which have been configured on ‘Show on Sports/Event hub’ field shall be displayed for all segments on the selected sports page /event hub
        """
        self.site.back_button.click()
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')
        self.test_007_navigate_to_home_page_and_verify_created_record()
        self.test_008_navigate_to_sports_pages_which_was_included_in_cms_and_verify()
