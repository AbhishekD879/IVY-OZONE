import pytest
import re
import tests
import voltron.environments.constants as vec
from faker import Faker
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - temporarily not applicable for PROD
@pytest.mark.sanity
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C874373_Verify_Featured_Module_adding_by_Type_ID_HL_TEST2(BaseFeaturedTest):
    """
    TR_ID: C874373
    NAME: Verify Featured Module adding by Type ID [HL/TEST2]
    DESCRIPTION: This test case verifies Modules configuring in CMS where Module consists of events retrieved by 'Type ID'
    DESCRIPTION: AUTOTESTS [C9690236] [C9697823] [C9690242] [C9690238]
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to 'Featured' tab/section
    PRECONDITIONS: **Configurations**
    PRECONDITIONS: 1) For creating the module in the 'Featured' tab/section by 'Type ID' via CMS use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=126685715
    PRECONDITIONS: 2) For reaching the appropriate CMS per env use the following link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To verify data for created 'Featured' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "EventsModule" an choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/32612728)
    PRECONDITIONS: 2) Be aware that Live events are not displayed in the 'Featured' modules for Desktop
    """
    keep_browser_open = True
    f = Faker()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test prematch event
        DESCRIPTION: Create Featured module in CMS by type id
        """
        if tests.settings.backend_env != 'prod':
            type_id = self.ob_config.football_config.england.premier_league.type_id
            event = self.ob_config.add_football_event_to_england_premier_league(team1=self.f.city(), team2=self.f.city(),
                                                                                start_time=self.get_date_time_formatted_string(hours=6))
            self.__class__.number_of_markets = len(event.ss_response['event']['children'])
        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            type_id, self.__class__.number_of_markets = event['event']['typeId'], len(event['event']['children'])
        self.__class__.module_data = self.cms_config.add_featured_tab_module(select_event_by='Type', id=type_id,
                                                                             events_time_from_hours_delta=-14,
                                                                             module_time_from_hours_delta=-14)
        self.__class__.module_name = self.module_data['title'].upper()

    def test_001_verify_created_module_on_featured_tabsection(self):
        """
        DESCRIPTION: Verify created module on 'Featured' tab/section
        EXPECTED: The created module is displayed and contains the following elements:
        EXPECTED: * Featured module header with module name set in CMS
        EXPECTED: * Odds Card Header (e.g. Home/Draw/Away) is displayed for the module
        EXPECTED: * Number of retrieved events corresponds to Max Events to Display value set in CMS
        EXPECTED: * All events within Module are in date/time range set in CMS #
        EXPECTED: * Event Start time/'Live'label/'Match Timer'/'Set'
        EXPECTED: * 'Watch Stream' icon if available
        EXPECTED: * 'Favourite' icon **Football Coral only**
        EXPECTED: * '<number of markets> MORE' link
        EXPECTED: * 'Footer' link set in CMS - only short internal URL should be used(e.x. /virtual-sports/virtual-horse-racing)
        """
        self.site.wait_content_state(state_name='Homepage')
        module_name = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        if not self.is_safari:
            self.wait_for_featured_module(name=self.module_name)
        self.__class__.module = self.get_module(module_content_name=module_name, module_name=self.module_name)
        self.assertTrue(self.module, msg=f'Featured module "{self.module_name}" not found')
        self.assertTrue(self.module.is_expanded(), msg=f'Featured module "{self.module_name}" is not expanded')
        self.assertEqual(self.module.name, self.module_name,
                         msg=f'Featured module name "{self.module.name}" is not as set in CMS "{self.module_name}"')
        self.assertEqual(self.module.fixture_header.header1, vec.sb.HOME,
                         msg=f'Actual fixture header: "{self.module.fixture_header.header1}" is not same as Expected fixure header: "{vec.sb.HOME}"')
        self.assertEqual(self.module.fixture_header.header2, vec.sb.DRAW,
                         msg=f'Actual fixture header: "{self.module.fixture_header.header2}" is not same as Expected fixure header: "{vec.sb.DRAW}"')
        self.assertEqual(self.module.fixture_header.header3, vec.sb.AWAY,
                         msg=f'Actual fixture header: "{self.module.fixture_header.header3}" is not same as Expected fixure header: "{vec.sb.AWAY}"')

        self.__class__.events = self.module.items_as_ordered_dict
        self.assertTrue(self.events, msg=f'No events found in "{self.module_name}" module')
        self.assertLessEqual(len(self.events), self.module_data['maxRows'],
                             msg=f'Actual number of events "{len(self.events)}" are more than max events set in CMS "{self.module_data["maxRows"]}"')

        for event in self.events.values():
            if event.has_watch_live_icon():
                self.assertTrue(event.has_watch_live_icon(), msg='"Watch Stream" icon is not displayed')
            if self.number_of_markets > 1:
                self.assertTrue(event.more_markets_link.is_displayed(), msg='"MORE" link is not displayed')
            if not event.is_live_now_event:
                self.assertTrue(event.template.event_time, msg='"Event time" is not displayed')

        footer_link_text = self.module_data['footerLink']['text']
        if self.device_type == 'desktop':
            footer_link_text = footer_link_text.upper()
        self.assertEqual(self.module.footer.text, footer_link_text,
                         msg=f'Footer link text "{self.module.footer.text}" '
                             f'is not as expected "{footer_link_text}"')

    def test_002_verify_events_order_within_the_module(self):
        """
        DESCRIPTION: Verify Events Order within the module
        EXPECTED: Events are ordered in the following way:
        EXPECTED: 1) Live events first:
        EXPECTED: * event displayOrder
        EXPECTED: * event start time
        EXPECTED: * alphabetically
        EXPECTED: 2) Not live events:
        EXPECTED: * event displayOrder
        EXPECTED: * event start time
        EXPECTED: * alphabetically
        """
        event_names_list = []
        if len(self.events) > 1:
            for event in self.events.values():
                if not event.is_live_now_event:
                    self.time = int(''.join([i for i in event.template.event_time if i.isdigit()]))
                    break

            for event_name, event in self.events.items():
                if not event.is_live_now_event:
                    event_time = int(''.join([i for i in event.template.event_time if i.isdigit()]))
                    self.assertTrue(event_time >= self.time, msg=f'Items are not sorted by time.')
                    if event_time == self.time:
                        event_names_list.append(event_name)
                    self.time = event_time
            self.assertEqual(event_names_list, sorted(event_names_list),
                             msg=f'Actual event names: "{event_names_list}" is not same as Expected sorted event names "{sorted(event_names_list)}"')

    def test_003_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: For Pre-Match events:
        EXPECTED: * For events that occur Today format is 24 hours:
        EXPECTED: HH:MM, Today (e.g. "14:00 or 05:00, Today")
        EXPECTED: * For events that occur in the future (including tomorrow) date format is 24 hours:
        EXPECTED: HH:MM, DD MMM (e.g. "14:00 or 05:00, 24 Nov or 02 Nov")
        EXPECTED: For Live events:
        EXPECTED: * Start time is substituted by 'LIVE' label/'Match Timer'/'<number> of Set'
        """
        for event in self.events.values():
            if not event.is_live_now_event:
                event_time = event.template.event_time
                if 'Today' in event_time:
                    self.assertTrue(re.findall("^[0-9][0-9]:[0-5][0-9],? Today$", event_time),
                                    msg=f'Event time: "{event_time}" is not displayed in expected formate')
                else:
                    self.assertTrue(re.findall("^[0-9][0-9]:[0-5][0-9],? [0-3][0-9] ("
                                               "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)$", event_time),
                                    msg=f'Event time: "{event_time}" is not displayed in expected formate')
