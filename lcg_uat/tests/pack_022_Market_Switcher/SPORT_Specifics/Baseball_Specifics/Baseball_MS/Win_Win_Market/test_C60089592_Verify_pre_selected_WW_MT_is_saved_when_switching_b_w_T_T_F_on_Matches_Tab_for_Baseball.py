import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Events with specific markets cannot created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60089592_Verify_pre_selected_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Baseball(BaseSportTest):
    """
    TR_ID: C60089592
    NAME: Verify pre selected ‘WW’ MT is saved when switching b/w T/T/F on Matches Tab for Baseball
    DESCRIPTION: This test case verifies that previously selected ‘WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Baseball landing page
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
    device_name = tests.desktop_default
    event_markets = [('total_runs',)]

    def verify_market_event_fixture(self, eventID=None, section_name=None, expected_tab=None):
        self.assertEqual(self.site.baseball.date_tab.current_date_tab, expected_tab,
                         msg=f'Current active date tab: "{self.site.baseball.date_tab.current_date_tab}" '
                             f'expected: "{expected_tab}"')
        market_selector_default_value = self.market_selector_default_value.upper() \
            if self.brand == 'ladbrokes' and self.device_type == 'desktop' else self.market_selector_default_value
        self.assertEqual(self.baseball_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{self.baseball_tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')
        usa_ahl_section = self.site.baseball.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
        self.assertTrue(usa_ahl_section, msg=f'Section "{section_name}" not found')
        event = self.get_event_from_league(event_id=eventID, section_name=section_name)
        events = usa_ahl_section.items_as_ordered_dict.values()
        self.assertTrue(event, msg='Event for the "Money Line" market not shown')
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

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Ice Hockey event with required markets
        EXPECTED: Event is successfully created
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
        # Today tab event
        event_params = self.ob_config.add_baseball_event_to_autotest_league(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        # Tomorrow Tab Event
        tomorrow = self.get_date_time_formatted_string(days=1)
        event_params_tomorrow = self.ob_config.add_baseball_event_to_autotest_league(markets=self.event_markets,
                                                                                     start_time=tomorrow)
        self.__class__.eventID_tomorrow = event_params_tomorrow.event_id
        event_resp_tomorrow = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_tomorrow,
                                                                        query_builder=self.ss_query_builder)
        self.__class__.section_name_tomorrow = self.get_accordion_name_for_event_from_ss(event=event_resp_tomorrow[0])

        # Future Tab Event
        future = self.get_date_time_formatted_string(days=7)
        event_params_future = self.ob_config.add_baseball_event_to_autotest_league(markets=self.event_markets,
                                                                                   start_time=future)
        self.__class__.eventID_future = event_params_future.event_id
        event_resp_future = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_future,
                                                                      query_builder=self.ss_query_builder)
        self.__class__.section_name_future = self.get_accordion_name_for_event_from_ss(event=event_resp_future[0])

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

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Money line' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Money line' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Money Line' in 'Market selector' **Coral**
        """
        # "Money line is selected by default" validation is done in verify_market_event_fixture() method
        self.__class__.baseball_tab_content = self.site.baseball.tab_content
        self.assertTrue(self.baseball_tab_content.has_dropdown_market_selector(timeout=20),
                        msg='"Market Selector" drop-down is not displayed on Baseball landing page')
        dropdown = self.site.contents.tab_content.dropdown_market_selector
        dropdown.click()
        if self.brand == 'bma':
            self.assertTrue(dropdown.has_up_arrow, msg='Market selector up arrow is not displayed')
            self.assertTrue(dropdown.has_down_arrow, msg='Market selector down arrow is not displayed')
        else:
            # sleep provided as it takes some time to close the market switcher dropdown
            sleep(2)
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing downwards')

    def test_002_verify_text_of_the_labels_for_money_line(self):
        """
        DESCRIPTION: Verify text of the labels for 'Money Line'
        EXPECTED: • The events for the Money Line market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        self.verify_market_event_fixture(eventID=self.eventID, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.today)

    def test_003_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Money Line)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note:
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(same applies to Today/Tomorrow/Future)
        """
        self.site.baseball.date_tab.tomorrow.click()
        self.verify_market_event_fixture(eventID=self.eventID_tomorrow, section_name=self.section_name_tomorrow,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.tomorrow)

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        """
        # Covered in step 3

    def test_005_repeat_steps_34_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 3,4 for the 'Future' tab
        """
        self.site.baseball.date_tab.future.click()
        self.verify_market_event_fixture(eventID=self.eventID_future, section_name=self.section_name_future,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.future)

    def test_006_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        self.site.baseball.date_tab.today.click()
        self.verify_market_event_fixture(eventID=self.eventID, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.today)
