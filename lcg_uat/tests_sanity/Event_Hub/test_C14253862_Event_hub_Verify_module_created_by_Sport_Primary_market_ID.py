from random import choice
import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod # Cannot configure Event hub module on prod cms
@pytest.mark.medium
@pytest.mark.featured
@pytest.mark.other
@pytest.mark.event_hub
@pytest.mark.module_ribbon
@pytest.mark.mobile_only
@vtest
class Test_C14253862_Event_hub_Verify_module_created_by_Sport_Primary_market_ID(BaseFeaturedTest):
    """
    TR_ID: C14253862
    VOL_ID: C58428336
    NAME: Event hub: Verify module created by <Sport> Primary market ID
    DESCRIPTION: This test case verifies featured events module created by <Sport> Primary Market ID on Event hub
    PRECONDITIONS: 1. CMS, TI:
    PRECONDITIONS: Coral: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: Ladbrokes: https://confluence.egalacoral.com/display/SPI/Ladbrokes+Environments
    PRECONDITIONS: 2. Event created in TI with Primary market available. Markets supported:
    PRECONDITIONS: -  Match Betting,
    PRECONDITIONS: -  Match Results,
    PRECONDITIONS: -  Extra Time Result,
    PRECONDITIONS: -  Extra-Time Result,
    PRECONDITIONS: -  Penalty Shoot-Out Winner,
    PRECONDITIONS: -  To Qualify
    PRECONDITIONS: 3. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
    PRECONDITIONS: 4. Featured module by Primary Market Id is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
    PRECONDITIONS: 5. Appropriate Module Ribbon Tab should be created for Event Hub
    PRECONDITIONS: 6. User is on Homepage > Event Hub tab
    """
    keep_browser_open = True
    extra_market = [('both_teams_to_score', {'cashout': True})]
    watch_live_flags = ['EVFLAG_AVA', 'EVFLAG_IVM', 'EVFLAG_PVM', 'EVFLAG_RVA', 'EVFLAG_RPM', 'EVFLAG_GVM']

    def test_000_preconditions(self):
        """
        DESCRIPTION: 2. Event created in TI with Primary market available. Markets supported:
        DESCRIPTION: -  Match Betting,
        DESCRIPTION: -  Match Results,
        DESCRIPTION: -  Extra Time Result,
        DESCRIPTION: -  Extra-Time Result,
        DESCRIPTION: -  Penalty Shoot-Out Winner,
        DESCRIPTION: -  To Qualify
        DESCRIPTION: 3. Event Hub is created and configured to be displayed on FE in CMS > Sport Pages > Event Hub
        DESCRIPTION: 4. Featured module by Primary Market Id is created in CMS > Sport Pages > Event Hub > %Specific event hub% > Featured events
        DESCRIPTION: 5. Appropriate Module Ribbon Tab should be created for Event Hub
        DESCRIPTION: 6. User is on Homepage > Event Hub tab
        """
        # Create event
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True)

            event = choice(events)
            self.__class__.eventID = event['event']['id']
            if event['event'].get('drilldownTagNames'):
                self.__class__.is_watch_live = any(flag in event['event']['drilldownTagNames'] for flag in self.watch_live_flags)
            else:
                self.__class__.is_watch_live = False
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event(markets=self.extra_market,
                                                                                     perform_stream=True)
            self.__class__.eventID = event_params.event_id
            self.__class__.is_watch_live = True

        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.markets = event_resp[0]['event']['children']
        default_market_id = [market['market']['id'] for market in self.markets if
                             market['market']['templateMarketName'] == 'Match Betting'][0]
        self.__class__.outcomes = next(((market['market'].get('children')) for market in self.markets), None)
        if self.outcomes is None:
            raise SiteServeException('There are no available outcomes')
        # outcomeMeaningMinorCode: A - away, H - home, D - draw
        self.__class__.team1 = next((outcome['outcome']['name'] for outcome in self.outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'H'), None)
        self.__class__.team2 = next((outcome['outcome']['name'] for outcome in self.outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') == 'A'), None)
        self._logger.info(f'*** Created Football event  with name "{event_name}"')

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
                                 timeout=60,
                                 bypass_exceptions=(IndexError, KeyError, TypeError, AttributeError))
        self.assertTrue(result, msg=f'Event hub module "{self.event_hub_tab_name}" was not found in initial data')

    def test_001_navigate_to_module_from_preconditions_make_sure_its_expanded_and_verify_its_contents(self):
        """
        DESCRIPTION: Navigate to Module from preconditions. Make sure it's expanded and verify it's contents
        EXPECTED: * Module name corresponds to Name set in CMS
        """
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        self.__class__.event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(self.event_hub_module, msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
        self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')

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

    def test_003_verify_fixture_header_and_price_buttons(self):
        """
        DESCRIPTION: Verify Fixture header and price buttons
        EXPECTED: * Fixture header depends on Market template:
        EXPECTED: - Home/Draw/Away
        EXPECTED: - 1/2
        EXPECTED: * Price buttons contain prices set in TI
        """
        self.assertEqual(self.event_hub_module.fixture_header.header1, vec.sb.HOME,
                         msg=f'Actual fixture header "{self.event_hub_module.fixture_header.header1}" does not '
                             f'equal to expected "{vec.sb.HOME}"')
        self.assertEqual(self.event_hub_module.fixture_header.header2, vec.sb.DRAW,
                         msg=f'Actual fixture header "{self.event_hub_module.fixture_header.header2}" does not '
                             f'equal to expected "{vec.sb.DRAW}"')
        self.assertEqual(self.event_hub_module.fixture_header.header3, vec.sb.AWAY,
                         msg=f'Actual fixture header "{self.event_hub_module.fixture_header.header3}" does not '
                             f'equal to expected "{vec.sb.AWAY}"')

        price_buttons = self.event_hub_module.get_active_prices()
        self.assertTrue(price_buttons, msg='Price buttons were not found')

        for name, bet_button in list(price_buttons.items()):
            price = bet_button.outcome_price_text
            self.assertRegexpMatches(price, self.fractional_pattern,
                                     msg=f'Odds value "{price}" is not in correct format "{self.fractional_pattern}"')
            price_resp = next((i["outcome"]["children"][0]["price"] for i in self.outcomes
                               if 'price' in i["outcome"]["children"][0].keys() and i["outcome"]['name'] == name), '')
            self.assertTrue(price_resp, msg=f'Price is not found in Siteserve response "{self.outcomes}"')
            price_resp = f'{price_resp["priceNum"]}/{price_resp["priceDen"]}'
            self.assertEqual(price, price_resp,
                             msg=f'Price "{price}" is not the same as in response "{price_resp}"')

    def test_004_verify_event_start_time(self):
        """
        DESCRIPTION: Verify Event Start time
        EXPECTED: Event start time corresponds to startTime attribute:
        EXPECTED: - 'Live' label is shown for in-play event
        EXPECTED: - For events that occur Today date format is 24 hours: HH:MM, Today (e.g. "14:00 or 05:00, Today")
        EXPECTED: - For events that occur in the future (including tomorrow) date format is 24 hours: HH:MM, DD MMM (e.g. 14:00 or 05:00, 24 Nov or 02 Nov)
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

    def test_005_verify_watch_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch' icon and label
        EXPECTED: 'Watch' icon and label are shown if **drilldownTagNames** attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: EVFLAG_GVM
        """
        if self.is_watch_live:
            self.assertTrue(self.event_hub_module.has_stream(), msg='"Watch Live" icon is not found')
        else:
            self.assertFalse(self.event_hub_module.has_stream(expected_result=False),
                             msg='"Watch Live" icon should not be present')

    def test_006_verify_favourites_icon(self):
        """
        DESCRIPTION: Verify 'Favourites' icon
        EXPECTED: 'Favourites' icon is displayed only for Football events within Module section (Coral only)
        """
        favourites_enabled = self.get_favourites_enabled_status()
        self.assertEqual(favourites_enabled, self.event_hub_module.has_favourite_icon(expected_result=favourites_enabled),
                         msg=f'"Favourites" icon presence status is not "{favourites_enabled}"')

    def test_007_verify__more_link(self):
        """
        DESCRIPTION: Verify '№ more' link
        EXPECTED: * '№ more' link present under price buttons in case there are more than 1 market in this event
        """
        if len(self.markets) > 1:
            markets_link = self.event_hub_module.get_markets_count_string()
            self.softAssert(self.assertRegexpMatches, markets_link, tests.settings.market_link_pattern,
                            msg=f'More link  "{markets_link}" not matching pattern "{tests.settings.market_link_pattern}"')

            extra_markets = len(self.markets) - 1
            markets_count = self.event_hub_module.get_markets_count()
            self.assertEqual(markets_count, extra_markets,
                             msg=f'Number of markets present in "MORE" link: "{markets_count}" '
                                 f'is not equal to expected: "{extra_markets}"')

    def test_008_tap_anywhere_on_event_section_except_for_price_buttons(self):
        """
        DESCRIPTION: Tap anywhere on Event section (except for price buttons)
        EXPECTED: Event Details Page is opened
        """
        self.event_hub_module.click()
        self.site.wait_content_state(state_name='EventDetails')
