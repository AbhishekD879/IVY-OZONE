import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089649_Verify_WDW_MT_on_Matches_Tab_for_Ice_Hockey(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089649
    NAME: Verify 'WDW’ MT on Matches Tab for Ice Hockey
    DESCRIPTION: This test case verifies displaying of ‘WDW market’ Template is displaying in Matches Tab under Market Selector Dropdown for Ice Hockey
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Money Line|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH
    PRECONDITIONS: 1.	Load the app
    PRECONDITIONS: 2.	Go to the Ice Hockey Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: *|60 Minutes Betting (WDW)|- "60 Minutes Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [('sixty_minutes_betting',)]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Ice Hockey event with required markets
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='icehockey',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='"Market Switcher" is disabled for IceHockey sport')
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(
            sport_category_id=self.ob_config.backend.ti.ice_hockey.category_id,
            disp_sort_names='HH,WH,MR,HL',
            primary_markets='|Money Line|,|Total Goals 2-way|,|Puck Line|,|60 Minutes Betting|')
        event_params = self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        wait_for_result(lambda: self.site.ice_hockey.tabs_menu.current is not None,
                        name=f'Matches Tab is displayed',
                        timeout=15)
        current_tab_name = self.site.ice_hockey.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Expected tab: "{self.expected_sport_tabs.matches}", Actual Tab: "{current_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • '60 Minutes Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '60 Minutes Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to '60 Minutes Betting' in 'Market selector' Coral
        """
        self.__class__.ice_hockey_tab_content = self.site.ice_hockey.tab_content
        wait_for_result(lambda: self.ice_hockey_tab_content.has_dropdown_market_selector(),
                        name=f'Matches Tab is displayed',
                        timeout=30)
        self.assertTrue(self.ice_hockey_tab_content.has_dropdown_market_selector(timeout=20),
                        msg='"Market Selector" drop-down is not displayed on IceHockey landing page')
        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value
        self.assertEqual(self.ice_hockey_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{self.ice_hockey_tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
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

    def test_002_verify_text_of_the_labels_for_60_minutes_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '60 Minutes Betting'
        EXPECTED: • The events for the '60 Minutes Betting' market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' , 'Tie' & '2' and corresponding Odds are present under Label 1 , tie and  2.
        """
        expected_market = '60 MINUTES BETTING' if self.brand == 'ladbrokes' and self.device_type == 'desktop' else '60 Minutes Betting'
        self.ice_hockey_tab_content.dropdown_market_selector.items_as_ordered_dict.get('60 Minutes Betting').click()
        result = wait_for_result(lambda: self.ice_hockey_tab_content.dropdown_market_selector.
                                 selected_market_selector_item == expected_market,
                                 name='"60 Minutes Betting" market to be selected',
                                 timeout=10)
        self.assertTrue(result, msg='Selected market is not "60 Minutes Betting"')
        usa_ahl_section = self.site.ice_hockey.tab_content.accordions_list.items_as_ordered_dict.get(
            self.section_name)
        self.assertTrue(usa_ahl_section, msg=f'Section "{self.section_name}" not found')
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        events = usa_ahl_section.items_as_ordered_dict.values()
        self.assertTrue(self.event, msg='Event for the "Money Line" market not shown')
        default_fixture_value = list(usa_ahl_section.fixture_header.items_as_ordered_dict.keys())
        expected_format = ['1', 'TIE', '2']
        self.assertEqual(default_fixture_value, expected_format,
                         msg=f'Actual fixture header "{default_fixture_value}" does not '
                             f'equal to expected "{expected_format}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, 3,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "3"')

    def test_003_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link are present
        """
        # "watch signposting" cannot be done as events are not live.
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
        dropdown = self.site.contents.tab_content.dropdown_market_selector
        if dropdown.is_expanded():
            dropdown.click()
            wait_for_result(lambda: dropdown.is_expanded() is not True,
                            name=f'Market switcher expanded/collapsed',
                            timeout=5)
        sections = self.site.ice_hockey.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in sections.items():
            if not section.is_expanded():
                section.expand()
            events_list = section.items_as_ordered_dict
            for event_name, event in events_list.items():
                self.assertFalse(event.is_live_now_event, msg='"LIVE" label present on the event "{event_name}"')

    def test_005_verify_ga_tracking_for_the_60_minutes_betting(self):
        """
        DESCRIPTION: Verify GA Tracking for the '60 Minutes Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "60 Minutes Betting"
        EXPECTED: categoryID: "22"
        EXPECTED: })
        """
        options = self.ice_hockey_tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get('60 Minutes Betting').click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='60 Minutes Betting')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': '60 Minutes Betting',
                             'categoryID': 22,
                             }
        self.compare_json_response(actual_response, expected_response)
