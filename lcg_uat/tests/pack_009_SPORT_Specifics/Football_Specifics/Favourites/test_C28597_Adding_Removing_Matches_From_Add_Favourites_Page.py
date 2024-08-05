import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # Coral Only
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.high
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.in_play
@pytest.mark.sports
@pytest.mark.login
@pytest.mark.desktop
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-50433')
class Test_C28597_Adding_Removing_Matches_From_Add_Favourites_Page(BaseSportTest):
    """
    TR_ID: C28597
    NAME: Verify adding/removing matches to favourites from 'Add Favourite' page
    """
    keep_browser_open = True

    def verify_favorite_counter_change(self, expected_counter: int, event_name: str = None):
        if self.device_type == 'mobile':
            wait_for_result(lambda: int(self.site.football.header_line.favourites_counter) == expected_counter,
                            timeout=2,
                            name='Favorite counter to change')
            counter = self.site.football.header_line.favourites_counter
        else:
            self.site.favourites.expand()
            sections = self.site.favourites.items_as_ordered_dict
            counter = len(sections)

            if expected_counter == 0:
                self.assertFalse(sections, msg='Favourites widget is not empty')
            else:
                self.assertTrue(sections, msg='No selections found on Favourites widget')

                event = sections.get(event_name)
                self.assertTrue(event, msg=f'Event: "{event_name}" not found among: {list(sections.keys())}')

        self.assertEqual(int(counter), expected_counter,
                         msg=f'Actual favourites counter {int(counter)} != "{expected_counter}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login and create event
        """
        favourites_enabled_status = self.get_favourites_enabled_status()
        if not favourites_enabled_status:
            raise CmsClientException(f'"Favourites" is not enabled for device type "{self.device_type}" in CMS')

        self.__class__.football_category_id = self.ob_config.football_config.category_id
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.football_category_id,
                                                         number_of_events=1)

            self.__class__.eventID = events[0]['event']['id']
            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=events[0])

            self._logger.info(f'*** Found football event with name "{self.event_name}" and league "{self.section_name}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
            self._logger.info(f'*** Event name: "{self.event_name}"')

            start_time = self.get_date_time_formatted_string(seconds=10)
            event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time)
            self.__class__.eventID_live = event_params.event_id
            event_resp_live = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID_live,
                                                                        query_builder=self.ss_query_builder)
            self.__class__.event_name_live = normalize_name(event_resp_live[0]['event']['name'])
            self.__class__.event_off_time = event_params.event_date_time
            self._logger.info(f'*** Live event name: "{self.event_name_live}"')

            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
            self.__class__.section_name_on_inplay = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play_tab_slp=True)

        self.site.login()

    def test_001_tap_football(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        """
        self.site.open_sport(name=self.get_sport_title(self.football_category_id))

    def test_002_verify_favourite_match_page_label(self):
        """
        DESCRIPTION: Verify 'Favourite matches' functionality is included
        """
        if self.device_type == 'mobile':
            self.site.football.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            page_title = self.site.favourites.header_line.page_title.title
            self.assertEqual(page_title, vec.sb.FAVOURITE_MATCHES,
                             msg=f'Actual page title "{page_title}" != Expected "{vec.sb.FAVOURITE_MATCHES}"')
        else:
            self.__class__.favorites_widget = self.site.favourites
            self.assertTrue(self.favorites_widget.is_displayed(), msg='"FAVORITES" widget is not displayed')
            self.favorites_widget.expand()
            self.assertTrue(self.favorites_widget.is_expanded(), msg='\'FAVORITES\' widget is not expanded')

    def test_003_go_to_matches(self):
        """
        DESCRIPTION: Tap on the 'Go to Matches' button
        """
        if self.device_type == 'mobile':
            self.site.favourites.go_to_matches_button.click()
            self.site.wait_content_state(state_name='Football')
            page_title = self.site.football.header_line.page_title.title
            self.assertEqual(page_title, 'FOOTBALL',
                             msg=f'Actual page title "{page_title}" != Expected "FOOTBALL"')

    def test_004_tap_favourite_icon(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' icon (star icon)
        EXPECTED: Verify favourite event counter increased
        EXPECTED: Verify event is present on Favourites page
        """
        event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        event.favourite_icon.click()
        self.assertTrue(event.favourite_icon.is_selected(), msg='Event favourite icon is not selected')
        self.verify_favorite_counter_change(expected_counter=1, event_name=self.event_name)

        if self.device_type == 'mobile':
            self.site.football.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            self.verify_event_on_favourites_page()

    def test_005_remove_event_from_favourites(self):
        """
        DESCRIPTION: Repeat step 2-3
        EXPECTED: Tap on the 'Favourite Matches' icon (bold star icon) near the same Event
        EXPECTED: Verify event is removed from Favourites page and counter is 0
        """
        self.test_003_go_to_matches()
        # deselect event
        event = self.get_event_from_league(event_id=self.eventID,
                                           section_name=self.section_name)
        event.favourite_icon.click()
        self.assertFalse(event.favourite_icon.is_selected(expected_result=False),
                         msg='Event favourite icon is not deselected')
        self.verify_favorite_counter_change(expected_counter=0, event_name=self.event_name)

        if self.device_type == 'mobile':
            self.site.football.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            self.assertTrue(self.site.contents.has_info_label, msg='No info label displayed')
            actual_message = self.site.favourites.info_label
            self.assertEqual(actual_message, vec.sb_desktop.NO_FAVOURITE_MATCHES,
                             msg=f'Actual message "{actual_message}" != Expected "{vec.sb_desktop.NO_FAVOURITE_MATCHES}"')
        else:
            ui_introductory_text = self.site.favourites.widget_text_logged.strip()
            self.assertEqual(ui_introductory_text, vec.sb_desktop.NO_FAVOURITE_MATCHES,
                             msg=f'Introductory text \n"{ui_introductory_text}" is not the same as expected \n"{vec.sb_desktop.NO_FAVOURITE_MATCHES}"')

    def test_006_go_to_in_play_matches(self):
        """
        DESCRIPTION: Repeat step 2-3
        EXPECTED: Tap on 'Go to In Play Matches' button
        EXPECTED: Verify it is possible to navigate form Favourites page to Football In-Play events
        """
        if self.device_type == 'mobile':
            self.site.favourites.go_to_in_play_matches.click()
            self.site.wait_content_state(state_name='Football')
            current_tab_name = self.site.inplay.tabs_menu.current
            self.assertEqual(current_tab_name, self.expected_sport_tabs.in_play,
                             msg=f'"{self.expected_sport_tabs.in_play}" tab is not active, active tab is: "{current_tab_name}"')

    def test_007_verify_adding_favourites_from_inplay_page(self):
        """
        DESCRIPTION: Add favourite from In-Play page
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='sport/football/live')
            self.site.wait_content_state(state_name=self.get_sport_title(self.football_category_id).upper())

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.football_category_id,
                                                         in_play_event=True,
                                                         number_of_events=1)
            self.__class__.eventID_live = events[0]['event']['id']
            self.__class__.event_name_live = normalize_name(events[0]['event']['name'])
            self.__class__.section_name_on_inplay = self.get_accordion_name_for_event_from_ss(event=events[0], in_play=True)
            self._logger.info(f'*** Found live football event with name "{self.event_name_live}" '
                              f'and league "{self.section_name_on_inplay}"')

        self.__class__.event_name = self.event_name_live
        event = self.get_event_from_league(event_id=self.eventID_live,
                                           section_name=self.section_name_on_inplay)
        event.favourite_icon.click()
        self.assertTrue(event.favourite_icon.is_selected(), msg='Event favourite icon is not selected')

        self.verify_favorite_counter_change(expected_counter=1, event_name=self.event_name)

        if self.device_type == 'mobile':
            self.site.football.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            self.verify_event_on_favourites_page()

    def test_008_verify_removing_event_from_favourites_on_inplay_page(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' icon (bold star icon) near the same Event
        EXPECTED: Verify event is removed from Favourites page and counter is 0
        """
        if self.device_type == 'mobile':
            self.site.favourites.go_to_in_play_matches.click()
        event = self.get_event_from_league(event_id=self.eventID_live,
                                           section_name=self.section_name_on_inplay)
        event.favourite_icon.click()
        self.assertFalse(event.favourite_icon.is_selected(expected_result=False),
                         msg='Event favourite icon is not deselected')

        self.verify_favorite_counter_change(expected_counter=0, event_name=self.event_name)
        if self.device_type == 'mobile':
            self.site.football.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            self.assertTrue(self.site.favourites.has_info_label,
                            msg=f'No events found on Favourites page but "{vec.sb_desktop.NO_FAVOURITE_MATCHES}" text is not displayed')
