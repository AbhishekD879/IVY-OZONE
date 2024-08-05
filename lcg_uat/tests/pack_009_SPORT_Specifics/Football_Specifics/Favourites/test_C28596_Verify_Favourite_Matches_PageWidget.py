import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.crl_hl
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.in_play
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.login
@vtest
class Test_C28596_Verify_Favourite_Matches_PageWidget(BaseSportTest):
    """
    TR_ID: C28596
    NAME: Verify 'Favourite Matches' Page/Widget
    DESCRIPTION: This Test Case verified ‘Favourite Matches’ page for both logged out and logged in users
    PRECONDITIONS: User is NOT logged in
    PRECONDITIONS: User can navigate to 'Favourite Matches' page by:
    PRECONDITIONS: - direct link /favourites
    PRECONDITIONS: - Favourites icon on Football Landing page
    PRECONDITIONS: - Favourites widget on tablet and desktop
    """
    keep_browser_open = True
    sport_name = 'Football'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create football event
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=1)

            self.__class__.eventID = events[0]['event']['id']
            self.__class__.event_name_1 = normalize_name(events[0]['event']['name'])

            self._logger.info(f'*** First football event with id "{self.eventID}" and name "{self.event_name_1}"')
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()

            self.__class__.eventID = event_params.event_id
            self.__class__.event_name_1 = event_params.team1 + ' v ' + event_params.team2

    def test_001_navigate_to_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Navigate to 'Favourite Matches' page/widget
        EXPECTED: 'Favourite Matches' page/widget is displayed
        """
        self.navigate_to_page(name='favourites')
        self.site.wait_content_state(state_name='Favourites')

    def test_002_verify_favourite_matches_page_elements(self):
        """
        DESCRIPTION: Verify 'Favourite Matches' page elements
        EXPECTED: *   Introductory text is displayed as follows: **"To view and add matches into your favourites, please log in into your account." ** (text is taken from CMS)
        EXPECTED: *   'Log In' button (text is taken from CMS)
        """
        login_button = self.site.favourites.login_button
        self.assertTrue(login_button.is_displayed(), msg='"Log In" button is not shown')

        has_please_login_text = self.site.favourites.please_login_text
        self.assertEqual(has_please_login_text, vec.sb.EXPECTED_PLEASE_LOGIN_TO_VIEW_FAVOURITES,
                         msg=f'Current message {has_please_login_text}'
                             f'is not equal to expected {vec.sb.EXPECTED_PLEASE_LOGIN_TO_VIEW_FAVOURITES}')

    def test_003_log_in_and_verify_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Log In and verify 'Favourite Matches' page/widget
        EXPECTED: *  Introductory text is displayed as follows: **"You currently have no favourites added. Browse through the matches currently available and add them to your favourite list."**
        EXPECTED: *  'Go to Matches' button
        EXPECTED: *  'Go to In-Play Matches' button
        """
        self.site.favourites.login_button.click()
        self.site.login(timeout_wait_for_dialog=2)
        self.assertEqual(self.site.favourites.info_label, vec.sb_desktop.NO_FAVOURITE_MATCHES,
                         msg=f'Current info text "{self.site.favourites.info_label}" is not equal to'
                             f'expected "{vec.sb_desktop.NO_FAVOURITE_MATCHES}"')
        self.assertTrue(self.site.favourites.go_to_matches_button.is_displayed(),
                        msg='"Go to Matches" button does not exist')
        self.assertTrue(self.site.favourites.go_to_in_play_matches.is_displayed(),
                        msg='"Go to In-Play Matches" button does not exist')

    def test_004_add_football_event_to_favourites_and_verify_favourite_matches_pagewidget(self):
        """
        DESCRIPTION: Add Football event to Favourites and verify 'Favourite Matches' page/widget
        EXPECTED: *  'Clear All Favourites' button
        EXPECTED: *  Added event is displayed on 'Favourite Matches' page/widget
        EXPECTED: *   Information text is displayed as follows: **"Browse through the matches currently available and add them to your favourite list."**
        EXPECTED: *  'Go to Matches' button
        EXPECTED: *  'Go to In-Play Matches' button
        """
        self.navigate_to_edp(event_id=self.eventID)
        fav_icon = self.site.sport_event_details.favourite_icon
        fav_icon.click()
        self.assertTrue(fav_icon.is_selected(), msg=f'Event favourite icon is not selected for "{self.event_name_1}"')

        header_line = self.site.sport_event_details.header_line
        header_line.go_to_favourites_page.click()

        sections = self.site.favourites.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Sections are not found')
        section = list(sections.values())[0]
        events = section.items_as_ordered_dict
        self.assertTrue(events, msg='Events are not found')
        self.assertTrue(self.event_name_1 in events.keys(),
                        msg=f'Event "{self.event_name_1}" not found in "{events.keys()}"')

        self.assertEqual(self.site.favourites.info_label, vec.favourites.BROWSE_FAVOURITE_MATCHES,
                         msg=f'Actual info text: "{self.site.favourites.info_label}" '
                             f'is no equal to expected: "{vec.favourites.BROWSE_FAVOURITE_MATCHES}"')

        self.assertTrue(self.site.favourites.go_to_matches_button.is_displayed(),
                        msg='"Go to Matches" button does not exist')
        self.assertTrue(self.site.favourites.go_to_in_play_matches.is_displayed(),
                        msg='"Go to In-Play Matches" button does not exist')

    def test_005_click_clear_all_favourites_button(self):
        """
        DESCRIPTION: Click 'Clear All Favourites' button
        EXPECTED: No events are displayed on 'Favourite Matches' page/widget
        """
        self.site.favourites.clear_all_favourites.click()
        result = wait_for_result(lambda: self.site.favourites.info_label == vec.sb_desktop.NO_FAVOURITE_MATCHES,
                                 name='favourite message to change',
                                 timeout=2)
        self.assertTrue(result, msg=f'Current info text "{self.site.favourites.info_label}" is not equal to '
                                    f'expected "{vec.sb_desktop.NO_FAVOURITE_MATCHES}"')

    def test_006_go_back_to_favourite_matches_pagewidget_and_click_go_to_matches_button(self):
        """
        DESCRIPTION: Go back to 'Favourite Matches' page/widget and click 'Go to Matches' button
        EXPECTED: User is navigated to Football->Matches->Today
        """
        self.site.favourites.go_to_matches_button.click()
        self.site.wait_content_state(state_name=self.sport_name)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                         msg=f'Active tab is "{current_tab}" but "{self.expected_sport_tabs.matches}" is expected')

    def test_007_go_back_to_favourite_matches_pagewidget_and_click_go_to_in_play_matches_button(self):
        """
        DESCRIPTION: Go back to 'Favourite Matches' page/widget and click 'Go to In-Play Matches' button
        EXPECTED: User is navigated to Football->In-Play
        """
        self.navigate_to_page(name='favourites')
        self.site.wait_content_state(state_name='Favourites')

        self.site.favourites.go_to_in_play_matches.click()
        self.site.wait_content_state(state_name=self.sport_name)
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, self.expected_sport_tabs.in_play,
                         msg=f'Active tab is "{current_tab}" but "{self.expected_sport_tabs.in_play}" is expected')
