import pytest
import voltron.environments.constants as vec
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
class Test_C60089604_Verify_WDW_MT_on_Competitions_Tab_for_Rugby_Union(BaseDataLayerTest):
    """
    TR_ID: C60089604
    NAME: Verify 'WDW’ MT on Competitions Tab for Rugby Union
    DESCRIPTION: This test case verifies displaying of ‘WDW market’ Template is displaying by default for Rugby Union Competition Landing page under Market Selector Dropdown
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Rugby Union-> 'Click on Competition Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Name:
    PRECONDITIONS: * |Match Betting(WDW)| - "Match Result"
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
    event_markets = [
        ('handicap_2_way',),
        ('total_match_points',)]

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Rugby Union Landing page -> 'Competitions' tab
        """
        self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.cms_config.verify_and_update_market_switcher_status(sport_name='rugbyunion', status=True)
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.rugby_union_config.category_id,
                                                       disp_sort_names='MR,WH,HL',
                                                       primary_markets='|Match Betting|,|Handicap 2-way|,'
                                                                       '|Total Match Points|')
        self.ob_config.add_rugby_union_event_to_rugby_union_all_rugby_union(markets=self.event_markets)

        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.rugby_union_config.category_id)
        self.navigate_to_page("sport/rugby-union")
        self.site.wait_content_state('rugby-union')
        self.site.contents.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the MS dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to (Matches/Outrights) on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' Coral
        """
        has_market_selector = self.site.contents.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Rugby Union')

        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
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
                self.site.wait_content_state_changed(timeout=20)
                self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')

        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result,
                         msg=f'Actual selected value: "{selected_value.upper()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result}"')

    def test_002_tap_on_match_result_from_the_market_selector_dropdown(self):
        """
        DESCRIPTION: Tap on 'Match Result' from the Market Selector dropdown
        EXPECTED: 'Match Result' should be selected
        """
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')

    def test_003_verify_displaying_of_preplayinplay_or_both_events(self):
        """
        DESCRIPTION: Verify displaying of Preplay/Inplay or both events
        EXPECTED: Events will be displayed as per the below conditions
        EXPECTED: Match Result (Preplay and Inplay)
        EXPECTED: Note:
        EXPECTED: If the market is preplay only preplay events will display
        EXPECTED: If the market is Inplay only Inplay events will display
        EXPECTED: If the market is both then both Preplay and Inplay events will display
        """
        self.__class__.leagues = list(
            self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict.values())
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

    def test_004_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result
        EXPECTED: • The events for the Match Result market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'Home' 'Draw' 'Away' and corresponding Odds are present under Labels Home Draw Away
        """
        # corresponding Odds are present under Labels  Home Draw Away - verified in step3
        fixture = self.leagues[0].fixture_header
        self.assertEqual(fixture.header1, vec.sb.HOME,
                         msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                             f'Expected "{vec.sb.HOME}"')
        self.assertEqual(fixture.header2, vec.sb.DRAW,
                         msg=f'Actual fixture header "{fixture.header2}" does not equal to'
                             f'Expected "{vec.sb.DRAW}"')
        self.assertEqual(fixture.header3, vec.sb.AWAY,
                         msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                             f'Expected "{vec.sb.AWAY}"')

    def test_005_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Preplay: Team names, date, time, watch signposting, "XX More" markets link are present
        EXPECTED: • Inplay: Team names, date,timer,scoreline,watch live/Live signposting, "XX More" markets link are present
        """
        # Covered in step 3

    def test_006_verify_ga_tracking_for_the_match_result(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Match Result'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Match Result"
        EXPECTED: categoryID: "31"
        EXPECTED: })
        """
        options = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Match Result')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': 'Match Result',
                             'categoryID': "31",
                             }
        self.compare_json_response(actual_response, expected_response)
