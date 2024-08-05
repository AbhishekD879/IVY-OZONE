import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.desktop
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod : # Events with specific markets cannot created in Prod/Beta
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.market_switcher
@vtest
class Test_C60089631_Verify_pre_selected_WDW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Darts(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089631
    NAME: Verify pre selected ‘WDW’ MT is saved when switching b/w T/T/F on Matches Tab for Darts
    DESCRIPTION: This test case verifies that previously selected ‘WDW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Darts Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Darts Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting(WDW)| - "Match Result"
    PRECONDITIONS: * |Most 180s (WDW)| - "Most 180s"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    event_markets = [('most_180s',)]

    def verify_market_event_fixture(self, eventID=None, section_name=None, expected_tab=None, market=None):
        self.assertEqual(self.site.darts.date_tab.current_date_tab, expected_tab,
                         msg=f'Current active date tab: "{self.site.darts.date_tab.current_date_tab}" '
                             f'expected: "{expected_tab}"')
        market_selector_default_value = market.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else market
        self.assertEqual(self.site.darts.tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{self.site.darts.tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')

        section = self.site.darts.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
        self.assertTrue(section, msg=f'Section "{section_name}" not found')
        event = self.get_event_from_league(event_id=eventID, section_name=section_name)
        events = section.items_as_ordered_dict.values()
        self.assertTrue(event, msg=f'Event for the "{market}" market not shown')
        default_fixture_value = list(section.fixture_header.items_as_ordered_dict.keys())
        self.assertEqual(default_fixture_value, ['1', 'TIE', '2'],
                         msg=f'Actual fixture header "{default_fixture_value}" does not '
                             f'equal to expected "1, TIE, 2"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, 3,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "3"')
        name, odds_from_page = list(section.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index], expected_odds_format="fraction")

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Darts event with required markets
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='darts',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for Darts sport')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.darts.category_id,
                                                       disp_sort_names='MR,HL,WH,HH',
                                                       primary_markets='|Match Betting|,|Total 180s Over/Under|,'
                                                                       '|Most 180s|,|Leg Handicap|,|Leg Winner|,'
                                                                       '|Match Betting Head/Head|,|Match Handicap|')
        # Today tab event creation
        event_params = self.ob_config.add_darts_event_to_darts_all_darts(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        self.__class__.section_name = 'DARTS - CHAMPIONSHIP LEAGUE'

        # Tomorrow Tab Event creation
        tomorrow = self.get_date_time_formatted_string(days=1)
        event_params_tomorrow = self.ob_config.add_darts_event_to_darts_all_darts(markets=self.event_markets,
                                                                                  start_time=tomorrow)
        self.__class__.eventID_tomorrow = event_params_tomorrow.event_id

        # Future Tab Event creation
        future = self.get_date_time_formatted_string(days=7)
        event_params_future = self.ob_config.add_darts_event_to_darts_all_darts(markets=self.event_markets,
                                                                                start_time=future)
        self.__class__.eventID_future = event_params_future.event_id
        self.navigate_to_page(name='sport/darts')
        self.site.wait_content_state(state_name='Darts')
        current_tab_name = self.site.darts.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Expected tab: "{self.expected_sport_tabs.matches}", Actual Tab: "{current_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Darts')
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if self.brand == 'bma':
            self.dropdown.click_item(market_name)
            self.site.wait_content_state_changed()
            self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
            self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
        else:
            self.dropdown.click_item(market_name)
            self.site.wait_content_state_changed()
            self.assertFalse(self.dropdown.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')

    def test_002_verify_text_of_the_labels_for_match_results(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default):
        """
        DESCRIPTION: Verify text of the labels for 'Match Results'
        EXPECTED: • The events for the Match Result market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 & 2.
        """
        self.verify_market_event_fixture(eventID=self.eventID, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.today,
                                         market=market_name)

    def test_003_switch_to_the_tomorrow_tab(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Match Result)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2.
        EXPECTED: Note: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        self.site.darts.date_tab.tomorrow.click()
        self.verify_market_event_fixture(eventID=self.eventID_tomorrow, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.tomorrow,
                                         market=market_name)

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        """
        # Covered in step 3

    def test_005_repeat_steps_34_for_the_future_tab(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default):
        """
        DESCRIPTION: Repeat steps 3,4 for the 'Future' tab
        """
        self.site.darts.date_tab.future.click()
        self.verify_market_event_fixture(eventID=self.eventID_future, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.future,
                                         market=market_name)

    def test_006_switch_back_to_today_tab(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' Tie '2' and corresponding Odds are present under Label 1 Tie 2
        """
        self.site.darts.date_tab.today.click()
        self.verify_market_event_fixture(eventID=self.eventID, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.today,
                                         market=market_name)

    def test_007_verify_ga_tracking_for_the_match_result(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default):
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
        """
        options = self.site.darts.tab_content.dropdown_market_selector.items_as_ordered_dict
        self.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get(market_name).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market_name)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market_name,
                             'categoryID': 13,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_008_repeat_steps_2_7_for_the_below_marketmost_180s(self):
        """
        DESCRIPTION: Repeat steps 2-7 for the below market
        DESCRIPTION: Most 180s
        """
        self.test_001_verify_displaying_of_the_market_selector(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s)
        self.test_002_verify_text_of_the_labels_for_match_results(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s)
        self.test_003_switch_to_the_tomorrow_tab(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s)
        self.test_005_repeat_steps_34_for_the_future_tab(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s)
        self.test_006_switch_back_to_today_tab(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s)
        self.test_007_verify_ga_tracking_for_the_match_result(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s)
