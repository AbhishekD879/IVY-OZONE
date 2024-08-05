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
@pytest.mark.event_details
@pytest.mark.favourites
@pytest.mark.in_play
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C2745932_Verify_Event_view_for_In_Play_events(BaseSportTest):
    """
    TR_ID: C2745932
    VOL_ID: C9697940
    NAME: Verify Event view for In-Play events
    """
    sport_name = 'Football'
    keep_browser_open = True
    favourites_widget_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event and Login
        """
        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        self.__class__.favourites_widget_name = self.get_filtered_widget_name(cms_type='favourites')

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         in_play_event=True,
                                                         number_of_events=1)
            self.__class__.eventID = events[0]['event']['id']
            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=events[0], in_play=True)
        else:
            start_time = self.get_date_time_formatted_string(seconds=10)
            event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                     start_time=start_time)
            self.__class__.eventID = event_params.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])

            self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play_tab_slp=True)

        self._logger.info(
            f'*** Found/Created live football event "{self.eventID}" with name "{self.event_name}" and league "{self.section_name}"')

        self.site.login(username=tests.settings.betplacement_user)
        self.site.close_all_dialogs(async_close=False, timeout=11)

    def test_001_tap_football(self):
        """
        DESCRIPTION: Tap 'Football' icon from the Sports Menu Ribbon
        """
        self.site.open_sport(name=self.sport_name)

    def test_002_tap_in_play(self):
        """
        DESCRIPTION: Tap 'IN-PLAY' tab
        """
        expected_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play, self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, expected_sport_tab,
                         msg=f'In-Play tab is not active, active is "{active_tab}"')

    def test_003_tap_event(self):
        """
        DESCRIPTION: Tap 'Event (Team A v Team B)' and verify 'Event details' page is opened
        """
        event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name.split("-")[1].strip(), inplay_section=vec.inplay.LIVE_NOW_SWITCHER)
        event.click()

    def test_004_tap_favourite_icon(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' icon (star icon) and verify icon appeared in bold
        """
        self.site.wait_content_state(state_name='EventDetails')
        self.__class__.event_name = self.site.sport_event_details.event_title_bar.event_name_without_scores
        self._logger.info('*** Event name: "%s"' % self.event_name)
        fav_icon = self.site.sport_event_details.favourite_icon
        fav_icon.click()
        fav_icon_is_selected = fav_icon.is_selected(timeout=10)
        self.assertTrue(fav_icon_is_selected, msg="'Favourite Matches' icon (star icon) is not selected")

    def test_005_tap_favourite_matches_page_label(self):
        """
        DESCRIPTION: Tap on the 'Favourite Matches' page label and verify 'Favourite Matches' page is opened
        """
        if self.device_type == 'desktop':
            page_title = self.site.favourites.section_header.title_text
            self.assertEqual(page_title, self.favourites_widget_name,
                             msg=f'Page title "{page_title}" doesn\'t match '
                             f'expected text "{self.favourites_widget_name}"')
        else:
            self.site.sport_event_details.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            page_title = self.site.favourites.header_line.page_title.title
            self.assertEqual(page_title, vec.sb.FAVOURITE_MATCHES,
                             msg=f'Page title "{page_title}" doesn\'t match expected '
                             f'text "{vec.sb.FAVOURITE_MATCHES}"')

    def test_006_verify_event_view(self):
        """
        DESCRIPTION: Verify Favourites Event view for In-Play event:
        EXPECTED: Event contain event name
        EXPECTED: Current Score
        EXPECTED: Time elapsed
        """
        if self.device_type == 'desktop':
            events = self.site.favourites.items_as_ordered_dict
            self.assertTrue(events, msg='*** No one event was found')
            event_name, event = list(events.items())[0]
            self.assertEqual(event_name.upper(), self.event_name,
                             msg='Event name on Favourites page "%s" is not the same as on Event Details page "%s"'
                                 % (event_name.upper(), self.event_name))
        else:
            self.assertTrue(self.site.favourites.has_info_label, msg='No info label on Favourites page')
            self.assertEqual(self.site.favourites.info_label,
                             'Browse through the matches currently available and add them to your favourite list.')
            self.assertFalse(vec.sb_desktop.NO_FAVOURITE_MATCHES in self.site.favourites.info_label,
                             msg='"%s" message displayed on page' % vec.sb_desktop.NO_FAVOURITE_MATCHES)
            sections = self.site.favourites.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='*** No one section was found on page')
            section_name, section = list(sections.items())[0]
            events = section.items_as_ordered_dict
            self.assertTrue(events, msg='*** No one event was found in section "%s"' % section_name)
            event_name, event = list(events.items())[0]
            self.assertEqual(event_name, self.event_name,
                             msg='Event name on Favourites page "%s" is not the same as on Event Details page "%s"'
                                 % (event_name, self.event_name))
