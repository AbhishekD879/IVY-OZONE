import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Events cannot be created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60089583_Verify_pre_selected_WW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Snooker(BaseSportTest):
    """
    TR_ID: C60089583
    NAME: Verify pre selected ‘WW’ MT is saved when switching b/w T/T/F on Matches Tab for Snooker
    DESCRIPTION: This test case verifies that previously selected ‘WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Snooker landing page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Match Betting|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: Load the app
    PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Matches Tab'
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
    device_name = tests.desktop_default
    event_markets = [('total_frames_over_under',)]

    @retry(stop=stop_after_attempt(5), retry=retry_if_exception_type((VoltronException, AttributeError)),
           wait=wait_fixed(wait=2),
           reraise=True)
    def wait_for_event_to_reflect(self):
        self.navigate_to_page(name='sport/snooker')
        self.site.wait_content_state('Snooker')
        self.site.sports_page.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name).click()
        if not (self.device_type in ['mobile', 'tablet'] and self.brand == 'bma'):
            usa_ahl_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(
                self.section_name)
            if usa_ahl_section:
                event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
                if event is None:
                    raise VoltronException(f'"{self.eventID}" Event not found')
            else:
                raise VoltronException(f'"{self.section_name}" League not found')

    def verify_market_event_fixture(self, eventID=None, section_name=None, expected_tab=None):
        self.site.wait_splash_to_hide(5)
        wait_for_result(lambda: self.site.sports_page.date_tab.current_date_tab == expected_tab, timeout=10,
                        name='Day(T/T/F) to be displayed')
        self.assertEqual(self.site.sports_page.date_tab.current_date_tab, expected_tab,
                         msg=f'Current active date tab: "{self.site.sports_page.date_tab.current_date_tab}" '
                             f'expected: "{expected_tab}"')
        market_selector_default_value = self.market_selector_default_value.title() if self.brand == 'bma' else self.market_selector_default_value
        self.assertEqual(self.snooker_tab_content.dropdown_market_selector.selected_market_selector_item,
                         market_selector_default_value,
                         msg=f'Incorrect market name is selected by default:\n'
                             f'Actual: "{self.snooker_tab_content.dropdown_market_selector.selected_market_selector_item}"\n'
                             f'Expected: "{market_selector_default_value}"')
        usa_ahl_section = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.get(section_name)
        self.assertTrue(usa_ahl_section, msg=f'Section "{section_name}" not found')
        event = self.get_event_from_league(event_id=eventID, section_name=section_name)
        events = usa_ahl_section.items_as_ordered_dict.values()
        self.assertTrue(event, msg='Event for the "Match Result" market not shown')
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
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Matches Tab'
        """
        all_sports_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                     status=True)
        self.assertTrue(all_sports_status, msg='Market switcher is disabled for All Sports')
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='snooker',
                                                                                          status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Snooker sport')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.snooker.category_id,
                                                       disp_sort_names='HH,MH,WH,HL',
                                                       primary_markets='|Match Result|,|Match Betting|,|Handicap Match Result|,'
                                                                       '|Total Frames Over/Under|,|Match Handicap|')

        # Today tab event
        event_params = self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.event_markets)
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.section_name = f'{event_resp[0]["event"]["categoryCode"]} - {event_resp[0]["event"]["typeName"]}'.upper()

        # Tomorrow Tab Event
        tomorrow = self.get_date_time_formatted_string(days=1)
        event_params_tomorrow = self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.event_markets,
                                                                                        start_time=tomorrow)
        self.__class__.eventID_tomorrow = event_params_tomorrow.event_id
        self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_tomorrow, query_builder=self.ss_query_builder)

        # Future Tab Event
        future = self.get_date_time_formatted_string(days=7)
        event_params_future = self.ob_config.add_snooker_event_to_snooker_all_snooker(markets=self.event_markets,
                                                                                      start_time=future)
        self.__class__.eventID_future = event_params_future.event_id
        self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_future, query_builder=self.ss_query_builder)

        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKET_SECTIONS.match_result
        self.__class__.expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                                   self.ob_config.snooker_config.category_id)
        self.wait_for_event_to_reflect()
        current_tab_name = self.site.sports_page.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as Expected Tab: "{self.expected_tab_name}"')

    def test_001_verify_displaying_of_the_market_selector(self):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • 'Match Result' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to 'Match Result' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to 'Match Result' in 'Market selector' **Coral**
        """
        # "Match result is selected by default" validation is done in verify_market_event_fixture() method
        self.__class__.snooker_tab_content = self.site.sports_page.tab_content
        self.assertTrue(self.snooker_tab_content.has_dropdown_market_selector(timeout=20),
                        msg='"Market Selector" drop-down is not displayed on Snooker landing page')
        dropdown = self.site.sports_page.tab_content.dropdown_market_selector
        dropdown.click()
        if self.brand == 'bma':
            self.assertTrue(dropdown.has_up_arrow, msg='Market selector up arrow is not displayed')
            self.assertTrue(dropdown.has_down_arrow, msg='Market selector down arrow is not displayed')
        else:
            # sleep provided as it takes some time to close the market switcher dropdown
            sleep(2)
            self.assertFalse(dropdown.is_expanded(), msg=f'"Dropdown arrow" is not pointing downwards')

    def test_002_verify_text_of_the_labels_for_match_result(self):
        """
        DESCRIPTION: Verify text of the labels for 'Match Result'
        EXPECTED: • The events for the Match Result market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        """
        self.verify_market_event_fixture(eventID=self.eventID, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.today)

    def test_003_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: Match Result)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2.
        EXPECTED: Note: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        self.site.sports_page.date_tab.tomorrow.click()
        self.verify_market_event_fixture(eventID=self.eventID_tomorrow, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.tomorrow)

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        """
        # functionality covered in step test_003

    def test_005_repeat_steps_34_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 3,4 for the 'Future' tab
        """
        self.site.sports_page.date_tab.future.click()
        self.verify_market_event_fixture(eventID=self.eventID_future, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.future)

    def test_006_switch_back_to_today_tab(self):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' & '2' and corresponding Odds are present under Label 1 & 2
        """
        self.site.sports_page.date_tab.today.click()
        self.verify_market_event_fixture(eventID=self.eventID, section_name=self.section_name,
                                         expected_tab=vec.sb.SPORT_DAY_TABS.today)
