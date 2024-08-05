import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod : # Events with specific markets cannot created in Prod/Beta
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.market_switcher
@vtest
class Test_C60089571_Verify_MS_behavior_on_Competitions_Tab_for_Darts(BaseSportTest):
    """
    TR_ID: C60089571
    NAME: Verify MS behavior on Competitions Tab for Darts
    DESCRIPTION: This test case verifies the behavior of 'Market Selector' dropdown list
    PRECONDITIONS: CMS Configurations:
    PRECONDITIONS: a) Market switcher toggle should be configured in CMS global level and individual sport level in config tab in System Configuration
    PRECONDITIONS: b) The markets which are mentioned under Note, those markets “Market template name” which is in OB should be mentioned in “Primary markets” section in pipe symbol separated by comma(** No space between two market template) in Sports configuration for Particular sport.
    PRECONDITIONS: eg: |Games Total (Over/Under)|,|Games Handicap (Handicap)|
    PRECONDITIONS: c) Dispsort name should be mentioned for the above created markets in Dispsort field.
    PRECONDITIONS: eg: HH,HL,WH
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Go to the Darts Competition page -> 'Matches' tab
    PRECONDITIONS: Note:
    PRECONDITIONS: 1) The set of markets should be created in OB system using the following Market Template Names:
    PRECONDITIONS: * |Match Betting(WW/WDW)| - "Match Result"
    PRECONDITIONS: * |Match Handicap| - "Handicap"
    PRECONDITIONS: * |Total 180s Over/Under (Over/Under)| - "Total 180s"
    PRECONDITIONS: * |Most 180s (WDW)| - "Most 180s"
    PRECONDITIONS: 2) To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    market_selector_options = [('match_handicap',),
                               ('total_180s_over_under',),
                               ('most_180s',)]

    expected_market_selector_options = [vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.most_180s,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.total_180s_over_under,
                                        vec.siteserve.EXPECTED_MARKETS_NAMES.handicap_2_way
                                        ]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Darts event with scores
        EXPECTED: Event is successfully created
        """
        market_switcher_status = self.cms_config.verify_and_update_market_switcher_status(sport_name='darts', status=True)
        self.assertTrue(market_switcher_status, msg='Market switcher is disabled for Darts sport')
        all_sports_status = \
            self.cms_config.verify_and_update_market_switcher_status(sport_name='AllSports', status=True)
        self.assertTrue(all_sports_status, msg='"All Sports" is disabled')
        self.cms_config.verify_and_update_sport_config(sport_category_id=self.ob_config.backend.ti.darts.category_id,
                                                       disp_sort_names='MR,HL,WH,HH',
                                                       primary_markets='|Match Betting|,|Total 180s Over/Under|,'
                                                                       '|Most 180s|,|Leg Handicap|,|Leg Winner|,'
                                                                       '|Match Betting Head/Head|,|Match Handicap|')
        self.ob_config.add_darts_event_to_darts_all_darts(markets=self.market_selector_options)
        expected_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                    self.ob_config.darts_config.category_id)

        self.navigate_to_page(name='sport/darts')
        self.site.wait_content_state(state_name='Darts')
        self.site.darts.tabs_menu.click_button(expected_tab_name)
        self.assertEqual(self.site.darts.tabs_menu.current, self.expected_sport_tabs.competitions,
                         msg=f'"{self.expected_sport_tabs.competitions}" tab is not active')

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
        self.assertTrue(has_market_selector, msg=' "Market selector" is not available for Darts')
        drop_down = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(drop_down.change_button, msg=f'"Change button" is not displayed')
            drop_down.click()
            self.assertFalse(drop_down.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        else:
            if self.brand == 'bma':
                self.assertTrue(drop_down.has_up_arrow, msg='"Up Arrow" is not shown')
                self.assertTrue(drop_down.has_down_arrow, msg='"Down Arrow" is not shown')
            else:
                self.assertTrue(drop_down.is_expanded(), msg=f'"dropdown arrow" is not pointing downwards')
        selected_value = self.site.competition_league.tab_content.dropdown_market_selector.selected_market_selector_item
        if self.brand == 'ladbrokes' and self.device_type == 'desktop':
            expected_selected_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default.upper()
        else:
            expected_selected_value = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result_default
        self.assertEqual(selected_value, expected_selected_value,
                         msg=f'Actual selected value: "{selected_value}" is not same as'
                             f'Expected selected value: "{expected_selected_value}"')

    def test_002_tap_on_the_change_button_in_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Tap on the 'Change' button in 'Market Selector' dropdown list
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • List of markets are displayed
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        self.__class__.list_of_drop_down = self.site.competition_league.tab_content.dropdown_market_selector.items_as_ordered_dict
        available_markets = list(self.list_of_drop_down.keys())
        self.assertEqual(available_markets, self.expected_market_selector_options,
                         msg=f'Incorrect list/order of markets in Market Selector drop-down.\n'
                             f'Actual: {available_markets}\nExpected: {self.expected_market_selector_options}')
        dropdown = self.site.competition_league.tab_content.dropdown_market_selector
        if self.device_type in ['mobile', 'tablet']:
            self.assertTrue(dropdown.change_button, msg=f'"Change button" is not displayed')
            dropdown.click()
            self.assertFalse(dropdown.is_expanded(), msg=f'dropdown arrow is not pointing upwards')

    def test_003_verify_the_behavior_of_market_selector_dropdown_list(self):
        """
        DESCRIPTION: Verify the behavior of 'Market Selector' dropdown list
        EXPECTED: User should be able to mouse over the markets in the list,The market which is in focus will get highlighted.
        """
        # This step cannot be automated for mobile.
        if self.device_type == 'desktop':
            drop_down = self.site.competition_league.tab_content.dropdown_market_selector
            for option, element in self.list_of_drop_down.items():
                element.mouse_over()
                # when mouse over, color is not reflecting immediately
                sleep(2)
                actual_bg_color = element.background_color_value
                self.assertEqual(actual_bg_color, vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR,
                                 msg=f'Actual background color: "{actual_bg_color}" is not same as'
                                     f'Expected background color: "{vec.colors.MARKET_SWITCHER_HIGHLIGHTED_COLOR}"')
                drop_down.select_value(value=option)
                dropdown = self.site.competition_league.tab_content.dropdown_market_selector
                selected_value = dropdown.selected_market_selector_item
                self.assertEqual(selected_value.upper(), option.upper(),
                                 msg=f'Actual selected value: "{selected_value}" is not same as '
                                     f'Expected selected value: "{option}"')

    def test_004_select_market_which_is_higlighted(self):
        """
        DESCRIPTION: Select market which is higlighted
        EXPECTED: Highlighted market should be displayed
        """
        # covered in step test_003

    def test_005_tap_on_the_change_button_again_and_mouse_over_the_content(self):
        """
        DESCRIPTION: Tap on the 'Change' button again and mouse over the content
        EXPECTED: • 'Market Selector' dropdown list opens
        EXPECTED: • select market which is higlighted
        EXPECTED: • The chevron near 'Change' button is pointed upwards
        """
        drop_down = self.site.competition_league.tab_content.dropdown_market_selector
        self.assertTrue(drop_down, msg='"Market Selector" dropdown is available')
        self.test_002_tap_on_the_change_button_in_market_selector_dropdown_list()
