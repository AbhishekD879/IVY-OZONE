import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from voltron.utils.exceptions.siteserve_exception import SiteServeException
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.grey_hounds_specific
@pytest.mark.sports_specific
@pytest.mark.races
@pytest.mark.reg165_fix
@vtest
class Test_C65969141_Verify_data_validation_in_the_Greyhounds_Specials_tab(BaseRacing):
    """
    TR_ID: C65969141
    NAME: Verify data validation in the Greyhounds Specials tab.
    DESCRIPTION: This test case verifies Greyhounds data loading in the Specials tab.
    PRECONDITIONS: To retrieve an information from the Site Server (*TST2 (CI-TEST2)*) use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk//openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/201?translationLang=LL
    PRECONDITIONS: Where X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: Class id = 201 - Greyhounds specials'typeName' on event level to identify needed event types to be displayed on the application.
    PRECONDITIONS: Greyhounds Specials present only for Today tab and only on 'By Meeting' sorting type.
    """
    keep_browser_open = True

    def extract_event_id_from_url(self):
        """
        Function to extract the last numbers(event id) from the URL
        """
        current_url = self.device.get_current_url()
        parts = current_url.split('/')
        for part in reversed(parts):
            if part.isnumeric():
                return part

    def test_001_load_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Load the Ladbrokes/Coral application.
        EXPECTED: The application should be successfully loaded.
        """
        # getting active special events for grey_hounds
        suspend_date = f'{get_date_time_as_string(time_format="%Y-%m-%dT%H:%M:%S")}'
        filters = [
            simple_filter(LEVELS.EVENT, attribute=ATTRIBUTES.CATEGORY_ID, operator=OPERATORS.EQUALS, value=19),
            simple_filter(LEVELS.EVENT, attribute=ATTRIBUTES.SITE_CHANNELS, operator=OPERATORS.CONTAINS, value='M'),
            simple_filter(LEVELS.EVENT, attribute=ATTRIBUTES.TYPE_FLAG_CODES, operator=OPERATORS.INTERSECTS, value='SP'),
            simple_filter(LEVELS.EVENT, attribute=ATTRIBUTES.IS_STARTED, operator=OPERATORS.IS_FALSE),
            simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, suspend_date),
            simple_filter(LEVELS.EVENT, attribute=ATTRIBUTES.IS_RESULTED, operator=OPERATORS.IS_FALSE)
        ]
        ss_bulider = self.ss_query_builder
        for fil in filters:
            ss_bulider.add_filter(fil)
        res = self.ss_req.ss_event_to_outcome_for_class(class_id=self.get_class_ids_for_category(category_id='19'), query_builder=ss_bulider)    #CLASS CODE FOR SPECIAL EVENTS = 201
        events = [event['event']['name'] for event in res]
        expected_event_names = [event.split(' (', 1)[0] for event in events]
        self.__class__.sorted_expected_events = sorted(expected_event_names)
        if not res:
            raise SiteServeException('no specials events available for greyhounds')
        self.site.wait_content_state("Homepage")

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon.
        EXPECTED: Greyhounds landing page is opened.
        EXPECTED: 'Today' tab is opened.
        EXPECTED: 'By Meeting' sorting type is selected by default.
        """
        self.navigate_to_page('greyhound-racing')
        self.site.wait_content_state('greyhound-racing', timeout=20)
        today = vec.sb.TABS_NAME_TODAY if self.brand == 'ladbrokes' else vec.sb.SPORT_DAY_TABS.today
        self.site.greyhound.tabs_menu.click_button(today)
        self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(today).is_selected(),
                        msg='"Today tab" is not selected')

    def test_003_go_to_the_special_event_type_section(self):
        """
        DESCRIPTION: Go to the Special event type section.
        EXPECTED: Event type section is shown.
        """
        if self.brand == 'ladbrokes':
            specials = vec.racing.RACING_SPECIALS_TAB_NAME
            self.site.greyhound.tabs_menu.click_button(specials)
            self.assertTrue(self.site.greyhound.tabs_menu.items_as_ordered_dict.get(specials).is_selected(),
                            msg='Specials tab is not selected')
        else:
            special_events_fe = []
            sections = {}
            if self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get('SPECIALS'):
                sections['SPECIALS'] = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get('SPECIALS')
            if self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get('TRAP CHALLENGES'):
                sections['TRAP CHALLENGES'] = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get('TRAP CHALLENGES')
            if self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get('WINNING DISTANCES'):
                sections['WINNING DISTANCES'] = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get('WINNING DISTANCES')
            self.assertTrue(len(sections.values())>0, msg='No special sections available in races tab')
            for section_name, section in sections.items():
                section.expand()
                available_special_events = section.items_as_ordered_dict
                for event_name in list(available_special_events.keys()):
                    special_events_fe.append(event_name)
            actual_event_names = [event.split(' (', 1)[0] for event in special_events_fe]
            sorted_actual_event_names = sorted(actual_event_names)
            self.assertListEqual(self.sorted_expected_events, sorted_actual_event_names,
                                 msg=f' expected events from site serve "{self.sorted_expected_events}" are not same as actual events"{sorted_actual_event_names}" in front end')

    def test_004_verify_class_name_and_class_id_from_the_site_server_response_for_chosen_event_type(self):
        """
        DESCRIPTION: Verify class Name and Class Id from the Site Server response for chosen event type.
        EXPECTED: Displayed event type corresponds to the attributes
        EXPECTED: 'classId'=201 and 'className'='|Greyhounds - Specials|'
        """
        if self.brand == 'ladbrokes':
            special_events_fe = []
            sections = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Specials tab')
            for section_name, section in sections.items():
                if section_name.upper() != "SPECIALS":
                    continue
                section.expand()
                available_special_events = section.items_as_ordered_dict
                for event_name in list(available_special_events.keys()):
                    special_events_fe.append(event_name)
            actual_event_names = [event.split(' (', 1)[0] for event in special_events_fe]
            sorted_actual_event_names = sorted(actual_event_names)
            self.assertListEqual(self.sorted_expected_events, sorted_actual_event_names, msg = f' expected events from site serve "{self.sorted_expected_events}" are not same as actual events"{sorted_actual_event_names}" in front end')

    def test_005_verify_section_content(self):
        """
        DESCRIPTION: Verify section content.
        EXPECTED: The events which have not started are displayed in the section.
        """
        #covered in above step

    def test_006_verify_events_within_section(self):
        """
        DESCRIPTION: Verify events within section.
        EXPECTED: Only events for current day are displayed (see 'startTime' attribute on event level).
        """
        # Covered in step 5

    def test_007_verify_started_event_within_sectionevent_with_attributesisstartedtrue_and_rawisoffcode__orrawisoffcodey(self):
        """
        DESCRIPTION: Verify started event within section
        DESCRIPTION: (event with attributes:
        DESCRIPTION: 'isStarted'=true AND r**awIsOffCode="-"** OR
        DESCRIPTION: rawIsOffCode="Y")
        EXPECTED: Started events disappear from the chosen section.
        """
        # Covered in step 5

    def test_008_verify_event_type_section_if_all_events_from_this_event_type_are_started(self):
        """
        DESCRIPTION: Verify event type section if all events from this event type are started.
        EXPECTED: Event type section disappear from the front end.
        """
        # Covered in step 5

    def test_009_go_to_the_tomorrow_tab__ampgt_verify_special_events(self):
        """
        DESCRIPTION: Go to the 'Tomorrow' tab -&amp;gt; verify special events.
        EXPECTED: Greyhounds special events are NOT shown on the 'Tomorrow' tab.
        EXPECTED: They are not shown neither on 'By Meeting' nor on 'By Time' sorting types.
        """
        if self.brand == 'ladbrokes':
            self.navigate_to_page('greyhound-racing')
            tomorrow = vec.sb.TABS_NAME_TOMORROW
            self.site.greyhound.tabs_menu.click_button(tomorrow)
            event_is_present = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict.get(
                "TRAP CHALLENGES")
        else:
            wait_for_result(lambda: self.site.has_back_button, expected_result=True,
                            name=f'back Button to be available in EDP "',
                            timeout=10, bypass_exceptions=VoltronException)
            tomorrow = vec.sb.SPORT_DAY_TABS.tomorrow
            self.site.greyhound.tabs_menu.click_button(tomorrow)
            event_is_present = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get(
                "TRAP CHALLENGES")
        self.assertFalse(event_is_present, msg='Special events found on tomorrow tab')

    def test_010_go_to_the_future_tab__ampgt_verify_special_events(self):
        """
        DESCRIPTION: Go to the 'Future' tab -&amp;gt; verify special events.
        EXPECTED: Greyhounds special events are NOT shown on the 'Future' tab.
        EXPECTED: They are not shown neither on 'By Meeting' nor on 'By Time' sorting types.
        """
        if self.brand == 'ladbrokes':
            future = vec.sb.TABS_NAME_FUTURE
            self.site.greyhound.tabs_menu.click_button(future)
            event_is_present = self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict.get(
                "TRAP CHALLENGES")
        else:
            future = vec.sb.SPORT_DAY_TABS.future
            self.site.greyhound.tabs_menu.click_button(future)
            event_is_present = self.site.greyhound.tab_content.accordions_list.racing_items_as_ordered_dict.get(
                "TRAP CHALLENGES")
        self.assertFalse(event_is_present, msg='Special events found on future tab')
