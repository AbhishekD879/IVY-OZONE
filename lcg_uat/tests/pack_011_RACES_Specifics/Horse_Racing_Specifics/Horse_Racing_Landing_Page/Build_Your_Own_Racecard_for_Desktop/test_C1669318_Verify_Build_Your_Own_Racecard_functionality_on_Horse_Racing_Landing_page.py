import re
import pytest
import tests
import voltron.environments.constants as vec

from collections import OrderedDict
from contextlib import suppress
from random import randint
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.desktop
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod We should result an event
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.build_own_racecard
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.slow
@pytest.mark.timeout(700)
@vtest
class Test_C1669318_Verify_Build_Your_Own_Racecard_functionality_on_Horse_Racing_Landing_page(BaseRacing):
    """
    TR_ID: C1669318
    VOL_ID: C9697615
    NAME: Verify Build Your Own Racecard functionality on Horse Racing Landing page
    DESCRIPTION: This test case verifies 'Build Your Own Racecard' functionality on 'Horse Racing' Landing page.
    PRECONDITIONS: There are HR events in 'UK&IRE', 'INTERNATIONAL', 'VIRTUALS' groups
    PRECONDITIONS: There is at least one resulted event
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    build_your_own_race_card_title = vec.sb_desktop.BUILD_YOUR_OWN_RACE_CARD
    uk_and_ire_type = vec.racing.UK_AND_IRE_TYPE_NAME
    international_type = vec.racing.INTERNATIONAL_TYPE_NAME
    build_race_card_text_block = f'{vec.racing.BEGIN_TO} {vec.racing.BUILD_YOUR_OWN_RACE_CARD}. {vec.racing.SELECT_FROM_MEETINGS}'
    build_your_race_card_button_text = vec.racing.BUILD_YOUR_RACECARD_BUTTON
    horse_racing_tab_name = re.sub(r'\W+', '-', vec.racing.HORSE_RACING_TAB_NAME)
    featured_tab = vec.racing.RACING_DEFAULT_TAB_NAME
    build_card_limit_message = vec.racing.BUILD_YOUR_RACE_CARD_LIMIT_MESSAGE

    def dict_event_generating(self, type_name, meeting_name):
        """
        Generate dictionary of events
        :param type_name: str, header name of events list
        :param meeting_name: str, name of meeting
        :return: dictionary where the key is event name, value is related web element
        """
        if self.brand == 'ladbrokes':
            type_name = type_name.upper()
        self.site.wait_content_state('Horseracing')
        sections = self.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        racing_section = sections[type_name] if type_name in sections.keys() else None
        racing_meetings = racing_section.items_as_ordered_dict
        for event_name, event in racing_meetings.items():
            if meeting_name in event_name:
                event.scroll_to()
                return event.items_as_ordered_dict

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create virtual racing event
        EXPECTED: Virtual Racing event added
        """
        virtual_event_params = self.ob_config.add_virtual_racing_event(number_of_runners=1)
        self.__class__.virtual_event_name = virtual_event_params.event_off_time
        # More than 10 events are required for building own racecard throws an limit
        # error message that it is too much event selected.
        for _ in range(12):
            time_to_start = randint(30, 90)
            self.ob_config.add_irish_racing_event(number_of_runners=1, time_to_start=time_to_start)

        international_event_params = self.ob_config.add_international_racing_event(number_of_runners=1)
        self.__class__.international_event_name = international_event_params.event_off_time

        event_params = self.ob_config.add_international_racing_event(number_of_runners=1)

        event_id, market_id, selection_ids, self.__class__.resulted_event_name = \
            event_params.event_id, event_params.market_id, event_params.selection_ids, event_params.event_off_time
        for key, value in selection_ids.items():
            self.ob_config.result_selection(selection_id=value, market_id=market_id, event_id=event_id)
            self.ob_config.confirm_result(selection_id=value, market_id=market_id, event_id=event_id)

    def test_001_navigate_to_horse_racing_landing_page_featured_tab(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' Landing page -> 'Featured' tab
        EXPECTED: * 'Horse Racing' Landing page is opened
        EXPECTED: * 'Featured' tab is selected by default
        EXPECTED: * 'Build Your Own Racecard' section with text block and 'Build a Racecard' button
        EXPECTED: is displayed at the top of the main content area and below the tabs
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        self.__class__.horse_racing = self.site.horse_racing
        selected_tab = self.horse_racing.tabs_menu.current
        self.assertEqual(selected_tab, self.featured_tab,
                         msg=f'{selected_tab} tab is selected by default instead of {self.featured_tab}')
        actual_build_card_text = self.horse_racing.tab_content.build_card.build_race_card_button.name
        self.assertEqual(actual_build_card_text, self.build_your_race_card_button_text,
                         msg=f'Actual text "{actual_build_card_text}" '
                             f'does not match expected f"{self.build_your_race_card_button_text}"')
        actual_text_block = self.horse_racing.tab_content.build_card.build_race_card_text_block
        self.assertEqual(self.horse_racing.tab_content.build_card.build_race_card_text_block,
                         self.build_race_card_text_block,
                         msg=f'Actual text "{actual_text_block}" does not match expected '
                             f'f"{self.build_race_card_text_block}"')

    def test_002_click_on_build_a_race_card_button(self):
        """
        DESCRIPTION: Click on 'Build a Racecard' button
        EXPECTED: * 'Build a Racecard' button is replaced by 'Exit Builder' with 'Close' icon
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons appear below the
        EXPECTED: 'Build Your Own Racecard' section
        """
        build_card = self.horse_racing.tab_content.build_card
        build_card.scroll_to()
        self.horse_racing.tab_content.build_card.build_race_card_button.click()
        self.assertTrue(build_card.exit_builder_button.is_displayed(),
                        msg="'Build a Racecard' button is not replaced by 'Exit Builder'")
        self.assertTrue(build_card.close_icon.is_displayed(),
                        msg="'Close' icon is not shown near 'Exit Builder'")
        self.assertTrue(build_card.build_your_race_card_button.is_displayed(),
                        msg="'Build Your Own Racecard' button is not shown")
        self.assertTrue(build_card.clear_all_selections_button.is_displayed(),
                        msg="'Clear All Selections' button is not shown")

    def test_003_verify_checkboxes_displaying_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Verify checkboxes displaying before 'Event off time' tabs
        EXPECTED: * Checkboxes appear before each of 'Event off time' tab only for 'UK&IRE' and 'INTERNATIONAL' sections
        EXPECTED: * Checkboxes are NOT displayed before 'Event off time' tabs for 'VIRTUALS' section
        EXPECTED: * Checkboxes are NOT displayed before 'Event off time' tabs with 'Resulted' icon
        """
        international_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_international.name_pattern
        virtual_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_virtual.name_pattern
        ireland_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_ireland.name_pattern

        if self.brand == "bma":
            self.international_type = vec.racing.INTERNATIONAL_TYPE_NAME.title()
            international_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_international.name_pattern.upper()
            virtual_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_virtual.name_pattern.upper()
            ireland_name = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_ireland.name_pattern.upper()

        international_racing_events = self.dict_event_generating(self.international_type, international_name)
        self.assertTrue(international_racing_events, msg=f'Can\'t found event with meeting name "{international_name}"')
        international_event = international_racing_events[self.international_event_name]
        international_event.scroll_to()
        self.assertTrue(international_event.check_box.is_enabled(),
                        msg=f'Checkbox is not shown near "{self.international_event_name}" event')
        if self.brand == "bma":
            virtual_type = "Coral Legends"
        else:
            virtual_type = "LADBROKES LEGENDS"
        virtual_racing_events = self.dict_event_generating(virtual_type, virtual_name)
        self.assertTrue(virtual_racing_events, msg=f'Can\'t found event with meeting name "{virtual_name}"')
        self.assertFalse(virtual_racing_events[self.virtual_event_name].has_checkbox(expected_result=False),
                         msg=f'Checkbox is displayed before {self.virtual_event_name} '
                             f'tab for {virtual_type} section')
        # self.assertFalse(international_racing_events[self.resulted_event_name].has_checkbox(expected_result=False),
        #                  msg=f'Checkbox is displayed before {self.resulted_event_name} tab '
        #                      f'for {self.international_type} section')

        self.__class__.uk_and_ire_type_name_racing_events = self.dict_event_generating(self.uk_and_ire_type,
                                                                                       ireland_name)
        self.site.wait_content_state_changed()
        self.assertTrue(self.uk_and_ire_type_name_racing_events,
                        msg=f'Can\'t found event with meeting name "{ireland_name}"')
        for event_name, event in self.uk_and_ire_type_name_racing_events.items():
            self.assertTrue(event.check_box.is_enabled(), msg=f'Checkbox is not shown near {event_name} event')

    def test_004_verify_clear_all_selections_and_build_your_own_racecard_buttons(self):
        """
        DESCRIPTION: Verify 'Clear All Selections' and 'Build Your Own Racecard' buttons
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons are disabled and NOT clickable
        EXPECTED: * Section with 'Clear All Selections' and 'Build Your Own Racecard' buttons is sticky
        """
        # NOT AUTOMATED:'EXPECTED: * Section with 'Clear All Selections'
        # and 'Build Your Own Racecard' buttons is sticky'
        build_card = self.horse_racing.tab_content.build_card
        self.assertFalse(build_card.build_your_race_card_button.is_selected(),
                         msg="'Build Your Own Racecard' button is clickable")
        self.assertFalse(build_card.clear_all_selections_button.is_selected(),
                         msg="'Clear All Selections' button is clickable")

    def test_005_verify_clear_all_selections_build_your_own_racecard_buttons(self):
        """
        DESCRIPTION: Tick at least one checkbox before 'Event off time' tab and verify
        DESCRIPTION: 'Clear All Selections'/'Build Your Own Racecard' buttons
        EXPECTED: * Checkbox before 'Event off time' tab is ticked
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons become active and clickable
        """
        event_name, event = next(iter(self.uk_and_ire_type_name_racing_events.items()))
        event.check_box.click()
        self.assertTrue(event.check_box.value, msg=f"Checkbox before tab {event_name} is not ticked")
        self.assertTrue(self.horse_racing.tab_content.build_card.build_your_race_card_button.is_selected(),
                        msg="'Build Your Own Racecard' button is not clickable")
        self.assertTrue(self.horse_racing.tab_content.build_card.clear_all_selections_button.is_selected(),
                        msg="'Clear All Selections' button is not clickable")

    def test_006_click_at_clear_all_selections_button(self):
        """
        DESCRIPTION: Click at 'Clear All Selections' button
        EXPECTED: * All ticked checkboxes before each 'Event off time' tab become unchecked
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons became disabled and NOT clickable
        """
        self.horse_racing.tab_content.build_card.clear_all_selections_button.click()
        for event_name, event in self.uk_and_ire_type_name_racing_events.items():
            result = wait_for_result(lambda: event.check_box.value,
                                     name='Wait for checkbox untick',
                                     timeout=2,
                                     expected_result=False)
            self.assertFalse(result, msg=f'Checkbox before {event_name} is checked')
        self.assertFalse(self.horse_racing.tab_content.build_card.build_your_race_card_button.is_selected(),
                         msg="'Build Your Own Racecard' button is clickable")
        self.assertFalse(self.horse_racing.tab_content.build_card.clear_all_selections_button.is_selected(),
                         msg="'Clear All Selections' button is clickable")

    def test_007_tick_several_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Tick several checkboxes before 'Event off time' tabs
        EXPECTED: * Checkboxes before 'Event off time' tabs are ticked
        EXPECTED: * 'Clear All Selections' and 'Build Your Own Racecard' buttons became active and clickable
        """
        for event_name, event in list(self.uk_and_ire_type_name_racing_events.items())[1:3]:
            event.check_box.scroll_to()
            event.check_box.click()
            self.assertTrue(event.check_box.value, msg=f'Checkbox before "{event_name}" is not checked')
        self.assertTrue(self.horse_racing.tab_content.build_card.build_your_race_card_button.is_selected(),
                        msg="'Build Your Own Racecard' button is not clickable")
        self.assertTrue(self.horse_racing.tab_content.build_card.clear_all_selections_button.is_selected(),
                        msg="'Clear All Selections' button is not clickable")

    def test_008_tick_10_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Tick 10 checkboxes before 'Event off time' tabs
        EXPECTED: * All unselected checkboxes before 'Event off time' tabs are disabled and NOT clickable
        EXPECTED: * 'You cannot select anymore races for build your racecard' message appears below
        EXPECTED: 'Clear All Selections' and 'Build Your Own Racecard' buttons
        """
        for event_name, event in list(self.uk_and_ire_type_name_racing_events.items())[3:11]:
            event.scroll_to()
            event.check_box.click()

        for event_name, event in list(self.uk_and_ire_type_name_racing_events.items())[11:16]:
            event.scroll_to_we()
            with suppress(VoltronException):
                self.site.wait_content_state_changed()
                event.check_box.click()
            self.site.wait_content_state_changed()
            clicked_event = self.uk_and_ire_type_name_racing_events[event_name]
            self.assertFalse(clicked_event.check_box.value, msg=f'Checkbox near {event_name} is clickable')
        actual_limit_message = self.horse_racing.tab_content.build_card.build_card_limit_message
        self.assertEqual(actual_limit_message,
                         self.build_card_limit_message, msg=f'{self.build_card_limit_message} is not shown. '
                                                            f'Actual message is: {actual_limit_message}')

    def test_009_untick_one_of_the_checkboxes_before_event_off_time_tabs(self):
        """
        DESCRIPTION: Untick one of the checkboxes before 'Event off time' tabs
        EXPECTED: * Checkbox before 'Event off time' tab is unticked
        EXPECTED: * 'You cannot select anymore races for build your racecard' message disappears
        """
        event_name, event = list(self.uk_and_ire_type_name_racing_events.items())[1]
        self.uk_and_ire_type_name_racing_events.pop(event_name)
        event.scroll_to()
        self.assertTrue(event.check_box.value, msg=f'Checkbox before {event_name} is not checked')
        self.site.wait_content_state_changed()
        event.check_box.click()
        self.site.wait_content_state_changed()
        self.assertFalse(event.check_box.value, msg=f'Checkbox before {event_name} is checked')
        actual_limit_message = self.horse_racing.tab_content.build_card.build_card_limit_message
        self.assertEqual(len(actual_limit_message), 0,
                         msg=f'"{self.build_card_limit_message}" message does not disappear')

    def test_010_click_at_build_your_own_racecard_button(self):
        """
        DESCRIPTION: Click at 'Build Your Own Racecard' button
        EXPECTED: * User is navigated to 'Build Your Own Racecard' page
        EXPECTED: * All selected race cards are displayed in the list
        """
        self.horse_racing.tab_content.build_card.build_your_race_card_button.click()
        breadcrumbs = OrderedDict((key.strip(), self.site.build_your_card.breadcrumbs.items_as_ordered_dict[key])
                                  for key in self.site.build_your_card.breadcrumbs.items_as_ordered_dict)
        self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
        self.assertIn(self.build_your_own_race_card_title, breadcrumbs,
                      msg=f'"{self.build_your_own_race_card_title}" was not found in breadcrumbs "{breadcrumbs.keys()}"')

        selected_race_cards = self.site.build_your_card.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(set(list(selected_race_cards.keys())),
                        msg=f'Not all selected race cards  {list(self.uk_and_ire_type_name_racing_events.keys())} ')
