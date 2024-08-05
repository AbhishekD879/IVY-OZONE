import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C3020303_Verify_that_the_Competitions_tab_is_displayed_when_events_are_available_Basketball(BaseSportTest):
    """
    TR_ID: C3020303
    NAME: Verify that the Competitions tab is displayed when events are available Basketball
    DESCRIPTION: Verify that the Competitions tab is displayed on the Basketball page when relevant events are available
    PRECONDITIONS: Competitions tab enabled in CMS
    PRECONDITIONS: Basketball Events in different classes/types are available
    PRECONDITIONS: **(!)** 'CompetitionsBasketball' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
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

    def test_001_navigate_to_oxygen_fe_basketball_page(self):
        """
        DESCRIPTION: Navigate to Oxygen FE> Basketball Page
        EXPECTED: Competitions tab is available
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')

    def test_002_tap_on_competitions_tab(self):
        """
        DESCRIPTION: Tap on Competitions tab
        EXPECTED: Competitions tab content is displayed
        """
        self.__class__.competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.basketball_config.category_id)
        self.assertTrue(self.competitions_tab_name, msg='competition tab is not available')
        self.site.basketball.tabs_menu.click_button(self.competitions_tab_name.upper())

        section_name_list = self.section_name_list.upper() \
            if (self.brand == 'bma') or (self.brand == 'ladbrokes' and self.device_type == 'mobile') \
            else self.section_name_list
        if self.device_type == 'desktop':
            sections = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict
        else:
            sections = self.site.basketball.tab_content.all_competitions_categories.get_items(name=section_name_list)
        self.assertTrue(sections, msg=f'Competitions page does not have any "{self.section_name_list}" section')
