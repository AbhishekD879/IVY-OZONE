import pytest
import voltron.environments.constants as vec
from time import sleep
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
class Test_C60089630_Verify_WDW_MT_on_Matches_Tab_for_Darts(BaseDataLayerTest):
    """
    TR_ID: C60089630
    NAME: Verify 'WDW’ MT on Matches Tab for Darts
    DESCRIPTION: This test case verifies the behaviour of ‘WDW market’ Template on Matches Tab for Darts
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Darts -> 'Click on Matches Tab'
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
    market_selector_options = [
        ('match_handicap',),
        ('most_180s',)]

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Dart Landing page -> 'Matches tab
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
        self.ob_config.add_darts_event_to_darts_all_darts(markets=self.market_selector_options)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.darts_config.category_id)

        self.navigate_to_page(name='sport/darts')
        self.site.wait_content_state(state_name='Darts')
        self.site.darts.tabs_menu.click_button(expected_tab_name)
        self.assertEqual(self.site.darts.tabs_menu.current, expected_tab_name,
                         msg=f'"{expected_tab_name}" tab is not active')

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default):
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
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Darts')
        self.__class__.dropdown = self.site.contents.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(self.dropdown.change_button, msg=f'"Change button" is not displayed')
            self.dropdown.click_item(market_name)
            self.assertFalse(self.dropdown.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.dropdown.click_item(market_name)
                sleep(1)
                self.assertTrue(self.dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(self.dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.dropdown.click_item(market_name)
                sleep(1)
                self.assertFalse(self.dropdown.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.assertEqual(selected_value, market_name.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{market_name.upper()}"')
        else:
            self.assertEqual(selected_value, market_name,
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{market_name}"')

    def test_002_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result'
        EXPECTED: • The events for the Match Result market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2.
        """
        self.__class__.leagues = list(self.site.contents.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(self.leagues, msg='Leagues not found')

        fixture = self.leagues[0].fixture_header
        self.assertEqual(fixture.header1, '1',
                         msg=f'Actual fixture header "{1}" does not equal to'
                             f'Expected "{1}"')
        self.assertEqual(fixture.header2, 'TIE',
                         msg=f'Actual fixture header "TIE" does not equal to'
                             f'Expected "TIE"')
        self.assertEqual(fixture.header3, '2',
                         msg=f'Actual fixture header "{2}" does not equal to'
                             f'Expected "{2}"')

    def test_003_verify_the_standard_match_event_details(self):
        """
        DESCRIPTION: Verify the standard match event details
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link are present
        """
        # "watch signposting" cannot be automated as events are not live.
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

    def test_004_verify_ga_tracking_for_the_match_result(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default):
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
        options = self.site.contents.tab_content.dropdown_market_selector.items_as_ordered_dict
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

    def test_005_repeat_steps_1_4_for_most_180s(self):
        """
        DESCRIPTION: Repeat steps 1-4 for 'Most 180s'
        """
        self.test_001_verify_displaying_of_the_market_selector_dropdown_list(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s)
        self.test_002_verify_text_of_the_labels_for_match_result()
        self.test_003_verify_the_standard_match_event_details()
        self.test_004_verify_ga_tracking_for_the_match_result(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s)
