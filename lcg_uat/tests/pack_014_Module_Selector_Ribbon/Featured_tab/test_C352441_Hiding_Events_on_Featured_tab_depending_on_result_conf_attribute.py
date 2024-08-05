import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Live updates cannot be tested on prod and Beta
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.desktop
@vtest
class Test_C352441_Hiding_Events_on_Featured_tab_depending_on_result_conf_attribute(BaseFeaturedTest):
    """
    TR_ID: C352441
    NAME: Hiding Events on Featured tab depending on 'result_conf' attribute
    DESCRIPTION: This test case verifies Hiding Events on Featured tab depending on 'result_conf' attribute
    DESCRIPTION: NEEDS TO BE UPDATED: 'result_conf' attribute is received in WS, not in push
    PRECONDITIONS: 1. To set result for event use http://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'result_conf' attribute value check LIVE SERV pushes: Network -> push -> Preview/response tab
    """
    keep_browser_open = True
    module_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event
        """
        start_time = self.get_date_time_formatted_string(hours=3)
        self.ob_config.add_football_event_to_autotest_league2(start_time=start_time)
        event_params = self.ob_config.add_football_event_to_featured_autotest_league(start_time=start_time)
        self.__class__.eventID = event_params.event_id
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        self.__class__.event_name = f'{self.team1} v {self.team2}'
        self.__class__.selection_ids = event_params.selection_ids
        self._logger.info(f'*** Created Football event "{self.event_name}"')

    def test_001_load_oxygen_application_and_navigate_to_featured_tab(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        EXPECTED:
        """
        type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', show_all_events=True, id=type_id, events_time_from_hours_delta=-10,
            module_time_from_hours_delta=-10)['title']

        self.__class__.module_name = module_name.upper()
        self._logger.info(f'*** Featured module name "{self.module_name}"')
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.site.home.get_module_content(
            module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

    def test_002_select_any_live_sport_event_from_featured_tab(self):
        """
        DESCRIPTION: Select any LIVE sport event from Featured tab
        EXPECTED:
        """
        is_event_present = self.is_event_present(section_name=self.module_name, event_name=self.event_name, timeout=20)
        self.assertTrue(is_event_present,
                        msg=f'Event "{self.event_name}" is not present on "Featured" tab in "{self.module_name}" module')

    def test_003_in_ti_tool_set_results_for_selected_event_and_save_changesgo_to_oxygen_application_and_verify_the_event_displaying_and_information_received_in_live_serve_push(self):
        """
        DESCRIPTION: In TI tool set results for selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify the event displaying and information received in Live Serve push
        EXPECTED: - result_conf:”Y” attribute is received in Live Serve push
        EXPECTED: - event stops to display on Featured tab in real time
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=True)
        is_event_visible = self.is_event_present(section_name=self.module_name, event_name=self.event_name,
                                                 is_present=False, timeout=20)
        self.assertFalse(is_event_visible, msg='Event "%s" is still present on "FEATURED" tab in %s module'
                                               % (self.event_name, self.module_name))
