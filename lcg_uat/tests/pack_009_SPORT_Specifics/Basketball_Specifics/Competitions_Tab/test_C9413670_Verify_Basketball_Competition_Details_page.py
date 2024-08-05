import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.reg157_fix
@vtest
class Test_C9413670_Verify_Basketball_Competition_Details_page(BaseSportTest):
    """
    TR_ID: C9413670
    NAME: Verify Basketball Competition Details page
    DESCRIPTION: This test case verifies Basketball competition details page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Basketball landing page > Competitions tab
    PRECONDITIONS: 3. Expand any class accordion
    PRECONDITIONS: Note! To have classes/types displayed on frontend, put class ID's in **'InitialClassIDs' and/or 'A-ZClassIDs' fields** in **CMS>SystemConfiguration>Competitions Basketball**. Events for those classes should be present as well.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add basketball event for specific league
        EXPECTED: Navigate to basketball Competition page
        """
        self.__class__.is_mobile = self.device_type == 'mobile'
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsBasketball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsBasketball')
            if str(self.ob_config.basketball_config.basketball_autotest.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException('Basketball competition class is not configured on Competitions tab')
            self.ob_config.add_basketball_event_to_autotest_league()
            self.ob_config.add_basketball_outright_event_to_autotest_league(ew_terms=self.ew_terms)
            self.__class__.section_name_list = 'Basketball Auto Test' if self.brand == 'ladbrokes' else "BASKETBALL AUTO TEST"
            self.__class__.league = tests.settings.basketball_autotest_competition_league.title()

        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.basketball_config.category_id)[0]
            self._logger.info(f'*** Found event: {event}')
            self.__class__.section_name_list = event['event']['className']
            self.__class__.league = event['event']['typeName']

        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        self.__class__.competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.basketball_config.category_id)
        self.assertTrue(self.competitions_tab_name, msg='competition tab is not available')
        self.site.basketball.tabs_menu.click_button(self.competitions_tab_name.upper())

    def test_001_select_any_competition_type_within_expanded_class(self):
        """
        DESCRIPTION: Select any competition (type) within expanded class
        EXPECTED: Competition details page is opened
        """
        section_name_list = self.section_name_list.upper() \
            if (self.brand == 'bma') or (self.brand == 'ladbrokes' and self.device_type == 'mobile') \
            else self.section_name_list
        if self.device_type == 'desktop':
            self.site.basketball.tab_content.grouping_buttons.items_as_ordered_dict.get('A - Z').click()
            sections = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict
        else:
            sections = self.site.basketball.tab_content.all_competitions_categories.get_items(name=section_name_list)
        self.assertTrue(sections, msg=f'Competitions page does not have any "{self.section_name_list}" section')
        section = sections.get(section_name_list)
        self.assertTrue(section, msg=f'Cannot find "{self.section_name_list}" section on Competitions page')
        section.expand()
        leagues = wait_for_result(lambda: section.get_items(name=self.league),
                                  name=f'"{self.section_name_list}" to expand for "{self.league}"', timeout=3)
        self.assertTrue(leagues, msg=f'No events are present for the league "{self.league}"')
        league = leagues.get(self.league)
        self.assertTrue(league, msg=f'Cannot find "{self.league}" on Competitions page')
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

    def test_002_verify_competition_details_page(self):
        """
        DESCRIPTION: Verify Competition details page
        EXPECTED: The following elements are present on the page:
        EXPECTED: **Mobile/Tablet:**
        EXPECTED: * 'COMPETITIONS' label next to the 'back' ('<') button
        EXPECTED: * Competition header with competition name and 'Change Competition' selector
        EXPECTED: * 'Matches' and 'Outrights' switchers (displayed only when there are both matches and outrights for selected type)
        EXPECTED: * 'Matches' switcher is selected by default and events from the league are shown
        EXPECTED: **Desktop:**
        EXPECTED: * Competition (type) name next to the 'Back' ('<') button
        EXPECTED: * 'Change Competition' selector at the right side of the Competition header
        EXPECTED: * Breadcrumbs trail below the Competitions header in the next format: 'Home' > 'Basketball' > 'Competitions' > 'Type (Competition) name'
        EXPECTED: * 'Matches' and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default and events are shown
        """
        if self.brand != 'ladbrokes' and self.device_type == 'mobile':
            coral_title = self.site.competition_league.header_line.page_title.title
            self.assertEqual(coral_title, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                             msg=f'Actual title "{coral_title}" is not equal to expected title'
                                 f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}"')
        competition_name = self.site.competition_league.title_section.type_name.text
        self.assertEqual(competition_name.upper(), self.league.upper(),
                         msg=f'Competition header with competition name is not same '
                             f'Actual: "{competition_name}" '
                             f'Expected: "{self.league}"')
        change_competition_selector = self.site.competition_league.title_section.competition_selector_link.name
        self.assertEqual(change_competition_selector, vec.sb.CHANGE_COMPETITION,
                         msg=f'Competition header with Change Competition selector is not same'
                             f'Actual: "{change_competition_selector}" '
                             f'Expected: "{vec.sb.CHANGE_COMPETITION}"')
        if self.device_type == 'desktop':
            if tests.settings.backend_env == 'prod':
                market_tab = self.site.competition_league.tabs_menu.items_as_ordered_dict
            else:
                expected_tabs = [vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                                 vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper()]
                market_tab = self.site.basketball.tab_content.grouping_buttons.items_as_ordered_dict

                for tab_name in list(market_tab):
                    self.assertIn(tab_name.upper(), expected_tabs, msg=f'Competition tab is not loaded with sections.'
                                                                       f'Actual: "{list(market_tab)}",'
                                                                       f'Expected: "{expected_tabs}"')
            self.assertTrue(market_tab, msg='Matches/ Outright tab is not present for event type in Competition')

            self.__class__.tabs_menu = self.site.competition_league.tabs_menu.items_as_ordered_dict
            self.assertTrue(self.tabs_menu, msg='Tabs menu items are not present')

            current_tab = self.site.competition_league.tabs_menu.current
            self.assertEqual(current_tab.upper(), self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                             msg=f'"Matches" tab is not selected by default'
                                 f'Actual: "{current_tab}" '
                                 f'Expected: "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper()}"')

        events_in_tab = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events_in_tab, msg='Matches tab has no content')

    def test_003_navigate_between_switchers(self):
        """
        DESCRIPTION: Navigate between switchers
        EXPECTED: * User is able to navigate between switchers
        EXPECTED: * Relevant information is shown in each case
        """
        if self.device_type == 'desktop':
            for tab_name, tab in self.tabs_menu.items():
                tab.click()
                result = wait_for_result(lambda: self.site.competition_league.tabs_menu.current == tab_name,
                                         timeout=2,
                                         name='Navigation to next tab')
                self.assertTrue(result,
                                msg=f'Relevant tab is not opened. Actual: "{self.site.competition_league.tabs_menu.current}".'
                                    f' Expected: "{tab_name}"')

    def test_004_tap_the_back__button(self):
        """
        DESCRIPTION: Tap the back ('<') button
        EXPECTED: User is taken to the 'Competitions' tab on the Basketball Landing page
        """
        self.site.back_button_click()
        self.site.wait_content_state('Basketball')
        self.assertEqual(self.site.basketball.tabs_menu.current,
                         self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                         msg=f'User is not taken to "Competitions" tab.'
                             f'Actual: "{self.site.basketball.tabs_menu.current}" '
                             f'Expected: "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}"')

    def test_005_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step 1
        EXPECTED: User is taken to the selected competition details page
        """
        self.test_001_select_any_competition_type_within_expanded_class()

    def test_006_on_matches_switcher_click_on_any_event_card(self):
        """
        DESCRIPTION: On 'Matches' switcher click on any event card
        EXPECTED: Respective event details page opens
        """
        if self.device_type == 'desktop':
            current_tab = self.site.competition_league.tabs_menu.current
            self.assertEqual(current_tab.upper(), self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                             msg=f'"Matches" tab is not selected by default'
                                 f'Actual: "{current_tab}" '
                                 f'Expected: "{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches.upper()}"')
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        section = list(sections.values())[0]
        events = section.items_as_ordered_dict
        event = list(events.values())[0]
        self.assertTrue(event, msg='Could not find event')
        event.click()
        self.site.wait_content_state(state_name='EventDetails')


    def test_007_for_mobiletabletclick__back_button_and_click_on_any_outright_event_on_outrights_switcher(self):
        """
        DESCRIPTION: **For mobile/tablet:**
        DESCRIPTION: Click '<' Back button and click on any outright event on 'Outrights' switcher
        EXPECTED: Respective Outright event details page opens
        """
        if self.device_type == 'mobile':
            self.navigate_to_page(name='sport/basketball')
            self.__class__.competitions_tab_name = self.get_sport_tab_name(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                self.ob_config.basketball_config.category_id)
            self.assertTrue(self.competitions_tab_name, msg='competition tab is not available')
            self.site.basketball.tabs_menu.click_button(self.competitions_tab_name.upper())

            for name, val in self.site.basketball.tab_content.all_competitions_categories.items_as_ordered_dict.items():
                val.expand()
                for league_name, league in val.items_as_ordered_dict.items():
                    league.click()
                    outright_tab_name = self.get_sport_tab_name(
                        self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                        self.ob_config.basketball_config.category_id)
                    self.assertTrue(outright_tab_name, msg='Outrights tab is not available')
                    if outright_tab_name.upper() in list(
                            self.site.competition_league.tabs_menu.items_as_ordered_dict.keys()):
                        self.site.competition_league.tabs_menu.click_button(outright_tab_name.upper())
                        tab_content = self.site.competition_league.tab_content
                        tab_content.click()
                        self.site.wait_content_state(state_name='EventDetails')
                        return
                    else:
                        self.site.back_button_click()
                        self.site.basketball.tabs_menu.click_button(self.competitions_tab_name.upper())
                        self.site.wait_content_state('CompetitionLeaguePage')