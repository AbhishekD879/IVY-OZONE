import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.liveserv_updates
@pytest.mark.medium
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.next_races
@pytest.mark.cms
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.safari
@vtest
class Test_C2807727_Delayed_Races_are_removed_when_flag_is_off_Y_is_received(BaseRacing):
    """
    TR_ID: C2807727
    NAME: Delayed Races are removed when flag "is_off = Y" is received
    DESCRIPTION: Test case verifies that delayed races disappear from Next Races carousel when flag "is_off = Y" is received
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure > Next Races
    PRECONDITIONS: **Events are derived from the following requests:**
    PRECONDITIONS: EventToMarketForClass (with minor data for each event) + EventToOutcomeForEvent (with all required data for required events)
    PRECONDITIONS: Delayed event has start time of 1 hr (or less) ago and flags "is_off = N"
    PRECONDITIONS: **User is on Horse Racing landing page. Delayed event is available on Next Races carousel**
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Preconditions
        DESCRIPTION: Create event for test
        DESCRIPTION: Check event presence on Next Races module
        """
        self.setup_cms_next_races_number_of_events()
        type_id = self.ob_config.horseracing_config.horse_racing_live.autotest_uk.type_id
        self.check_and_setup_cms_next_races_for_type(type_id=type_id)

        event = self.ob_config.add_UK_racing_event(number_of_runners=1, time_to_start=-30, is_off='N')
        self.__class__.eventID = event.event_id
        name = self.horseracing_autotest_uk_name_pattern if self.brand == 'bma' and self.device_type == 'desktop' else self.horseracing_autotest_uk_name_pattern.upper()
        self.__class__.created_event_name = f'{event.event_off_time} {name}'

        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        next_races_title = self.next_races_title
        self.__class__.next_races = sections.get(next_races_title, None)
        self.assertTrue(self.next_races, msg=f'There\'s no "{next_races_title}" section')
        events = self.next_races.items_as_ordered_dict
        self.assertTrue(events, msg='No events were found in Next races section')
        self.assertIn(self.created_event_name, events, msg=f'Event "{self.created_event_name}" was not found')

    def test_001_in_ti_on_the_event_level_set_isOff_yes_for_the_delayed_event(self):
        """
        DESCRIPTION: In TI on the event level set IsOff = Yes for the delayed event
        EXPECTED: Event disappears from Next Races carousel in real time
        """
        self.ob_config.change_is_off_flag(event_id=self.eventID, is_off=True)

        wait_for_result(lambda: self.created_event_name in self.next_races.items_as_ordered_dict,
                        name=f'Event "{self.created_event_name}" to disappear from Next Races module',
                        expected_result=False,
                        timeout=30,
                        bypass_exceptions=(VoltronException, IndexError))
        self.assertNotIn(self.created_event_name, self.next_races.items_as_ordered_dict,
                         msg=f'Event "{self.created_event_name}" does not disappear')
