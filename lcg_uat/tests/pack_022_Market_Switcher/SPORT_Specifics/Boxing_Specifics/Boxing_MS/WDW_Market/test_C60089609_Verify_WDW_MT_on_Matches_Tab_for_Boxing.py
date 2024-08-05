import pytest
from time import sleep
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C60089609_Verify_WDW_MT_on_Matches_Tab_for_Boxing(BaseDataLayerTest):
    """
    TR_ID: C60089609
    NAME: Verify 'WDW’ MT on Matches Tab for Boxing
    DESCRIPTION: This test case verifies displaying of behaviour of ‘WDW market’ Template in Matches Tab  for Boxing
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to Boxing  Landing page -> 'Click on Matches Tab'
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Fight Betting(WDW)| - "Fight Betting"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Boxing landing page -> 'Matches' tab
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='boxing',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Boxing sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.boxing_config.category_id,
                                                       disp_sort_names='MR',
                                                       primary_markets='|Fight Betting|')
        self.ob_config.add_autotest_boxing_event()
        self.navigate_to_page(name='sport/boxing/matches')
        self.site.wait_content_state_changed()
        current_tab_name = self.site.boxing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.sb.TABS_NAME_FIGHTS.upper(),
                         msg=f'Default tab is "{current_tab_name}",instead of "{vec.sb.TABS_NAME_FIGHTS}"')
        self.__class__.boxing = self.site.boxing.tab_content

    def test_001_verify_displaying_of_the_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector' dropdown list
        EXPECTED: Tablet/Mobile:
        EXPECTED: • ‘Market Selector’ is displayed on upcoming module header (with 1st option selected by default)
        EXPECTED: •'Change' button with chevron (pointing down) on the module header opens the Market Selector dropdown
        EXPECTED: Desktop:
        EXPECTED: • 'Market Selector' is displayed next to Day Selectors (Today/Tomorrow/Future) on the right side
        EXPECTED: • 'Fight Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Fight Betting' Ladbrokes
        EXPECTED: • Up and down arrows are shown next to 'Fight Betting' in 'Market selector' Coral
        """
        has_market_selector = self.boxing.has_dropdown_market_selector()
        self.assertTrue(has_market_selector,
                        msg=' "Market Selector" drop-down is not displayed on Fights tab in boxing')
        selected_value = self.boxing.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.title(), vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.title(),
                         msg=f'Actual selected value: "{selected_value.title()}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting.title()}"')
        self.__class__.dropdown = self.boxing.dropdown_market_selector
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
                sleep(2)
                self.assertFalse(self.dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')

    def test_002_verify_displaying_of_preplay_events_for_fight_betting(self):
        """
        DESCRIPTION: Verify displaying of Preplay events for 'Fight Betting'
        EXPECTED: Preplay events are displayed
        """
        self.__class__.leagues = list(self.boxing.accordions_list.items_as_ordered_dict.values())
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
                    self._logger.info(f'"{event_template.event_name}" has more markets')
                else:
                    self._logger.info(f'"{event_template.event_name}" has no more markets')

    def test_003_verify_text_of_the_labels_for_fight_betting(self):
        """
        DESCRIPTION: Verify text of the labels for 'Fight Betting'
        EXPECTED: • The events for the 'Fight Betting' market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'Home''Draw' 'Away' and corresponding Odds are present under Label Home Draw Away
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
        EXPECTED: • Team names, date, time, watch signposting, "XX More" markets link is present in the landing page
        """
        # Covered in step 2
        # "watch signposting" cannot be automated as events are not live.

    def test_005_verify_ga_tracking_for_the_fight_betting(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Fight Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Fight Betting"
        EXPECTED: categoryID: "9"
        EXPECTED: })
        """
        options = self.site.sports_page.tab_content.dropdown_market_selector.items_as_ordered_dict
        if not self.dropdown.is_expanded():
            self.dropdown.expand()
        options.get(vec.siteserve.EXPECTED_MARKETS_NAMES.fight_betting).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Fight Betting')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': 'Fight Betting',
                             'categoryID': 9,
                             }
        self.compare_json_response(actual_response, expected_response)
