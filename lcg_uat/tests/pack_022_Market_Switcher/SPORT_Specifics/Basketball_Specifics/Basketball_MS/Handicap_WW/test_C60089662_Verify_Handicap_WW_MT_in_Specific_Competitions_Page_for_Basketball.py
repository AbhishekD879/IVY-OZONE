import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #cannot create events in beta/prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.slow
@vtest
class Test_C60089662_Verify_Handicap_WW_MT_in_Specific_Competitions_Page_for_Basketball(BaseDataLayerTest):
    """
    TR_ID: C60089662
    NAME: Verify ‘Handicap WW’ MT in Specific Competitions Page for Basketball
    DESCRIPTION: This test case verifies the behavior of Handicap WW market’ Template in Specific Competition Page
    PRECONDITIONS: Precondition:
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Basketball Landing Page -> Click on 'Specific Competition Page'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'HandicapValue' (2,2.5,3)etc  using the following Market Template Names:
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Home Team Total Points (Over/Under)| - "Home Team Total Points"
    PRECONDITIONS: * |Away Team Total Points (Over/Under)| - "Away Team Total Points"
    PRECONDITIONS: * |Half Total Points  (Over/Under)| - "Half Total Points"
    PRECONDITIONS: * |Quarter Total Points (Over/Under) | - "Quarter Total Points"
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

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1=None, header3=None):
        items = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())[0]
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
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state('basketball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.basketball_config.category_id)
        self.site.basketball.tabs_menu.click_button(expected_tab_name)
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')
        self.navigate_to_page(name='competitions/basketball/basketball-auto-test/basketball-autotest-total-points')
        self.device.refresh_page()

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Total Points' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Total Points' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Total Points' in 'Market selector' Coral
        """
        self.__class__.basketball_tab_content = self.site.competition_league.tab_content
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No Leagues present for basketball')
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.total_points
        self.assertTrue(self.basketball_tab_content.has_dropdown_market_selector(timeout=20),
                        msg='"Market Selector" drop-down is not displayed on basketball landing page')
        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value
        self.assertEqual(self.basketball_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{self.basketball_tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')
        self.__class__.dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        self.dropdown.click()
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing upwards')
        if self.brand == 'bma' and self.device_type == 'desktop':
            self.assertTrue(self.dropdown.has_up_arrow, msg='Market selector up arrow is not displayed')
            self.assertTrue(self.dropdown.has_down_arrow, msg='Market selector down arrow is not displayed')
        elif self.device_type == 'mobile' or self.brand == 'ladbrokes':
            # sleep provided as it takes some time to close the market switcher dropdown
            sleep(2)
            self.assertFalse(self.dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Total Points
        EXPECTED: • Handicap (handicap in Lads and Spread in coral)
        EXPECTED: • Home Team Total Points
        EXPECTED: • Away Team Total Points
        EXPECTED: • Half Total Points
        EXPECTED: • Quarter Total Points
        """
        if self.brand == 'bma':
            self.expected_list[1] = 'Spread'
        actual_list = list(self.basketball_tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        for item in self.expected_list:
            self.assertIn(item, actual_list, msg=f'Actual List: "{item} is not same as Expected List: '
                                                 f'"{actual_list}"')

    def test_003_select_total_points_in_the_market_selector_dropdown_list(self,
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
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
        self.site.wait_content_state_changed()
        self.__class__.leagues = list(
            self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
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

    def test_004_verify_displaying_of_preplayinplay_or_both_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay/Inplay or both events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • Total Points (Preplay and Inplay)
        EXPECTED: • Handicap (handicap in Lads and Spread in coral) (Preplay and Inplay)
        EXPECTED: • Home Team Total Points (Preplay and Inplay)
        EXPECTED: • Away Team Total Points (Preplay and Inplay)
        EXPECTED: • Half Total Points (Preplay and Inplay)
        EXPECTED: • Quarter Total Points (Preplay and Inplay)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
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

    def test_005_verify_text_of_the_labels_for_total_points(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points'
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels Over & Under.
        """
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='OVER', header3='UNDER')

    def test_006_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        # covered in step_004

    def test_007_verify_ga_tracking_for_the_games_total(self,
                                                        market=vec.siteserve.EXPECTED_MARKETS_NAMES.total_points.title()):
        """
        DESCRIPTION: Verify GA Tracking for the 'Games Total'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Total Points"
        EXPECTED: categoryID: "6"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.get(market).click()
        self.site.wait_content_state_changed()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market,
                             'categoryID': "6",
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_008_repeat_3_7_steps_for_the_below_markets_total_points_handicap_expect_step_5_home_team_total_points_away_team_total_points_half_total_points_quarter_total_points(
            self):
        """
        DESCRIPTION: Repeat 3-7 steps for the below markets
        DESCRIPTION: • Total Points
        DESCRIPTION: • Handicap (expect step 5)
        DESCRIPTION: • Home Team Total Points
        DESCRIPTION: • Away Team Total Points
        DESCRIPTION: • Half Total Points
        DESCRIPTION: • Quarter Total Points
        EXPECTED:
        """
        # for home team total points
        self.test_003_select_total_points_in_the_market_selector_dropdown_list(
            market=vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points.title())
        self.test_007_verify_ga_tracking_for_the_games_total(
            market=vec.siteserve.EXPECTED_MARKETS_NAMES.home_team_total_points.title())

        # for away team total points
        self.test_003_select_total_points_in_the_market_selector_dropdown_list(
            market=vec.siteserve.EXPECTED_MARKETS_NAMES.away_team_total_points.title())
        self.test_007_verify_ga_tracking_for_the_games_total(
            market=vec.siteserve.EXPECTED_MARKETS_NAMES.away_team_total_points.title())

        # for half total points
        self.test_003_select_total_points_in_the_market_selector_dropdown_list(
            market=vec.siteserve.EXPECTED_MARKETS_NAMES.half_total_points.title())
        self.test_007_verify_ga_tracking_for_the_games_total(
            market=vec.siteserve.EXPECTED_MARKETS_NAMES.half_total_points.title())

        # quarter total points
        self.test_003_select_total_points_in_the_market_selector_dropdown_list(
            market=vec.siteserve.EXPECTED_MARKETS_NAMES.quarter_total_points.title())
        self.test_007_verify_ga_tracking_for_the_games_total(
            market=vec.siteserve.EXPECTED_MARKETS_NAMES.quarter_total_points.title())

        # for handicap
        self.test_003_select_total_points_in_the_market_selector_dropdown_list(
            market=self.expected_list[1])
        self.test_007_verify_ga_tracking_for_the_games_total(
            market=self.expected_list[1])

    def test_009_verify_text_of_the_labels_for_handicap_handicap_in_lads_and_spread_in_coral(self):
        """
        DESCRIPTION: Verify text of the labels for 'Handicap' (Handicap in Lads and Spread in Coral)
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels 1 & 2.
        """
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=2, header1='1', header3='2')
