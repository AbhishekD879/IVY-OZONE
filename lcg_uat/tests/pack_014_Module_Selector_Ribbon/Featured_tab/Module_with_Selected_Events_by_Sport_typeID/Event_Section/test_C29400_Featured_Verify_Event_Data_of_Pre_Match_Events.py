import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - since Featured module is created
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.featured
@pytest.mark.module_ribbon
@pytest.mark.cms
@pytest.mark.high
@vtest
class Test_C29400_Featured_Verify_Event_Data_of_Pre_Match_Events(BaseFeaturedTest):
    """
    TR_ID: C29400
    NAME: Featured: Verify Event Data of Pre-Match Events
    DESCRIPTION: This test case verifies Event Data of Pre-Match events.
    PRECONDITIONS: 1. Active Featured module is created in CMS by sport Type ID and displayed on Featured tab in app. Make sure you have retrieved Pre-Match events in this module.
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3. In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4. User is on Homepage > Featured tab
    """
    keep_browser_open = True
    event_resp = None
    has_stream_expected = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test prematch event
        EXPECTED: Football event and featured module were created
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            self.__class__.eventID = event['event']['id']
            type_id = event['event']['typeId']
            watch_live_flags = ['EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']
            if not any(flag in event['event'].get('drilldownTagNames', '') for flag in watch_live_flags):
                self.__class__.has_stream_expected = False
        else:
            start_time = self.get_date_time_formatted_string(hours=3)
            event_params = self.ob_config.add_football_event_to_featured_autotest_league(
                start_time=start_time, perform_stream=True)
            self.__class__.eventID = event_params.event_id
            team1, team2 = event_params.team1, event_params.team2
            self.__class__.event_name = f'{team1} v {team2}'
            self._logger.info(f'*** Created Football event "{self.event_name}"')

            type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', show_all_events=True, show_expanded=True, id=type_id)['title'].upper()

    def test_001_go_to_event_section_of_pre_match_event(self):
        """
        DESCRIPTION: Go to event section of Pre-Match event
        EXPECTED: Event is shown
        """
        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name)
        modules = self.site.home.get_module_content(
            module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        ).accordions_list.items_as_ordered_dict
        self.assertIn(self.module_name, modules,
                      msg=f'"{self.module_name}" module is not found among modules "{modules.keys()}"')
        self.__class__.module = modules[self.module_name]
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        events = self.module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.module_name}" module')

        self.__class__.event = events.get(self.event_name)
        self.assertTrue(self.event, msg=f'Event "{self.event_name}" not found among events "{events.keys()}"')

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: * Event name corresponds to **name** attribute OR to **name** set in CMS if it was overridden
        EXPECTED: * Event name is displayed in two lines:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        """
        # Verified on step1
        pass

    def test_003_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: *   Event start time corresponds to **startTime** attribute
        EXPECTED: *   Event Start Time is shown below event name
        EXPECTED: *   For events that occur Today date format is 24 hours: for Coral: HH:MM, Today (e.g. "14:00 or 05:00, Today"), for Ladbrokes: HH:MM Today (e.g. "14:00 or 05:00 Today")
        EXPECTED: *   For events that occur in the future (including tomorrow) date format is 24 hours: for Coral: HH:MM, DD MMM (e.g. 14:00 or 05:00, 24 Nov or 02 Nov), for Ladbrokes: HH:MM DD MMM (e.g. 14:00 or 05:00 24 Nov or 02 Nov)
        """
        event_time_ui = self.event.event_time
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        event_time_resp = event_resp[0]['event']['startTime']
        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               ui_format_pattern=self.event_card_today_time_format_pattern,
                                                               future_datetime_format=self.event_card_future_time_format_pattern,
                                                               ss_data=True
                                                               )
        self.assertEqual(event_time_ui, event_time_resp_converted,
                         msg=f'Event time on UI "{event_time_ui}" is not the same as got from '
                             f'response "{event_time_resp_converted}"')

    def test_004_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: * 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: *   EVFLAG_AVA
        EXPECTED: *   EVFLAG_IVM
        EXPECTED: *   EVFLAG_PVM
        EXPECTED: *   EVFLAG_RVA
        EXPECTED: *   EVFLAG_RPM
        EXPECTED: *   EVFLAG_GVM
        """
        self.assertEqual(self.event.has_stream(), self.has_stream_expected,
                         msg=f'"Watch Live" icon presence: "{self.event.has_stream()}". Expected: "{self.has_stream_expected}"')

    def test_005_verify_cash_out_label(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label
        EXPECTED: 'CASH OUT' label is not shown on module header
        """
        self.assertFalse(self.module.group_header.has_cash_out_mark(expected_result=False), msg='"Cashout" icon is found')

    def test_006_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        favourites_enabled = self.get_favourites_enabled_status()
        self.assertEqual(favourites_enabled, self.event.has_favourite_icon(expected_result=favourites_enabled),
                         msg=f'"Favourites" icon presence status is not "{favourites_enabled}"')

    def test_007_tap_anywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        self.event.click()
        self.site.wait_content_state(state_name='EventDetails')
