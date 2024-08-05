import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
# @pytest.mark.prod : # Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.market_switcher
@vtest
class Test_C60089574_Verify_WW_MT_on_Competitions_Tab_for_Darts(BaseDataLayerTest):
    """
    TR_ID: C60089574
    NAME: Verify 'WW’ MT on Competitions Tab for Darts
    DESCRIPTION: This test case verifies the behaviour of ‘WW market’ Template on Competition page for Darts
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Darts -> 'Click Competition Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting(WW)| - "Match Result"
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

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Dart Landing page -> 'Competition Tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='darts', status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Darts sport')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.darts.category_id,
                                                       disp_sort_names='MR,HL,WH,HH',
                                                       primary_markets='|Match Betting|,|Total 180s Over/Under|,'
                                                                       '|Most 180s|,|Leg Handicap|,|Leg Winner|,'
                                                                       '|Match Betting Head/Head|,|Match Handicap|')
        self.ob_config.add_autotest_darts_event_for_WW_type()
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.darts_config.category_id)

        self.navigate_to_page(name='sport/darts')
        self.site.wait_content_state(state_name='Darts')
        self.site.wait_content_state_changed(timeout=20)
        self.site.darts.tabs_menu.click_button(expected_tab_name)
        actual_tab = self.site.darts.tabs_menu.current
        self.assertEqual(actual_tab, expected_tab_name,
                         msg=f'"{actual_tab}" tab is not same as'
                             f'"{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' Coral
        """
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Darts')
        self.__class__.dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                self.site.wait_content_state_changed(timeout=20)
                self.assertFalse(self.dropdown.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            expected_selected_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()
        else:
            expected_selected_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        self.assertEqual(selected_value, expected_selected_value,
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{expected_selected_value}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Match Result
        """
        expected_market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        actual_list = list(self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        self.assertIn(expected_market_name, actual_list,
                      msg=f'Actual Market : "{expected_market_name} is not in'
                          f'Expected List: "{actual_list}"')

    def test_003_select_match_result_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Match Result' in the 'Market Selector' dropdown list
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        """
        self.__class__.leagues = list(
            self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')

        fixture = self.leagues[0].fixture_header
        self.assertEqual(fixture.header1, "1",
                         msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "1"')
        self.assertEqual(fixture.header3, "2",
                         msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "2"')

        events = self.leagues[0].items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')

        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, 2,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "2".')

    def test_004_verify_displaying_of_preplay_and_inplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay and Inplay events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: • Match Result (Preplay and Inplay market)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        # "watch signposting" cannot be automated as events are not live.
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

    def test_005_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result'
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        # Covered in step 3

    def test_006_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link are present
        """
        # Covered in step 4

    def test_007_verify_ga_tracking_for_the_match_result(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Match Result'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Match Result"
        EXPECTED: categoryID: "13"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        options = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.click()
        options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Match Result')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': 'Match Result',
                             'categoryID': "13",
                             }
        self.compare_json_response(actual_response, expected_response)
