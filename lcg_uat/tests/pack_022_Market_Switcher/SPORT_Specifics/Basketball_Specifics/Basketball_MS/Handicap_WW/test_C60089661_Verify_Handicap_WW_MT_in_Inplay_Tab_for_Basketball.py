import pytest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #cannot create events in beta/prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089661_Verify_Handicap_WW_MT_in_Inplay_Tab_for_Basketball(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089661
    NAME: Verify ‘Handicap WW’ MT in Inplay Tab for Basketball
    DESCRIPTION: This test case verifies displaying behaviour of ‘Handicap WW market’ Template in Inplay Tab
    PRECONDITIONS: Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to Basketball ->Inplay Tab and Inplay from (Desktop - Inplay tab(Sub header menu) -> Basketball) and in Mobile (Inplay (Sports ribbon menu) ->Basketball)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'rawHandicapValue' (2,2.5,3 etc) using the following Market Template Names:
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Current Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under)| - "Current Quarter Total Points"
    PRECONDITIONS: 2) Be aware that market switching using 'Market Selector' is applied only for events from the 'Live Now' section
    """
    keep_browser_open = True
    preplay_list = []
    inplay_list = []
    markets = [
        ('total_points_1', {'handicap': 2}),
        ('handicap_2_way',),
        ('handicap_2_way_2', {'handicap': 3}),
        ('home_team_total_points',),
        ('home_team_total_points_2', {'handicap': 3}),
        ('away_team_total_points',),
        ('away_team_total_points_2', {'handicap': 3}),
        ('half_total_points',),
        ('half_total_points_2', {'handicap': 3}),
        ('quarter_total_points',),
        ('quarter_total_points_2', {'handicap': 3})]

    expected_handicap_value_to_display = 5

    expected_list = [vec.siteserve.EXPECTED_MARKETS_NAMES.total_points,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.away_team_total_points,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.half_total_points,
                     vec.siteserve.EXPECTED_MARKETS_NAMES.quarter_total_points,
                     ]

    live_now_switcher = vec.inplay.LIVE_NOW_SWITCHER.upper()

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None):
        items = list(self.site.inplay.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        self.assertEqual(event.header3, header3,
                         msg=f'Actual fixture header "{event.header2}" does not equal to'
                             f'Expected "{header3}"')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate to basketball page
        EXPECTED: Event is successfully created
        """
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
        event = self.ob_config.add_basketball_event_to_basketball_autotest_handicap(markets=self.markets)
        self.__class__.event_name = event.team1 + ' v ' + event.team2
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.total_points
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state('basketball')
        expected_tab = self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play
        self.site.basketball.tabs_menu.click_button(self.expected_sport_tabs.in_play)
        expected_tab_name = self.get_sport_tab_name(expected_tab, self.ob_config.basketball_config.category_id)
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: * The 'Market Selector' is displayed below the 'Live Now (n)' header
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change' button is placed next to 'Main Markets' name with the chevron pointing downwards
        EXPECTED: Desktop:
        EXPECTED: * The 'Market Selector' is displayed below the 'Live Now' (n) switcher
        EXPECTED: * 'Main Markets' option is selected by default
        EXPECTED: * 'Change Market' button is placed next to 'Main Markets' name with the chevron pointing downwards (for Ladbrokes)
        EXPECTED: * 'Market' title is placed before 'Main Markets' name and the chevron pointing downwards is placed at the right side of dropdown (for Coral)
        EXPECTED: Note: If 'Money Line' market is not present then event will display as outright market
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(self.live_now_switcher)
            actual_btn = self.site.inplay.tab_content.grouping_buttons.current
            self.assertEqual(actual_btn, self.live_now_switcher, msg=f'"{self.live_now_switcher}" is not selected')
        self.__class__.basketball_tab_content = self.site.inplay.tab_content
        self.assertTrue(self.basketball_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on basketball landing page')
        if self.device_type == 'mobile':
            actual = self.site.inplay.tab_content.dropdown_market_selector.value
        elif self.brand == 'bma' and self.device_type == 'desktop':
            actual = self.site.basketball.tab_content.dropdown_market_selector.value
        else:
            actual = self.site.inplay.tab_content.selected_market
        try:
            self.assertEqual(actual, self.market_selector_default_value,
                             msg=f'Selected market selector "{actual}" is not the same as '
                             f'expected "{self.market_selector_default_value}"')
        except Exception as e:
            self.assertEqual(actual.rstrip(), vec.siteserve.EXPECTED_MARKETS_NAMES.main_markets,
                             msg=f'Selected market selector "{actual}" is not the same as '
                                 f'expected "{vec.siteserve.EXPECTED_MARKETS_NAMES.main_markets}"')
        self.__class__.dropdown = self.site.basketball.tab_content.dropdown_market_selector
        if self.device_type == 'desktop':
            if self.brand == "bma":
                self.assertFalse(self.dropdown.is_expanded(),
                                 msg='chevron (pointing down) arrow not displayed')
            else:
                self.assertTrue(self.dropdown.change_market_button, msg=f'"Change Market" button is not displayed')
                self.assertFalse(self.dropdown.is_expanded(),
                                 msg='chevron (pointing down) arrow not displayed')
        else:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change Market" button is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(),
                             msg='chevron (pointing down) arrow not displayed')

    def test_002_select_total_points_in_the_market_selector_dropdown_list(self,
                                                                          market=vec.siteserve.EXPECTED_MARKETS_NAMES.total_points.title()):
        """
        DESCRIPTION: Select 'Total Points' in the 'Market Selector' dropdown list
        EXPECTED: • Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        EXPECTED: Note- When multiple markets are created for the any handicap market , then user should be able to see one market for each market type in landing page and in EDP page whole list will be displayed with all the different handicap values for that particular market.
        """
        if self.brand == "bma":
            if self.device_type == "desktop":
                self.site.basketball.tab_content.dropdown_market_selector.select_value_by_text(market)
            else:
                self.site.inplay.tab_content.dropdown_market_selector.items_as_ordered_dict.get(
                    market).click()
        else:
            options = self.site.inplay.tab_content.dropdown_market_selector.items_as_ordered_dict
            if not self.dropdown.is_expanded():
                self.dropdown.expand()
            options.get(market).click()

        self.__class__.leagues = list(
            self.site.basketball.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')
        for league in self.leagues:
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                if self.event_name == event_template.event_name:
                    handicap = event_template.items_names
                    handicap_values = list(event_template.items_as_ordered_dict.values())
                    for val in handicap_values:
                        self.assertEqual(val.handicap_value.text_color_value, vec.colors.HANDICAP_COLOR,
                                         msg=' "Handicap Value" is not in blue color')
                    if market in ['Handicap', 'Spread']:
                        odd1, odd2 = handicap[0].split('\n')[0], handicap[1].split('\n')[0]
                        self.assertGreater(float(odd1), 0,
                                           msg=f'Odd1 "{odd1}" is not positive for Handicap market as per dispsort value')
                        self.assertLess(float(odd2), 0,
                                        msg=f'Odd2 "{odd2}" is not negative for Handicap market as per dispsort value')
                    else:
                        odd1, odd2 = handicap[0].split('\n')[0], handicap[1].split('\n')[0]
                        self.assertGreater(float(odd1), 0,
                                           msg=f'Odd1 "{odd1}" is not positive for Handicap market as per dispsort value')
                        self.assertGreater(float(odd2), 0,
                                           msg=f'Odd2 "{odd2}" is not positive for Handicap market as per dispsort value')

    def test_003_verify_text_of_the_labels_for_total_points(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points'
        EXPECTED: • The events for the Total Points market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under.
        """
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='OVER', header3='UNDER')

    def test_004_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        self.__class__.leagues = list(
            self.basketball_tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')

        for league in self.leagues:
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                is_live = event_template.is_live_now_event
                self.inplay_list.append(is_live) if is_live else self.preplay_list.append(is_live)
                odds = list(event_template.items_as_ordered_dict.values())
                for odd in odds:
                    self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                self.assertTrue(event_template.event_name,
                                msg=' "Event Name" not displayed')
                if is_live:
                    self._logger.info(f'{event_template.event_name} is live event')
                else:
                    self.assertTrue(event_template.event_time,
                                    msg=' "Event time" not displayed')
                if event_template.has_markets():
                    self._logger.info(f'{event_template.event_name} has more markets')
                else:
                    self._logger.info(f'{event_template.event_name} has no more markets')

        if len(self.inplay_list) > 0 and len(self.preplay_list) == 0:
            self._logger.info(msg=f'Only "In-Play" events are available ')
        elif len(self.inplay_list) == 0 and len(self.preplay_list) > 0:
            self._logger.info(msg=f'Only "Pre-Play" events are available ')
        else:
            self._logger.info(msg=f'Both "In-Play" and "Pre-play" events are available ')

    def test_005_verify_displaying_of_inplay_events(self):
        """
        DESCRIPTION: Verify displaying of Inplay events
        EXPECTED: Only Inplay events should be displayed
        """
        # covered in step_004
