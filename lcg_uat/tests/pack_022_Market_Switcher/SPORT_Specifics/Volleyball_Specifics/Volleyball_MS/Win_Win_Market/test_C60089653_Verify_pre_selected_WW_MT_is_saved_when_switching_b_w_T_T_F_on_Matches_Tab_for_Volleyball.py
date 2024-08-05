import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Events with specific markets cannot created in Prod/Beta
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.market_switcher
@vtest
class Test_C60089653_Verify_pre_selected_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Volleyball(BaseDataLayerTest):
    """
    TR_ID: C60089653
    NAME: Verify pre selected ‘WW’ MT is saved when switching b/w T/T/F on Matches Tab for Volleyball
    DESCRIPTION: This test case verifies that previously selected ‘WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Volleyball landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Volleyball Landing Page -> 'Click on Matches Tab'
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: |Match Betting (WW)| - "Match Result"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    event_markets = [
        ('match_set_handicap',),
        ('total_match_points',)]

    def goto_the_day_tab_and_verify_MS(self, day):
        self.grouping_buttons.items_as_ordered_dict.get(day).click()
        self.site.wait_content_state_changed()
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        if has_market_selector:
            selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
            self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')
        else:
            self.assertFalse(has_market_selector, msg=' "Market Selector" is displayed" ')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events with required markets
        DESCRIPTION: Navigate volleybal landing page
        EXPECTED: Event is successfully created
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        status = self.cms_config.verify_and_update_market_switcher_status(sport_name='volleyball', status=True)
        self.assertTrue(status, msg=f'The sport "volleyball" is not checked')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.volleyball_config.category_id,
                                                       disp_sort_names='HH,MH,WH,HL,3W',
                                                       primary_markets='|Match Betting|,|Handicap Match Result|,|Match Set Handicap|,|Total Match Points|,|Set X Winner||Handicap 3-Way|')

        event_params = self.ob_config.add_volleyball_event_to_austrian_league(markets=self.event_markets)

        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        self.navigate_to_page(name='sport/volleyball')
        self.site.wait_content_state('volleyball')
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.volleyball_config.category_id)
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(expected_tab_name).click()
        current_tab = self.site.contents.tabs_menu.current
        self.assertEqual(expected_tab_name, current_tab, msg=f'Actual tab: "{current_tab}" is not same as '
                                                             f'Expected tab: "{expected_tab_name}"')
        if self.device_type == 'desktop':
            self.__class__.grouping_buttons = self.site.contents.tab_content.grouping_buttons
            current_tab = self.grouping_buttons.current
            self.assertEqual(current_tab.upper(), vec.sb.TABS_NAME_TODAY.upper(),
                             msg=f'Actual tab: "{current_tab.upper()}" is not same as'
                                 f'Expected tab: "{vec.sb.TABS_NAME_TODAY.upper()}".')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' **Coral**
        """
        has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Volleyball')
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                dropdown.click()
                sleep(2)
                self.assertFalse(dropdown.is_expanded(), msg=f' "Dropdown Arrow" is not pointing downwards')
        selected_value = self.site.sports_page.tab_content.dropdown_market_selector.selected_market_selector_item
        self.assertEqual(selected_value.upper(), vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper(),
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default}"')

    def test_002_verify_displaying_of_preplay_events_for_match_result(self):
        """
        DESCRIPTION: Verify displaying of Preplay events for 'Match Result'
        EXPECTED: Preplay events should be displayed
        EXPECTED: Note: If there are no events Market Selector dropdown should not display
        """
        self.__class__.leagues = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        if len(self.leagues) > 0:
            for league in self.leagues:
                if not league.is_expanded():
                    league.expand()
                events = list(league.items_as_ordered_dict.values())
                self.assertTrue(events, msg='Events not found')
                for event in events:
                    self.assertFalse(event.template.is_live_now_event,
                                     msg=f'Event: "{event}" is an "In-Play" Event')
        else:
            self._logger.info(msg=' "No events found".')
            has_market_selector = self.site.sports_page.tab_content.has_dropdown_market_selector()
            self.assertFalse(has_market_selector, msg=' "Market Selector" is displayed" ')

    def test_003_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result'
        EXPECTED: • The events for the Match Result market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        if len(self.leagues) > 0:
            fixture = self.leagues[0].fixture_header
            self.assertEqual(fixture.header1, '1',
                             msg=f'Actual fixture header "{fixture.header1}" does not equal to'
                                 f'Expected "1"')

            self.assertEqual(fixture.header3, '2',
                             msg=f'Actual fixture header "{fixture.header3}" does not equal to'
                                 f'Expected "2"')

    def test_004_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Match Result)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note:
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        if self.brand == 'bma':
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.upper(),
                                        vec.sb.TABS_NAME_FUTURE.upper(),
                                        vec.sb.TABS_NAME_TODAY.upper()]
        else:
            self.__class__.days_list = [vec.sb.TABS_NAME_TOMORROW.title(),
                                        vec.sb.TABS_NAME_FUTURE.title(),
                                        vec.sb.TABS_NAME_TODAY.title()]

        if self.device_type == 'desktop':
            self.goto_the_day_tab_and_verify_MS(day=self.days_list[0])
            self.test_002_verify_displaying_of_preplay_events_for_match_result()
            self.test_003_verify_text_of_the_labels_for_match_result()

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        """
        # covered in step 4

    def test_006_repeat_steps_34_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 2,3 for the 'Future' tab
        """
        if self.device_type == 'desktop':
            self.goto_the_day_tab_and_verify_MS(day=self.days_list[1])
            self.test_002_verify_displaying_of_preplay_events_for_match_result()
            self.test_003_verify_text_of_the_labels_for_match_result()

    def test_007_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        if self.device_type == 'desktop':
            self.goto_the_day_tab_and_verify_MS(day=self.days_list[2])
            self.test_003_verify_text_of_the_labels_for_match_result()
