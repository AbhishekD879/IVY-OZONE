import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.crl_tst2  # Only applicable for Coral
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C28825_Verify_By_Time_Sorting_Type(BaseRacing):
    """
    TR_ID: C28825
    NAME: Verify 'By Time' Sorting Type
    DESCRIPTION: This test case verifies 'Tomorrow' tab when 'By Time' sorting type is selected
    PRECONDITIONS: 1. In order to get a list with Classes ids use a link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id =21
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2. To retrieve all event outcomes for class id indentified in step 1 use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/ZZZZ?translationLang=LL?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *Where:*
    PRECONDITIONS: *-* *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *- XX - sport category id*
    PRECONDITIONS: *- ZZZZ is a comma separated list of Class id's(e.g. 97 or 97, 98);*
    PRECONDITIONS: *- YYYY1-MM1-DD1 is tomorrow's date;*
    PRECONDITIONS: *- YYYY2-MM2-YY2 is the day after tomorrow's date;
    PRECONDITIONS: *LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on event level to see event name and local time
    PRECONDITIONS: **FOR LADBROKES** BY MEETING/BY TIME subtabs removed according to the story BMA-42462 and design https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Load app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default -> 'BY MEETING' sorting type is selected by default
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create greyhound events
        EXPECTED: Events are created
        """
        self.__class__.tomorrow = vec.sb.SPORT_DAY_TABS.tomorrow
        if tests.settings.backend_env != 'prod':
            self.__class__.meeting_name = self.greyhound_autotest_name_pattern.upper()
            start_time_tomorrow = self.get_date_time_formatted_string(days=1, hours=2)
            self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1,
                                                         start_time=start_time_tomorrow)

    def test_001_tap_tomorrow_tab(self):
        """
        DESCRIPTION: Tap 'TOMORROW' tab
        EXPECTED: 'TOMORROW' tab is opened
        EXPECTED: 'BY MEETING' sorting type is selected by default
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')

        self.site.greyhound.tabs_menu.click_button(self.tomorrow)
        sleep(5)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(self.tomorrow).is_selected(),
                        msg='"Tomorrow tab" is not present')
        self.assertEqual(self.site.greyhound.tab_content.grouping_buttons.current,
                         vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[0],
                         msg=f'Opened grouping button "{self.site.greyhound.tab_content.grouping_buttons.current}" '
                             f'is not the same as expected "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[0]}"')

    def test_002_select_by_time_sorting_type(self):
        """
        DESCRIPTION: Select 'BY TIME' sorting type
        EXPECTED: 'BY TIME' sorting type is selected
        """
        sleep(5)
        self.site.greyhound.tab_content.grouping_buttons.click_button(
            vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1])
        self.assertEqual(self.site.greyhound.tab_content.grouping_buttons.current,
                         vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1],
                         msg=f'Opened grouping button "{self.site.greyhound.tab_content.grouping_buttons.current}" '
                             f'is not the same as expected "{vec.racing.EXPECTED_TIME_GROUPING_BUTTONS_RACING[1]}"')
        self.__class__.sections = self.get_sections('greyhound-racing')
        self.assertTrue(self.sections, msg='No race sections are found in by time')

    def test_003_check_events_section(self):
        """
        DESCRIPTION: Check Events section
        EXPECTED: 1.  Events Section is displayed
        EXPECTED: 2.  Events section is expanded by default
        """
        if self.device_type == "mobile":
            self.__class__.events_section = self.sections.get('EVENTS')
        else:
            self.__class__.events_section = self.sections.get('Events')
        self.assertTrue(self.events_section, msg='No events sections are found in by time')
        self.assertTrue(self.events_section.is_expanded(), msg='event section is not expanded')

    def test_004_verify_section_content(self):
        """
        DESCRIPTION: Verify section content
        EXPECTED: List of events for tomorrow's date is shown
        """
        race_events = self.events_section.race_by_time
        self.__class__.ls_events = race_events.items
        self.assertTrue(self.ls_events, msg="list of events are not displayed")

    def test_005_check_event_section(self):
        """
        DESCRIPTION: Check event section
        EXPECTED: 1.  Each event is in a separate block
        EXPECTED: 2.  Event name corresponds to the **'name'** attribute from the Site Server response (it includes race local time and event name)
        """
        for i in range(len(self.ls_events)):
            if tests.settings.backend_env != 'prod':
                self.assertIn(self.greyhound_autotest_name_pattern, self.ls_events[i].name,
                              msg=f'{self.ls_events[i].name} not includes {self.greyhound_autotest_name_pattern}')
            else:
                self.assertTrue(self.ls_events[i].name, msg='name attribute is not there in event section')

    def test_006_verify_stream_icon(self):
        """
        DESCRIPTION: Verify 'Stream' icon
        EXPECTED: 1.  Stream icon is displayed under the event name
        EXPECTED: 2.  Event name and Stream icon are aligned
        """

        # step NA as stream icon is not displaying
