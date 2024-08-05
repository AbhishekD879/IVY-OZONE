import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Events with specific markets cannot be created in Prod/Beta
@pytest.mark.desktop
@pytest.mark.market_switcher
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60089658_Verify_WDW_MT_on_Competitions_Tab_for_Golf(BaseDataLayerTest):
    """
    TR_ID: C60089658
    NAME: Verify 'WDW’ MT on Competitions Tab for Golf
    DESCRIPTION: This test case verifies the behaviour of  ‘WW market’ Template on Competitions Tab for Golf
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf -> 'Click on Competition Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |2 Ball Betting| - "2 Ball Betting"
    PRECONDITIONS: * |3 Ball Betting| - "3 Ball Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    preplay_list = []
    inplay_list = []

    event_markets = [('2_ball_betting',)]
    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.three_ball_betting,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        items = list(self.golf_tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        if header2:
            self.assertEqual(event.header2, header2,
                             msg=f'Actual fixture header "{event.header2}" does not equal to'
                                 f'Expected "{header2}"')
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
        DESCRIPTION: Navigate to Golf page
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='golf',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Golf sport')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        self.ob_config.add_golf_event_to_golf_all_golf(markets=self.event_markets)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.golf_config.category_id)
        self.navigate_to_page(name='sport/golf')
        self.site.wait_content_state('golf')
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed(timeout=10)
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • '2 Ball Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '3 Ball Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to '3 Ball Betting' in 'Market selector' Coral
        """
        self.__class__.golf_tab_content = self.site.competition_league.tab_content
        self.assertTrue(self.golf_tab_content.has_dropdown_market_selector(),
                        msg=' "Market selector" is not available for Golf Leauge')
        dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'"Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • 3 Ball Betting
        EXPECTED: • 2 Ball Betting
        """
        list_of_drop_down = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.assertTrue(list_of_drop_down, msg=f'"Market Selector" dropdown list not opened')
        actual_list = list(list_of_drop_down.keys())
        self.assertListEqual(actual_list, self.expected_market_selector_options,
                             msg=f'Actual list : "{actual_list}" is not same as '
                                 f'Expected list : "{self.expected_market_selector_options}"')

    def test_003_select_3_ball_betting_in_the_market_selector_dropdown_list(self,
                                                                            market_option=vec.siteserve.EXPECTED_MARKETS_NAMES.three_ball_betting,
                                                                            header1='1', header2='2', header3='3'):
        """
        DESCRIPTION: Select '3 Ball Betting' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        self.golf_tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            market_option).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=header1, header2=header2,
                                                          header3=header3)

    def test_004_verify_displaying_of_preplay_and_inplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay and Inplay events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • 3 Ball Betting (Preplay and Inplay market)
        EXPECTED: • 2 Ball Betting (Preplay and Inplay market)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        leagues = list(
            self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(leagues, msg='Leagues not found')

        for league in leagues:
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

    def test_005_verify_text_of_the_labels_for_3_ball_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '3 Ball Betting'
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' '2' '3' and corresponding Odds are present under Label 1 2 3.
        """
        self.golf_tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_market_selector_options[0]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='2',
                                                          header3='3')

    def test_006_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        # Covered in step 4

    def test_007_verify_ga_tracking_for_the_3_ball_betting(self,
                                                           market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.three_ball_betting):
        """
        DESCRIPTION: Verify GA Tracking for the '3 Ball Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "3 Ball Betting"
        EXPECTED: categoryID: "18"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        options = self.site.golf.tab_content.dropdown_market_selector.items_as_ordered_dict
        dropdown = self.site.contents.tab_content.dropdown_market_selector
        if not dropdown.is_expanded():
            dropdown.expand()
        options.get(market_name).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market_name)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market_name,
                             'categoryID': '18',
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_008_repeat_3_7_steps_for_the_below_market2_ball_betting_expect_step_5(self):
        """
        DESCRIPTION: Repeat 3-7 steps for the below market
        DESCRIPTION: 2 Ball Betting (Expect Step 5)
        EXPECTED: As per steps
        """
        self.test_003_select_3_ball_betting_in_the_market_selector_dropdown_list(
            market_option=vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting, header1='1', header2='TIE',
            header3='2')
        self.test_004_verify_displaying_of_preplay_and_inplay_events()
        self.test_006_verify_the_standard_match_event_details()
        self.test_007_verify_ga_tracking_for_the_3_ball_betting(
            market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting)

    def test_009_verify_text_of_the_labels_for_2_ball_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '2 Ball Betting'
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2.
        """
        self.golf_tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_market_selector_options[1]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='TIE',
                                                          header3='2')
