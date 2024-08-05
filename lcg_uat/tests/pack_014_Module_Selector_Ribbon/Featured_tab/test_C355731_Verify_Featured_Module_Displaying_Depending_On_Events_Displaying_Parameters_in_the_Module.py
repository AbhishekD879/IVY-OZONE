import pytest

from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Live updates cannot be tested on prod and hl
# @pytest.mark.hl
@pytest.mark.module_ribbon
@pytest.mark.featured
@pytest.mark.liveserv_updates
@pytest.mark.cms
@pytest.mark.medium
@vtest
class Test_C355731_Verify_Featured_Module_Displaying_Depending_On_Events_Displaying_Parameters_in_the_Module(BaseFeaturedTest):
    """
    TR_ID: C355731
    VOL_ID: C9698375
    NAME: Verify Featured Module displaying depending on events displaying parameters in the Module
    """
    keep_browser_open = True
    module_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football events
        """
        start_time = self.get_date_time_formatted_string(hours=3)
        event_params = self.ob_config.add_football_event_to_autotest_league2(start_time=start_time)
        self.__class__.eventID, self.__class__.team1, self.__class__.team2 = \
            event_params.event_id, event_params.team1, event_params.team2
        self.__class__.event_name = '%s v %s' % (self.team1, self.team2)
        self._logger.info('*** Created Football event "%s"' % self.event_name)
        self.__class__.selection_ids = event_params.selection_ids

    def test_001_create_featured_tab_module(self):
        """
        DESCRIPTION: Go to 'Featured Tab Modules' section and create featured tab module
        """
        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Selection', id=self.selection_ids[self.team1])['title'].upper()

        self._logger.info('*** Featured module name %s' % self.module_name)

    def test_002_tap_featured_tab(self):
        """
        DESCRIPTION: Open FEATURED tab
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

    def test_003_verify_module_is_present(self):
        """
        DESCRIPTION: Open FEATURED tab
        DESCRIPTION: Verify featured module is present on FEATURED tab
        DESCRIPTION: Verify event starts to display on FEATURED tab
        """
        section = self.get_section(self.module_name)
        if not section:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            section = self.get_section(self.module_name)
        self.assertIsNotNone(section, msg='Module "%s" is not present on FEATURED tab' % self.module_name)
        is_event_present = self.is_event_present(section_name=self.module_name, event_name=self.team1)
        self.assertTrue(is_event_present, msg='Event "%s" is not displayed in section %s'
                                              % (self.team1, self.module_name))

    def test_004_undisplay_all_events(self):
        """
        DESCRIPTION: Undisplay all events
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=True)

    def test_005_verify_featured_module_is_not_present_on_featured_tab(self):
        """
        DESCRIPTION: Verify Featured Tab Module stops to display on Featured tab in real time
        """
        section = self.get_section(self.module_name, expected_result=False)
        self.assertIsNone(section, msg='Module "%s" is present on Featured tab' % self.module_name)

    def test_006_display_all_events(self):
        """
        DESCRIPTION: Display all events
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

    def test_007_verify_featured_module_is_present(self):
        """
        DESCRIPTION: Verify featured module is present on Featured tab in real time
        """
        section = self.get_section(self.module_name)
        self.assertIsNotNone(section, msg='Module "%s" is not present on Featured tab' % self.module_name)

    def test_008_make_event_live(self):
        """
        DESCRIPTION: Make the event LIVE in TI tool and save changes (is OFF = YEs and Bet In Play List is selected)
        """
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.market_id = self.ob_config.market_ids[self.eventID][market_short_name]
        self.ob_config.make_event_live(market_id=self.market_id, event_id=self.eventID)

    def test_009_set_results_for_selected_event(self):
        """
        DESCRIPTION: In TI tool set results for selected event and save changes.
        """
        self.ob_config.update_selection_result(selection_id=self.selection_ids[self.team1],
                                               result='W',
                                               market_id=self.market_id, event_id=self.eventID)
        self.ob_config.update_selection_result(selection_id=self.selection_ids[self.team2],
                                               result='L',
                                               market_id=self.market_id, event_id=self.eventID)
        self.ob_config.update_selection_result(selection_id=self.selection_ids['Draw'],
                                               result='L',
                                               market_id=self.market_id, event_id=self.eventID)
        self.ob_config.change_event_state(event_id=self.eventID, active=False)

    def test_010_verify_featured_module_is_not_present_on_featured_tab(self):
        """
        DESCRIPTION: Verify Featured Tab Module stops to display on Featured tab in real time
        """
        self.wait_for_featured_module(name=self.module_name, timeout=65, expected_result=False)
        section = self.get_section(self.module_name, expected_result=False)
        self.assertIsNone(section, msg='Module "%s" is present on Featured tab' % self.module_name)
