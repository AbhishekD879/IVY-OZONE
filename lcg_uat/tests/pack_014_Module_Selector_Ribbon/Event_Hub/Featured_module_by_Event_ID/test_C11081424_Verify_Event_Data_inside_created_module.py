import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #cannot create event hub in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C11081424_Verify_Event_Data_inside_created_module(BaseFeaturedTest):
    """
    TR_ID: C11081424
    NAME: Verify Event Data inside created module
    DESCRIPTION: This test case verifies Event Data inside the created module
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Active Featured module is created in CMS by sport Sport Event ID (not Outright Event with primary market) and displayed on Eventub tab.
    PRECONDITIONS: 3. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: In order to check event data use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: User is on Homepage > Featured tab
    """
    keep_browser_open = True
    watch_live_flags = ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Event Hub is created in CMS > Sport Pages > Event Hub.
        """
        event = self.ob_config.add_football_event_to_autotest_league2()
        self.__class__.eventID = event.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        event_name = normalize_name(event_resp[0]['event']['name'])
        markets = event_resp[0]['event']['children']
        outcomes = next(((market['market'].get('children')) for market in markets), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        self.__class__.is_watch_live = True if event.ss_response["event"]["drilldownTagNames"] in self.watch_live_flags else False
        self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'H'), None)
        self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'A'), None)
        self._logger.info(f'*** Created Football event  with name "{event_name}"')
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Event', id=self.eventID,
                                                              page_type='eventhub',
                                                              page_id=index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)
        self.__class__.module_name = module_data['title'].upper()
        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)
        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.site.wait_content_state("homepage")

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_navigate_to_the_configured_module_and_event_inside_the_module(self):
        """
        DESCRIPTION: navigate to the configured module and Event inside the module
        EXPECTED: Configured Event is shown inside the created module.
        """
        self.device.refresh_page()
        self.__class__.event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(self.event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: * Event name corresponds to name attribute
        EXPECTED: * Event name is displayed in two lines:
        EXPECTED: <Team1/Player1>
        EXPECTED: <Team2/Player2>
        """
        event_hub_modules = self.event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        self.__class__.event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(self.event_hub_module,
                        msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
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
        if self.is_watch_live:
            self.assertTrue(self.event_hub_module.has_stream(), msg='"Watch Live" icon is not found')
        else:
            self.assertFalse(self.event_hub_module.has_stream(expected_result=False),
                             msg='"Watch Live" icon should not be present')

    def test_005_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        """
        favourites_enabled = self.get_favourites_enabled_status()
        self.assertEqual(favourites_enabled,
                         self.event_hub_module.has_favourite_icon(expected_result=favourites_enabled),
                         msg=f'"Favourites" icon presence status is not "{favourites_enabled}"')

    def test_006_tap_anywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        self.event_hub_module.click()
        self.site.wait_content_state(state_name='EventDetails')
