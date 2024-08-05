import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.high
@pytest.mark.homepage_featured
@pytest.mark.featured
@pytest.mark.football
@pytest.mark.cms
@pytest.mark.mobile_only
@vtest
class Test_C10877930_Verify_Event_Data_inside_created_module(BaseFeaturedTest):
    """
    TR_ID: C10877930
    VOL_ID: C13032153
    NAME: Verify Event Data inside created module
    DESCRIPTION: This test case verifies Event Data inside the created module
    PRECONDITIONS: 1. Active Featured module is created in CMS by sport Sport Event ID (not Outright Event with primary market) and displayed on Featured tab.
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3. In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 4. User is on Homepage > Featured tab
    """
    keep_browser_open = True
    has_stream_expected = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        DESCRIPTION: Create Featured module by eventID
        """
        if tests.settings.backend_env == 'prod':
            category_id = self.ob_config.football_config.category_id
            event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.eventID = event['event']['id']
            self.__class__.event_name = normalize_name(event['event']['name'])
            self._logger.info(f'*** Found Football event with id "{self.eventID}"')
            watch_live_flags = ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']
            if not any(flag in event['event'].get('drilldownTagNames', '') for flag in watch_live_flags):
                self.__class__.has_stream_expected = False
        else:
            params = self.ob_config.add_autotest_premier_league_football_event(perform_stream=True)
            self.__class__.event_name = f'{params.team1} v {params.team2}'
            self.__class__.eventID = params.event_id

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=self.eventID)['title'].upper()

        self.site.wait_content_state('Homepage')

    def test_001_navigate_to_the_configured_module_and_event_inside_module(self):
        """
        DESCRIPTION: Navigate to the configured module and Event inside module
        EXPECTED: Configured Event is shown inside the created module.
        """
        self.wait_for_featured_module(name=self.module_name)
        modules = self.site.home.get_module_content(
            module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        ).accordions_list.items_as_ordered_dict
        self.assertTrue(modules, msg='No Featured modules found')
        module = modules.get(self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')
        self.assertTrue(module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')
        events = module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.module_name}" module')
        self.__class__.event = events.get(self.event_name)
        self.assertTrue(self.event, msg=f'Event "{self.event_name}" not found among events "{list(events.keys())}"')

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: * Event name corresponds to **name** attribute
        EXPECTED: * Event name is displayed in two lines:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        """
        self._logger.warning('*** This validation is covered by step 1 validations')

    def test_003_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: *   Event start time corresponds to **startTime** attribute
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
                                                               future_datetime_format=self.event_card_coupon_and_competition_future_time_format_pattern,
                                                               ss_data=True)
        self.assertEqual(event_time_ui, event_time_resp_converted,
                         msg=f'Event time on UI "{event_time_ui}" is not the same as got from '
                             f'response "{event_time_resp_converted}"')

    def test_004_verify_watch_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch' icon and label
        EXPECTED: * 'Watch' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: *   EVFLAG_AVA
        EXPECTED: *   EVFLAG_IVM
        EXPECTED: *   EVFLAG_PVM
        EXPECTED: *   EVFLAG_RVA
        EXPECTED: *   EVFLAG_RPM
        EXPECTED: *   EVFLAG_GVM
        """
        self.assertEqual(self.event.has_stream(), self.has_stream_expected,
                         msg=f'"Watch Live" icon presence: "{self.event.has_stream()}". Expected: "{self.has_stream_expected}"')

    def test_005_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        favourites_enabled = self.get_favourites_enabled_status()
        self.assertEqual(favourites_enabled, self.event.has_favourite_icon(expected_result=favourites_enabled),
                         msg=f'"Favourites" icon presence status is not "{favourites_enabled}" for Football event: "{self.event_name}"')

    def test_006_tap_anywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        self.event.click()
        self.site.wait_content_state(state_name='EventDetails')
