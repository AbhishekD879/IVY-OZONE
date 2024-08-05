import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod # Cannot configure Event hub module on prod cms
@pytest.mark.medium
@pytest.mark.featured
@pytest.mark.other
@pytest.mark.event_hub
@pytest.mark.sanity
@pytest.mark.module_ribbon
@pytest.mark.mobile_only
@vtest
class Test_C14253856_Event_Hub_Verify_Event_Data_inside_module_created_by_Event_ID(BaseFeaturedTest):
    """
    TR_ID: C14253856
    NAME: Event Hub: Verify Event Data inside module created by Event ID.
    DESCRIPTION: This test case verifies Event Data inside the created module
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Active Featured module is created in CMS by Sport Event ID (not Outright Event with primary market) for Event Hub.
    PRECONDITIONS: 3. Module Ribbon Tab is created for Event Hub
    PRECONDITIONS: 4. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: In order to check event data use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: User is on Homepage > Featured tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Event created in TI with Primary market available. Markets supported:
        DESCRIPTION: 2. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
        DESCRIPTION: 3. Featured module by Primary Market Id is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
        DESCRIPTION: 4. Appropriate Module Ribbon Tab should be created for Event Hub
        DESCRIPTION: 5. User is on Homepage > Event Hub tab
        """
        # Create event
        event_params = self.ob_config.add_autotest_premier_league_football_event(perform_stream=True)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        event_name = normalize_name(event_resp[0]['event']['name'])
        markets = event_resp[0]['event']['children']
        outcomes = next(((market['market'].get('children')) for market in markets), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        # outcomeMeaningMinorCode: A - away, H - home, D - draw
        self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'H'), None)
        self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'A'), None)
        self._logger.info(f'*** Created Football event  with name "{event_name}"')

        # Create Event Hub module
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        # need a unique non-existing index for new Event hub
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')

        module_data = self.cms_config.add_featured_tab_module(events_time_from_hours_delta=-14, module_time_from_hours_delta=-14,
                                                              select_event_by='Event',
                                                              id=self.eventID,
                                                              page_type='eventhub',
                                                              page_id=index_number)
        self.__class__.module_name = module_data['title'].upper()

        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        result = wait_for_result(lambda: self.event_hub_tab_name in [module.get('title').upper() for module in
                                                                     self.cms_config.get_initial_data().get('modularContent', [])
                                                                     if module['@type'] == 'COMMON_MODULE'],
                                 name=f'Event hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=200,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')

    def test_001_navigate_to_the_configured_event_hub_module_and_event_inside_the_module(self):
        """
        DESCRIPTION: Navigate to the configured Event Hub module and Event inside the module
        EXPECTED: Configured Event is shown inside the created module.
        """
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        self.__class__.event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(self.event_hub_module, msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: * Event name corresponds to name attribute
        EXPECTED: * Event name is displayed in two lines:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        """
        event_hub_team_1 = self.event_hub_module.first_player
        event_hub_team_2 = self.event_hub_module.second_player
        self.assertEqual(event_hub_team_1, self.team1, msg=f'Team1 name "{event_hub_team_1}" on Event hub module is '
                                                           f'not equal to expected "{self.team1}"')
        self.assertEqual(event_hub_team_2, self.team2, msg=f'Team2 name "{event_hub_team_2}" on Event hub module is '
                                                           f'not equal to expected "{self.team2}"')

    def test_003_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: * Event start time corresponds to startTime attribute
        EXPECTED: * For events that occur Today date format is 24 hours: HH:MM, Today (e.g. "14:00 or 05:00, Today")
        EXPECTED: * For events that occur in the future (including tomorrow) date format is 24 hours: HH:MM, DD MMM (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        event_time_ui = self.event_hub_module.event_time
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
        EXPECTED: * 'Watch' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: * EVFLAG_AVA
        EXPECTED: * EVFLAG_IVM
        EXPECTED: * EVFLAG_PVM
        EXPECTED: * EVFLAG_RVA
        EXPECTED: * EVFLAG_RPM
        EXPECTED: * EVFLAG_GVM
        """
        self.assertTrue(self.event_hub_module.has_stream(), msg='"Watch Live" icon is not found')

    def test_005_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        self.assertTrue(self.event_hub_module.has_favourite_icon,
                        msg=f'"Favourites" icon is not displayed"')

    def test_006_tap_anywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        self.event_hub_module.click()
        self.site.wait_content_state(state_name='EventDetails')
