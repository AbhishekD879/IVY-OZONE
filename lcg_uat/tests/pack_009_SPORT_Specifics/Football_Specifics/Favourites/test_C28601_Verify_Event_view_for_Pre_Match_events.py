import voltron.environments.constants as vec
import pytest
import tests
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
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.login
@vtest
class Test_C28601_Verify_Event_view_for_Pre_Match_events(BaseSportTest):
    """
    TR_ID: C28601
    NAME: Verify Event view for Pre-Match events
    DESCRIPTION: This Test Case verified Event view for Pre-Match events on Favourites page/widget
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event and log in
        """
        if self.cms_config.get_widgets(widget_type='favourites')[0]['disabled']:
            raise CmsClientException('"Favourites" widget is disabled in CMS')

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)

            self.__class__.eventID = events[0]['event']['id']
            self.__class__.event_name = normalize_name(events[0]['event']['name'])
            self.__class__.event_start_time = self.convert_time_to_local(
                date_time_str=events[0]['event']['startTime'],
                ob_format_pattern=self.ob_format_pattern,
                future_datetime_format=self.event_card_future_time_format_pattern,
                ss_data=True)
            self.__class__.league = self.get_accordion_name_for_event_from_ss(event=events[0])

            self._logger.info(f'*** Found football event with id "{self.eventID}", name "{self.event_name}", '
                              f'league "{self.league}" and start time "{self.event_start_time}"')

        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.eventID = event_params.event_id
            event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                   query_builder=self.ss_query_builder)
            self.__class__.event_name = normalize_name(event_resp[0]['event']['name'])
            self.__class__.event_start_time = self.convert_time_to_local(date_time_str=event_params.event_date_time,
                                                                         future_datetime_format=self.event_card_future_time_format_pattern)
            self.__class__.league = self.get_accordion_name_for_event_from_ss(event=event_resp[0])

        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        self.__class__.initial_prices = self.get_output_prices_values(
            section_name=self.league, event_id=self.eventID)

    def test_001_add_football_pre_match_event_to_favourites(self):
        """
        DESCRIPTION: Add Football Pre-Match event to Favourites
        """
        self.__class__.event = self.get_event_from_league(event_id=self.eventID, section_name=self.league)
        self.event.favourite_icon.click()
        self.assertTrue(self.event.favourite_icon.is_selected(),
                        msg=f'Favourites icon is not highlighted for event "{self.event_name}"')

    def test_002_navigate_to_favourite_matches_matches_widget(self):
        """
        DESCRIPTION: Navigate to 'Favourite Matches' matches/widget
        """
        if self.device_type == 'mobile':
            self.site.football.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            page_title = self.site.favourites.header_line.page_title.title
            self.assertEqual(page_title, vec.sb.FAVOURITE_MATCHES,
                             msg=f'Page title "{page_title}" doesn\'t match '
                                 f'expected text "{vec.sb.FAVOURITE_MATCHES}"')
        else:
            self.__class__.favorites_widget = self.site.favourites
            self.assertTrue(self.favorites_widget.is_displayed(), msg='"FAVORITES" widget is not displayed')
            self.favorites_widget.expand()
            self.assertTrue(self.favorites_widget.is_expanded(), msg='\'FAVORITES\' widget is not expanded')

    def test_003_verify_event_view_for_pre_match_event(self):
        """
        DESCRIPTION: Verify Event view for Pre-Match event
        EXPECTED: Pre-Match event contains:
        EXPECTED: - Fixture header (Home, Draw, Away)
        EXPECTED: - Primary Market Price/Odds buttons
        EXPECTED: - Event name
        EXPECTED: - Event time
        EXPECTED: - "+x Markets" link
        EXPECTED: - Favourite icon
        EXPECTED: All data is correct and corresponds to added event info
        """
        # Verify Event name
        if self.device_type == 'mobile':
            sections = self.site.favourites.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(sections, msg='Sections are not found')
            section = list(sections.values())[0]
            events = section.items_as_ordered_dict
        else:
            section = self.favorites_widget
            events = section.items_as_ordered_dict
        self.assertTrue(events, msg='Events are not found')
        self.assertIn(self.event_name, events.keys(),
                      msg=f'Event "{self.event_name}" not found in "{events.keys()}"')

        # Verify Fixture header (Home, Draw, Away)
        self.__class__.expected_fixture_header_1 = vec.sb.HOME
        self.__class__.expected_fixture_header_2 = vec.sb.DRAW
        self.__class__.expected_fixture_header_3 = vec.sb.AWAY
        self.verify_section_fixture_header(section=section)

        event = events.get(self.event_name)
        all_prices = [v.name for k, v in event.get_active_prices().items()]
        self.assertEqual(all_prices, list(self.initial_prices.values()),
                         msg=f'Current price "{all_prices}" is no the same '
                             f'as expected "{list(self.initial_prices.values())}"')

        # Verify Favourite icon
        self.assertTrue(event.favourite_icon.is_displayed(), msg=f'Favourite icon is not shown for "{self.event_name}"')

        # Verify Event time
        event_time = event.event_time

        self.assertEqual(event_time, self.event_start_time,
                         msg=f'Current "{event_time}" is not the same as expected "{self.event_start_time}"')

        # Verify "Markets" link
        event.click()
        self.site.wait_content_state(state_name='EventDetails')
        event_name_on_details_page = self.site.sport_event_details.event_title_bar.event_name
        expected_event_name = self.event_name.upper() if self.device_type == 'desktop' else self.event_name

        self._logger.info(f'*** Event name on details page: "{event_name_on_details_page}"')
        self.assertEqual(event_name_on_details_page, expected_event_name,
                         msg=f'Event name on details page "{event_name_on_details_page}" '
                             f'not match expected "{expected_event_name}"')
