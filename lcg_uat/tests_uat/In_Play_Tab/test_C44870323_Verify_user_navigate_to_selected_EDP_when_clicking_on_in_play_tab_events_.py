import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.prod
@vtest
class Test_C44870323_Verify_user_navigate_to_selected_EDP_when_clicking_on_in_play_tab_events_(BaseSportTest):
    """
    TR_ID: C44870323
    NAME: "Verify user navigate to selected EDP when clicking on in-play tab events "
    DESCRIPTION: this test case verify navigation to EDP pages
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home Page is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to In-Play tab
        EXPECTED: All inplay sports is displayed
        """
        self.navigate_to_page(name='in-play')
        self.site.wait_content_state(state_name='InPlay')

    def test_003_click_on_any_football_event(self):
        """
        DESCRIPTION: Click on any football event
        EXPECTED: Event Detail page is opened
        """
        # This step is covered in test step #4

    def test_004_repeat_step_3_for_all_inplay_sports_egtennis_golf(self):
        """
        DESCRIPTION: Repeat step #3 for all inplay sports eg:tennis, golf
        """
        inplay_sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(inplay_sports.keys(), msg='"inplay sports" are not verified')
        for sport_name in list(inplay_sports.keys())[1:]:
            inplay_sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
            inplay_sports[sport_name].click()
            sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
            if len(sections) == 0:
                if self.device_type == 'desktop':
                    self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
                    sections = self.site.inplay.tab_content.accordions_list.items_as_ordered_dict
                else:
                    sections = self.site.inplay.tab_content.upcoming.items_as_ordered_dict
                self.assertTrue(sections, msg=f'No "{vec.inplay.UPCOMING_SWITCHER}" and "{vec.inplay.LIVE_NOW_EVENTS_SECTION}" events found')
            section_name, section = list(sections.items())[0]
            if section_name is not None:
                if not section.is_expanded():
                    section.expand()
                events = section.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events on "{section_name}"')
                event_name, event = list(events.items())[0]
                event.scroll_to_we()
                event.click()
                try:
                    edp_event_name = self.site.sport_event_details.event_name
                    self.assertTrue(edp_event_name, msg=f'event name:"{event_name}"is not found')
                except VoltronException:
                    self.site.wait_content_state('EventDetails', raise_exceptions=False, timeout=15)
                self.navigate_to_page(name='in-play')
                self.site.wait_content_state(state_name='InPlay')
