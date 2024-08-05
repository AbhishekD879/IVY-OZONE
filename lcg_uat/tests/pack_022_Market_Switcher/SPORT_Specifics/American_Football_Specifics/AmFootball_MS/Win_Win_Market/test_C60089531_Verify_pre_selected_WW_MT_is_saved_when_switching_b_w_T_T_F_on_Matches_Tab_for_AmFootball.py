import pytest

import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089531_Verify_pre_selected_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_AmFootball(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089531
    NAME: Verify pre selected ‘WW’ MT is saved when switching b/w T/T/F on Matches Tab for Am.Football
    DESCRIPTION: This test case verifies that previously selected ‘WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on American Football Landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the American Football Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) Below market should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Money line(WW)| - "Money Line"
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
    device_name = tests.desktop_default

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

    def goto_the_day_tab_and_verify_MS(self, day):
        self.grouping_buttons.items_as_ordered_dict.get(day).click()
        self.site.wait_content_state_changed()
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        if has_market_selector:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_value.upper(), self.market_selector_default_value.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{self.market_selector_default_value}"')
        else:
            self.assertFalse(has_market_selector, msg=' "Market Selector" is displayed" ')

    def verify_market_template_labels_text(self, event_id=None):
        self.site.contents.scroll_to_top()
        section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(self.section_name)
        self.assertTrue(section, msg=f'Section "{self.section_name}" not found')
        self.__class__.event = self.get_event_from_league(event_id=event_id, section_name=self.section_name)
        events = section.items_as_ordered_dict.values()
        self.assertTrue(self.event, msg='Event for the "Money Line" market not shown')
        default_fixture_value = list(section.fixture_header.items_as_ordered_dict.keys())
        self.assertEqual(default_fixture_value, ['1', '2'],
                         msg=f'Actual fixture header "{default_fixture_value}" does not '
                             f'equal to expected "{[1, 2]}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, 2,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "2"')
        name, odds_from_page = list(section.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index], expected_odds_format="fraction")

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate american football landing page
        EXPECTED: Event is successfully created
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
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0]).replace(
            ' AUTO TEST', '', 1)

        event_tomorrow = self.ob_config.add_american_football_event_to_autotest_league(markets=self.event_markets, is_tomorrow=True)
        self.__class__.eventID_tomorrow = event_tomorrow.event_id

        event_future = self.ob_config.add_american_football_event_to_autotest_league(
            cashout=True, start_time=self.get_date_time_formatted_string(days=14))
        self.__class__.eventID_future = event_future.event_id

        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.money_line
        self.navigate_to_page(name='sport/american-football')
        self.site.wait_content_state(state_name='american-football')
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Expected tab: "{self.expected_sport_tabs.matches}", Actual Tab: "{current_tab_name}"')

        self.__class__.grouping_buttons = self.site.contents.tab_content.grouping_buttons
        current_tab = self.grouping_buttons.current
        self.assertEqual(current_tab.upper(), vec.sb.TABS_NAME_TODAY.upper(),
                         msg=f'Actual tab: "{current_tab.upper()}" is not same as'
                             f'Expected tab: "{vec.sb.TABS_NAME_TODAY.upper()}".')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Money Line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money Line' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector(timeout=20)
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for american football')
        self.verify_chevron_display()
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), self.market_selector_default_value.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{self.market_selector_default_value}"')

    def test_002_verify_displaying_of_preplay_events_for_money_line(self):
        """
        DESCRIPTION: Verify displaying of Preplay events for 'Money Line'
        EXPECTED: Only Preplay events should display
        """
        self.__class__.leagues = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(self.leagues) > 0:
            for league in self.leagues:
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    self.assertFalse(event.template.is_live_now_event,
                                     msg=f'Event: "{event}" is an "In-Play" Event')
        else:
            self._logger.info(msg=' "No events found".')
            has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
            self.assertFalse(has_market_selector, msg=' "Market Selector" is displayed" ')

    def test_003_verify_text_of_the_labels_for_money_line(self):
        """
        DESCRIPTION: Verify text of the labels for 'Money Line'
        EXPECTED: • The events for the Money Line market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        self.verify_market_template_labels_text(event_id=self.eventID)

    def test_004_verify_ga_tracking_for_the_money_line(self):
        """
        DESCRIPTION: Verify GA Tracking for the 'Money Line'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "Money Line"
        EXPECTED: categoryID: "1"
        EXPECTED: })
        """
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        options = dropdown.items_as_ordered_dict
        if not dropdown.is_expanded():
            dropdown.expand()
        options.get('Money Line').click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value='Money Line')
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': 'Money Line',
                             'categoryID': 1,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_005_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Money Line)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        if self.brand == 'bma':
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.upper(),
                                        vec.sb.TABS_NAME_FUTURE.upper(),
                                        vec.sb.TABS_NAME_TODAY.upper()]
        else:
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.title(),
                                        vec.sb.TABS_NAME_FUTURE.title(),
                                        vec.sb.TABS_NAME_TODAY.title()]

        self.goto_the_day_tab_and_verify_MS(day=self.days_list[0])
        self.test_002_verify_displaying_of_preplay_events_for_money_line()
        self.verify_market_template_labels_text(event_id=self.eventID_tomorrow)
        self.test_004_verify_ga_tracking_for_the_money_line()

    def test_006_repeat_step_34(self):
        """
        DESCRIPTION: Repeat step 3,4
        """
        # covered in step 005

    def test_007_repeat_steps_345_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 3,4,5 for the 'Future' tab
        """
        self.goto_the_day_tab_and_verify_MS(day=self.days_list[1])
        self.test_002_verify_displaying_of_preplay_events_for_money_line()
        self.verify_market_template_labels_text(event_id=self.eventID_future)
        self.test_004_verify_ga_tracking_for_the_money_line()

    def test_008_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        self.goto_the_day_tab_and_verify_MS(day=self.days_list[2])
        self.test_003_verify_text_of_the_labels_for_money_line()
        self.test_004_verify_ga_tracking_for_the_money_line()
