import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.mobile_only
@vtest
class Test_C29377_Featured_Verify_Module_is_removed_from_Featured_tab_when_there_are_no_events_to_display_of_module_is_disabled(BaseFeaturedTest, BaseRacing):
    """
    TR_ID: C29377
    NAME: Featured: Verify Module is removed from Featured tab when there are no events to display of module is disabled
    DESCRIPTION: This test case verifies that Module is not present if there are no available events to display or if 'Enabled' field in CMS is unchecked.
    DESCRIPTION: To be run on mobile, tablet and desktop
    PRECONDITIONS: 1) 2 Featured Modules with at least 2 events in each created in CMS. Modules are Active and are displayed on Featured tab in app.
    PRECONDITIONS: 2) CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football event and featured tab with event type
        """
        if tests.settings.backend_env == 'prod':
            event_1 = self.get_active_events_for_category(
                category_id=self.ob_config.backend.ti.football.category_id)[0]
            self.__class__.eventID_1 = event_1['event']['id']

            event_2 = self.get_active_events_for_category(
                category_id=self.ob_config.backend.ti.football.category_id)[0]
            self.__class__.eventID_2 = event_2['event']['id']
        else:
            event_1 = self.ob_config.add_autotest_premier_league_football_event()
            event_2 = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_1 = event_1.event_id
            self.__class__.eventID_2 = event_2.event_id

        self.__class__.featured_module_1 = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=self.eventID_1,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10, show_expanded=False,
            show_all_events=True)

        self.__class__.featured_module_2 = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=self.eventID_2,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10, show_expanded=False,
            show_all_events=True)

        self.__class__.featured_module_name_1 = self.featured_module_1['title'].upper()
        self.__class__.featured_module_name_2 = self.featured_module_2['title'].upper()

        self._logger.info(f'*** Created Modules with Featured module-1 : "{self.featured_module_name_1}"  & Featured '
                          f'module-2 : "{self.featured_module_name_2}')

    def test_001_go_to_cms_and_uncheck_enabled_for_the_first_module___click_save_button(self):
        """
        DESCRIPTION: Go to CMS and uncheck 'Enabled' for the first Module -> click 'Save' button
        EXPECTED:
        """
        self.cms_config.update_featured_tab_module(module_id=self.featured_module_1['id'], enabled=False)

    def test_002_verify_module_area_in_app(self):
        """
        DESCRIPTION: Verify Module Area in app
        EXPECTED: Module is removed from Featured tab
        """
        self.site.login()
        self.site.wait_content_state(state_name='Homepage')
        featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        featured_module.scroll_to()
        featured_module_1 = self.get_section(self.featured_module_name_1, timeout=10, expected_result=False)
        self.assertFalse(featured_module_1,
                         msg=f'Module: "{self.featured_module_name_1}" is found in FEATURED tab section, whereas it should not appear')

    def test_003_go_to_cms_and_click_remove_all_in_events_in_module_section_for_second_module___click_save_button(self):
        """
        DESCRIPTION: Go to CMS and click 'Remove all in 'Events in Module section' for second Module -> click 'Save' button
        EXPECTED:
        """
        self.cms_config.update_featured_tab_module(module_id=self.featured_module_2['id'], data=[])

    def test_004_verify_module_area_in_app(self):
        """
        DESCRIPTION: Verify Module Area in app
        EXPECTED: Module is removed from Featured tab
        """
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')
        featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        featured_module.scroll_to()
        featured_module_2 = self.get_section(self.featured_module_name_2, timeout=10, expected_result=False)
        self.assertFalse(featured_module_2,
                         msg=f'Module "{self.featured_module_name_1}" is found in FEATURED tab section, whereas it should not appear')
