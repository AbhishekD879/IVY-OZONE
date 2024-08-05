import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from time import sleep
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.desktop_only
@vtest
# this test case covers C65946737,C65946738
class Test_C1048467_In_Play_Widget_Header_and_Footer_for_Desktop(Common):
    """
    TR_ID: C1048467
    NAME: In-Play Widget Header and Footer for Desktop
    DESCRIPTION: This test case verifies In-Play Widget Header and Footer for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Navigate to Sports Landing page that contains Live events
    PRECONDITIONS: 3. Choose 'Matches' tab
    PRECONDITIONS: 4. Make sure that In-Play widget is displayed in 3-rd column and expanded by default
    PRECONDITIONS: 5. Live events are displayed in the carousel
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    widget_section_name = 'In-Play LIVE '

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get live events
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(in_play_event=True, raise_exceptions=False)
            self.__class__.sport_name = "football"
            if not events:
                self.get_active_events_for_category(in_play_event=True, category_id=34)
                self.__class__.sport_name = "tennis"
        else:
            self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.sport_name = "football"

        in_play_status = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle').get('inPlay')
        live_stream_status = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle').get("liveStream")
        if not in_play_status:
            self.cms_config.update_system_configuration_structure(config_item='DesktopWidgetsToggle',
                                                                  field_name='inPlay', field_value=True)
        if not live_stream_status:
            self.cms_config.update_system_configuration_structure(config_item='DesktopWidgetsToggle',
                                                                  field_name='liveStream', field_value=True)

    def test_001_verify_in_play_widget_header(self):
        """
        DESCRIPTION: Verify In-Play widget Header
        EXPECTED: In-Play widget Header contains:
        EXPECTED: * Capitalized text 'In-Play'
        EXPECTED: * 'Live' badge
        EXPECTED: * Capitalized Sport name e.g. 'Football'
        EXPECTED: * Up/down chevron
        """
        self.navigate_to_page(f'sport/{self.sport_name}')
        self.site.wait_content_state(self.sport_name)
        self.__class__.widget = self.site.sports_page.in_play_widget.items_as_ordered_dict.get(self.widget_section_name+self.sport_name.title())
        self.assertTrue(self.widget.is_chevron_up(), msg='up arrow not present in inplay widget header')
        self.assertEqual(self.widget.name, self.widget_section_name+self.sport_name.title(), msg=f'Actual name "{self.widget.name}" is not same as'
                         f'Expected name "{self.widget_section_name+self.sport_name.title()}"')

    def test_002_verify_in_play_widget_footer_when_there_are_more_than_1_in_play_events(self):
        """
        DESCRIPTION: Verify In-Play widget Footer
        EXPECTED: * In-Play widget Footer contains 'View all in-play events' link
        EXPECTED: * Link takes user to 'In-play' page with specific sport selected in Sports Menu Ribbon e.g. Football
        """
        view_all_inplay_events = self.widget.view_all_inplay_events
        self.assertTrue(view_all_inplay_events.is_displayed(), msg='"view all inplay events" link is not displayed on the widget footer')
        view_all_inplay_events.click()
        self.site.wait_content_state(vec.sb.IN_PLAY)
        inplay_sport_tab = self.site.inplay.inplay_sport_menu.items_as_ordered_dict.get(self.sport_name.title() if self.brand != 'bma' else self.sport_name.upper())
        sleep(2)
        sport_tab_selected = wait_for_result(lambda: inplay_sport_tab.is_selected(), timeout=10)
        self.assertTrue(sport_tab_selected, msg=f'{self.sport_name} sports tab is not selected by default')

    def test_003_click_anywhere_in_the_header(self):
        """
        DESCRIPTION: Click anywhere in the header
        EXPECTED: * Widget gets collapsed together with footer
        EXPECTED: * Up chevron changes to down one
        """
        self.navigate_to_page(f'sport/{self.sport_name}')
        self.site.wait_content_state(self.sport_name)
        self.__class__.widget = self.site.sports_page.in_play_widget.items_as_ordered_dict.get(self.widget_section_name + self.sport_name.title())
        self.widget.game_status.click()
        widget_expanded = wait_for_result(lambda: self.widget.is_expanded(expected_result=False), timeout=15)
        self.assertFalse(widget_expanded, msg='widget not collapsed')
        self.assertTrue(self.widget.is_chevron_down(), msg='chevron did not turned down')

    def test_004_click_again_anywhere_in_the_header(self):
        """
        DESCRIPTION: Click again anywhere in the header
        EXPECTED: * Widget gets expanded: in-play cards and footer are shown
        EXPECTED: * Down chevron changes to up one
        """
        self.widget.game_status.click()
        self.assertTrue(self.widget.is_expanded(), msg='widget not expanded')
        self.assertTrue(self.widget.is_chevron_up(), msg='chevron did not turned up')
        events = self.widget.content.items_as_ordered_dict
        self.assertTrue(events, msg='no events are present in the widget')
