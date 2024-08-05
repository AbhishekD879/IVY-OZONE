import pytest
from crlat_cms_client.utils.date_time import get_date_time_as_string
import voltron.environments.constants as vec
import tests
from selenium.common.exceptions import StaleElementReferenceException
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.cms
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.markets
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.reg165_fix
@pytest.mark.smoke
@pytest.mark.safari
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-53563')  # Ladbrokes Desktop only
@vtest
class Test_C28474_C28479_Verify_Sport_Pre_Match_Event_Details_Page(BaseSportTest):
    """
    TR_ID: C28474
    TR_ID: C28479
    NAME: Verify Sport Pre-Match Event Details Page
    """
    keep_browser_open = True
    event_details_page = None
    executed_on_mobile = None
    sport_name = 'Football'
    expanded_count = 0
    end_date = f'{get_date_time_as_string(days=1)}T00:00:00.000Z'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)

            self.__class__.event = events[0]
            self.__class__.eventID = self.event['event']['id']
            self.__class__.event_off_time = self.event['event']['startTime']
            self.__class__.market_name = next((market.get('market').get('name') for market in self.event['event']['children']
                                               if market.get('market').get('templateMarketName') == 'Match Betting'),
                                              None)
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event(
                markets=[('extra_time_result', {'cashout': False}),
                         ('to_win_not_to_nil', {'cashout': False}),
                         ('both_teams_to_score', {'cashout': False}),
                         ('draw_no_bet', {'cashout': False}),
                         ('handicap', {'cashout': False}),
                         ('to_qualify', {'cashout': False})])
            self.__class__.eventID = event_params.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.event = event_resp[0]
            self.__class__.event_off_time = self.event['event']['startTime']
            self.__class__.market_name = self.ob_config.football_config. \
                autotest_class.autotest_premier_league.market_name.replace('|', '')

        self.__class__.type_name = self.event['event']['typeName']
        self.__class__.created_event_name_raw = self.event['event']['name']
        self.__class__.created_event_name = normalize_name(self.created_event_name_raw)
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=self.event)

    def test_001_tap_sport(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon
        """
        self.site.open_sport(name=self.sport_name, timeout=10)
        self.__class__.executed_on_mobile = self.device_type in ['mobile', 'tablet']
        self.__class__.expanded_count = 2 if self.executed_on_mobile else 4

    def test_002_verify_tabs(self):
        """
        DESCRIPTION: Verify the following tabs There are the following tabs on the <Sport>
        EXPECTED: Landing page: 'IN-PLAY', 'COUPONS', 'MATCHES', 'OUTRIGHTS'
        """
        self.verify_tabs_length()
        self.verify_default_tabs_with_cms(self.ob_config.football_config.category_id)

    def test_003_click_event(self):
        """
        DESCRIPTION: Tap Event name on the event section, Football Event Details page is opened
        """
        try:
            event = self.get_event_from_league(section_name=self.section_name,
                                               event_id=self.eventID)
        except VoltronException:
            self.site.football.tab_content.grouping_buttons.items_as_ordered_dict.get(vec.sb.SPORT_DAY_TABS.tomorrow).click()
            event = self.get_event_from_league(section_name=self.section_name,
                                               event_id=self.eventID)
        event.click()
        self.site.wait_content_state('EventDetails')

    def test_004_back_button_exists(self):
        """
        DESCRIPTION: Verify back button
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: 'Back' button is displayed on the top of Event Details Page near <Sport> icon and label
        EXPECTED: **For desktop view:**
        EXPECTED: 'Back' button is displayed on the top of Event Details Page, on the left side from Event name
        """
        has_back_btn = wait_for_result(lambda:self.site.has_back_button, timeout=5)
        self.assertTrue(has_back_btn, msg='Event details page doesn\'t have back button')

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Event name corresponds to **name** attribute
        EXPECTED: Event name matches with event name on the event section we navigated from
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed below the 'Back' button
        EXPECTED: **For desktop view:**
        EXPECTED: It is displayed in the same line as 'Back' button, next to it
        EXPECTED: Long names are truncated
        """
        self.__class__.event_details_page = self.site.sport_event_details
        header_title = self.event_details_page.header_line.page_title.title

        if self.brand == 'ladbrokes':
            expected_header_title = self.type_name if self.executed_on_mobile else self.created_event_name.replace(' v ', ' V ')
        else:
            expected_header_title = self.sport_name.upper() if self.executed_on_mobile else self.created_event_name.upper()

        self.assertEqual(header_title.upper(), expected_header_title.upper(),
                         msg=f'Header title on Event Details Page "{header_title}"  does not match '
                             f'expected "{expected_header_title}" for "{self.device_type}" device')

        if self.executed_on_mobile:
            event_name_details_page = wait_for_result(lambda :self.event_details_page.event_title_bar.event_name, timeout=10)
            # Sometimes on opta scoreboard some other event name format is used, team names might be incomplete
            event_name = event_name_details_page.replace("(", "").replace(")", "")
            result = all((event.strip().replace(' FC',"") in self.event_name_on_sports_page) or (event.strip().replace(' FC',"") in self.created_event_name) for event in event_name.split('v'))
            # result = event_name in (self.event_name_on_sports_page, self.created_event_name)
            self.assertTrue(result, msg=f'Event name "{event_name_details_page}" on details page is not the same '
                                        f'as expected "{(self.event_name_on_sports_page, self.created_event_name)}"')
        else:
            breadcrumbs = OrderedDict((normalize_name(key.replace('  ', ' - ') if '(Bo1)' in key else key),
                                       self.site.sport_event_details.breadcrumbs.items_as_ordered_dict[key])
                                      for key in self.site.football.breadcrumbs.items_as_ordered_dict)
            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')
            self.assertIn(self.sport_name.title(), breadcrumbs,
                          msg=f'Sport title "{self.sport_name.title()}" was not found in breadcrumbs "{breadcrumbs}"')
            self.assertIn(self.created_event_name, breadcrumbs,
                          msg=f'Event name "{self.created_event_name}" was not found in breadcrumbs "{breadcrumbs.keys()}"')

    def test_006_verify_event_time_and_stream_link(self):
        """
        DESCRIPTION: Verify event start date/time
        DESCRIPTION: Verify event stream link
        """
        if not self.brand == 'ladbrokes':
            ui_format_pattern = '%A, %d-%b-%y. %H:%M' if \
                self.device_type == 'desktop' else '%H:%M - %d/%m/%y'
            ui_format_pattern_opta = '%A, %d-%b-%y. %H:%M' if \
                self.device_type == 'desktop' else '%H:%M - %d/%m/%Y'
        else:
            ui_format_pattern = ui_format_pattern_opta = '%A, %d-%b-%y, %I:%M %p' if \
                self.device_type == 'desktop' else '%H:%M, %d %b'

        event_time_ui = self.event_details_page.event_title_bar.event_time
        event_time_ob = self.event_off_time
        event_time_ob_converted = self.convert_time_to_local(
            ob_format_pattern=self.ob_format_pattern,
            date_time_str=event_time_ob,
            ui_format_pattern=ui_format_pattern,
            future_datetime_format=ui_format_pattern,
            ss_data=True)
        event_time_ob_converted_opta = self.convert_time_to_local(
            ob_format_pattern=self.ob_format_pattern,
            date_time_str=event_time_ob,
            ui_format_pattern=ui_format_pattern_opta,
            future_datetime_format=ui_format_pattern_opta,
            ss_data=True)
        if self.device_type=='desktop':
            result = event_time_ui in (event_time_ob_converted, event_time_ob_converted_opta)
            self.assertTrue(result,
                            msg=f'Event time on UI "{event_time_ui}" is not the same as got '
                                f'from response "{(event_time_ob_converted, event_time_ob_converted_opta)}"')

            is_live_event = self.event_details_page.event_title_bar.is_live_now_event
            self.assertFalse(is_live_event, msg='Created event is not live event')
            has_stream = self.event_details_page.has_stream(expected_result=False)
            self.assertFalse(has_stream, msg='Created event does not have stream')

    def test_007_market_tabs(self):
        """
        DESCRIPTION: Verify market tabs:
        EXPECTED: Market tabs are displayed and it is possible to navigate between all market tabs (those which have no content to be displayed are not shown)
        EXPECTED: 'MAIN MARKETS' tab is selected by default
        EXPECTED: Order of tabs is the same as configured in CMS
        """
        markets_tabs = self.event_details_page.markets_tabs_list.items_as_ordered_dict

        self.verify_edp_market_tabs_order(edp_market_tabs=markets_tabs.keys())
        if self.device_type=='desktop':
            default_tab = self.get_default_tab_name_on_sports_edp(event_id=self.eventID)
            for tab_name, tab in markets_tabs.items():
                if tab_name == default_tab:
                    is_tab_selected = tab.is_selected(timeout=3)
                    self.assertTrue(is_tab_selected, msg=f'"{default_tab}" tab is not selected by default')
                else:
                    is_tab_selected = tab.is_selected(expected_result=False)
                    self.assertFalse(is_tab_selected, msg=f'"{tab_name}" tab shouldn\'t be selected by default')
            tabs_context = self.event_details_page.markets_tabs_list
            for tab in markets_tabs.keys():
                tabs_context.open_tab(tab_name=tab)
                self.assertEqual(tab, tabs_context.current,
                                 msg=f'"{tab}" tab is not opened')
            self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=default_tab)

    def test_008_verify_markets_sections(self):
        """
        DESCRIPTION: Verify present market type sections:
        EXPECTED: The first **two** Market sections are expanded by default For Mobile/Tablet
        EXPECTED: The first **four** Market sections are expanded by default For Desktop
        EXPECTED: The remaining sections are collapsed by default
        EXPECTED: It is possible to collapse/expand market type sections by clicking the section's header
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No Markets found')

        if self.executed_on_mobile:
            for market_name, market in list(markets.items())[:self.expanded_count]:
                market.scroll_to()
                is_market_section_expanded = market.is_expanded(timeout=3,
                                                                bypass_exceptions=(StaleElementReferenceException, AttributeError))
                self.assertTrue(is_market_section_expanded,
                                msg=f'The section "{market_name}" is not expanded by default')

            for market_name, market in list(markets.items())[self.expanded_count:6]:  # 6 is here because we cannot check all accordions on prod, and on tst2/stg2 we create event with 6 markets, so the verification will be the same on all envs
                is_market_section_expanded = market.is_expanded(timeout=3, expected_result=False)
                self.assertFalse(is_market_section_expanded,
                                 msg=f'The section "{market_name}" is not collapsed by default')
        else:
            expanded_markets = len([market_name for market_name, market in markets.items() if market.is_expanded()])
            expected_count = len(markets.items()) if len(markets.items()) < self.expanded_count else self.expanded_count
            self.assertEqual(expanded_markets, expected_count,
                             msg=f'Found "{expanded_markets}" expanded markets while expected "{expected_count}"')

    def test_009_verify_price_odds_buttons(self):
        """
        DESCRIPTION: Verify Price/Odds buttons for selections
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No Markets found')
        market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=self.market_name)
        market = market_name.upper() if self.brand=='bma' and self.device_type=='mobile' else market_name.title()
        section = markets.get(market)
        self.assertTrue(section, msg=f'"{market_name}" section is not found in "{markets.keys()}"')
        output_prices_list = section.outcomes.items_as_ordered_dict
        self.assertTrue(output_prices_list, msg='Match result output prices were not found on Event Details page')
        prices = {}
        for output_price_name, output_price in output_prices_list.items():
            self.assertTrue(output_price.bet_button.is_enabled(),
                            msg=f'"{output_price_name}" price somehow shown as disabled')
            prices[output_price_name] = output_price.bet_button.outcome_price_text
        market = next(
            (market for market in self.event['event']['children'] if market['market'].get('templateMarketName') == 'Match Betting'),
            None)
        if not market:
            raise SiteServeException('Market with templateMarketName="Match Betting" is not found in response')
        self.__class__.prices = [
            f'{selection.get("outcome").get("children")[0].get("price").get("priceNum")}/{selection.get("outcome").get("children")[0].get("price").get("priceDen")}'
            for selection in market['market']['children']]

        self.assertListEqual(sorted(prices.values()), sorted(self.prices),
                             msg=f'List of prices "{sorted(prices.values())}" '
                                 f'is not the same as received from response "{sorted(self.prices)}"')
