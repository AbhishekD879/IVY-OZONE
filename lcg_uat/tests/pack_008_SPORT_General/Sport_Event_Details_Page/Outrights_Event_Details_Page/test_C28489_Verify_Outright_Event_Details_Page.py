import pytest
import time
import voltron.environments.constants as vec
from crlat_ob_client.utils.date_time import validate_time
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.outrights
@pytest.mark.desktop
@pytest.mark.event_details
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C28489_Verify_Outright_Event_Details_Page(BaseSportTest):
    """
    TR_ID: C28489
    NAME: Verify Outright Event Details Page
    DESCRIPTION: This test case verifies <Sport> Event Details Page for 'Outrights' events
    PRECONDITIONS: *   'Outright' events are present
    PRECONDITIONS: *   http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: *   See attributes:
    PRECONDITIONS: - **'name'** on event level to see event name
    PRECONDITIONS: - '**startTime' **to check event start time and event start date
    PRECONDITIONS: - **'name****' **on outcome level to check selection name
    PRECONDITIONS: - **'priceNum',** **'priceDen'**,** 'priceDec'** on outcome level to check Price/Odds buttons correctness
    PRECONDITIONS: **Note:**
    PRECONDITIONS: *   LivePrice updates are NOT applicable for Outrights
    PRECONDITIONS: *   Scores are NOT applicable for Outrights
    PRECONDITIONS: *   Please check in Sport Specifics test cases whether Outrights are displayed in 'In-Play' and 'Outrights' tabs only or in all tabs (<Sports> where all events are Outrights)
    """
    keep_browser_open = True
    event_name = f'Outright event {int(time.time())}'
    markets_params = [('to_qualify', {'cashout': False}), ('to_win_to_nil', {'cashout': True})]
    available_markets = outright_market = None
    event_time = None

    def get_market_outcomes_for_event(self, event_id: (str, int)) -> dict:
        """
        Gets outcomes for all markets for specific event
        :param event_id: int, event id
        :return: dictionary where the key is market name, value is dictionary of outcome names and ids
        """
        resp = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id, query_builder=self.ss_query_builder)
        markets = resp[0]['event']['children'] if 'event' in resp[0] and 'children' in resp[0]['event'] else []
        markets_outcomes = {}
        for market in markets:
            if 'market' in market and 'children' in market['market']:
                outcomes = {}
                for outcome in market['market']['children']:
                    outcomes.update({outcome['outcome']['name']: outcome['outcome']['id']})
                markets_outcomes[market['market']['name']] = {'id': market['market']['id'], 'outcomes': outcomes}
        return markets_outcomes

    def verify_price_odds_format(self, expected_odds_format: str) -> None:
        """
        This method verifies whether odds format within market outcomes meets expected odds format (fraction or decimal)
        :param expected_odds_format: string type value that indicates odds format (fraction or decimal)
        """
        available_markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(available_markets, msg='There are no available markets')

        self.__class__.outright_market = available_markets.get(self.outright_market_section)
        self.assertTrue(self.outright_market, msg=f'"{self.outright_market_section}" '
                                                  f'is not found among markets "{list(available_markets.keys())}"')
        self.outright_market.expand()
        market_selections_list = self.outright_market.outcomes.items_as_ordered_dict
        self.assertTrue(market_selections_list, msg=f'"{self.outright_market}" market has no available selections')

        for outcome_name, odds_price in market_selections_list.items():
            self.check_odds_format(odds_price.bet_button.outcome_price_text, expected_odds_format=expected_odds_format)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create outright event and log in
        EXPECTED: User should be able to access previously generated event
        """
        event = self.ob_config.add_autotest_premier_league_football_outright_event(
            event_name=self.event_name, is_live=True, img_stream=True, markets=self.markets_params)
        self.__class__.eventID, self.__class__.event_time = event.event_id, event.event_date_time

        self.site.login(async_close_dialogs=False)

    def test_001_open_sport_outright_details_page(self):
        """
        DESCRIPTION: Open <Sport> Outright Details Page
        EXPECTED: Outright Details Page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

    def test_002_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: Event name corresponds to '**name**' attribute
        """
        if self.device_type == 'desktop' and self.brand != 'ladbrokes':
            self.__class__.expected_event_name = self.event_name.upper()
        elif self.device_type == 'desktop' and self.brand == 'ladbrokes':
            self.__class__.expected_event_name = self.event_name.title()
        else:
            self.__class__.expected_event_name = self.event_name
        event_name_ui = self.site.sport_event_details.event_title_bar.event_name
        self.assertEqual(event_name_ui, self.expected_event_name,
                         msg=f'"{event_name_ui}" event title is not the same as expected: "{self.expected_event_name}"')

    def test_003_verify_event_start_date_time(self):
        """
        DESCRIPTION: Verify Event start date/time
        EXPECTED: Event start date corresponds to startTime attribute
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed below the event name
        EXPECTED: Event start time is shown in: "HH:mm, DD-MMM" - 24h format (e.g. 14:00, 28 Feb)
        EXPECTED: **For desktop view:**
        EXPECTED: It is displayed below  the market name, on the right side
        EXPECTED: Event start time is shown in: "<name of the day>, DD-MMM-YY, HH:mm AM/PM" - 12h format (e.g. Tuesday, 24-Sep-19, 11:33 AM)
        """
        event_time_ui = self.site.sport_event_details.event_title_bar.event_time
        # VOL-1755
        if self.device_type == 'desktop':
            pattern = '%A, %d-%b-%y, %I:%M %p' if self.brand == 'ladbrokes' else '%A, %d-%b-%y. %H:%M'
            validate_time(actual_time=event_time_ui, format_pattern=pattern)
            self.compare_date_time(item_time_ui=event_time_ui, event_date_time_ob=self.event_time,
                                   format_pattern="%A, %d-%b-%y, %I:%M %p", dayfirst=False)
        else:
            validate_time(actual_time=event_time_ui, format_pattern=self.event_card_future_time_format_pattern)
            self.compare_date_time(item_time_ui=event_time_ui, event_date_time_ob=self.event_time,
                                   format_pattern=self.event_card_future_time_format_pattern, dayfirst=False)

    def test_004_verify_live_label(self):
        """
        DESCRIPTION: Verify 'LIVE' label
        EXPECTED: 'LIVE' label is displayed if event is live now:
        EXPECTED: * rawIsOffCode="Y"
        EXPECTED: * rawIsOffCode="-" AND isStarted="true"
        """
        is_live_event = self.site.sport_event_details.event_title_bar.is_live_now_event
        self.assertTrue(is_live_event, msg='"LIVE" label is not shown on the screen')

    def test_005_verify_market_sections(self):
        """
        DESCRIPTION: Verify market sections
        EXPECTED: Market sections is displayed under event start time
        EXPECTED: Markets are shown based on **'dispayOrder'** attribute in ascending if more than one are available
        EXPECTED: The first two sections are expanded by default
        EXPECTED: Market collection is NOT shown
        EXPECTED: Market section header corresponds to 'name' attribute from SS response on market level
        """
        self.__class__.available_markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertEqual(len(self.available_markets), 3,
                         msg=f'Markets quantity: "{len(self.available_markets)}" is not the same as expected: "{3}"')

        market_outcomes = self.get_market_outcomes_for_event(event_id=self.eventID)
        if self.device_type == 'desktop' and self.brand != 'ladbrokes':
            for key in market_outcomes.keys():
                market_outcomes[key.upper()] = market_outcomes.pop(key)

        self.assertListEqual(sorted(list(self.available_markets.keys())), sorted(list(market_outcomes.keys())),
                             msg=f'Available markets: "{sorted(list(self.available_markets.keys()))}" '
                                 f'are not the same as expected: "{sorted(list(market_outcomes.keys()))}"')
        for market in list(self.available_markets.values())[:2]:
            self.assertTrue(market.is_expanded(), msg=f'"{market.name}" market is not expanded by default')

    def test_006_verify_cash_out_label(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label
        EXPECTED: 'CASH OUT' label is shown next to market name if cashoutAvail="Y" on market level
        """

        if self.brand == 'ladbrokes':
            self.__class__.outright_market_section = self.expected_market_sections.outright
        else:
            self.__class__.outright_market_section = vec.siteserve.EXPECTED_MARKET_SECTIONS_TITLE.outright if \
                self.device_type != 'desktop' else vec.siteserve.EXPECTED_MARKET_SECTIONS.outright
        self.__class__.outright_market = self.available_markets.get(self.outright_market_section)
        self.assertTrue(self.outright_market, msg='Outright market section is not found')
        self.assertTrue(self.outright_market.market_section_header.has_cash_out_mark(),
                        msg=f'"{self.outright_market_section}" market has no "CASH OUT" label')
        to_qualify_market_section = self.expected_market_sections.to_qualify.title() if self.device_type == 'mobile' or self.brand == 'ladbrokes' \
            else self.expected_market_sections.to_qualify.upper()
        to_qualify_market = self.available_markets.get(to_qualify_market_section)
        self.assertFalse(to_qualify_market.market_section_header.has_cash_out_mark(expected_result=False),
                         msg=f'"{to_qualify_market_section}" market expected without "CASH OUT" label')

    def test_007_verify_the_list_of_selections(self):
        """
        DESCRIPTION: Verify the list of selections
        EXPECTED: The list of selections corresponds to 'name' attribute for each outcome for verified event
        """
        outright_section = self.available_markets.get(self.outright_market_section)
        self.assertTrue(outright_section, msg=f'"{self.outright_market_section}" not found in "{self.available_markets}"')
        outright_section.expand()
        self.assertTrue(outright_section.is_expanded(), msg='Outright section is not expanded')
        market_outcomes = self.get_market_outcomes_for_event(event_id=self.eventID)
        outright_selections_list_from_ss_response = list(market_outcomes['Outright']['outcomes'].keys())
        outright_selections_list_from_ui = \
            list(self.outright_market.outcomes.items_as_ordered_dict.keys())
        self.assertListEqual(outright_selections_list_from_ss_response, outright_selections_list_from_ui,
                             msg=f'List of selections from SiteServe: "{outright_selections_list_from_ss_response}" '
                                 f'does not match with selections from ui: "{outright_selections_list_from_ui}"')

    def test_008_verify_price_odds_button(self):
        """
        DESCRIPTION: Verify Price/Odds button
        EXPECTED: * Price/Odds corresponds to the **'priceNum/priceDen' **in fraction format
        EXPECTED: * Price/Odds corresponds to the **'priceDec'** in decimal format
        """
        self.verify_price_odds_format(expected_odds_format='fraction')

        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.site.go_to_home_page()
        self.test_001_open_sport_outright_details_page()

        self.verify_price_odds_format(expected_odds_format='decimal')

    def test_009_verify_ordering_of_selection(self):
        """
        DESCRIPTION: Verify ordering of selection
        EXPECTED: Selections are ordered by:
        EXPECTED: * Price / Odds in ascending order
        EXPECTED: * Alphabetically by selection name - if prices are the same
        """
        odds_selections_list = self.outright_market.outcomes.items_as_ordered_dict.values()
        odds = [odds_price.bet_button.outcome_price_text for odds_price in odds_selections_list]
        self.assertTrue(all(odds[i] <= odds[i + 1] for i in range(len(odds) - 1)),
                        msg=f'Odds: "{odds}" should be sorted in ascending order')
