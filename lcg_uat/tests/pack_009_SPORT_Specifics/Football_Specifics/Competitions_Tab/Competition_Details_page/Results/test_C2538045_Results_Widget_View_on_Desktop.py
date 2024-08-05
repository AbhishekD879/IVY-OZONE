import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from time import sleep


# @pytest.mark.tst2 #can't execute on tst2 and stg2 due to result/standing tabs will be displayed for real events
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C2538045_Results_Widget_View_on_Desktop(BaseSportTest):
    """
    TR_ID: C2538045
    NAME: Results Widget View on Desktop
    DESCRIPTION:
    PRECONDITIONS:
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_preconditions(self):
        """
        DESCRIPTION: Events with results tab is loaded
        """
        event = self.get_competition_with_results_and_standings_tabs(
            category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
        sport_name = event.class_name.upper().split(" ")
        if sport_name[0] == vec.siteserve.FOOTBALL_TAB.upper():
            self.__class__.section_name_list = sport_name[1]
        else:
            self.__class__.section_name_list = sport_name[0]
        self.__class__.league = event.league_name
        self.__class__.is_mobile = self.device_type == 'mobile'

    def test_002_choose_competitions_tab(self):
        """
        DESCRIPTION: Choose 'Competitions' tab
        EXPECTED: 'Competitions' tab is selected
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        competitions_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                        self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')

    def test_003_choose_some_competition_from_expanded_class_accordion_and_tap_on_it(self):
        """
        DESCRIPTION: Choose some competition from expanded 'Class' accordion and tap on it
        EXPECTED: Competitions Details page is opened
        EXPECTED: 'Matches' tab is selected by default
        """
        football = self.site.football.tab_content
        grouping_buttons = football.grouping_buttons
        grouping_buttons.click_item(vec.sb_desktop.COMPETITIONS_SPORTS)
        self.sections = football.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='Sections not found')

        self.assertTrue(grouping_buttons.items_as_ordered_dict, msg='No grouping buttons found')

        section_name_list = self.section_name_list.title() if not self.is_mobile and self.brand == 'ladbrokes' else self.section_name_list
        section = self.sections.get(section_name_list)
        self.assertTrue(section, msg=f'"{section_name_list}" was not found')
        section.expand()
        self.assertTrue(section.is_expanded(), msg=f'Section "{section_name_list}" is not expanded')
        self.__class__.leagues = section.items_as_ordered_dict
        self.assertTrue(self.leagues, msg=f'No leagues found in the "{section_name_list}" section')
        league = self.leagues.get(self.league)
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')
        self.__class__.tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(self.tabs_menu, msg='Tabs menu was not found')

        self.__class__.desktop_tabs = list(vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()) \
            if self.brand == 'bma' else [tab.title() for tab in vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()]
        for tab_name, tab in self.tabs_menu.items_as_ordered_dict.items():
            self.assertIn(tab_name, self.desktop_tabs,
                          msg=f'Market switcher tab {tab_name} is not present in the list')

        current_tab = self.tabs_menu.current
        self.assertEqual(current_tab, self.desktop_tabs[0],
                         msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                             f'expected "{self.desktop_tabs[0]}"')

    def test_004_verify_results_tab_displaying(self):
        """
        DESCRIPTION: Verify 'Results' tab displaying
        EXPECTED: *  'Results' widget is displayed in 3-rd column or at the bottom of page below the main content, it depends on page width
        EXPECTED: *  'Results' widget is expanded by default
        EXPECTED: *  'Results' widget is expandable/collapsible
        """
        sleep(3)
        self.__class__.results_widget = self.site.competition_league.results_widget
        self.assertTrue(self.results_widget.is_displayed(), msg='Results widget is not displayed')

    def test_005_verify_content(self):
        """
        DESCRIPTION: Verify content
        EXPECTED: Date Section is NOT expandable/collapsible
        """
        self.assertTrue(self.results_widget.header_label, msg="'Results'text is not displayed")
        self.assertTrue(self.results_widget.collapse, msg="'Results' widget is not collapsible")
        self.assertTrue(self.results_widget.expand, msg="'Results' widget is not expandable")
