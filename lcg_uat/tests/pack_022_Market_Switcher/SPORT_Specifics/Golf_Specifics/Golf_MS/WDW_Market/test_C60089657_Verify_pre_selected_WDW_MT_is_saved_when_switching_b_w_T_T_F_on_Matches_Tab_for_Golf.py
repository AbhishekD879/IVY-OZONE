import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # # Events with specific markets cannot be created in Prod/Beta
@pytest.mark.market_switcher
@pytest.mark.desktop
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C60089657_Verify_pre_selected_WDW_MT_is_saved_when_switching_b_w_T_T_F_on_Matches_Tab_for_Golf(BaseSportTest, BaseDataLayerTest):
    """
    TR_ID: C60089657
    NAME: Verify pre selected ‘WDW’ MT is saved when switching b/w T/T/F on Matches Tab for Golf
    DESCRIPTION: This test case verifies that previously selected ‘WW Market’ Template is saved when user is switching between Today/Tomorrow/Future on Golf Landing Page
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) Is Outright sport should be ‘enabled’ and Odds card Header type should be ‘None’
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Golf Landing page -> 'Matches' tab
    PRECONDITIONS: 3. Select the 'Today' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |2 Ball Betting| - "2 Ball Betting"
    PRECONDITIONS: * |3 Ball Betting| - "3 Ball Betting"
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    event_markets = [('2_ball_betting',)]

    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.three_ball_betting,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting
                                        ]

    def verify_fixture_header_and_qty_of_bet_buttons(self, bet_button_qty, header1, header3, header2=None):
        items = list(self.golf_tab_content.accordions_list.items_as_ordered_dict.values())[0]
        events = items.items_as_ordered_dict.values()
        self.assertTrue(events, msg='"Events" are not available')
        event = items.fixture_header
        self.assertEqual(event.header1, header1,
                         msg=f'Actual fixture header "{event.header1}" does not equal to'
                             f'Expected "{header1}"')
        if header2:
            self.assertEqual(event.header2, header2,
                             msg=f'Actual fixture header "{event.header2}" does not equal to'
                                 f'Expected "{header2}"')
        self.assertEqual(event.header3, header3,
                         msg=f'Actual fixture header "{event.header2}" does not equal to'
                             f'Expected "{header3}"')
        bet_buttons = len(list(list(events)[0].template.items_as_ordered_dict.items()))
        self.assertEqual(bet_buttons, bet_button_qty,
                         msg=f'Actual Buttons: "{bet_buttons}" are not same as'
                             f'Expected Buttons: "{bet_button_qty}".')
        section_name = tests.settings.golf_allianz_championship
        sections = self.site.golf.tab_content.accordions_list.items_as_ordered_dict
        golf_section = sections.get(section_name)

        name, odds_from_page = list(golf_section.items_as_ordered_dict.items())[0]
        default_odds = odds_from_page.template.items_names
        for index in range(len(default_odds)):
            self.check_odds_format(odds=default_odds[index],
                                   expected_odds_format="fraction")

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Load the app
        PRECONDITIONS: 2. Go to the Golf Landing page -> 'Matches tab
        PRECONDITIONS: 3. Make sure that 'Market Selector' is present on the page
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='golf', status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Golf sport')
        all_sport_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports',
                                                                                             status=True)
        self.assertTrue(all_sport_switcher_status, msg='"All Sports" is disabled')
        self.ob_config.add_golf_event_to_golf_all_golf(markets=self.event_markets)
        tomorrow = self.get_date_time_formatted_string(days=1)
        self.ob_config.add_golf_event_to_golf_all_golf(start_time=tomorrow)
        future = self.get_date_time_formatted_string(days=7)
        self.ob_config.add_golf_event_to_golf_all_golf(start_time=future)

        self.__class__.market_selector_default_value = vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting
        self.navigate_to_page(name='sport/golf')
        self.site.wait_content_state(state_name='Golf', timeout=10)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                    self.ob_config.golf_config.category_id)
        if self.brand == 'bma':
            self.site.golf.tabs_menu.click_button(vec.SB.TABS_NAME_EVENTS.upper())
        else:
            self.site.golf.tabs_menu.click_button(vec.SB.TABS_NAME_MATCHES.upper())
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name, expected_tab_name,
                         msg=f'Actual tab: "{current_tab_name}" is not same as'
                             f'Expected tab: "{expected_tab_name}".')
        self.__class__.grouping_buttons = self.site.contents.tab_content.grouping_buttons
        current_tab = self.grouping_buttons.current
        self.assertEqual(current_tab.upper(), vec.sb.TABS_NAME_TODAY.upper(),
                         msg=f'Actual tab: "{current_tab.upper()}" is not same as'
                             f'Expected tab: "{vec.sb.TABS_NAME_TODAY.upper()}".')

    def test_001_verify_displaying_of_the_market_selector(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.three_ball_betting):
        """
        DESCRIPTION: Verify displaying of the 'Market Selector'
        EXPECTED: • 'Market Selector' is displayed next to Days Selector on the right side
        EXPECTED: • '2 Ball Betting' is selected by default in 'Market Selector' dropdown list
        EXPECTED: • Chevron (pointing down) are shown next to '3 Ball Betting' **Ladbrokes**
        EXPECTED: • Up and down arrows are shown next to '3 Ball Betting' in 'Market selector' **Coral**
        """
        self.__class__.golf_tab_content = self.site.golf.tab_content
        self.assertTrue(self.golf_tab_content.has_dropdown_market_selector(),
                        msg='"Market Selector" drop-down is not displayed on Golf landing page')
        dropdown = self.golf_tab_content.dropdown_market_selector
        if self.brand == 'bma':
            dropdown.click_item(market_name)
            sleep(1)
            self.assertTrue(dropdown.has_up_arrow, msg='"Up Arrow" is not shown')
            self.assertTrue(dropdown.has_down_arrow, msg='"Down Arrow" is not shown')
        else:
            dropdown.click_item(market_name)
            sleep(1)
            self.assertFalse(dropdown.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        selected_value = self.site.contents.tab_content.dropdown_market_selector.selected_market_selector_item
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            self.assertEqual(selected_value, market_name.upper(),
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{market_name.upper()}"')
        else:
            self.assertEqual(selected_value, market_name,
                             msg=f'Actual selected value: "{selected_value}" is not same as'
                                 f'Expected selected value: "{market_name}"')

    def test_002_verify_text_of_the_labels_for_3_ball_betting_in_matches_tab_today(self):
        """
        DESCRIPTION: Verify text of the labels for '3 Ball Betting' in Matches Tab (Today)
        EXPECTED: • The events for the 3 Ball Betting market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' '2' '3' and corresponding Odds are present under Label 1 2 3.
        """
        self.golf_tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_market_selector_options[0]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='2',
                                                          header3='3')

    def test_003_switch_to_the_tomorrow_tab(self):
        """
        DESCRIPTION: Switch to the 'Tomorrow' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown (Ex: 3 Ball Betting)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' '2' '3' and corresponding Odds are present under Label 1 2 3.
        EXPECTED: Note:
        EXPECTED: If events are not present for 3 Ball Betting market and if events are present for 2 Ball Betting market then 2 Ball Betting will be displayed in the switcher (Same logic applies to Today/Tomorrow/Future Tabs)
        EXPECTED: If there are no events Market Selector dropdown should not display and 'No events found' msg should display(Applies to Today/Tomorrow/Future)
        """
        self.site.golf.date_tab.tomorrow.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='2',
                                                          header3='3')

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: Same as step#2
        """
        # step covered into step 3

    def test_005_repeat_steps_34_for_the_future_tab(self):
        """
        DESCRIPTION: Repeat steps 3,4 for the 'Future' tab
        EXPECTED: Same as Step# 3, 4
        """
        self.site.golf.date_tab.future.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='2',
                                                          header3='3')

    def test_006_switch_back_to_today_tab(self, header1='1', header2='2', header3='3'):
        """
        DESCRIPTION: Switch back to 'Today' tab
        EXPECTED: • Previously selected option is displayed in the 'Market Selector' dropdown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' '2' '3' and corresponding Odds are present under Label 1 2 3
        """
        self.site.golf.date_tab.today.click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1=header1, header2=header2,
                                                          header3=header3)

    def test_007_verify_ga_tracking_for_the_3_ball_betting(self, market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.three_ball_betting):
        """
        DESCRIPTION: Verify GA Tracking for the '3 Ball Betting'
        EXPECTED: Click on Inspect and goto Browser console type "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: event: "trackEvent"
        EXPECTED: eventCategory: "market selector"
        EXPECTED: eventAction: "change market"
        EXPECTED: eventLabel: "3 Ball Betting"
        EXPECTED: categoryID: "18"
        EXPECTED: })
        EXPECTED: Note: Corresponding market name will be displayed in 'eventLabel' field
        """
        options = self.site.golf.tab_content.dropdown_market_selector.items_as_ordered_dict
        dropdown = self.site.contents.tab_content.dropdown_market_selector
        if not dropdown.is_expanded():
            dropdown.expand()
        options.get(market_name).click()
        actual_response = self.get_data_layer_specific_object(object_key='eventLabel', object_value=market_name)
        expected_response = {'event': 'trackEvent',
                             'eventCategory': 'market selector',
                             'eventAction': 'change market',
                             'eventLabel': market_name,
                             'categoryID': 18,
                             }
        self.compare_json_response(actual_response, expected_response)

    def test_008_repeat_steps_1_7_for_the_below_markets_2_ball_betting_expect_step_2(self):
        """
        DESCRIPTION: Repeat steps 1-7 for the below markets
        DESCRIPTION: • 2 Ball Betting (expect step 2)
        EXPECTED: As per steps
        """

        self.test_001_verify_displaying_of_the_market_selector(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting)
        self.test_003_switch_to_the_tomorrow_tab()
        self.test_005_repeat_steps_34_for_the_future_tab()
        self.test_006_switch_back_to_today_tab(header1='1', header2='TIE', header3='2')
        self.test_007_verify_ga_tracking_for_the_3_ball_betting(market_name=vec.siteserve.EXPECTED_MARKETS_NAMES.two_ball_betting)

    def test_009_verify_text_of_the_labels_for_2_ball_betting_in_matches_tab_today(self):
        """
        DESCRIPTION: Verify text of the labels for '2 Ball Betting' in Matches Tab (Today)
        EXPECTED: • The events for selected market are shown
        EXPECTED: • Values on Fixture header are displayed with Market Labels'1' 'Tie' '2' and corresponding Odds are present under Label 1 Tie 2.
        """
        self.golf_tab_content.dropdown_market_selector.items_as_ordered_dict.get(
            self.expected_market_selector_options[1]).click()
        self.verify_fixture_header_and_qty_of_bet_buttons(bet_button_qty=3, header1='1', header2='TIE',
                                                          header3='2')
