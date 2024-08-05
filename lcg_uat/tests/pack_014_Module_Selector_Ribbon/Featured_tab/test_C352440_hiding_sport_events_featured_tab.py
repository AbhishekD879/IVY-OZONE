import pytest

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl # Live updates cannot be tested on prod and hl
# @pytest.mark.prod
@pytest.mark.featured
@pytest.mark.liveserv_updates
@pytest.mark.cms
@pytest.mark.timeout(800)
@pytest.mark.slow
@pytest.mark.module_ribbon
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.pipelines
@vtest
class Test_C352440_Hiding_Sport_Events_Featured_Tab(BaseFeaturedTest):
    """
    TR_ID: C352440
    NAME: Verify hiding sport Events on Featured tab depending on Displayed attribute
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

    def test_001_create_featured_tab_module(self):
        """
        DESCRIPTION: Go to 'Featured Tab Modules' section and create featured tab module
        """
        type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', show_all_events=True, id=type_id, events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)['title']

        self.__class__.module_name = module_name.upper()
        self._logger.info(f'*** Featured module name "{self.module_name}"')

    def test_002_tap_featured_tab(self):
        """
        DESCRIPTION: Open Featured tab
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

    def test_003_verify_event_is_present(self):
        """
        DESCRIPTION: Verify event is present
        """
        is_event_present = self.is_event_present(section_name=self.module_name, event_name=self.event_name, timeout=20)
        self.assertTrue(is_event_present,
                        msg=f'Event "{self.event_name}" is not present on "Featured" tab in "{self.module_name}" module')

    def test_004_undisplay_1_event(self):
        """
        DESCRIPTION: Undisplay 1 of the events
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=True)

    def test_005_verify_event_is_not_present_on_featured(self):
        """
        DESCRIPTION: Verify event is not present on featured tab
        """
        is_event_visible = self.is_event_present(section_name=self.module_name, event_name=self.event_name,
                                                 is_present=False, timeout=20)
        self.assertFalse(is_event_visible, msg='Event "%s" is still present on "FEATURED" tab in %s module'
                                               % (self.event_name, self.module_name))

    def test_006_display_event(self):
        """
        DESCRIPTION: Display event
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

    def test_007_verify_event_is_not_present_on_featured(self):
        """
        DESCRIPTION: Verify event does NOT start to display in real time
        """
        is_event_visible = self.is_event_present(section_name=self.module_name, event_name=self.event_name, is_present=False, timeout=5)
        self.assertFalse(is_event_visible,
                         msg=f'Event "{self.event_name}" is present on "FEATURED" tab in "{self.module_name}" module')

    def test_008_verify_event_is_present_after_refresh(self):
        """
        DESCRIPTION: Verify event is present on featured tab after refresh
        """
        self.device.refresh_page()
        sleep(5)
        self.test_003_verify_event_is_present()
