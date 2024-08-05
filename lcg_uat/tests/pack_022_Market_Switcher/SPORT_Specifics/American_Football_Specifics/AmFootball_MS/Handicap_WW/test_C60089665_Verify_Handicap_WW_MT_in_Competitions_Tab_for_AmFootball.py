import pytest
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089665_Verify_Handicap_WW_MT_in_Competitions_Tab_for_AmFootball(BaseDataLayerTest, BaseSportTest):
    """
    TR_ID: C60089665
    NAME: Verify ‘Handicap WW’ MT in Competitions Tab for Am.Football
    DESCRIPTION: This test case verifies behaviour of ‘Handicap WW market’ Template in Competition Tab
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the American Football -> 'Click on Competition Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system with different 'rawHandicapValue' (2,2.5,3 etc) using the following Market Template Names:
    PRECONDITIONS: * |Handicap 2-way (Handicap)| - "Handicap"
    PRECONDITIONS: * |Total Points (Over/Under)| - "Total Points"
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
    expected_low_sort_handicap = 2.5
    expected_same_sort_handicap = 1.5
    event_markets = [
        ('handicap_2_way_2', {'handicap': expected_low_sort_handicap, 'disp_order': -3}),
        ('handicap_2_way_3', {'handicap': 3.0, 'disp_order': 7}),
        ('total_points', {'handicap': expected_same_sort_handicap}),
        ('total_points_1', {'handicap': 2.0}), ]

    def verify_handicap_event_values(self, handicap_value, events):
        for event in reversed(events):
            event_template = event.template
            if event_template.event_name in self.event_names:
                handicap = event_template.items_names
                handicap_values = list(event_template.items_as_ordered_dict.values())
                for val in handicap_values:
                    self.assertEqual(val.handicap_value.text_color_value, vec.colors.HANDICAP_COLOR,
                                     msg=' Handicap Value is not in blue color')
                for value in handicap:
                    actual_value = value.split('\n')[0]
                    self.assertIn(str(handicap_value), actual_value,
                                  msg=f' "{handicap_value}" value is not displayed as per dispsort value ')
                self.__class__.event_found = True
                break
            else:
                self.__class__.event_found = False

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the American Football -> 'Click on Competition Tab'
        """
        self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='americanfootball', status=True)
        self.assertTrue(status, msg=f'The sport "americanfootball" is not checked')
        self.cms_config.verify_and_update_sport_config(self.ob_config.american_football_config.category_id,
                                                       disp_sort_names='HH,WH,MR,HL',
                                                       primary_markets='|Money Line|,|Handicap 2-way|,|60 Minute Betting|,|Total Points|')
        created_event = self.ob_config.add_american_football_event_to_autotest_handicap(markets=self.event_markets)
        self.__class__.event_names = [created_event.team1 + ' v ' + created_event.team2, created_event.team2 + ' v ' + created_event.team1]
        eventID = created_event.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0]).replace(' AUTO TEST', '', 1)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.american_football_config.category_id)
        self.navigate_to_page("sport/american-football")
        self.site.wait_content_state_changed(timeout=15)
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')
        if self.brand == 'bma':
            self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKET_SECTIONS.spread.title(),
                                            vec.siteserve.EXPECTED_MARKET_SECTIONS.total_points.title()]
        else:
            self.__class__.expected_list = [vec.siteserve.EXPECTED_MARKET_SECTIONS.handicap.title(),
                                            vec.siteserve.EXPECTED_MARKET_SECTIONS.total_points.title()]

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Handicap' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Handicap' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'handicap' in 'Market selector' Coral
        """
        has_market_selector = self.site.competition_league.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Rugby Leauge')

        self.__class__.dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click()
            self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click()
                self.site.wait_content_state_changed(timeout=3)
                self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        try:
            self.assertEqual(selected_value.upper(), self.expected_list[0].upper(),
                             msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                 f'Expected selected value: "{self.expected_list[0].upper()}"')
        except VoltronException:
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line,
                             msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.money_line}"')

    def test_002_clicktap_on_market_selector(self):
        """
        DESCRIPTION: Click/Tap on 'Market Selector'
        EXPECTED: Dropdown list appears with the following markets in the order listed below:
        EXPECTED: • Handicap (Handicap in Lads and Spread in Coral)
        EXPECTED: • Total Points
        """
        actual_list = list(self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict.keys())
        for market in self.expected_list:
            self.assertIn(market, actual_list,
                          msg=f'Actual market: "{market} is not in'
                              f'Expected market List: "{actual_list}"')

    def test_003_select_handicap_in_the_market_selector_dropdown_list(self, handicap_value=expected_low_sort_handicap, market=None):
        """
        DESCRIPTION: Select 'Handicap' in the 'Market Selector' dropdown list
        EXPECTED: • Events for the most favorable markets are shown
        EXPECTED: • Values on Fixture header are changed for each event according to selected market
        EXPECTED: • Number and order of 'Price/Odds' buttons are changed for each event according to selected market
        EXPECTED: Note: Based on the disporder and event time most favorable markets will display
        """
        market = market if market else self.expected_list[0]
        options = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get(market).click()
        self.site.wait_content_state_changed()

        leagues = self.site.competition_league.tab_content.accordions_list.items
        self.assertTrue(leagues, msg='Leagues not found')
        for league in reversed(leagues):
            self.__class__.events = list(league.items_as_ordered_dict.values())
            self.assertTrue(self.events, msg='Events not found')
            if self.device_type == 'mobile':
                if len(self.events) <= 2:
                    self.verify_handicap_event_values(handicap_value=handicap_value, events=self.events)
                    self.__class__.has_see_all_link = False
                else:
                    required_league = league.get_league(league_name=self.section_name)
                    self.__class__.has_see_all_link = required_league.has_see_all_link(timeout=10)
                    self.assertTrue(self.has_see_all_link, msg=f'*** SEE ALL link not present in the section %s' % self.section_name)
                    required_league.scroll_to()
                    required_league.see_all_link.click()
                    self.site.wait_content_state('CompetitionLeaguePage')
                    options = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
                    options.get(market).click()
                    sections = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
                    self.assertTrue(sections, msg='No list of available events are present on competition league page')
                    for section in sections:
                        self.__class__.events = list(section.items_as_ordered_dict.values())
                        self.assertTrue(self.events, msg='Events not found')
                        self.verify_handicap_event_values(handicap_value=handicap_value, events=self.events)
                        if self.event_found:
                            break
            else:
                self.verify_handicap_event_values(handicap_value=handicap_value, events=self.events)
            if self.event_found:
                break
        else:
            raise Exception("Required section not found")

    def test_004_verify_displaying_of_preplayinplay_or_both_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay/Inplay or both events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: Handicap/Spread (Inplay and Preplay)
        EXPECTED: Total Points (Inplay and Preplay)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        for event in self.events:
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
                                msg=' "Event time and day" not displayed')
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

    def test_005_verify_text_of_the_labels_for_handicap(self, label1="1", label2="2", market=None):
        """
        DESCRIPTION: Verify text of the labels for 'handicap'
        EXPECTED: • Values on Fixture header are displayed with Market Labels '1' & '2' and corresponding Odds are present under Labels 1 & 2.
        """
        if self.device_type == 'mobile':
            if self.has_see_all_link:
                self.site.back_button_click()
                market = market if market else self.expected_list[0]
                options = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
                options.get(market).click()
        leagues = list(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(leagues, msg='Leagues not found')
        fixture = leagues[0].fixture_header
        self.assertEqual(fixture.header1, label1,
                         msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "{label1}"')
        self.assertEqual(fixture.header3, label2,
                         msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "{label2}"')

    def test_006_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        # Covered in step 4

    def test_007_verify_ga_tracking_for_the_handicap(self, market=None):
        """
        DESCRIPTION: Verify GA Tracking for the 'Handicap'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Handicap"
        EXPECTED: categoryID: "1"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        market = market if market else self.expected_list[0]
        self.site.wait_content_state_changed()
        options = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        options.get(market).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market,
                             'categoryID': "1",
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_008_repeat_3_7_steps_for_the_below_markettotal_pointsexpect_step_5(self):
        """
        DESCRIPTION: Repeat 3-7 steps for the below market
        DESCRIPTION: Total Points(expect step 5)
        """
        self.__class__.dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        self.test_003_select_handicap_in_the_market_selector_dropdown_list(handicap_value=self.expected_same_sort_handicap, market=self.expected_list[1])
        self.test_004_verify_displaying_of_preplayinplay_or_both_events()
        self.test_006_verify_the_standard_match_event_details()
        self.test_007_verify_ga_tracking_for_the_handicap(market=self.expected_list[1])

    def test_009_verify_text_of_the_labels_for_total_points(self):
        """
        DESCRIPTION: Verify text of the labels for 'Total Points'
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Over' & 'Under' and corresponding Odds are present under Labels Over & Under.
        """
        self.test_005_verify_text_of_the_labels_for_handicap(label1=vec.sb.OVER.upper(), label2=vec.sb.UNDER.upper(), market=self.expected_list[1])
