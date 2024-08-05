import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from voltron.utils.exceptions.voltron_exception import VoltronException
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089603_Verify_WDW_MT_on_Matches_Tab_for_Rugby_Union(BaseDataLayerTest):
    """
    TR_ID: C60089603
    NAME: Verify 'WDW’ MT on Matches Tab for Rugby Union
    DESCRIPTION: This test case verifies displaying of ‘WDW market’ Template is displaying by default for Rugby Union Landing Page on Matches Tab under Market Selector Dropdown
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Rugby Union  Landing page -> 'Click on Matches Tab'
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
    event_markets = [
        ('handicap_2_way',),
        ('total_match_points',)]

    @retry(stop=stop_after_attempt(4), retry=retry_if_exception_type((VoltronException, AttributeError)),
           wait=wait_fixed(wait=2),
           reraise=True)
    def verify_event_to_be_reflected(self):
        self.navigate_to_page("sport/rugby-union")
        self.site.wait_content_state(state_name='rugby-union', timeout=5)
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name).click()
        current_tab_name = self.site.competition_league.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_tab_name,
                         msg=f'Actual tab is "{current_tab_name}", instead of "{self.expected_tab_name}"')
        league = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
            self.section_name)
        if league:
            event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
            if event is None:
                raise VoltronException(f'"{self.eventID}" event not found')
        else:
            raise VoltronException(f'"{self.section_name}" league not found')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Rugby Union Landing page -> 'Matches' tab
        """
        self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.cms_config.verify_and_update_market_switcher_status(sport_name='rugbyunion', status=True)
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.rugby_union_config.category_id,
                                                       disp_sort_names='MR,WH,HL',
                                                       primary_markets='|Match Betting|,|Handicap 2-way|,'
                                                                       '|Total Match Points|')
        event_params = self.ob_config.add_rugby_union_event_to_rugby_union_all_rugby_union(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.section_name = f'{event_resp[0]["event"]["categoryCode"]} - {event_resp[0]["event"]["typeName"]}'.replace("_", " ").upper()
        self.__class__.expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                                   self.ob_config.rugby_union_config.category_id)
        self.verify_event_to_be_reflected()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{self.expected_tab_name}".')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
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

    def test_002_verify_displaying_for_preplay_events_for_match_result(self):
        """
        DESCRIPTION: Verify displaying for Preplay events for 'Match Result'
        EXPECTED: Only Preplay events are displayed
        """
        self.__class__.leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')

        for league in self.leagues:
            events = list(league.items_as_ordered_dict.values())
            self.assertTrue(events, msg='Events not found')
            for event in events:
                event_template = event.template
                odds = list(event_template.items_as_ordered_dict.values())
                for odd in odds:
                    self.assertTrue(odd.is_displayed(), msg=' "Odds" are not displayed.')
                self.assertFalse(event_template.is_live_now_event,
                                 msg=f'Event: "{event}" is an "In-Play" Event')
                self.assertTrue(event_template.event_name,
                                msg=' "Event Name" not displayed')
                self.assertTrue(event_template.event_time,
                                msg=' "Event time and date " are not displayed')
                if event_template.has_markets():
                    self._logger.info(f'{event_template.event_name} has more markets')
                else:
                    self._logger.info(f'{event_template.event_name} has no more markets')

    def test_003_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result'
        EXPECTED: • The events for the Match Betting market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels 'Home' 'Draw' and Away'and corresponding Odds are present under Labels  Home Draw Away
        """
        # corresponding Odds are present under Labels  Home Draw Away - verified in step 2
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

    def test_004_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link are present
        """
        # Covered in step 2
        # "watch signposting" cannot be automated as events are not live.

    def test_005_verify_ga_tracking_for_the_match_result(self):
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
        options = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Match Result')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': 'Match Result',
                             'categoryID': 31,
                             }
        self.compare_json_response(actual_response, expected_response)
