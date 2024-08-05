import pytest

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name
import voltron.environments.constants as vec


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod  # Cannot start event during test execution
# @pytest.mark.crl_hl
@pytest.mark.football
@pytest.mark.favourites
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.login
@vtest
class Test_C28598_Verify_Session_Storage(BaseSportTest):
    """
    TR_ID: C28598
    VOL_ID: C9697633
    NAME: Verify Session Storage
    DESCRIPTION: This Test Case verified Session Storage
    """
    keep_browser_open = True
    event = None
    username = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login into Invictus application, create event
        EXPECTED: User is logged in, event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0])
        self.__class__.section_name_live = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play_tab_slp=True)

        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username, async_close_dialogs=False)

    def test_001_tap_football_icon_from_the_sports_menu(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports menu
        """
        self.site.open_sport(name='FOOTBALL')

    def test_002_tap_on_the_favourite_matches_icon_star_icon_near_matchevent(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' icon (star icon) near match/event
        """
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        self.assertTrue(self.event, msg=f'Event "{self.event_name}" was not found')
        self.event.favourite_icon.click()
        self.assertTrue(self.event.favourite_icon.is_selected(), msg='Event favourite icon is not selected')

    def test_003_tap_on_the_favourite_button_on_page_header(self):
        """
        DESCRIPTION: Tap on the 'Favourite' button on page header
        EXPECTED: User has navigated to the 'Favourite Matches' page
        EXPECTED: Match/event displayed on the 'Favourite Matches' page
        """
        header_line = self.site.football.header_line
        counter = header_line.favourites_counter
        self.assertEqual(counter, '1', msg=f'Actual favourites counter is: {counter}, instead of "1"')
        header_line.go_to_favourites_page.click()
        self.site.wait_content_state(state_name='Favourites')
        page_title = self.site.favourites.header_line.page_title.title
        self.assertEqual(page_title, vec.sb.FAVOURITE_MATCHES,
                         msg='Page title "%s" doesn\'t match expected text "%s"'
                             % (page_title, vec.sb.FAVOURITE_MATCHES))
        self.verify_event_on_favourites_page()

    def test_004_match_with_favourite_matches_selection_has_started(self):
        """
        DESCRIPTION: Match with 'Favourite Matches' selection has started
        EXPECTED: Match with 'Favourite Matches' selection available, on the 'Favourite Matches' page until 12 hours after the match has started
        """
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.ob_config.make_event_live(market_id=self.ob_config.market_ids[self.eventID][market_short_name],
                                       event_id=self.eventID)
        self.navigate_to_page(name='sport/football')
        in_play_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                   self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(in_play_tab_name)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        current_tab = self.site.football.tabs_menu.current
        self.assertEqual(current_tab, in_play_tab_name,
                         msg='"%s" tab is not selected after click, active tab is "%s"'
                             % (in_play_tab_name, current_tab))
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name_live)
        self.assertTrue(self.event, msg='Event "%s" was not found' % self.event_name)
        self.assertTrue(self.event.favourite_icon.is_selected(), msg='Event favourite icon is not selected')

    def test_005_log_out(self):
        """
        DESCRIPTION: Log out
        """
        self.site.logout()

    def test_006_login_by_the_same_user(self):
        """
        DESCRIPTION: Login by the same user
        """
        self.site.login(username=self.username)

    def test_007_go_to_the_favourite_matches_page(self):
        """
        DESCRIPTION: Go to the 'Favourite Matches' page
        EXPECTED: Selections within the 'favourite matches' page is still displayed
        """
        self.navigate_to_page(name='favourites')
        page_title = self.site.favourites.header_line.page_title.title
        self.assertEqual(page_title, vec.sb.FAVOURITE_MATCHES,
                         msg='Page title "%s" doesn\'t match expected text "%s"'
                             % (page_title, vec.sb.FAVOURITE_MATCHES))
        self.verify_event_on_favourites_page()
