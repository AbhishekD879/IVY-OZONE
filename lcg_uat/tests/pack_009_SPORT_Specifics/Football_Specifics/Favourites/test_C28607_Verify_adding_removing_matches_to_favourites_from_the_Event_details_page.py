import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.event_details
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.login
@vtest
class Test_C28607_Verify_adding_removing_matches_to_favourites_from_the_Event_details_page(BaseSportTest):
    """
    TR_ID: C28607
    NAME: Verify adding/removing matches to favourites from the Event details page
    DESCRIPTION: This Test Case verified adding/removing matches to favourites from the Event details page
    """
    keep_browser_open = True
    event_name_2, event_name_3 = None, None
    sport_name = 'Football'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Load Invictus application
        DESCRIPTION: Login into app
        EXPECTED: Homepage is opened
        EXPECTED: User is logged in
        """
        if not self.get_favourites_enabled_status():
            raise CmsClientException(f'"Favourites" is not enabled for device type "{self.device_type}" in CMS')
        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=3)

            self.__class__.events = events

            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            self.__class__.event_name_2 = normalize_name(events[1]['event']['name'])
            self.__class__.event_name_3 = normalize_name(events[2]['event']['name'])
            self.__class__.eventID = events[0]['event']['id']
            self.__class__.eventID2 = events[1]['event']['id']
            self.__class__.eventID3 = events[2]['event']['id']

            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=events[0])
            self.__class__.league2 = self.get_accordion_name_for_event_from_ss(event=events[1])
            self.__class__.league3 = self.get_accordion_name_for_event_from_ss(event=events[2])
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
            self._logger.info(f'*** Created Football event "{self.event_name}"')

            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID2 = event_params.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID2,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.event_name_2 = normalize_name(event_resp[0]['event']['name'])
            self._logger.info(f'*** Created Football event "{self.event_name_2}"')

            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID3 = event_params.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID3,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.event_name_3 = normalize_name(event_resp[0]['event']['name'])
            self._logger.info(f'*** Created Football event "{self.event_name_3}"')

            section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
            self.__class__.league1 = self.__class__.league2 = self.__class__.league3 = section_name

        self._logger.info(f'*** First football event with name "{self.event_name}" from league "{self.league1}"')
        self._logger.info(f'*** Second football event with name "{self.event_name_2}" from league "{self.league2}"')
        self._logger.info(f'*** Third football event with name "{self.event_name_3}" from league "{self.league3}"')

        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

    def test_001_tap_football_icon_from_the_sports_menu(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu:
        EXPECTED: 'Football' landing page is opened
        EXPECTED: 'Favourite matches' functionality is included
        """
        self.site.open_sport(name=self.sport_name)
        self.site.wait_content_state(state_name='Football')

    def test_002_tap_event_team_a_v_team_b(self):
        """
        DESCRIPTION: Tap 'Event (Team A v Team B)'
        EXPECTED: 'Event (Team A v Team B) details page is opened
        EXPECTED: 'Favourite Matches' icon is displayed on Event details page
        """
        event = self.get_event_from_league(event_id=self.eventID, section_name=self.league1)
        event.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_003_tap_on_the_favourite_matches_icon_star_icon_near_match_event(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' icon (star icon) near match/event
        EXPECTED: Icon appeared in bold
        EXPECTED: Event added to the 'Favourite Matches' page
        """
        fav_icon = self.site.sport_event_details.favourite_icon
        fav_icon.click()
        self.assertTrue(fav_icon.is_selected(), msg='Favourite button is not selected after click')
        header_line = self.site.sport_event_details.header_line
        if self.device_type != 'desktop':
            count = header_line.favourites_counter
            self.assertTrue(count and int(count) == 1,
                            msg=f'The event "{self.event_name}" is not added to the "Favourite Matches" page')

            header_line.go_to_favourites_page.click()
            self.site.wait_content_state('Favourites', timeout=3)
            self.verify_event_on_favourites_page()
        else:
            events = self.site.favourites.items_as_ordered_dict
            self.assertTrue(events, msg='*** No one event was found')
            self.assertIn(self.event_name, events.keys(),
                          msg=f'Event "{self.event_name}" didn\'t added to the "Favourite Matches" page')

    def test_004_repeat_steps_1_2(self):
        """
        DESCRIPTION: Repeat steps 1-2
        """
        if self.device_type != 'desktop':
            self.site.favourites.back_button_click()
            self.site.sport_event_details.back_button_click()
        else:
            self.site.sport_event_details.header_line.back_button.click()
        self.site.wait_content_state(state_name='Football')
        current_tab_name = self.site.football.tabs_menu.current
        self.assertEqual(current_tab_name, self.expected_sport_tabs.matches,
                         msg=f'Current tab name "{current_tab_name}" is not '
                             f'the same as expected "{self.expected_sport_tabs.matches}"')

        event = self.get_event_from_league(event_id=self.eventID2, section_name=self.league2)
        event.click()
        self.site.wait_content_state(state_name='EventDetails')

        fav_icon = self.site.sport_event_details.favourite_icon
        fav_icon.click()
        self.assertTrue(fav_icon.is_selected(), msg='Favourite button is not selected after click')

        if self.device_type != 'desktop':
            counter = self.site.sport_event_details.header_line.favourites_counter
            self.assertEqual(int(counter), 2,
                             msg=f'The event "{self.event_name_2}" is not added to the "Favourite Matches" page')
        else:
            events = self.site.favourites.items_as_ordered_dict
            self.assertTrue(events, msg='*** No one event was found')
            self.assertIn(self.event_name_2, events.keys(),
                          msg=f'Event "{self.event_name_2}" is not added to the "Favourite Matches" page')

        self.site.sport_event_details.back_button_click()
        self.site.wait_content_state(state_name='Football')

        event = self.get_event_from_league(event_id=self.eventID3, section_name=self.league3)
        event.click()
        self.site.wait_content_state(state_name='EventDetails')

        fav_icon = self.site.sport_event_details.favourite_icon
        fav_icon.click()
        self.assertTrue(fav_icon.is_selected(), msg='Favourite button is not selected after click')

        if self.device_type != 'desktop':
            counter = self.site.sport_event_details.header_line.favourites_counter
            self.assertEqual(int(counter), 3,
                             msg=f'The event "{self.event_name_3}" is not added to the "Favourite Matches" page')

            self.site.sport_event_details.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            self.verify_event_on_favourites_page(expected_events=(self.event_name, self.event_name_2, self.event_name_3))
        else:
            events = self.site.favourites.items_as_ordered_dict
            self.assertTrue(events, msg='*** No one event was found')
            for event in (self.event_name, self.event_name_2, self.event_name_3):
                self.assertIn(event, events.keys(),
                              msg=f'Event "{event}" is not added to the "Favourite Matches" page')

    def test_005_tap_on_the_favourite_matches_icon_bold_star_icon_in_the_same_event_details_page(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' icon (bold star icon) in the same Event details page
        EXPECTED: Icon became not filled (not selected)
        EXPECTED: Event removed from the 'Favourite Matches' page
        """
        if self.device_type != 'desktop':
            self.site.favourites.back_button_click()
            self.site.wait_content_state(state_name='EventDetails')
        fav_icon = self.site.sport_event_details.favourite_icon
        fav_icon.click()
        self.assertFalse(fav_icon.is_selected(expected_result=False),
                         msg='Favourite button is not selected after click')

        if self.device_type != 'desktop':
            counter = self.site.sport_event_details.header_line.favourites_counter
            self.assertEqual(int(counter), 2,
                             msg=f'The event "{self.event_name_3}" is not removed from the "Favourite Matches" page')

            self.site.sport_event_details.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            self.verify_event_on_favourites_page(expected_events=(self.event_name, self.event_name_2))
        else:
            events = self.site.favourites.items_as_ordered_dict
            self.assertTrue(events, msg='*** No one event was found')
            for event in (self.event_name, self.event_name_2):
                self.assertIn(event, events.keys(),
                              msg=f'Event "{event}" is not added to the "Favourite Matches" page')
