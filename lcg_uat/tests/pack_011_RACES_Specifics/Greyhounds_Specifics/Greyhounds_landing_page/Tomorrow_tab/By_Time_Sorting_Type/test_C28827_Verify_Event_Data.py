import re
import pytest
import tests
import voltron.environments.constants as vec
from json import JSONDecodeError
from tests.base_test import vtest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import do_request


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C28827_Verify_Event_Data(BaseRacing):
    """
    TR_ID: C28827
    NAME: Verify Event Data.
    DESCRIPTION: This test case verifies whether data about events is displayed correctly
    PRECONDITIONS: To get data about event statuses use the following steps;
    PRECONDITIONS: 1) Retrieve all classes for the category 'Horse racing'.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Horse Racing category id = 21
    PRECONDITIONS: Greyhound category id = 19
    PRECONDITIONS: 2. Retrieve all events for class identified in step 1. Use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/ZZZZ?translationLang=LL?simpleFilter=market.dispSortName:equals:MR&simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&simpleFilter=event.startTime:lessThan:YYYY2-MM2-DD2T00:00:00Z&simpleFilter=event.startTime:greaterThanOrEqual:YYYY1-MM1-DD1T00:00:00Z
    PRECONDITIONS: *Where:*
    PRECONDITIONS: *- X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *- XX - sport category id*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: *- ZZZZ is a comma separated list of class ids. (e.g. 97 or 97,98);*
    PRECONDITIONS: *- YYYY1-MM1-DD1 is tomorrow's date;*
    PRECONDITIONS: *- YYYY2-MM2-DD2 is the day after tomorrow's date;*
    PRECONDITIONS: **FOR LADBROKES** BY MEETING/BY TIME subtabs removed according to the story BMA-42462 and design https://app.zeplin.io/project/5c6d3e910cb0f599dfd2145b/screen/5d01033ae1287915e4816435
    PRECONDITIONS: Load app
    PRECONDITIONS: Navigate to Greyhounds page -> 'TODAY'tab is selected by default -> 'BY MEETING' sorting type is selected by default
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response(self, url):
        perflog = self.device.get_performance_log()
        final_request_url = ''

        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    final_request_url = request_url
                    break
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue

        response = do_request(url=final_request_url, method='GET')
        return response

    def test_001_go_to_tomorrow_tab___select_by_time_sorting_type(self):
        """
        DESCRIPTION: Go to 'TOMORROW' tab -> Select 'BY TIME' sorting type
        EXPECTED: 'Events' section is visible
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing')
        if tests.settings.backend_env != 'prod':
            start_time = self.get_date_time_formatted_string(days=1, hours=2)
            self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, start_time=start_time)
        tomorrow = vec.sb.TABS_NAME_TOMORROW.upper()
        self.site.greyhound.tabs_menu.click_button(tomorrow)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(tomorrow).is_selected(),
                        msg='"Tomorrow" tab is not present')
        tab_content = self.site.greyhound.tab_content
        tab_data = tab_content.has_grouping_buttons
        if not tab_data:
            raise SiteServeException(f'"events are not available in "{tomorrow}" tab"')
        tab_content.grouping_buttons.items_as_ordered_dict.get(vec.racing.BY_TIME_GROUPING_BUTTON_RACING).click()
        self.site.wait_content_state_changed(timeout=5)
        self.assertTrue(self.site.greyhound.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.racing.BY_TIME_GROUPING_BUTTON_RACING).is_selected(),
                        msg=f'"{vec.racing.BY_TIME_GROUPING_BUTTON_RACING}" is not selected after clicking on it')
        self.__class__.sections = self.get_sections('greyhound-racing')
        try:
            self.__class__.sections = self.get_sections('greyhound-racing')
            self.assertTrue(self.sections, msg='No sections found in future tab')
        except:
            self.device.refresh_page()
            self.site.wait_content_state_changed(timeout=15)
            self.__class__.sections = self.get_sections('greyhound-racing')
            self.assertTrue(self.sections, msg='No sections found in future tab')

    def test_002_verify_event_name_and_local_time(self):
        """
        DESCRIPTION: Verify Event name and local time
        EXPECTED: *   Event name corresponds to the **'name' **attribute
        EXPECTED: *   Event name and local time are hyperlinked
        EXPECTED: *   Event name is shown in 'HH:MM EventName' format
        EXPECTED: *   Events with LP prices are displayed in bold if **'priceTypeCodes="LP,"'** attribute is available for **'Win or Each way'** market only
        """
        events_section = self.sections.get('EVENTS' if self.device_type == "mobile" else 'Events')
        self.assertTrue(events_section, msg='No events sections are found in by time')
        if len(events_section.race_by_time.items_as_ordered_dict) == 0:
            raise VoltronException(f'No events are found in "by time" section of tomorrow tab')
        events = events_section.race_by_time.items_as_ordered_dict
        event = list(events.values())[-1] if len(events) > 1 else list(events.values())[0]
        event_name = event.race_name.text
        self.assertTrue(event.race_name.is_enabled(), msg='Event name and time are not hiperlinked')
        self.assertTrue(event_name, msg='Event name not found')
        match = re.match(r'^([01]?[0-9]|2[0-3]):[0-5][0-9][\s][\w\s-]*$', event_name)
        if not match:
            raise VoltronException('Event name: "{event_name}" was not in the expected formate')
        for event in events.values():
            if event.has_watch_live_icon():
                self.assertTrue(event.watch_live_icon.is_displayed(), msg='"Watch Live" icon is not displayed')
                self.assertTrue(event.watch_live.is_displayed(), msg='"Watch Live" label is not displayed')

        try:
            event.click()
        except Exception:
            event.go_to_race_card.click()
        self.site.wait_content_state_changed(timeout=5)

    def test_003_check_event_name__time_displaying(self):
        """
        DESCRIPTION: Check event name / time displaying
        EXPECTED: Event name/ time are in bold if **'priceTypeCodes="LP, '** attribute is available for **'Win or Each way'** market only
        """
        response = self.get_response('EventToOutcomeForEvent')
        market = response['SSResponse']['children'][0]['event']['children'][0]['market']
        if market['name'] == 'Win or Each Way':
            self.assertIn('SP', market['priceTypeCodes'],
                          msg=f'Actual PriceTypeCodes: "{market["priceTypeCodes"]}" is not same as Expected: "SP"')

    def test_004_verify_stream_icon(self):
        """
        DESCRIPTION: Verify 'Stream' icon
        EXPECTED: If event has stream available -> 'Stream' icon will be shown
        EXPECTED: ![](index.php?/attachments/get/38594)
        """
        # Covered in the step test_002

    def test_005_tap_event_name(self):
        """
        DESCRIPTION: Tap event name
        EXPECTED: Event landing page is opened
        """
        #  Covered in the step test_002

    def test_006_verify_by_time_sorting_type_when_there_are_no_events_to_show(self):
        """
        DESCRIPTION: Verify 'BY TIME' sorting type when there are no events to show
        EXPECTED: * Events section is not displayed
        EXPECTED: * Message is visible 'No events found'
        """
        try:
            no_events_lable = self.site.greyhound.tab_content.has_no_events_label()
            self.assertTrue(no_events_lable, msg='"No Events Found" lable is not dispalyed')
        except Exception:
            pass
