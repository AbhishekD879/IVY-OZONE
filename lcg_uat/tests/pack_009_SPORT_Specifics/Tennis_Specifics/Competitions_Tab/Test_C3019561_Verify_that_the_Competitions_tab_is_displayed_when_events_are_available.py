import pytest
import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C3019561_Verify_that_the_Competitions_tab_is_displayed_when_events_are_available(BaseSportTest):
    """
    TR_ID: C3019561
    NAME: Verify that the Competitions tab is displayed when events are available
    DESCRIPTION: Verify that the Competitions tab is displayed on the Tennis page when relevant events are available
    PRECONDITIONS: Competitions tab enabled in CMS
    PRECONDITIONS: Tennis Events in different classes/types are available
    PRECONDITIONS: **(!)** 'CompetitionsTennis' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def verify_events_are_present(self, resp):
        event = next((event for event in resp if
                      event.get('event') and event['event'] and event['event'].get('children')), None)
        if not event:
            raise SiteServeException(
                f'No active events found for category id "{self.ob_config.backend.ti.tennis.category_id}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add tennis events
        """
        tennis_category_id = self.ob_config.backend.ti.tennis.category_id
        if tests.settings.backend_env == 'prod':
            event1 = self.get_active_events_for_category(category_id=tennis_category_id)[0]
            self._logger.info(f'*** Found event: {event1}')
        else:
            self.check_sport_configured(tennis_category_id)
            self.ob_config.add_tennis_event_to_davis_cup()
            self.ob_config.add_tennis_event_to_european_open()

    def test_001_navigate_to_oxygen_fe_tennis_page(self):
        """
        DESCRIPTION: Navigate to Oxygen FE> Tennis Page
        EXPECTED: Competitions tab is available
        """
        self.site.open_sport(name='TENNIS', timeout=40)

        competitions = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                               category_id=self.ob_config.tennis_config.category_id,
                                               raise_exceptions=False)

        self.assertTrue(self.site.tennis.tabs_menu.items_as_ordered_dict.get(competitions).is_displayed(),
                        msg=f'"{competitions}" tab is not displayed')

    def test_002_tap_on_competitions_tab(self):
        """
        DESCRIPTION: Tap on Competitions tab
        EXPECTED: Competitions tab content is displayed
        """
        self.site.tennis.tabs_menu.click_button(
            button_name=self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                category_id=self.ob_config.tennis_config.category_id))

        if self.device_type == 'desktop':
            sections = self.site.tennis.tab_content.items_as_ordered_dict
        else:
            sections = self.site.tennis.tab_content.competitions_categories.items_as_ordered_dict
        self.assertTrue(sections, msg=f'No sections found')
