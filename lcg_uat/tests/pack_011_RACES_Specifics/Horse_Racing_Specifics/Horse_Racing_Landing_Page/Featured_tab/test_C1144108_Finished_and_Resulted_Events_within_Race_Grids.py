import voltron.environments.constants as vec
from random import randint

import pytest

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.medium
@pytest.mark.safari
@vtest
class Test_C1144108_Finished_and_Resulted_Events_within_Race_Grids(BaseRacing):
    """
    TR_ID: C1144108
    VOL_ID: C9697825
    NAME: Finished and Resulted Events within Race Grids
    """
    keep_browser_open = True
    event_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create UK & IRE events
        EXPECTED: Events are created
        """
        minutes = randint(30, 50)
        start_time = self.get_date_time_formatted_string(minutes=-minutes)
        event_params = self.ob_config.add_UK_racing_event(start_time=start_time, cashout=True)
        event_id, market_id, selection_ids, self.__class__.event_name = \
            event_params.event_id, event_params.market_id, event_params.selection_ids, event_params.event_off_time

        self.result_event(selection_ids=list(selection_ids.values()), market_id=market_id, event_id=event_id)

    def test_001_navigate_to_horse_racing_featured_tab_uk_ire_race_grid(self):
        """
        DESCRIPTION: Navigate to Horse Racing -> Featured tab -> UK & IRE race grid
        EXPECTED: * Tab for first available day is opened by default
        EXPECTED: * List of Race meeting sections for first day tab is displayed
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        current_tab = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg='Current tab %s is not the same as expected %s'
                             % (current_tab, vec.racing.RACING_DEFAULT_TAB_NAME))
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertIn(self.uk_and_ire_type_name, sections)
        section = sections[self.uk_and_ire_type_name]
        section.expand()
        self.__class__.meetings = section.items_as_ordered_dict
        self.assertTrue(self.meetings, msg='No meetings found in %s' % self.uk_and_ire_type_name)
        self.__class__.autotest_racing_meeting = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern if self.brand == 'ladbrokes' \
            else self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.name_pattern.upper()
        self.assertIn(self.autotest_racing_meeting, self.meetings)

    def test_002_verify_event_off_time_for_resulted_event_events_with_attribute_isresulted__true_(self):
        """
        DESCRIPTION: Verify event off time for resulted event (events with attribute: **'isResulted' = true** )
        EXPECTED: Event off time is greyed and 'Resulted' icon is displayed near.
        """
        autotest_uk_events = self.meetings[self.autotest_racing_meeting].items_as_ordered_dict
        self.assertTrue(autotest_uk_events, msg='Event not found for %s' % self.autotest_racing_meeting)
        self.assertIn(self.event_name, autotest_uk_events)
        self.__class__.event = autotest_uk_events[self.event_name]
        self.assertTrue(self.event.is_resulted, msg='Event %s: %s is not resulted' % (self.autotest_racing_meeting, self.event_name))

    def test_003_tap_event_off_time_for_verified_event(self):
        """
        DESCRIPTION: Tap event off time for verified event
        EXPECTED: Page redirects to Results tab with current event results
        """
        self.event.click()
        self.site.wait_content_state(state_name='Horseracing', raise_exceptions=True, timeout=5)

    # TODO VOL-1061 find out how to make event finished
    # def test_004_go_to_current_day_tab(self):
    #     """
    #     DESCRIPTION: Go to current day tab
    #     EXPECTED:
    #     """
    #     pass
    #
    #
    # def test_005_verify_event_off_time_for_finished_events_event_with_attributes_isfinishedtrue_andisresulted__true_(self):
    #     """
    #     DESCRIPTION: Verify event off time for finished events (event with attributes **isFinished='true'** and **'isResulted' = true** )
    #     EXPECTED: Event off time is greyed and 'Resulted' icon is displayed near.
    #     """
    #     pass
    #
    #
    # def test_006_tap_event_off_time_for_verified_event(self):
    #     """
    #     DESCRIPTION: Tap event off time for verified event
    #     EXPECTED: Page redirect to Results tab with current event results
    #     """
    #     pass
    #
    #
    # def test_007_repeat_steps_1_6_for_international_race_grid(self):
    #     """
    #     DESCRIPTION: Repeat steps #1-6 for 'INTERNATIONAL' race grid
    #     EXPECTED: Results are the same
    #     """
    #     pass
    #
    #
    # def test_008_repeat_steps_1_6_for_virtual_race_grid(self):
    #     """
    #     DESCRIPTION: Repeat steps #1-6 for 'VIRTUAL' race grid
    #     EXPECTED: Results are the same
    #     """
    #     pass
