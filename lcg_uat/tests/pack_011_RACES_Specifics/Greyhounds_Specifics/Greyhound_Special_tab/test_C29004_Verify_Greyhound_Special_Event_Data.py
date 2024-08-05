import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.stg2
@pytest.mark.tst2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C29004_Verify_Greyhound_Special_Event_Data(BaseRacing, BaseSportTest):
    """
    TR_ID: C29004
    NAME: Verify 'Greyhound Special' Event Data
    DESCRIPTION: This test case verifies 'Greyhound Special' events data
    PRECONDITIONS: To retrieve an information from the Site Server (tst2) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/*X.XX */EventToOutcomeForClass/201?translationLang=LL
    PRECONDITIONS: Where *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Class id = 201 for Greyhound Specials class
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'typeName'** on event level to identify needed event types to be displayed on the application
    PRECONDITIONS: **'classID'** on event level to see class id for selected event type
    PRECONDITIONS: **'className'** on event level to see class name where event belongs to
    PRECONDITIONS: **'name'** on event level to see event name and local time
    PRECONDITIONS: **'isStarted'**=true to see whether event is started
    PRECONDITIONS: **The full request to check data:**
    PRECONDITIONS: Ladbrokes
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/198,201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.isStarted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T14:17:00.000Z&simpleFilter=event.isResulted:isFalse&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    PRECONDITIONS: Coral
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForClass/201?simpleFilter=event.siteChannels:contains:M&simpleFilter=event.typeFlagCodes:intersects:SP&simpleFilter=event.startTime:greaterThanOrEqual:2020-08-26T00:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-08-27T00:00:00.000Z&simpleFilter=event.isFinished:isFalse&simpleFilter=event.isStarted:isFalse&simpleFilter=event.eventStatusCode:equals:A&simpleFilter=event.suspendAtTime:greaterThan:2020-08-26T13:35:30.000Z&limitRecords=outcome:1&limitRecords=market:1&translationLang=en&responseFormat=json&prune=event&prune=market
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load 'Invictus' application
        EXPECTED:
        """
        self.site.wait_content_state("Homepage")
        params = self.ob_config.add_greyhound_racing_specials_event(number_of_runners=2,
                                                                    ew_terms=self.ew_terms, time_to_start=20)
        self.__class__.event_id = params.event_id

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: Greyhounds landing page is opened
        EXPECTED: 'Today' tab is opened
        EXPECTED: **'By Meeting'** sorting type is selected by default
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing', timeout=20)
        if self.brand == 'ladbrokes':
            today = vec.sb.TABS_NAME_TODAY
        else:
            today = vec.sb.SPORT_DAY_TABS.today
        self.site.greyhound.tabs_menu.click_button(today)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(today).is_selected(),
                        msg='"Today tab" is not present')

    def test_003_go_to_the_special_event_type_section(self):
        """
        DESCRIPTION: Go to the special event type section
        EXPECTED: Event type section is shown
        """
        if self.brand == 'ladbrokes':
            specials = vec.racing.RACING_SPECIALS_TAB_NAME
            self.site.greyhound.tabs_menu.click_button(specials)
            self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(specials).is_selected(),
                            msg='Specials tab is not present')
        else:
            events = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get("GREYHOUND RACING SPECIALS")
            self.assertTrue(events, msg='No special events found races tab')
            events.click()

    def test_004_verify_class_name_and_class_id_from_the_site_server_response_for_chosen_event_type(self):
        """
        DESCRIPTION: Verify class Name and Class Id from the Site Server response for chosen event type
        EXPECTED: Displayed event type corresponds to the attributes
        EXPECTED: **'classId'**=201 and **'className'**='|Greyhounds - Specials|'
        """
        if self.brand == 'ladbrokes':
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Specials tab')
            first_section_name, first_section = list(sections.items())[0]
            first_section.expand()
            first_section_events = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(first_section_events, msg='Special tab has no events')
            self.__class__.event_name, event = list(first_section_events.items())[0]
            event.click()
            current = self.device.get_current_url()
            expected_value = 'greyhounds-specials'
            self.assertIn(expected_value, current, msg='User is not navigated to Specials EDP')

    def test_005_verify_section_content(self):
        """
        DESCRIPTION: Verify section content
        EXPECTED: Only NOT started events are displayed in the section
        """
        ss_request = self.ss_req.ss_event_to_outcome_for_event(event_id=self.event_id, query_builder=self.ss_query_builder)
        classid = ss_request[0]['event']['classId']
        self.assertEqual(classid, '201', msg='No class id found')
        classname = ss_request[0]['event']['className']
        self.assertEqual(classname, 'Greyhounds - Specials', msg='No class name found')
        eventtime = ss_request[0]['event']['isNext24HourEvent']
        self.assertTrue(eventtime, msg='Event is not next 24 hour event')
        rawisoffcode = ss_request[0]['event']['rawIsOffCode']
        self.assertIn(rawisoffcode, ['N', 'Y', '-'], msg='No raw_is_off_code found')

    def test_006_verify_events_within_section(self):
        """
        DESCRIPTION: Verify events within section
        EXPECTED: Only events for current day are displayed (see **'startTime'** attribute on event level)
        """
        # Covered in step 5

    def test_007_verify_started_event_within_sectionevent_with_attributesisstartedtrue_and_rawisoffcode_orrawisoffcodey(self):
        """
        DESCRIPTION: Verify started event within section
        DESCRIPTION: (event with attributes:
        DESCRIPTION: **'isStarted'**=true AND r**awIsOffCode="-"** OR
        DESCRIPTION: **rawIsOffCode="Y"**)
        EXPECTED: Started events disappear from the chosen section
        """
        # Covered in step 5

    def test_008_verify_event_type_section_if_all_events_from_this_event_type_are_started(self):
        """
        DESCRIPTION: Verify event type section if all events from this event type are started
        EXPECTED: Event type section disappear from the front end
        """
        # Covered in step 5

    def test_009_go_to_the_by_time_sorting_type___verify_special_events(self):
        """
        DESCRIPTION: Go to the 'By Time' sorting type -> verify special events
        EXPECTED: Greyhound special events are NOT shown on the 'By Time' sorting type
        """
        if self.brand == 'bma':
            self.navigate_to_page('greyhound-racing')
            self.site.greyhound.tab_content.grouping_buttons.click_button(
                vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1])
            self.assertEqual(self.site.greyhound.tab_content.grouping_buttons.current,
                             vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1],
                             msg=f'Opened grouping button "{self.site.greyhound.tab_content.grouping_buttons.current}" '
                                 f'is not the same as expected "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1]}"')
            events = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get("TRAP CHALLENGES")
            self.assertFalse(events, msg='Special events found on sort by meeting')

    def test_010_go_to_the_tomorrow_tab___verify_special_events(self):
        """
        DESCRIPTION: Go to the 'Tomorrow' tab -> verify special events
        EXPECTED: Greyhound special events are NOT shown on the 'Tomorrow' tab
        EXPECTED: They are not shown neither on 'By Meeting' nor on 'By Time' sorting types
        """
        if self.brand == 'ladbrokes':
            self.navigate_to_page('greyhound-racing')
            tomorrow = vec.sb.TABS_NAME_TOMORROW
            self.site.greyhound.tabs_menu.click_button(tomorrow)
        else:
            tomorrow = vec.sb.SPORT_DAY_TABS.tomorrow
            self.site.greyhound.tabs_menu.click_button(tomorrow)
            event_is_present = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get("TRAP CHALLENGES")
            self.assertFalse(event_is_present, msg='Special events found on tomorrow tab')

    def test_011_go_to_the_future_tab___verify_special_events(self):
        """
        DESCRIPTION: Go to the 'Future' tab -> verify special events
        EXPECTED: Greyhound special events are NOT shown on the 'Future' tab
        EXPECTED: They are not shown neither on 'By Meeting' nor on 'By Time' sorting types
        """
        if self.brand == 'ladbrokes':
            today = vec.sb.TABS_NAME_TODAY
            self.site.greyhound.tabs_menu.click_button(today)
        else:
            today = vec.sb.SPORT_DAY_TABS.today
            self.site.greyhound.tabs_menu.click_button(today)
            event_is_present = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get("TRAP CHALLENGES")
            self.assertFalse(event_is_present, msg='Special events found on future tab')
