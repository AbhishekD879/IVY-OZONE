import pytest
import voltron.environments.constants as vec
from time import sleep
from voltron.utils.helpers import normalize_name
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089600_Verify_WDW_MT_on_Matches_Tab_for_AmFootball(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089600
    NAME: Verify 'WDW’ MT on Matches Tab for Am.Football
    DESCRIPTION: This test case verifies displaying of ‘WDW market’ Template is displaying by default for American Football Landing Page on Matches Tab under Market Selector Dropdown
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the American Football Landing page -> 'Click on Matches Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Name:
    PRECONDITIONS: * |60 Minute Betting(WDW)| - "60 Minute Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [
        ('60_minute_betting',),
        ('handicap_2_way',),
        ('total_points',)
    ]

    def verify_chevron_display(self):
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            sleep(2)
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                sleep(2)
                self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Dart Landing page -> 'Matches tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='americanfootball', status=True)
        self.assertTrue(status, msg=f'The sport "americanfootball" is not checked')
        all_sport_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sport_status, msg='"All Sport" Market switcher is disabled')
        self.cms_config.verify_and_update_sport_config(self.ob_config.backend.ti.american_football.category_id,
                                                       disp_sort_names='HH,WH,MR,HL',
                                                       primary_markets='|Money Line|,|Handicap 2-way|,|60 Minute Betting|,|Total Points|')
        event_params = self.ob_config.add_american_football_event_to_autotest_league(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0]).replace(' AUTO TEST', '', 1)
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.sixty_minute_betting
        self.navigate_to_page(name='sport/american-football')
        self.site.wait_content_state(state_name='american-football')
        current_tab_name = self.site.sports_page.tabs_menu.current
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
        EXPECTED: • '60 Minute Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '60 Minute Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to '60 Minute Betting' in 'Market selector' Coral
        """
        has_market_selector = self.site.american_football.tab_content.has_dropdown_market_selector(timeout=20)
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for american football')
        self.verify_chevron_display()
        market_selector = self.site.sports_page.tab_content.dropdown_market_selector
        options = market_selector.items_as_ordered_dict
        if not market_selector.is_expanded():
            market_selector.expand()
        options.get(self.market_selector_default_value).click()
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), self.market_selector_default_value.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{self.market_selector_default_value}"')

    def test_002_verify_displaying_for_preplay_events_for_60_minute_betting(self):
        """
        DESCRIPTION: Verify displaying for Preplay events for '60 Minute Betting'
        EXPECTED: Only Preplay events should display
        """
        sections = self.site.american_football.tab_content.accordions_list.items_as_ordered_dict
        for section_name, section in sections.items():
            if not section.is_expanded():
                section.expand()
            events_list = section.items_as_ordered_dict
            for event_name, event in events_list.items():
                self.assertFalse(event.is_live_now_event, msg='"LIVE" label present on the event "{event_name}"')

    def test_003_verify_text_of_the_labels_for_60_minute_betting(self):
        """
        DESCRIPTION: Verify text of the labels for '60 Minute Betting'
        EXPECTED: • The events for the 60 Minute Betting market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2
        """
        self.site.contents.scroll_to_top()
        usa_ahl_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(self.section_name)
        self.assertTrue(usa_ahl_section, msg=f'Section "{self.section_name}" not found')
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        events = usa_ahl_section.items_as_ordered_dict.values()
        self.assertTrue(self.event, msg='Event for the "Money Line" market not shown')
        default_fixture_value = list(usa_ahl_section.fixture_header.items_as_ordered_dict.keys())
        self.assertEqual(default_fixture_value, ['1', 'TIE', '2'],
                         msg=f'Actual fixture header "{default_fixture_value}" does not '
                             f'equal to expected "1, TIE, 2"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, 3,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "3"')
        name, odds_from_page = list(usa_ahl_section.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index], expected_odds_format="fraction")

    def test_004_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link are present
        """
        self.assertIn(self.event.first_player, self.event_name,
                      msg=f'First player name "{self.event.first_player}" is not present in "{self.event_name}"')
        self.assertIn(self.event.second_player, self.event_name,
                      msg=f'Second player name "{self.event.second_player}" is not present in "{self.event_name}"')
        self.assertTrue(self.event.has_set_number(), msg=f'"Date/Time" not displayed for the event "{self.event_name}')
        self.assertTrue(self.event.has_markets(),
                        msg=f'More Markets link not displayed for the event "{self.event_name}')

    def test_005_verify_ga_tracking_for_the_60_minute_betting(self):
        """
        DESCRIPTION: Verify GA Tracking for the '60 Minute Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "60 Minute Betting"
        EXPECTED: categoryID: "1"
        EXPECTED: })
        """
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        options = self.site.american_football.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not dropdown.is_expanded():
            dropdown.expand()
        options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.money_line).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='60 Minute Betting')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': '60 Minute Betting',
                             'categoryID': 1,
                             }
        self.compare_json_response(actual_response, expected_response)
