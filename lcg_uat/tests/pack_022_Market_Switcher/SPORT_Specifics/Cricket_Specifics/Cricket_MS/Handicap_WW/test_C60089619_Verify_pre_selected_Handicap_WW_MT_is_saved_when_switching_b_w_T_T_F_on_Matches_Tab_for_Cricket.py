import pytest
import tests
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.environments import constants as vec
from voltron.utils.exceptions.siteserve_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089619_Verify_pre_selected_Handicap_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Cricket(BaseDataLayerTest):
    """
    TR_ID: C60089619
    NAME: Verify pre selected ‘Handicap WW’ MT is saved when switching b/w T/T/F on Matches Tab for Cricket
    DESCRIPTION: This test case verifies that previously selected ‘Handicap WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Cricket Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Cricket Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'rawHandicapValue' (2,2.5,3 etc) using the following Market Template Names:
    PRECONDITIONS: * |Total Sixes (Over/Under)| - "Total Sixes"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    markets = [
        ('total_sixes_2', {'handicap': 2}),
        ('total_sixes_3', {'handicap': 3})
    ]
    expected_handicap_value_to_display = 5
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate to american football page
        EXPECTED: Event is successfully created
        """
        if self.brand == 'bma':
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.upper(),
                                        vec.sb.TABS_NAME_FUTURE.upper(),
                                        vec.sb.TABS_NAME_TODAY.upper()]
        else:
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.title(),
                                        vec.sb.TABS_NAME_FUTURE.title(),
                                        vec.sb.TABS_NAME_TODAY.title()]
        self.cms_config.verify_and_update_market_switcher_status(sport_name='cricket', status=True)
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(self.ob_config.backend.ti.cricket.category_id,
                                                       disp_sort_names='MR,HH,WH,HL',
                                                       primary_markets='|Match Betting|,|Match Betting Head/Head|,|Total Sixes|,|Team Runs (Main)|,|Next Over Runs (Main)|,|Runs At Fall Of Next Wicket|')
        event = self.ob_config.add_autotest_cricket_event_with_total_sixes(markets=self.markets, disp_order=2)
        self.__class__.event_name = event.team1 + ' v ' + event.team2
        self.navigate_to_page(name='sport/cricket')
        self.site.wait_content_state('cricket')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.cricket_config.category_id)
        self.site.cricket.tabs_menu.click_button(expected_tab_name)
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Total Sixes' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Total Sixes' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Total Sixes' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Cricket')
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if self.brand == 'bma':
            self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
            self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
        else:
            self.dropdown.click()
            self.site.wait_content_state_changed(5)
            self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes}"')
        except VoltronException:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')

    def test_002_select_total_sixes_in_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Select 'Total Sixes' in the 'Market Selector' dropdown list
        EXPECTED: • Events for the most favorable market is shown based on the below condition:
        EXPECTED: a) Based on the disporder in OB for Market(- to + )value will get the priority.
        EXPECTED: b) When the display order is same for all the markets, then the market with least handicap value markets (with odds) will be displayed.
        EXPECTED: • Values(Labels) on fixture header are changed for each event according to selected market.
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: a) Handicap value will be displayed in blue color above the odds value in the same box
        EXPECTED: b) If it is a handicap market template then one positive and one negative handicap value will be displayed above the odds.
        EXPECTED: c) If it is an Over/Under market template then both handicap values will be positive which will be displayed above the odds.
        """
        self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict.get(vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes).click()
        self.__class__.leagues = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
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
                    for value in handicap:
                        actual_value = value.split('\n')[0]
                        self.assertIn(str(self.expected_handicap_value_to_display), actual_value,
                                      msg=f'{self.expected_handicap_value_to_display} value is not displayed as per dispsort value ')
                        self.assertNotIn('-', actual_value,
                                         msg=' "Negative value" present in button')

    def test_003_verify_text_of_the_labels_for_total_sixes_in_matches_tab(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Sixes' in Matches Tab
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under.
        """
        if len(self.leagues) > 0:
            fixture = self.leagues[0].fixture_header
            self.assertEqual(fixture.header1, vec.sb.OVER.upper(),
                             msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                                 f'Expected "{vec.sb.OVER.upper()}"')
            self.assertEqual(fixture.header3, vec.sb.UNDER.upper(),
                             msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                                 f'Expected "{vec.sb.UNDER.upper()}"')
            for league in self.leagues:
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    self.assertFalse(event.template.is_live_now_event,
                                     msg=f'Event: "{event}" is an "In-Play" Event')
        else:
            no_events = self.site.contents.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def test_004_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed
        """
        if len(self.leagues) > 0:
            for league in self.leagues:
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    self.assertFalse(event.template.is_live_now_event,
                                     msg=f'Event: "{event}" is an "In-Play" Event')
        else:
            no_events = self.site.contents.tab_content.has_no_events_label()
            self.assertTrue(no_events, msg=' "No Events Found" msg not displayed')

    def test_005_verify_ga_tracking_for_the_total_sixes(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Total Sixes'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Total Sixes"
        EXPECTED: categoryID: "10"
        EXPECTED: })
        """
        if len(self.leagues) > 0:
            options = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
            if not self.dropdown.is_expanded():
                self.dropdown.expand()
            options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes).click()
            actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Total Sixes')
            expected_response = {'event': 'trackEvent',
                                 'eventCategory': 'market selector',
                                 'eventAction': 'change market',
                                 'eventLabel': 'Total Sixes',
                                 'categoryID': 10,
                                 }
            self.compare_json_response(actual_response, expected_response)
        self.site.contents.tab_content.grouping_buttons.items_as_ordered_dict.get(self.days_list[0]).click()

    def test_006_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Total Sixes)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'Over' & 'Under' and corresponding Odds are present under Label Over & Under.
        EXPECTED: Note
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/tomorrow/Future)
        """
        self.site.wait_content_state_changed()
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.leagues = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        if has_market_selector:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.total_sixes}"')
            self.test_003_verify_text_of_the_labels_for_total_sixes_in_matches_tab()
        else:
            self._logger.info(msg=' "Market Selector" is not displayed in "tomorrow".')
        self.test_004_verify_displaying_of_preplay_events()

    def test_007_repeat_step3(self):
        """
        DESCRIPTION: Repeat step3
        """
        # covered in step_006

    def test_008_repeat_steps_67_for_future_tab(self):
        """
        DESCRIPTION: Repeat Steps 6,7 for Future tab
        """
        self.site.contents.tab_content.grouping_buttons.items_as_ordered_dict.get(self.days_list[1]).click()
        self.test_006_switch_to_the_tomorrow_tab()

    def test_009_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Label Over & Under
        """
        self.site.contents.tab_content.grouping_buttons.items_as_ordered_dict.get(self.days_list[2]).click()
        self.test_006_switch_to_the_tomorrow_tab()
