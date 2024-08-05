import time
import tests
import voltron.environments.constants as vec
import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException
from voltron.pages.shared.contents.competitions_league_page import CompetitionsOutrightsTabContent

from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests, exists_filter
from crlat_siteserve_client.utils.date_time import get_date_time_as_string


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.sports
@pytest.mark.tennis
@pytest.mark.desktop
@pytest.mark.high
@vtest
class Test_C9346561_Verify_Tennis_Competitions_Landing_Page_Functionality(BaseSportTest):
    """
    TR_ID: C9346561
    NAME: Verify Tennis Competitions Landing Page Functionality
    DESCRIPTION: This test case verified Tennis Competitions Landing Page Functionality
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to the Tennis Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Tennis' and put class ID's in 'InitialClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. To verify types that are available in the class please use the following link: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForClass/XXX?translationLang=en&simpleFilter=type.hasOpenEvent:isTrue
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: * XXX - class id
    PRECONDITIONS: **(!)** 'CompetitionsTennis' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def verify_events_are_present(self, resp):
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "{self.ob_config.backend.ti.tennis.category_id}"')

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by type typeDisplayOrder in ascending order otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {f"{sport['event']['categoryName']} - {sport['event']['typeName']}":
                            int(sport['event']['typeDisplayOrder']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add football event for specific league
        EXPECTED: Navigate to Football Competition page
        """
        tennis_category_id = self.ob_config.backend.ti.tennis.category_id
        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=tennis_category_id)[0]
            self._logger.info(f'*** Found event: {event1}')
        else:
            self.check_sport_configured(tennis_category_id)
            self.ob_config.add_tennis_event_to_davis_cup()
            self.ob_config.add_tennis_event_to_european_open()
            self.ob_config.add_tennis_event_to_nice_open()

            start_time = self.get_date_time_formatted_string(hours=6)
            self.ob_config.add_tennis_event_to_autotest_trophy(start_time=self.get_date_time_formatted_string(hours=1))
            self.ob_config.add_tennis_event_to_autotest_trophy(start_time=self.get_date_time_formatted_string(hours=2))

            self.ob_config.add_tennis_event_to_autotest_trophy(start_time=self.get_date_time_formatted_string(hours=3))
            self.ob_config.add_tennis_event_to_autotest_trophy(start_time=self.get_date_time_formatted_string(hours=4))

            if self.device_type == 'desktop':
                tomorrow = self.get_date_time_formatted_string(days=1)
                self.ob_config.add_tennis_event_to_autotest_trophy(start_time=tomorrow)

                future = self.get_date_time_formatted_string(days=7)
                self.ob_config.add_tennis_event_to_autotest_trophy(start_time=future)

            for outright in range(0, 4):
                outright_name = f'Outright {int(time.time())}'
                self.ob_config.add_tennis_outright_event_to_autotest_league(
                    event_name=outright_name, start_time=start_time)
        start_date = f'{get_date_time_as_string(days=-10)}T21:00:00.000Z'
        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS, str(tennis_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.GREATER_THAN_OR_EQUAL,
                                      start_date)) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.START_TIME, OPERATORS.LESS_THAN,
                                      f'{get_date_time_as_string(days=10)}T21:00:00.000Z')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME, OPERATORS.INTERSECTS, 'HH, MH, WH')) \
            .add_filter(exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME,
                                                                  OPERATORS.INTERSECTS, 'HH, MH, WH'))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_FALSE))
        class_ids = self.get_class_ids_for_category(category_id=tennis_category_id)

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=tennis_category_id)
        events_list = ss_req.ss_event_to_outcome_for_class(query_builder=query, class_id=class_ids)
        self.verify_events_are_present(resp=events_list)

        sorted_leagues = self.sort_by_disp_order(events_list)
        self.__class__.expected_leagues_order = [item.replace('Tennis - ', '') for item in sorted_leagues]
        if tests.settings.backend_env == 'prod':
            self.__class__.section_name_list = self.expected_leagues_order[0]
        elif self.device_type == 'mobile':
            self.__class__.section_name_list = 'Auto Test Trophy'
        else:
            self.__class__.section_name_list = tests.settings.tennis_autotest_competition_trophy

    def test_001_clicktap_on_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Competition' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' switcher is selected and highlighted
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        """
        self.site.open_sport(name='TENNIS')
        self.site.tennis.tabs_menu.click_button(
            button_name=self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                category_id=self.ob_config.tennis_config.category_id))

    def test_002_verify_ordering_of_the_leagues_types(self):
        """
        DESCRIPTION: Verify ordering of the leagues (types)
        EXPECTED: Type ID's are ordered by OpenBet display order (starting with lowest one)
        """
        if self.device_type == 'desktop':
            sections = self.site.tennis.tab_content.items_as_ordered_dict
        else:
            sections = self.site.tennis.tab_content.competitions_categories.items_as_ordered_dict
        self.assertTrue(sections, msg=f'No sections found')

        actual_order = list(sections.keys())
        for expected_league in self.expected_leagues_order:
            self.assertIn(expected_league, actual_order, msg=f'\nActual leagues order: "{actual_order}" '
                                                             f'\nExpected leagues order: "{expected_league}"')

    def test_003_clicktap_on_any_league_type_from_the_list(self):
        """
        DESCRIPTION: Click/Tap on any League (Type) from the list
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 2 tabs (navigation buttons) on the page: 'Matches', 'Outrights' (if Outrights (or Matches) are not available for Type tabs won't be displayed)
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: **For Desktop:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 'Matches and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default
        """
        if self.device_type == 'desktop':
            leagues = self.site.tennis.tab_content.items_as_ordered_dict
        else:
            leagues = self.site.tennis.tab_content.competitions_categories.get_items(name=self.section_name_list)
        self.assertTrue(leagues, msg=f'Competitions page does not have any "{self.section_name_list}" section')
        league = leagues.get(self.section_name_list)
        self.assertTrue(league, msg=f'Cannot find "{self.section_name_list}" section on Competitions page')
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

        if self.device == 'mobile':
            coral_title = self.site.competition_league.header_line.page_title.title
            self.assertEqual(coral_title, self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper(),
                             msg=f'Actual title "{coral_title}" is not equal to expected title'
                                 f'"{self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions.upper()}"')
            competition_name = self.site.competition_league.title_section.type_name.text
            self.assertEqual(competition_name, self.section_name_list,
                             msg=f'Competition header with competition name is not same '
                                 f'Actual: "{competition_name}" '
                                 f'Expected: "{self.section_name_list}"')
        change_competition_selector = self.site.competition_league.title_section.competition_selector_link.name
        self.assertEqual(change_competition_selector, vec.sb.CHANGE_COMPETITION,
                         msg=f'Competition header with Change Competition selector is not same'
                             f'Actual: "{change_competition_selector}" '
                             f'Expected: "{vec.sb.CHANGE_COMPETITION}"')

        events_in_tab = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(events_in_tab, msg='Matches tab has no content')

        if self.device_type == 'mobile':
            tab_content = self.site.competition_league.tab_content
            current_tab_content = self.site.competition_league.current_tab_content
            if not tab_content.has_no_events_label():
                if current_tab_content is CompetitionsOutrightsTabContent:
                    tab_content.click()
                else:
                    sections = tab_content.accordions_list.items_as_ordered_dict
                    self.assertTrue(sections, msg='No events sections are present on page')
        market_tab = None
        if tests.settings.backend_env == 'prod':
            market_tab = self.site.tennis.tab_content.accordions_list.items
            if len(market_tab) == 0:
                market_tab = self.site.tennis.tab_content.grouping_buttons.items_as_ordered_dict
        else:
            expected_tabs = [vec.sb.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                             vec.sb.SPORT_TABS_INTERNAL_NAMES.outrights.upper()]
            market_tab = self.site.tennis.tab_content.grouping_buttons.items_as_ordered_dict
            for tab_name in list(market_tab):
                self.assertIn(tab_name.upper(), expected_tabs, msg=f'Competition tab is not loaded with sections.'
                                                                   f'Actual: "{list(market_tab)}",'
                                                                   f'Expected: "{expected_tabs}"')
        self.assertTrue(market_tab, msg='Matches/ Outright tab is not present for event type in Competition')
