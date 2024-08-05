import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.environments.constants.base.markets_abbreviation import MarketAbbreviation


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.market_switcher_bpp
@pytest.mark.reg156_fix
@vtest
class Test_C60089508_Verify_MS_on_Matches_Tab_for_Basketball_SLP(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C60089508
    NAME: Verify MS on Matches Tab for Basketball SLP
    DESCRIPTION: This test case verifies 'Market Selector' dropdown list on Basketball landing page
    PRECONDITIONS: Precondition:
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Landing Page -> 'Click on Matches
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money Line (WW)| - "Money Line"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    inplay_list = []
    preplay_list = []

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None, header2=None,
                                                     aggregated=None, markets_qty=None):
        first_accordion = self.site.sports_page.tab_content.accordions_list.first_item[1]
        events = first_accordion.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = first_accordion.fixture_header
        market_abbr = MarketAbbreviation.FIXTURE_HEADERS_MARKETS_ABBREVIATION
        cms_header1 = market_abbr.get(header1.lower().replace(' ', ''), None)
        header1 = [header1.upper(), cms_header1.upper()] if cms_header1 != None else [header1.upper()]
        self.assertIn(event.header1.upper(), header1,
                      msg=f'Actual fixture header "{event.header1}" does not equal to'
                          f'Expected "{header1}"')
        if header2:
            cms_header2 = market_abbr.get(header2.lower().replace(' ', ''), None)
            header2 = [header2.upper(), cms_header2.upper()] if cms_header2 != None else [header2.upper()]
            self.assertIn(event.header2.upper(), header2,
                          msg=f'Actual fixture header "{event.header2}" does not equal to'
                              f'Expected "{header2}"')
        cms_header3 = market_abbr.get(header3.lower().replace(' ', ''), None)
        header3 = [header3.upper(), cms_header3.upper()] if cms_header3 != None else [header3.upper()]
        self.assertIn(event.header3.upper(), header3,
                      msg=f'Actual fixture header "{event.header2}" does not equal to'
                          f'Expected "{header3}"')
        if aggregated:
            markets_count = list(events)[0].aggregated_template.get_aggregated_markets_count
            self.assertEqual(markets_count, markets_qty, f'Actual Number of Aggregate Markets is "{markets_count}"'
                                                         f'is not same as Expected Number of Aggregated Markets "{markets_qty}"')
        else:
            bet_buttons = len(list(events)[-1].template.get_available_prices())
            self.assertEqual(bet_buttons, bet_button_qty,
                             msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                                 f'Expected Buttons: "{bet_button_qty}".')

    def place_bet_and_verify(self, aggregated=False, market_names=[], index_of_market=0):
        sections = list(self.site.sports_page.tab_content.accordions_list.n_items_as_ordered_dict().values())
        self.assertTrue(sections,
                        msg='"Sections" are not available')
        for section in sections:
            if not section.is_expanded():
                section.expand()
            events = list(section.items_as_ordered_dict.values())
            self.assertTrue(' "Events" are not available')
            for event in events:
                if aggregated:
                    market_section_objects = event.aggregated_template.get_market_sections
                    selections = list(market_section_objects[index_of_market].get_bet_buttons.values())
                else:
                    selections = list(event.template.items_as_ordered_dict.values())
                self.assertTrue(' "Selections" are not available')
                for selection in selections:
                    if selection.is_enabled():
                        selection.click()
                        self.__class__.is_clicked = True
                        break
                if self.is_clicked:
                    break
            if self.is_clicked:
                break

        self.__class__.is_clicked = False
        if self.device_type == 'mobile':
            self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=30), msg='Quick Bet panel is not opened')
            self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(),
                            msg='Bet Receipt is not displayed')
            self.site.quick_bet_panel.header.close_button.click()
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
        if aggregated and index_of_market+1 < len(market_names):
            self.place_bet_and_verify(aggregated=True, market_names=market_names, index_of_market=index_of_market+1)

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Basketball events  with scores
        EXPECTED: Event is successfully created
        """
        if tests.settings.backend_env != 'prod':
            all_sport_MS_Status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                           status=True)
            self.assertTrue(all_sport_MS_Status, msg='Market switcher is disabled for all sport')
            market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='basketball',
                                                                                              status=True)
            self.assertTrue(market_switcher_status, msg='Market switcher is disabled for basketball sport')
            self.cms_config.verify_and_update_sport_config(
                sport_category_id=self.ob_config.backend.ti.basketball.category_id,
                disp_sort_names='HL,WH,HH',
                primary_markets='|Money Line|,|Total Points|,'
                                '|Home team total points|,|Away team total points|,'
                                '|Half Total Points|,|Quarter Total Points|,'
                                '|Handicap 2-way|')
            markets = [
                ('total_points',),
                ('handicap_2_way',),
                ('home_team_total_points',),
                ('away_team_total_points',)]
            self.ob_config.add_basketball_event_to_us_league(markets=markets)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.basketball_config.category_id)
        matches_tab_data = self.cms_config.get_sports_tab_data(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            sport_id=self.ob_config.basketball_config.category_id)

        self.__class__.cms_markets = matches_tab_data.get('marketsNames', None)

        self.__class__.expected_market_selector_options = []

        self.__class__.expected_aggregate_market_names = []

        for market in self.cms_markets:
            self.expected_market_selector_options.append(market.get('title').strip().upper())
            if ',' in market.get('templateMarketName'):
                self.expected_aggregate_market_names.append(market.get('title').strip().upper())

        self.site.login()
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state_changed()
        sport_title = self.site.sports_page.header_line.page_title.text
        self.assertEqual(sport_title.upper(), vec.sb.BASKETBALL.upper(),
                         msg=f'Actual page is "{sport_title}",instead of "{vec.sb.BASKETBALL}"')
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed(timeout=10)
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: **Tablet/Mobile:**
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: **Desktop:**
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' **Coral**
        """
        if tests.settings.backend_env == 'prod' and self.device_type == 'desktop':
            for tab_name, tab in list(self.site.sports_page.date_tab.items_as_ordered_dict.items()):
                tab.click()
                no_events = self.site.sports_page.tab_content.has_no_events_label()
                if no_events:
                    self._logger.info(f'No Events available in the "{tab_name}" tab')
                else:
                    break
        else:
            has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
            self.assertTrue(has_market_selector, msg=' "Market selector" is not available for basketball')

        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                sleep(2)
                self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        dropdown.click()
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertIn(selected_value.upper(), self.expected_market_selector_options,
                         msg=f'Actual selected value: "{selected_value.upper()}" is not in'
                             f'Expected selected values: "{self.expected_market_selector_options}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Money Line
        EXPECTED: • Total Points
        EXPECTED: • Handicap (Handicap in lads and Spread in Coral)
        EXPECTED: • Home Team Total Points
        EXPECTED: • Away Team Total Points
        EXPECTED: **Note:**
        EXPECTED: • If any Market is not available then it is skipped in the Market selector drop down list*
        """
        available_markets = self.site.sports_page.tab_content.dropdown_market_selector.available_options
        for market in available_markets:
            self.assertIn(market.upper(), self.expected_market_selector_options,
                          msg=f'Actual market: {market} is not present in '
                              f'the Expected list: {self.expected_market_selector_options}')

    def test_003_select_total_points_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Total Points' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown (NO flikering issue should be there or same events getting displayed multiple times)
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        options = self.site.sports_page.tab_content.dropdown_market_selector
        markets_dropdown_list = list(options.items_as_ordered_dict.keys())
        if markets_dropdown_list == ['']:
            options = self.site.sports_page.tab_content.dropdown_market_selector
            markets_dropdown_list = list(options.items_as_ordered_dict.keys())
        for market in markets_dropdown_list:
            options.select_value(value=market)
            sleep(2)
            if market.upper() in self.expected_aggregate_market_names:
                fixture_markets = next((cms_market.get('templateMarketName') for cms_market in self.cms_markets if
                                        cms_market.get('title').upper() == market.upper()), None).upper().split(
                    ',')
                if len(fixture_markets) == 2:
                    self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=0,
                                                                      header1=fixture_markets[0],
                                                                      header3=None,
                                                                      header2=fixture_markets[1],
                                                                      aggregated=True,
                                                                      markets_qty=2)
                else:
                    self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=0,
                                                                      header1=fixture_markets[0],
                                                                      header2=fixture_markets[1],
                                                                      header3=fixture_markets[2],
                                                                      aggregated=True,
                                                                      markets_qty=3)
                self.place_bet_and_verify(aggregated=True, market_names=fixture_markets)
            else:
                if market.upper() in [vec.siteserve.EXPECTED_MARKETS_NAMES.money_line.upper(),
                                      vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way.upper()]:
                    self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1',
                                                                      header3='2')
                elif market.upper() in [vec.siteserve.EXPECTED_MARKETS_NAMES.total_points.upper(),
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points.upper(),
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.away_team_total_points.upper()]:
                    self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='OVER', header3='UNDER')

                self.place_bet_and_verify()
            options = self.site.sports_page.tab_content.dropdown_market_selector

    def test_004_verify_see_all_when_more_than_one_event_is_present_applicable_for_mobile_and_tablet___coral_and_lads__lads__desktop(
            self):
        """
        DESCRIPTION: Verify 'SEE ALL' when more than one event is present (Applicable for mobile and tablet - Coral and Lads & Lads- Desktop)
        EXPECTED: 'SEE All' option will be displayed when more than one event is there for that particular Tournament/League
        """
        if self.device_type == 'mobile':
            section_name, self.__class__.section = self.site.contents.tab_content.accordions_list.first_item
            self.assertTrue(self.section, msg=' "Sections" are not avaialbe')
            events = list(self.section.items_as_ordered_dict.values())
            if len(events) > 1:
                self.__class__.has_see_all_link = self.section.group_header.has_see_all_link()
                self.assertTrue(self.has_see_all_link, msg=f'*** SEE ALL link present in the section %s' % section_name)
            else:
                self.__class__.has_see_all_link = None
                self._logger.info(msg=' "SEE ALL" link is not available')

    def test_005_click_on_see_all(self):
        """
        DESCRIPTION: Click on 'SEE ALL'
        EXPECTED: User should be navigated to competition page where whole list of available events(Preplay/Inplay) will be displayed for that particular Tournament/League with Primary market displayed by default in Market switcher dropdown
        """
        if self.device_type == 'mobile':
            self.site.wait_splash_to_hide()
            if self.has_see_all_link:
                dropdown = self.site.contents.tab_content.dropdown_market_selector
                if dropdown.is_expanded():
                    dropdown.collapse()
                self.section.group_header.see_all_link.click()
                self.site.wait_content_state('CompetitionLeaguePage')
                sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(sections, msg='No list of available events are present on competition league page')
                for section in list(sections.values()):
                    events = list(section.items_as_ordered_dict.values())
                    for event in events:
                        event_template = event.template
                        is_live = event_template.is_live_now_event
                        self.inplay_list.append(is_live) if is_live else self.preplay_list.append(is_live)
                        odds = list(event_template.items_as_ordered_dict.values())
                        for odd in odds:
                            self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                        if is_live:
                            self._logger.info(f'{event_template.event_name} is live event')
                        else:
                            self.assertTrue(event_template.event_time,
                                            msg=' "Event time" not displayed')

                if len(self.inplay_list) > 0 and len(self.preplay_list) == 0:
                    self._logger.info(msg=f'Only "In-Play" events are available ')
                elif len(self.inplay_list) == 0 and len(self.preplay_list) > 0:
                    self._logger.info(msg=f'Only "Pre-Play" events are available ')
                else:
                    self._logger.info(msg=f'Both "In-Play" and "Pre-play" events are available ')

    def test_006_repeat_steps_3_5_for_the_following_markets_money_line_handicap_handicap_in_lads_and_spread_in_coral_home_team_total_points_away_team_total_points(
            self):
        """
        DESCRIPTION: Repeat steps 3-5 for the following markets:
        DESCRIPTION: • Money Line
        DESCRIPTION: • Handicap (Handicap in lads and Spread in Coral)
        DESCRIPTION: • Home Team Total Points
        DESCRIPTION: • Away Team Total Points
        """
        # covered in step 3

    def test_007_verify_bet_placement_for_single_and_quick_bet_for_the_below_markets_money_line_total_points_handicap_handicap_in_lads_and_spread_in_coral_home_team_total_points_away_team_total_points(
            self):
        """
        DESCRIPTION: Verify Bet Placement for Single and Quick Bet for the below markets
        DESCRIPTION: • Money Line
        DESCRIPTION: • Total Points
        DESCRIPTION: • Handicap (Handicap in lads and Spread in Coral)
        DESCRIPTION: • Home Team Total Points
        DESCRIPTION: • Away Team Total Points
        EXPECTED: Bet should be placed successfully
        """
        # covered in step 3
