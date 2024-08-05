import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.sports
@pytest.mark.handball
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.live_scores
@vtest
class Test_C13035461_Verify_Handball_Score_correctness_for_teams_with_names_in_brackets_on_Event_Details_page(BaseFeaturedTest, BaseSportTest):
    """
    TR_ID: C13035461
    NAME: Verify Handball Score correctness for teams with names in brackets on Event Details page
    DESCRIPTION: This test case verifies Scoreboard for teams with names in brackets on Event Details page
    PRECONDITIONS: 1) In order to have a Scores Sports event should be BIP
    PRECONDITIONS: 3) In order to get commentary for event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: Look at the attributes:
    PRECONDITIONS: *    **name** - to see event name that contains Points
    PRECONDITIONS: 4) Open Development tool ->Network-> XHR
    """
    keep_browser_open = True
    home_score_expected = '25'
    away_score_expected = '18'
    score = {'current': f'{home_score_expected}-{away_score_expected}'}
    league_name = None
    sport_name = vec.siteserve.HANDBALL_TAB.upper()

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        number_of_events = cms_config.get_max_number_of_inplay_event(
            sport_category=cls.sport_category)
        if number_of_events != cls.initial_number_of_events:
            cms_config.update_inplay_event_count(
                sport_category=cls.sport_category, event_count=int(cls.initial_number_of_events))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Go to OB and create Handball live event with name:
        DESCRIPTION: |Team A Name| ScoreA-ScoreB |Team B Name|
        EXPECTED: Event is successfully created
        """
        self.__class__.sport_category = self.ob_config.backend.ti.handball.category_id
        event_params = self.ob_config.add_handball_event_to_croatian_premijer_liga(
            score=self.score, is_live=True, perform_stream=True)
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
        self.__class__.event_name = f'{self.team1} v {self.team2}'
        self.__class__.initial_number_of_events = self.cms_config.get_max_number_of_inplay_event(
            sport_category=self.sport_category)
        self.cms_config.update_inplay_event_count(
            sport_category=self.sport_category, event_count=((int(self.initial_number_of_events)) + 10))
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False

        event = self.ss_req.ss_event_to_outcome_for_event(event_id=event_params.event_id, query_builder=self.ss_query_builder)

        self.__class__.league_name_in_play_sport_tab = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                 in_play_page_sport_tab=True)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Home')

    def test_002_go_to_sport_landing_page_in_play_tab(self):
        """
        DESCRIPTION: Go to:
        DESCRIPTION: 'Handball' landing page -> 'In Play' tab
        DESCRIPTION: OR
        DESCRIPTION: In Play page -> Handball Sport
        DESCRIPTION: OR
        DESCRIPTION: Handball Page ->In Play Module
        EXPECTED: Page is opened
        EXPECTED: List of Handball events is loaded
        """
        self.navigate_to_page(name='in-play/watchlive')
        self.site.wait_content_state(state_name='in-play')
        self.site.inplay.inplay_sport_menu.click_item(vec.siteserve.HANDBALL_TAB)
        self.site.wait_content_state(state_name='in-play')
        self.verify_active_sport_on_inplay_page(sport_name=vec.siteserve.HANDBALL_TAB)

    def test_003_choose_sport_event_with_live_scores_available_and_go_to_event_details_page(self):
        """
        DESCRIPTION: Choose Sport event with Live Scores available and go to Event details page
        EXPECTED: Event details page is opened
        """
        events = self.get_inplay_events(sport_name=self.sport_name, league_name=self.league_name_in_play_sport_tab, watch_live_page=False)
        self.assertTrue(events, msg=f'No events found')
        event = events.get(self.event_name)
        if not event:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state('in-play')
            events = self.get_inplay_events(sport_name=self.sport_name, league_name=self.league_name,
                                            watch_live_page=False)
            self.assertTrue(events, msg=f'No events found')
            event = events.get(self.event_name)
        self.assertTrue(event, msg=f'"{self.event_name}" is not found')
        self.__class__.home_score_actual = event.score_table.match_score.home_score
        self.assertTrue(self.home_score_actual, msg=f'Home score is not shown for "{self.event_name}"')
        self.__class__.away_score_actual = event.score_table.match_score.away_score
        self.assertTrue(self.away_score_actual, msg=f'Away score is not shown for "{self.event_name}"')
        if self.device_type == 'desktop':
            self.__class__.expected_event_name = self.event_name.upper() if not self.brand == 'ladbrokes' \
                else self.event_name.title()
        else:
            self.__class__.expected_event_name = self.event_name
        event.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_004_verify_score_displaying(self):
        """
        DESCRIPTION: Verify Score displaying
        EXPECTED: * Game and Set Scores are displayed between team names in the next format:
        EXPECTED: |Team A (Test A)| ScoreA - ScoreB |Team B (Test B)|
        EXPECTED: e.g. Yong Kong (e.g. Woman) 1 - 13 Matsuda (e.g. Men)
        EXPECTED: **For mobile:**
        EXPECTED: Event name and Scores are left aligned and are transferred to the second line if there is not enough space
        EXPECTED: **For desktop:**
        EXPECTED: Event name and Scores are left aligned and are truncated in case of long name
        """
        title_bar = self.site.sport_event_details.scoreboard_title_bar
        self.assertRegexpMatches(title_bar.home_team_name, r'[\D]+',
                                 msg=f'Home Score is showed in the event name "{title_bar.home_team_name}"')
        self.assertRegexpMatches(title_bar.away_team_name, r'[\D]+',
                                 msg=f'Home Score is showed in the event name "{title_bar.away_team_name}"')

        actual_full_event_name = title_bar.event_name
        expected_event_name = f'{self.team1} {self.home_score_expected} {self.away_score_expected} {self.team2}'
        self.assertEqual(actual_full_event_name, expected_event_name,
                         msg=f'Actual event name "{actual_full_event_name}" '
                             f'with team names and scores are not same as expected "{expected_event_name}"')

    def test_005_verify_score_correctness(self):
        """
        DESCRIPTION: Verify Score correctness
        EXPECTED: Scores correspond to values in event.name received in Response from SS for GET Request EventToOutcomeForEvent
        EXPECTED: No extra values are added to the scores
        """
        self.assertEqual(self.home_score_expected, self.home_score_actual,
                         msg=f'Actual score value {self.home_score_actual}'
                         f' for Home team is not the same as expected {self.home_score_expected}')
        self.assertEqual(self.away_score_expected, self.away_score_actual,
                         msg=f'Actual score value {self.away_score_actual}'
                         f' for Away team is not the same as expected {self.away_score_expected}')
