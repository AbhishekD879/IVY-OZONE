import pytest
import tests
from time import sleep
from crlat_siteserve_client.constants import OPERATORS, LEVELS, ATTRIBUTES
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.mobile_only
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C9346558_Verify_Change_Competition_selector_on_Football_Competition_Details_page(BaseSportTest):
    """
    TR_ID: C9346558
    NAME: Verify 'Change Competition' selector on Football Competition Details page
    DESCRIPTION: This test case verifies 'Change Competition' selector on Football competition details page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football landing page > Competitions tab
    PRECONDITIONS: 3. Expand any class accordion and click on any type
    PRECONDITIONS: **NOTE!**
    PRECONDITIONS: * To verify competitions (classes) that are displayed within 'Change competition' selector check values in **OX.competitionsMainClasses_football** and **OX.competitionsAZClasses_football** keys in Local Storage
    PRECONDITIONS: * To verify types that are displayed within specific competition (class) in 'Change competition' selector check request
    PRECONDITIONS: https:{environment}/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForClass/YY?translationLang=en&simpleFilter=type.hasOpenEvent:isTrue
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - current openbet version
    PRECONDITIONS: YY - competition (class) ID
    """
    keep_browser_open = True

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by DisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {
            f"{sport['event']['className']} - {sport['event']['typeName']}": int(sport['event']['typeDisplayOrder']) for
            sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def test_000_preconditions(self):
        """
       PRECONDITIONS: 1. Load Oxygen app
       PRECONDITIONS: 2. Navigate to Football landiC492062ng page > Competitions tab
       PRECONDITIONS: 3. Expand any class accordion and click on any type
       """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.football_config.category_id)
        query_builder = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      self.ob_config.football_config.category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))
        class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)

        self.__class__.sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query_builder,
                                                                          class_id=class_ids)
        response = ss_req.ss_class(class_id='', query_builder=query_builder)
        self.assertTrue(response, msg='No response from site server')
        for res in response:
            self.assertTrue(res['class']['hasOpenEvent'],
                            msg=f'No site server response with hasOpenEvent query parameter for {res}')
        sorted_leagues = self.sort_by_disp_order(sports_list=self.sports_list)
        self.__class__.expected_leagues_order = [item.replace('Football ', '') for item in sorted_leagues]
        self.__class__.section_name_list = 'International'
        self.navigate_to_page(name='sport/football')
        self.site.football.tabs_menu.click_button(
            button_name=self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                category_id=self.ob_config.football_config.category_id))
        self.__class__.competitions = self.site.football.tab_content.competitions_categories.items_as_ordered_dict
        self.assertTrue(self.competitions, msg='No competitions are present on page')
        competition = self.competitions.get(vec.siteserve.ENGLAND)
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=10)
        self.assertTrue(leagues, msg='No leagues are present on page')
        league = leagues.get(vec.siteserve.PREMIER_LEAGUE_NAME)
        league.click()
        self.site.wait_content_state_changed()
        self.site.wait_content_state(state_name='CompetitionLeaguePage')
        self.site.wait_splash_to_hide(5)
        sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections are present on page')

    def test_001_verify_displaying_change_competitions_selector(self):
        """
        DESCRIPTION: Verify displaying 'Change Competitions' selector
        EXPECTED: * Change Competitions' selector is displayed in the type name header
        EXPECTED: * Change Competitions' selector is tappable
        """
        change_competition_selector = self.site.competition_league.title_section.competition_selector_link.name
        self.assertEqual(change_competition_selector, vec.sb.CHANGE_COMPETITION,
                         msg=f'Competition header with Change Competition selector is not same'
                             f'Actual: "{change_competition_selector}" '
                             f'Expected: "{vec.sb.CHANGE_COMPETITION}"')

    def test_002_tap_change_competition_selector(self):
        """
        DESCRIPTION: Tap 'Change Competition' selector
        EXPECTED: * The chevron of the 'Change Competitions' selector changed
        EXPECTED: * 'Change Competition' selector is a cascaded list of competitions (classes)
        EXPECTED: * The list animates down the page after user taps on it
        EXPECTED: * The list corresponds to values from **OX.competitionsMainClasses_football** key in Local Storage
        EXPECTED: * Classes are displayed in Openbet display order
        EXPECTED: * 'A-Z Competitions' is displayed at the end of the list
        EXPECTED: * The class is tappable (to open/close accordion)
        EXPECTED: * The types are tappable
        EXPECTED: * The page is scrollable where there is more content available
        """
        self.site.competition_league.title_section.competition_selector_link.click()
        cookie_name = 'OX.competitionsMainClasses_football'
        cookie = self.get_local_storage_cookie_value_as_dict(cookie_name=cookie_name)
        self.assertTrue(cookie, msg="OX.competitionsMainClasses_football* key (Local Storage) is not displayed")
        sleep(3)
        a_z_competition_name = self.site.competition_league.a_z_competition_label.text
        self.assertTrue(a_z_competition_name,
                        msg=f'A-Z competition name label is not found on "Competitions" tab')
        a_z_competition_list = self.site.competition_league.a_z_competition_list.items_as_ordered_dict
        for league in a_z_competition_list.values():
            if not league.is_expanded():
                league.expand()
        if len(self.competitions) > 6:
            self.site.contents.scroll_to_bottom()

    def test_003_select_any_competitionclass_from_the_list_eg_england(self):
        """
        DESCRIPTION: Select any competition(class) from the list e.g. England
        EXPECTED: * Selected accordion is expanded
        EXPECTED: * Types that belong to selected competition are shown in Openbet display order
        """
        sorted_leagues = self.sort_by_disp_order(self.sports_list)
        self.__class__.expected_leagues_order_upper = [item.upper() for item in sorted_leagues]

        type_order_list = []
        section_name_list = self.section_name_list.upper()
        section = self.site.competition_league.competition_list.items_as_ordered_dict[section_name_list]
        self.assertTrue(section, msg=f'Competitions page does not have any "{section_name_list}" section')
        section.expand()
        if not section.is_expanded():
            section.expand()
        self.__class__.leagues = section.items_as_ordered_dict
        order = [item.upper() for item in list(self.leagues.keys())]
        for item in self.expected_leagues_order:
            if self.section_name_list in item:
                type_order_list.append(item.split("-")[1].strip().upper())
        for league in order:
            self.assertIn(league, type_order_list,
                          msg=f'Type IDs are not ordered by OpenBet display order (lowest display order at the top) "{league}" "{type_order_list}"')

    def test_004_select_any_type_eg_premier_league(self):
        """
        DESCRIPTION: Select any type e.g. Premier League
        EXPECTED: * 'Change Competitions' page is closed
        EXPECTED: * Corresponding competition details page is opened
        """
        league = list(self.leagues.values())[0]
        league.click()
        self.site.wait_content_state_changed(timeout=5)

    def test_005_tap_change_competition_selector_again(self):
        """
        DESCRIPTION: Tap 'Change Competition' selector again
        EXPECTED: * 'Change Competitions' page is closed
        EXPECTED: * The chevron of the 'Change Competitions' selector changed
        EXPECTED: * The underlying page is displayed
        """
        self.site.competition_league.title_section.competition_selector_link.click()

    def test_006_tap_change_competition_selector__tap_a_z(self):
        """
        DESCRIPTION: Tap 'Change Competition' selector > tap 'A-Z'
        EXPECTED: * List corresponds to values from **OX.competitionsAZClasses_football** key in Local Storage
        """
        a_z_competition_name = self.site.competition_league.a_z_competition_label.text
        self.assertTrue(a_z_competition_name,
                        msg=f'A-Z competition name label is not found on "Competitions" tab')
        cookie_name = 'OX.competitionsAZClasses_football'
        cookie = self.get_local_storage_cookie_value_as_dict(cookie_name=cookie_name)
        self.assertTrue(cookie, msg="OX.competitionsAZClasses_football* key (Local Storage) is not displayed")
