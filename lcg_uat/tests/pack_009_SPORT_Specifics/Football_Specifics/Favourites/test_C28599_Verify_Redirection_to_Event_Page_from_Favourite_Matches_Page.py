import pytest

import tests
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.event_details
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.login
@pytest.mark.desktop
@vtest
class Test_C28599_Verify_Redirection_to_Event_Page_from_Favourite_Matches_Page(BaseSportTest):
    """
    TR_ID: C28599
    NAME: Verify Redirection to Event Page from Favourite Matches Page
    DESCRIPTION: This test case verifies redirection to Event page from 'Favourite Matches' page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events for test
        """
        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=2)

            self.__class__.eventID_1 = events[0]['event']['id']
            self.__class__.eventID_2 = events[1]['event']['id']

            self.__class__.event_name_1 = normalize_name(events[0]['event']['name'])
            self.__class__.event_name_2 = normalize_name(events[1]['event']['name'])
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_1 = event_params.event_id
            self.__class__.event_name_1 = event_params.team1 + ' v ' + event_params.team2

            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID_2 = event_params.event_id
            self.__class__.event_name_2 = event_params.team1 + ' v ' + event_params.team2

        self._logger.info(f'*** First football event with id "{self.eventID_1}" and name "{self.event_name_1}"')
        self._logger.info(f'*** Second football event with id "{self.eventID_2}" and name "{self.event_name_2}"')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_log_in_to_the_application(self):
        """
        DESCRIPTION: Log in to the application
        EXPECTED: The user is logged in successfully
        """
        self.site.login(username=tests.settings.betplacement_user)

    def test_003_tap_football_icon_on_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on Sports Menu Ribbon
        """
        self.site.open_sport(name='FOOTBALL')

    def test_004_add_several_events_to_favourite_matches_from_football_details_pages(self):
        """
        DESCRIPTION: Add several events to 'Favourite Matches' from Football Details pages
        """
        self.navigate_to_edp(event_id=self.eventID_1)
        fav_icon = self.site.sport_event_details.favourite_icon
        fav_icon.click()
        self.assertTrue(fav_icon.is_selected(), msg=f'Event favourite icon is not selected for "{self.event_name_1}"')

        self.navigate_to_edp(event_id=self.eventID_2)
        fav_icon = self.site.sport_event_details.favourite_icon
        fav_icon.click()
        self.assertTrue(fav_icon.is_selected(), msg=f'Event favourite icon is not selected for "{self.event_name_2}"')

    def test_005_tap_favourite_icon_from_match_centre_header_of_football_pages(self):
        """
        DESCRIPTION: Tap Favourite icon from Match Centre header of Football pages
        EXPECTED: 'Favourite Matches' page is opened
        """
        if self.device_type == 'mobile':
            header_line = self.site.sport_event_details.header_line
            counter = header_line.favourites_counter
            self.assertEqual(counter, '2', msg=f'Favourites counter is not "2" it is "{counter}"')
            header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            page_title = self.site.favourites.header_line.page_title.title
            self.assertEqual(page_title, vec.sb.FAVOURITE_MATCHES,
                             msg=f'Page title "{page_title}" doesn\'t match expected '
                                 f'text "{vec.sb.FAVOURITE_MATCHES}"')

            sections = self.site.favourites.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='Sections are not found')
            section = list(sections.values())[0]
            events = section.items_as_ordered_dict
            self.assertTrue(events, msg='Events are not found')
            self.assertTrue(self.event_name_1 in events.keys() and self.event_name_2 in events.keys(),
                            msg=f'One of events ["{self.event_name_1}" "{self.event_name_2}"] '
                                f'is not found in "{events.keys()}"')

            self.__class__.event = events[self.event_name_1]
        else:
            events = self.site.favourites.items_as_ordered_dict
            self.assertTrue(events, msg='*** No one event was found')
            self.assertEqual(len(events), 2, msg=f'Favourites counter is not "2" it is "{len(events)}"')
            self.__class__.event = events.get(self.event_name_1)
            self.assertTrue(self.event, msg=f'Event {self.event_name_1} not found in "{events.keys()}"')

    def test_006_click_on_any_event_name_displayed_on_favourite_matches_page(self):
        """
        DESCRIPTION: Click on any Event name displayed on 'Favourite Matches' page
        EXPECTED: The user is redirected to the appropriate Event Details page
        """
        self.event.click()
        self.site.wait_content_state(state_name='EventDetails')
        event_name_on_details_page = self.site.sport_event_details.event_title_bar.event_name
        self._logger.info(f'*** Event name on details page: "{event_name_on_details_page}"')
        event_name_1 = self.event_name_1.upper() if self.device_type == 'desktop' else self.event_name_1
        self.assertEqual(event_name_on_details_page, event_name_1,
                         msg=f'Event name on details page "{event_name_on_details_page}" '
                             f'does not match expected "{event_name_1}"')
