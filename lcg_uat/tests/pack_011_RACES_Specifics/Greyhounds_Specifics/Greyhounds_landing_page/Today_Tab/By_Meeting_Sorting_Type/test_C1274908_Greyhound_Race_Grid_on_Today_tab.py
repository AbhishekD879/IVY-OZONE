import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  cannot create events on prod/beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C1274908_Greyhound_Race_Grid_on_Today_tab(BaseRacing):
    """
    TR_ID: C1274908
    NAME: Greyhound Race Grid on Today tab
    DESCRIPTION: This test case verifies the Race Grid on Greyhounds landing page
    DESCRIPTION: New Design (LADBROKES Desktop) - https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: To get the UK/Irish/International daily races events check modules (modules name can be changed in CMS) in 'FEATURED_STRUCTURE_CHANGED' request from websocket (wss://featured-sports)
    PRECONDITIONS: Example of event structure:
    PRECONDITIONS: **flag:** "UK",
    PRECONDITIONS: **data:** [{
    PRECONDITIONS: **id:** "230549330",
    PRECONDITIONS: **categoryId:** "21",
    PRECONDITIONS: **categoryName:** "Horse Racing",
    PRECONDITIONS: **className:** "Horse Racing - Live",
    PRECONDITIONS: **name:** "Southwell",
    PRECONDITIONS: **typeName:** "Southwell",
    PRECONDITIONS: **startTime:** 1593614400000,
    PRECONDITIONS: **classId:** "285",
    PRECONDITIONS: **cashoutAvail:** "Y",
    PRECONDITIONS: **poolTypes:**  ["UPLP", "UQDP"],
    PRECONDITIONS: **liveStreamAvailable:** true,
    PRECONDITIONS: **isResulted:** false,
    PRECONDITIONS: **isStarted:** false,
    PRECONDITIONS: **eventIsLive:** false,
    PRECONDITIONS: **isFinished:** false,
    PRECONDITIONS: **isBogAvailable:** false,
    PRECONDITIONS: **isLpAvailable:** false,
    PRECONDITIONS: **drilldownTagNames:** "EVFLAG_BL,EVFLAG_AVA,",
    PRECONDITIONS: **localTime:** "15:40"
    PRECONDITIONS: **markets:** [{
    PRECONDITIONS: **drilldownTagNames:** 'MKTFLAG_EPR',
    PRECONDITIONS: **eachWayFactorNum:** 1,
    PRECONDITIONS: **eachWayFactorDen:** 2,
    PRECONDITIONS: **eachWayPlaces:** 3,
    PRECONDITIONS: **isEachWayAvailable:** true
    PRECONDITIONS: **New changes:
    PRECONDITIONS: Added "simpleFilter=class.hasOpenEvent" query to /Class request to receive info only about classes with available events.
    PRECONDITIONS: Removed request /EventToOutcomeForClass/201 on Ladbrokes (Specials Events).
    PRECONDITIONS: Removed simpleFilter=event.categoryId:intersects:21 from request /EventToOutcomeForClass (horse racing category id: 21, greyhound category id: 19)
    PRECONDITIONS: Added to /EventToOutcomeForClass filter &limitRecords=outcome:1, &limitRecords=market:1
    PRECONDITIONS: Date range should be: 1 day (today or tomorrow).
    PRECONDITIONS: Only one WS connection is between switching By Meeting/By time tab (Coral greyhounds).
    PRECONDITIONS: Parameter **startTime** defines event start time (note, this is not a race local time)
    PRECONDITIONS: Load the app
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """Events Creation"""
        start_time = self.get_date_time_formatted_string(seconds=10)
        end_time = self.get_date_time_formatted_string(seconds=20)
        uk_event1 = self.ob_config.add_UK_greyhound_racing_event()
        self.__class__.event_off_time1 = uk_event1.event_off_time
        uk_event2 = self.ob_config.add_UK_greyhound_racing_event(start_time=start_time, suspend_at=end_time)
        self.__class__.event_off_time2 = uk_event2.event_off_time
        self.ob_config.add_virtual_greyhound_racing_event()

    def test_001_navigate_to_greyhounds_landing_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds landing page
        EXPECTED: **FOR CORAL:**
        EXPECTED: - 'TODAY' tab is opened and the race grid is shown with 'By Meeting' sorting switched on by default
        EXPECTED: - 'TODAY' tab contains 2 sub-tabs - 'BY MEETING' and 'BY TIME'
        EXPECTED: **FOR LADBROKES:**
        EXPECTED: - 'TODAY' tab is opened and the race grid is shown with 'By Meeting' sorting switched on by default
        EXPECTED: - NO sub-tabs available
        """
        self.site.wait_content_state('homepage')
        sport_name = vec.sb.GREYHOUND if tests.settings.brand == 'ladbrokes' else vec.sb.GREYHOUND.upper()
        self.site.open_sport(name=sport_name, timeout=15)
        self.site.wait_content_state_changed(timeout=40)
        if self.brand == 'ladbrokes':
            today = vec.sb.TABS_NAME_TODAY
        else:
            today = vec.sb.SPORT_DAY_TABS.today
        self.site.greyhound.tabs_menu.click_button(today)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(today).is_selected(),
                        msg='"Today tab" is not present')
        if self.brand == 'bma':
            actual_sub_tabs = self.site.greyhound.tab_content.items_names
            self.assertEqual(actual_sub_tabs, vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING,
                             msg=f'Actual tabs: "{actual_sub_tabs}" is not equal with the'
                                 f'Expected tabs: "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING}"')

            actual_sub_tab = self.site.greyhound.tab_content.current
            self.assertEqual(actual_sub_tab, vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING,
                             msg=f'Actual tabs: "{actual_sub_tab}" is not equal with the'
                                 f'Expected tab: "{vec.racing.DEFAULT_TIME_GROUPING_BUTTON_RACING}"')

    def test_002_verify_race_grid_sections(self):
        """
        DESCRIPTION: Verify race grid sections
        EXPECTED: The following sections are displayed and expanded by default:
        EXPECTED: **FOR CORAL (Mobile/Desktop):**
        EXPECTED: - UK&IRE
        EXPECTED: - VIRTUAL
        EXPECTED: - NEXT RACES
        EXPECTED: **FOR LADBROKES (Mobile/Desktop):**
        EXPECTED: - UK/IRELAND RACES
        EXPECTED: - VIRTUAL RACES
        """
        if self.brand == 'ladbrokes':
            sections = self.get_sections('greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
        sections = list(sections.values())
        self.assertTrue(sections, msg='No sections found in today tab')
        for i in range(len(sections)):
            self.assertTrue(sections[i].is_expanded(), msg=f'Event "{sections[i]}" is not expanded')
            sections[i].collapse()
            self.assertFalse(sections[i].is_expanded(expected_result=False), msg=f'Event "{sections[i]}" is not collapsed')
            if not self.brand == 'ladbrokes' and self.device_type == 'mobile':
                self.assertTrue(sections[i].is_chevron_down(), msg=f'Event "{sections[i]}" Chevron arrow to point to the top')
            sections[i].expand()
            self.assertTrue(sections[i].is_expanded(), msg=f'Event "{sections[i]}" is not expanded')
            if self.brand == 'bma' and self.device_type == 'desktop':
                self.assertTrue(sections[i].is_chevron_up(), msg=f'Event "{sections[i]}" Chevron arrow to point to the bottom')

    def test_003_collapse_and_expand_the_grid_sections_by_tapping_on_the_headers(self):
        """
        DESCRIPTION: Collapse and expand the grid sections by tapping on the headers
        EXPECTED: It is possible to collapse/expand accordions by tapping on the headers
        EXPECTED: **FOR MOBILE (Coral/Ladbrokes) and DESKTOP (Ladbrokes):**
        EXPECTED: - After collapsing: the downward arrow is displayed on the right side
        EXPECTED: - After expanding: No arrows displayed
        EXPECTED: **FOR DESKTOP (Coral):**
        EXPECTED: - After collapsing: the downward arrow is displayed on the right side
        EXPECTED: - After expanding: the upward arrow is displayed on the right side
        """
        # covered in step 2

    def test_004_verify_race_grid_content(self):
        """
        DESCRIPTION: Verify Race Grid content
        EXPECTED: All events from SS response with start time ( **startTime** attribute) corresponding to today's day  are displayed within the corresponding type (race meeting) section
        """
        section_name = vec.racing.UK_AND_IRE_TYPE_NAME.upper() if self.brand == 'bma' and self.device_type == 'mobile' else vec.racing.UK_AND_IRE_TYPE_NAME
        row_name = self.greyhound_autotest_name_pattern.upper() if self.brand == 'bma' else self.greyhound_autotest_name_pattern
        if self.brand == 'ladbrokes':
            sections = self.get_sections('greyhound-racing')
        else:
            sections = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in today tab')
        section = sections.get(section_name)
        section.expand()
        rows = section.items_as_ordered_dict
        self.assertTrue(rows, msg=f'No one row was found in section: "{section_name}"')
        row = rows.get(row_name)
        self.assertTrue(row, msg=f'"{row_name}" row was not found in "{rows.keys()}"')
        events = row.items_as_ordered_dict
        self.assertTrue(events, msg=f'No one event was found in row: "{row_name}"')
        event = events.get(self.event_off_time1)
        self.assertTrue(event, msg=f'Event with off time "{self.event_off_time1}" was not found in "{events.keys()}"')
        event = events.get(self.event_off_time2)
        self.assertFalse(event, msg=f'Event with off time "{self.event_off_time2}" was found in "{events.keys()}"')

    def test_005_verify_filtered_out_events(self):
        """
        DESCRIPTION: Verify filtered out events
        EXPECTED: Events that passed "Suspension Time" are not received and shown (**suspendAtTime** attribute)
        """
        # covered in step 4
