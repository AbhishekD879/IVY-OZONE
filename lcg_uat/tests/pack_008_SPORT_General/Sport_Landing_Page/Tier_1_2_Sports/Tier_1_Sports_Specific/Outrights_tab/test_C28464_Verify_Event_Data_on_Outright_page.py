import pytest
import tests
import time
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.utils.helpers import normalize_name
from voltron.environments import constants as vec
from crlat_ob_client.utils.date_time import validate_time
from crlat_siteserve_client.constants import LEVELS, OPERATORS, ATTRIBUTES
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests
from datetime import datetime


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28464_Verify_Event_Data_on_Outright_page(Common):
    """
    TR_ID: C28464
    NAME: Verify Event Data on Outright page
    DESCRIPTION: This test case verifies event data on Outright page
    PRECONDITIONS: **NOTE** :
    PRECONDITIONS: for Football Sport only, Outright' tab is removed from the module header into 'Competition Module Header' within 'Matches' tab
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: Sport icon is CMS configurable - https://CMS\_ENDPOINT/keystone/sport-categories (check CMS\_ENDPOINT via *devlog *function)
    """
    keep_browser_open = True

    def basic_active_events_filter(self):
        return self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_LIVE_NOW_EVENT, OPERATORS.IS_FALSE))

    def test_000_preconditions(self):
        if tests.settings.backend_env == 'prod':
            class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)

            ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                       class_id=class_ids,
                                       brand=self.brand)
            events_filter = self.basic_active_events_filter() \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                                          vec.siteserve.OUTRIGHT_EVENT_SORT_CODES))

            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
            event = next((event for event in resp if
                          event.get('event') and event['event'] and event['event'].get('children')), None)
            if not event:
                raise SiteServeException(f'No active events found for category id "{self.ob_config.football_config.category_id}"')
            self.__class__.outright_name = normalize_name(event['event']['name'])
            self.__class__.eventID = event['event']['id']
            class_name = event['event']['className'].split()[-1]
            type_name = event['event']['typeName']
            self.__class__.section_name = f'{class_name} - {type_name}'

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_for_mobiletabletnavigate_to_sport_landing_page_from_the_sports_menu_ribbonfor_desktopnavigate_to_sport_landing_page_from_the_left_navigation_menu(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to 'Sport' Landing page from the Sports Menu Ribbon
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Navigate to 'Sport' Landing page from the 'Left Navigation' menu
        EXPECTED: **Desktop**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        self.site.open_sport(name='FOOTBALL')
        current_tab_name = self.site.football.tabs_menu.current
        expected_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper()
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Default tab is not "{expected_tab_name}", it is "{current_tab_name}"')
        if self.device_type == 'desktop':
            actual_date_tab_name = self.site.football.date_tab.current_date_tab
            self.assertEqual(actual_date_tab_name, vec.sb.SPORT_DAY_TABS.today,
                             msg=f'Actual date tab is "{actual_date_tab_name}" not "{vec.sb.SPORT_DAY_TABS.today}"')

    def test_003_go_to_outrights_events_page(self):
        """
        DESCRIPTION: Go to 'Outrights' Events page
        EXPECTED:
        """
        outright_tab_name = vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper()
        wait_for_haul(2)
        outright_tab = self.site.football.tabs_menu.click_button(outright_tab_name)
        self.assertTrue(outright_tab, msg=f'"{outright_tab_name}" is not opened')
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            league = self.section_name
        else:
            league = self.section_name.upper()
            wait_for_haul(2)
        self.__class__.section = self.site.contents.tab_content.accordions_list.items_as_ordered_dict.get(league)
        self.section.expand()

    def test_004_verify_outrights_event_card(self):
        """
        DESCRIPTION: Verify 'Outrights' Event card
        EXPECTED: *   Event name corresponds to '**name**' attribute
        EXPECTED: *   Time and Date is removed from the 'Outrights' Event card
        EXPECTED: *   'Show All' button is removed from the 'Outrights' Event card
        EXPECTED: *   If 'LIVE' label is available, it is displayed next to 'Outrights' Event Name
        """
        # Cannot verify the unavailable elements.

    def test_005_clicktap_anywhere_whithin_outrights_event_card(self):
        """
        DESCRIPTION: Click/Tap anywhere whithin 'Outrights' Event card
        EXPECTED: 'Outright' Event details page is opened
        """
        outright = self.section.items_as_ordered_dict.get(self.outright_name)
        outright.click()
        self.site.wait_content_state('EventDetails')
        event_name_on_EDP = self.site.sport_event_details.event_title_bar.event_name.title()
        expected_outright_name = self.outright_name.title()
        self.assertEqual(event_name_on_EDP, expected_outright_name,
                         msg=f'Event name "{event_name_on_EDP}" on details page doesn\'t match with '
                             f'event name "{expected_outright_name}" on Football page')

    def test_006_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * It is displayed below the Event name
        EXPECTED: * Event start date corresponds to '**startTime**' attribute
        EXPECTED: * Event start date is shown in following format: ** HH:MM, ## MMM **
        EXPECTED: <HH:MM> is a 24 hour time range(i.e. 23:59)
        EXPECTED: <##> is the date integer value(i.e. 21, 31, 11)
        EXPECTED: <MMM> is the shortened name of the month(i.e. Mar, Apr, May)
        EXPECTED: **For Desktop:**
        EXPECTED: * It is displayed below in the right side of Sport Header
        EXPECTED: * Event start date corresponds to '**startTime**' attribute
        EXPECTED: * Event start date is shown in** '<name of the day>, DD-MMM-YY. 12 hours AM/PM'** format
        """
        event_time_ui = self.site.sport_event_details.event_title_bar.event_time
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)[0]['event']
        event_time_resp = self.event_resp['startTime']
        #UTC offset is not required in jenkins , if required remove commented lines and run the script 
        #is_dst = time.localtime().tm_isdst
        #utc_offset = 60 if is_dst == 0 else 0
        utc_offset = 0

        if self.device_type == 'desktop':
            #utc_offset = 60 if is_dst == 0 else 0
            # Ladbrokes 12 hrs format and Coral 24 hrs format
            pattern = '%A, %d-%b-%y, %I:%M %p' if self.brand == 'ladbrokes' else '%A, %d-%b-%y. %H:%M'
            date_time_obj = datetime.strptime(event_time_ui, pattern)
            new_date = date_time_obj.replace(date_time_obj.year)
            event_time_ui_new = datetime.strftime(new_date, pattern)
            event_time_resp_converted = self.convert_time_to_local(
                ob_format_pattern=self.ob_format_pattern,
                date_time_str=event_time_resp,
                ui_format_pattern=self.event_card_today_time_format_pattern,
                future_datetime_format=pattern,
                ss_data=True, utcoffset=utc_offset)
            validate_time(actual_time=event_time_ui_new, format_pattern=pattern)
            self.assertEqual(event_time_ui_new, event_time_resp_converted,
                             msg='UI date "%s" is not equal to created OB event date "%s"'
                                 % (event_time_ui_new, event_time_resp_converted))
        else:
            event_time_resp_converted = self.convert_time_to_local(
                ob_format_pattern=self.ob_format_pattern,
                date_time_str=event_time_resp,
                ui_format_pattern=self.event_card_today_time_format_pattern,
                future_datetime_format=self.event_card_coupon_and_competition_future_time_format_pattern,
                ss_data=True, utcoffset=utc_offset)
            validate_time(actual_time=event_time_ui, format_pattern=self.event_card_future_time_format_pattern)
            self.compare_date_time(item_time_ui=event_time_ui, event_date_time_ob=event_time_resp_converted,
                                   format_pattern=self.event_card_future_time_format_pattern, dayfirst=False)

    def test_007_verify_live_label(self):
        """
        DESCRIPTION: Verify 'LIVE' label
        EXPECTED: 'LIVE' label is shown if event is live now: rawIsOffCode="Y" OR rawIsOffCode="-" AND isStarted="true"
        """
        rawIsOffCode = self.event_resp['rawIsOffCode']
        is_started = wait_for_result(lambda: 'isStarted' in [self.event_resp.keys()], timeout=0.5)
        if rawIsOffCode in ['-' or 'Y'] and is_started:
            is_live_event = self.site.sport_event_details.event_title_bar.is_live_now_event
            self.assertTrue(is_live_event, msg='"LIVE" label is not shown on the screen')
