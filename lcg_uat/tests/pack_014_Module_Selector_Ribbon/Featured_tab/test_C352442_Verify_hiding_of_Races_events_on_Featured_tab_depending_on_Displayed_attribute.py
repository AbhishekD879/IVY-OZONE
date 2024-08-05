import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # events cannot suspend on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.desktop
@vtest
class Test_C352442_Verify_hiding_of_Races_events_on_Featured_tab_depending_on_Displayed_attribute(BaseFeaturedTest,
                                                                                                  BaseRacing):
    """
    TR_ID: C352442
    NAME: Verify hiding of <Races> events on Featured tab depending on 'Displayed' attribute
    DESCRIPTION: This test case verifies  hiding of <Races> events on Featured tab depending on 'Displayed' attribute
    PRECONDITIONS: 1. To display/undisplay events use ttp://backoffice-tst2.coral.co.uk/ti/ tool
    PRECONDITIONS: 2. To verify 'Displayed' attribute value check Featured webSocket: Network -> WS -> wss://featured-sports.coralsports.nonprod.cloud.ladbrokescoral.com/socket.io/?EIO=3&transport=websocket
    """
    keep_browser_open = True

    def featured_tab(self):
        self.wait_for_featured_module(name=self.race_module_name)
        featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        )
        featured_module.scroll_to()
        self.__class__.section = featured_module.accordions_list.items_as_ordered_dict.get(self.race_module_name)
        self.assertTrue(self.section, msg=f'Section "{self.race_module_name}" is not found on FEATURED tab')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Horse racing event and featured tab with racing type
        """
        event = self.ob_config.add_UK_racing_event(number_of_runners=2)
        self.__class__.eventID = event.event_id

        race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        self.__class__.event_name = f'{event.event_off_time} {self.horseracing_autotest_uk_name_pattern}'

        self.__class__.race_module_name = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=race_type_id, events_time_from_hours_delta=-10,
            module_time_from_hours_delta=-10, show_expanded=False, show_all_events=True)['title'].upper()

        self._logger.info(f'*** Created Module "{self.race_module_name}"')

    def test_001_load_oxygen_application_and_navigate_to_featured_tab(self):
        """
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        EXPECTED:
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.race_module_name)

    def test_002_select_any_race_event_from_featured_tab(self):
        """
        DESCRIPTION: Select any Race event from Featured tab
        EXPECTED:
        """
        self.featured_tab()

    def test_003_in_ti_tool_undisplay_selected_event_and_save_changesgo_to_oxygen_application_and_verify_event_displaying_on_the_featured_tab(
            self):
        """
        DESCRIPTION: In TI tool undisplay selected event and save changes.
        DESCRIPTION: Go to Oxygen application and verify event displaying on the Featured tab
        EXPECTED: - displayed:"N" attribute is received in Featured webSocket
        EXPECTED: - event stops to display on Featured tab in real time
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=False, active=False)

    def test_004_refresh_the_page_and_verify_event_displaying_on_the_featured_tab(self):
        """
        DESCRIPTION: Refresh the page and verify event displaying on the Featured tab
        EXPECTED: Race event is NOT displayed in application
        """
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')
        try:
            featured_module = self.site.home.get_module_content(
                self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            )
            section = featured_module.accordions_list.items_as_ordered_dict.get(
                self.race_module_name)
            self.assertFalse(section, msg=f'Section "{self.race_module_name}" is found on FEATURED tab')
        except Exception:
            pass

    def test_005_set_previously_selected_event_to_displayed_and_save_changesgo_to_oxygen_application_and_verify_event_displaying_on_the_featured_tab(
            self):
        """
        DESCRIPTION: Set previously selected event to 'Displayed' and save changes.
        DESCRIPTION: Go to Oxygen application and verify event displaying on the Featured tab
        EXPECTED: - displayed:"Y" attribute is received in Featured webSocket
        EXPECTED: - event doesn't appear on Featured tab in real time
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

    def test_006_refresh_the_page_and_verify_event_displaying_on_the_featured_tab(self):
        """
        DESCRIPTION: Refresh the page and verify event displaying on the Featured tab
        EXPECTED: Event is displayed on Featured tab
        """
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')
        self.site.wait_splash_to_hide()
        self.featured_tab()
        self.section.expand()
        cards = self.section.items_as_ordered_dict
        self.assertTrue(cards, msg=f'No Cards found on {self.race_module_name} module')
        event_name = self.event_name if self.brand != "ladbrokes" else self.event_name.upper()
        self.assertIn(event_name, list(cards.keys()),
                      msg=f'"{event_name}" is not in "{list(cards.keys())}"')
