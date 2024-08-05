import pytest
import voltron.environments.constants as vec
from time import sleep
from voltron.utils.helpers import normalize_name
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod -Events with specific markets cannot created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60089591_Verify_WW_MT_on_Matches_Tab_for_Baseball(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089591
    NAME: Verify 'WW’ MT on Matches Tab for Baseball
    DESCRIPTION: This test case verifies displaying of ‘WW market’ Template is displaying by default for Baseball Landing Page on Matches Tab under Market Selector Dropdown
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Baseball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: *|Money Line|- Money Line
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [('run_line',), ('total_runs',)]

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the Baseball Landing Page -> 'Click on Matches Tab'
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='baseball',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for Baseball sport')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        baseball_category_id = self.ob_config.baseball_config.category_id
        self.cms_config.verify_and_update_sport_config(sport_category_id=baseball_category_id,
                                                       disp_sort_names='HH,HL,WH',
                                                       primary_markets='|Money Line|,|Run Line|,|Total Runs|')
        event_params = self.ob_config.add_baseball_event_to_autotest_league(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/baseball')
        self.site.wait_content_state(state_name='Baseball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.baseball_config.category_id)
        current_tab_name = self.site.sports_page.tabs_menu.current
        if current_tab_name != expected_tab_name:
            self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
            current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' Coral
        """
        baseball_tab_content = self.site.baseball.tab_content
        self.assertTrue(baseball_tab_content.has_dropdown_market_selector(timeout=20),
                        msg='"Market Selector" drop-down is not displayed on Baseball landing page')
        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value
        self.assertEqual(baseball_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{baseball_tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
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

    def test_002_verify_text_of_the_labels_for_money_line(self):
        """
        DESCRIPTION: Verify text of the labels for 'Money Line'
        EXPECTED: • The events for the Money Line market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        usa_ahl_section = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict.get(
            self.section_name)
        self.assertTrue(usa_ahl_section, msg=f'Section "{self.section_name}" not found')
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        events = usa_ahl_section.items_as_ordered_dict.values()
        self.assertTrue(self.event, msg='Event for the "Money Line" market not shown')
        default_fixture_value = list(usa_ahl_section.fixture_header.items_as_ordered_dict.keys())
        self.assertEqual(default_fixture_value, ['1', '2'],
                         msg=f'Actual fixture header "{default_fixture_value}" does not '
                             f'equal to expected "{[1, 2]}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, 2,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "2"')
        name, odds_from_page = list(usa_ahl_section.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index], expected_odds_format="fraction")

    def test_003_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link is present in the landing page
        """
        self.assertIn(self.event.first_player, self.event_name,
                      msg=f'First player name "{self.event.first_player}" is not present in "{self.event_name}"')
        self.assertIn(self.event.second_player, self.event_name,
                      msg=f'Second player name "{self.event.second_player}" is not present in "{self.event_name}"')
        self.assertTrue(self.event.has_set_number(), msg=f'"Date/Time" not displayed for the event "{self.event_name}')
        self.assertTrue(self.event.has_markets(),
                        msg=f'More Markets link not displayed for the event "{self.event_name}')

    def test_004_verify_displaying_of_preplay_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay events
        EXPECTED: Only Preplay events should be displayed in Matches tab
        """
        sections = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in sections.items():
            if not section.is_expanded():
                section.expand()
            events_list = section.items_as_ordered_dict
            for event_name, event in events_list.items():
                self.assertFalse(event.is_live_now_event, msg='"LIVE" label present on the event "{event_name}"')

    def test_005_verify_ga_tracking_for_the_money_line(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Money Line'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Money Line"
        EXPECTED: categoryID: "5"
        EXPECTED: })
        """
        options = self.site.baseball.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get('Money Line').click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Money Line')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': 'Money Line',
                             'categoryID': 5,
                             }
        self.compare_json_response(actual_response, expected_response)
