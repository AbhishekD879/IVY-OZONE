import tests
import time
import pytest
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.homepage
@pytest.mark.featured
@pytest.mark.outrights
@pytest.mark.cms
@pytest.mark.high
@pytest.mark.mobile_only
@vtest
class Test_C29399_Featured_Verify_Event_Data_of_BIP_Events(BaseFeaturedTest):
    """
    TR_ID: C29399
    VOL_ID: C9697823
    NAME: Featured: Verify Event Data of BIP Events
    DESCRIPTION: This test case verifies Event Data of BIP events
    PRECONDITIONS: Active Featured module is created in CMS and is displayed on Featured tab. Make sure you have retrieved BIP events in this module.
    PRECONDITIONS: CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: In order to check event data use link:
    PRECONDITIONS:  - http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS:  - XXX - event ID
    PRECONDITIONS:  - X.XX - current supported version of OpenBet release
    PRECONDITIONS:  - LL - language (e.g. en, ukr)
    PRECONDITIONS: User is on Homepage > Featured tab
    PRECONDITIONS: Note: there are no BIP events on Desktop
    """
    keep_browser_open = True

    @classmethod
    def custom_tearDown(cls, **kwargs):
        if cls.inplay_module['disabled']:
            cms = cls.get_cms_config()
            cms.change_sport_module_state(cls.inplay_module)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create BIP test events in OB and Featured module in CMS
        """
        self.__class__.inplay_module = self.cms_config.get_sport_module()[0]
        if not self.inplay_module['disabled']:
            self.cms_config.change_sport_module_state(self.inplay_module, False)

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            type_id = event['event']['typeId']
            watch_live_flags = ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']
            if not any(flag in event['event']['drilldownTagNames'] for flag in watch_live_flags
                       if event['event'].get('drilldownTagNames')):
                self.__class__.has_stream_expected = False
            else:
                self.__class__.has_stream_expected = True
            self._logger.info(f'*** Found event "{self.event_name}" with type id "{type_id}" and stream'
                              f' availability: {self.has_stream_expected}')

            class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)
            ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                       class_id=class_ids,
                                       brand=self.brand)
            events_filter = self.basic_active_events_filter() \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))\
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                                          vec.siteserve.OUTRIGHT_EVENT_SORT_CODES))

            resp = ss_req.ss_event_to_outcome_for_class(query_builder=events_filter)
            outright_event_params = next((event for event in resp if
                                          event.get('event') and event['event'] and event['event'].get('children')), None)
            if not outright_event_params:
                raise SiteServeException(f'No active events found for category id "{self.ob_config.football_config.category_id}"'
                                         f' and event sort codes "{vec.siteserve.OUTRIGHT_EVENT_SORT_CODES}"')

            self.__class__.outright_name = outright_event_params['event']['name']
            outright_type_id = outright_event_params['event']['typeId']
            self._logger.info(f'*** Found outright event "{self.outright_name}" with type id "{outright_type_id}"')

        else:
            self.__class__.outright_name = f'Outright {int(time.time())}'
            start_time = self.get_date_time_formatted_string(seconds=15)
            self.__class__.event_params = \
                self.ob_config.add_football_event_to_featured_autotest_league(is_live=True,
                                                                              start_time=start_time,
                                                                              perform_stream=True)
            self.__class__.event_name = f'{self.event_params.team1} v {self.event_params.team2}'
            self.__class__.outright_event_params = \
                self.ob_config.add_autotest_premier_league_football_outright_event(event_name=self.outright_name,
                                                                                   selections_number=1,
                                                                                   is_live=True,
                                                                                   start_time=start_time,
                                                                                   perform_stream=True)
            self.__class__.has_stream_expected = True
            outright_type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        self.__class__.event_module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', show_all_events=True, id=type_id)['title'].upper()

        self.__class__.outright_module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', show_all_events=True, id=outright_type_id)['title'].upper()

    def test_001_go_to_event_section_of_bip_event(self):
        """
        DESCRIPTION: Go to event section of BIP event
        EXPECTED: BIP event is shown within Module just if it has:
        EXPECTED: Not Outright event:
        EXPECTED:  - isMarketBetInRun="true" (on the Primary Market level)
        EXPECTED:  - AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        EXPECTED: Outright event:
        EXPECTED:  - eventSortCode="TNMT"
        EXPECTED:  - AND **isMarketBetInRun="true" **(on the any Market level)
        EXPECTED:  - AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.event_module_name)
        self.wait_for_featured_module(name=self.outright_module_name)

        self.__class__.event_module_section = self.get_section(self.event_module_name)
        self.assertTrue(self.event_module_section, msg=f'Featured module: "{self.event_module_name}" not found')

        sport_events = self.event_module_section.items_as_ordered_dict
        self.assertTrue(sport_events, msg=f'No one event found in featured module: "{self.event_module_name}"')
        self.__class__.sport_event = sport_events.get(self.event_name)
        self.assertTrue(self.sport_event,
                        msg=f'Event: "{self.event_name}" not found in featured module: "{self.event_module_name}"')

        self.__class__.outright_module_section = self.get_section(self.outright_module_name)
        self.assertTrue(self.outright_module_section, msg=f'Featured module: "{self.outright_module_name}" not found')

        outright_events = self.outright_module_section.items_as_ordered_dict

        self.__class__.outright_event = outright_events.get(self.outright_name)
        self.assertTrue(self.outright_event,
                        msg=f'Outright event: "{self.outright_name}" not found in featured module: '
                            f'"{self.outright_module_name}"')

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: Event name corresponds to '**name**' attribute OR to <name> set in CMS if name was overridden
        EXPECTED: Event name is displayed in two lines:
        EXPECTED:  - <Team1/Player1>
        EXPECTED:  - <Team2/Player2>
        """
        self._logger.warning('*** This validation is covered indirectly by step 1 validations')

    def test_003_verify_live_label(self):
        """
        DESCRIPTION: Verify start time
        EXPECTED: Start time of event is not shown
        """
        if not self.brand == 'ladbrokes' and self.has_stream_expected:
            self.assertFalse(self.sport_event.event_time, msg=f'Start time is shown for event: "{self.event_name}"')

    def test_004_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED:  - EVFLAG_AVA
        EXPECTED:  - EVFLAG_IVM
        EXPECTED:  - EVFLAG_PVM
        EXPECTED:  - EVFLAG_RVA
        EXPECTED:  - EVFLAG_RPM
        EXPECTED:  - EVFLAG_GVM
        """
        self.assertEqual(self.sport_event.has_stream(), self.has_stream_expected,
                         msg=f'"Watch Live" icon presence: "{self.sport_event.has_stream()}". '
                             f'Expected: "{self.has_stream_expected}"')

    def test_005_verify_cash_out_label(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label
        EXPECTED: 'CASH OUT' label is not shown on module header
        """
        self.assertFalse(self.event_module_section.group_header.has_cash_out_mark(expected_result=False),
                         msg=f'"CASH OUT" label is found for featured module: "{self.event_module_name}"')

    def test_006_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        favourites_enabled = self.get_favourites_enabled_status()
        self.assertEqual(favourites_enabled, self.sport_event.has_favourite_icon(expected_result=favourites_enabled),
                         msg=f'"Favourites" icon presence status is not "{favourites_enabled}" for Football '
                             f'event: "{self.event_name}"')
        self.assertFalse(self.outright_event.has_favourite_icon(expected_result=False),
                         msg=f'"Favourites" icon is displayed for Outright event: "{self.outright_name}"')

    def test_007_tap_anywhere_on_event_section(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        self.sport_event.click()
        self.site.wait_content_state(state_name='EventDetails')
