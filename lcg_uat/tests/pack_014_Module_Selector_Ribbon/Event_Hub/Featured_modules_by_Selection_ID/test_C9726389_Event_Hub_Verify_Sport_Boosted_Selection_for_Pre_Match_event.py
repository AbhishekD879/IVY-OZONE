import pytest
import tests
from tests.base_test import vtest
from tzlocal import get_localzone
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod # Cannot configure Event hub module on prod cms
@pytest.mark.high
@pytest.mark.featured
@pytest.mark.other
@pytest.mark.event_hub
@pytest.mark.module_ribbon
@pytest.mark.mobile_only
@vtest
class Test_C9726389_Event_Hub_Verify_Sport_Boosted_Selection_for_Pre_Match_event(BaseFeaturedTest):
    """
    TR_ID: C9726389
    NAME: Event Hub: Verify <Sport> Boosted Selection for Pre-Match event
    DESCRIPTION: This test case verifies Modules configured in CMS for <Sport> where Module consists of one selection retrieved by 'Selection ID'.
    PRECONDITIONS: 1) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 2) To retrieve an information about event outcomes use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ?translationLang=LL
    PRECONDITIONS: *   *ZZZZ - an **'event id'***
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 4) Featured Events module by Selection Id with ID of Pre Match event
    PRECONDITIONS: 5) User is on Homepage > Event hub
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
        DESCRIPTION: 2. Featured module by Primary Market Id is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
        DESCRIPTION: 3. Appropriate Module Ribbon Tab should be created for Event Hub
        DESCRIPTION: 4. User is on Homepage > Event Hub tab
        """
        # Create event
        event_params = self.ob_config.add_autotest_premier_league_football_event(perform_stream=True)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        markets = event_resp[0]['event']['children']
        expected_market_name = 'Match Betting' if tests.settings.brand == 'bma' else 'Match Result'
        default_market_id = [market['market']['id'] for market in markets if
                             market['market']['templateMarketName'] == expected_market_name][0]
        outcomes = next(((market['market'].get('children')) for market in markets), None)
        if outcomes is None:
            raise SiteServeException('There are no available outcomes')
        # outcomeMeaningMinorCode: A - away, H - home, D - draw
        self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'H'), None)
        self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'A'), None)
        self._logger.info(f'*** Created Football event  with name "{self.event_name}"')

        # Create Event Hub module
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        # need a unique non-existing index for new Event hub
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')

        module_data = self.cms_config.add_featured_tab_module(select_event_by='Market',
                                                              id=default_market_id,
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

        result = wait_for_result(lambda: self.event_hub_tab_name in [module.get('title').upper() for module in
                                                                     self.cms_config.get_initial_data().get(
                                                                         'modularContent', [])
                                                                     if module['@type'] == 'COMMON_MODULE'],
                                 name=f'Event hub tab "{self.event_hub_tab_name}" appears',
                                 timeout=60,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')

    def test_001_verify_selection_name(self):
        """
        DESCRIPTION: Verify 'Selection Name'
        EXPECTED: * 'Selection Name' within module corresponds to <name> attribute from SS response OR to <name> set in CMS if name was overridden
        EXPECTED: * Name of a long selection is wrapped into a few lines without cutting the text
        """
        self.site.wait_content_state('Homepage')
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')

        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(event_hub_module,
                        msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
        self.assertTrue(event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')

        self.__class__.module = self.get_section(self.module_name)
        events = self.module.items_as_ordered_dict
        self.assertTrue(events, msg=f'No events found in "{self.module_name}" module')

        self.__class__.event = events.get(self.event_name)
        self.assertTrue(self.event, msg=f'Event "{self.event_name}" not found among events "{events.keys()}"')

        selections = self.event.get_available_prices()
        self.assertTrue(selections, msg=f'No selections found in Boosted selections module event')
        self.__class__.selection_name, self.__class__.selection = list(selections.items())[0]

        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                              query_builder=self.ss_query_builder)
        self.__class__.outcomes_resp = self.event_resp[0]['event']['children'][0]['market']['children']
        name_resp = next((i['outcome']['name'] for i in self.outcomes_resp if i['outcome']['name'] == self.team1), '')
        self.assertEqual(self.selection_name, name_resp,
                         msg=f'*Selection Name* "{self.selection_name}" within module '
                             f'does not correspond to <name> attribute from SS response "{name_resp}"')

    def test_002_verify_event_start_time_within_created_module(self):
        """
        DESCRIPTION: Verify 'Event Start time' within created Module
        EXPECTED: *   'Event Start time' corresponds to '**startTime**' attribute
        EXPECTED: *   For events that occur Today date format is **HH:MM, Today**
        EXPECTED: *   For events that occur Tomorrow date format is **HH:MM, DD MMM** (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
        """
        event_time_ui = self.event.event_time
        event_time_resp = self.event_resp[0]['event']['startTime']
        timezone = str(get_localzone())
        self._logger.info(f'*** Current timezone is: "{timezone}"')
        utcoffset = 60 if timezone == 'Asia/Calcutta' else 0

        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               ui_format_pattern=self.event_card_today_time_format_pattern,
                                                               future_datetime_format=self.event_card_future_time_format_pattern,
                                                               ss_data=True,
                                                               utcoffset=utcoffset)
        self.assertEqual(event_time_ui, event_time_resp_converted,
                         msg=f'Event time on UI "{event_time_ui}" is not the same '
                             f'as got from response "{event_time_resp_converted}"')

    def test_003_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section
        EXPECTED: NOTE: 'Favourites' functionality is turned off for Ladbrokes by Default
        """
        favourites_enabled = self.get_favourites_enabled_status()
        self.assertEqual(favourites_enabled, self.event.has_favourite_icon(expected_result=favourites_enabled),
                         msg=f'"Favourites" icon presence status is not "{favourites_enabled}"')

    def test_004_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: EVFLAG_GVM
        """
        self.assertTrue(self.event.has_stream(), msg='"Watch Live" icon is not found')

    def test_005_verify_priceodds_button_within_created_module(self):
        """
        DESCRIPTION: Verify 'Price/Odds' button within created Module
        EXPECTED: 'Price/Odds' button is shown with correct price which corresponds to **'priceNum/priceDen'** in fractional format (**'priceDec'** in decimal format) attributes values in SS response
        """
        bet_buttons = self.module.get_available_prices()
        self.assertTrue(bet_buttons, msg=f'No selections found: "{bet_buttons}"')
        bet_button = bet_buttons.get(self.team1)
        self.assertTrue(bet_button,
                        msg=f'"{self.team1}" selection bet button is not found within module "{self.module_name}"')

        price_resp = next((i["outcome"]["children"][0]["price"] for i in self.outcomes_resp
                           if 'price' in i["outcome"]["children"][0].keys() and i["outcome"]['name'] == self.team1), '')
        self.assertTrue(price_resp, msg=f'Price is not found in Siteserve response "{self.outcomes_resp}"')
        lp_price_resp = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}'
        self.assertEqual(bet_button.outcome_price_text, lp_price_resp,
                         msg=f'Price "{bet_button.outcome_price_text}" is not the same as in response "{lp_price_resp}"')

    def test_006_clicktapanywhere_on_event_card_except_for_price_buttons_within_verified_module(self):
        """
        DESCRIPTION: Click/Tap anywhere on Event card (except for price buttons) within verified module
        EXPECTED: Event Details page is opened
        """
        self.event.click()
        self.site.wait_content_state(state_name='EventDetails')
