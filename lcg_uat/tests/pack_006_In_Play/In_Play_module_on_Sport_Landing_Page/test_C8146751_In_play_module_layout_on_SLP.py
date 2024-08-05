
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import get_in_play_module_from_ws, normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.football
@pytest.mark.mobile_only
@vtest
class Test_C8146751_In_play_module_layout_on_SLP(BaseSportTest):
    """
    TR_ID: C8146751
    VOL_ID: C10548290
    NAME: 'In-play' module layout on SLP
    DESCRIPTION: This test case verifies 'In-play' module layout on <Sport> Landing Page
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: * 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: * 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: * 'In-play' module is set to 'Active'
    PRECONDITIONS: * Inplay event count' is set to any digit e.g. 10
    PRECONDITIONS: 2) In-play events should be present for selected sport e.g. Football
    PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: Open 'Matches' tab
    """
    keep_browser_open = True
    tab_name = vec.sb.IN_PLAY

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In-play events should be present for selected sport e.g. Football
        PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
        PRECONDITIONS: Open 'Matches' tab
        """
        inplay_module = self.get_initial_data_system_configuration().get('Inplay Module', {})
        if not inplay_module:
            inplay_module = self.cms_config.get_system_configuration_item('Inplay Module')
        if not inplay_module.get('enabled'):
            raise CmsClientException('"Inplay Module" module is disabled on system config')
        inplay_module = self.cms_config.get_sport_module(sport_id=self.ob_config.backend.ti.football.category_id,
                                                         module_type='INPLAY')
        if inplay_module[0]['disabled']:
            raise CmsClientException('"In play module" module is disabled for Football category')
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')

        flatten_names = []
        try:
            in_play_module_data = get_in_play_module_from_ws(delimiter='42/16,')['data']
            for sport_segment in in_play_module_data:
                if sport_segment['categoryName'] == 'Football':
                    for league in sport_segment.get('eventsByTypeName'):
                        events = league.get('events')
                        if not events:
                            continue
                        event = events[0]
                        self.__class__.league_name = event['typeName'].upper() if self.brand == 'ladbrokes' else event['typeName']
                        event_name = event['name'].replace(' vs ', ' v ')
                        flatten_names.append(event_name)
                        self._logger.info(f'*** Found event "{event_name}" in league "{self.league_name}"')
                        break
            self._logger.info(f'*** Found events in In-Play module: {flatten_names}')
        except KeyError:
            pass

        if flatten_names:
            self.__class__.event_name = normalize_name(flatten_names[-1])
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.event_name = event_params.team1 + ' v ' + event_params.team2

            self.__class__.league_name = tests.settings.football_autotest_competition_league.upper() if self.brand == 'ladbrokes' \
                else tests.settings.football_autotest_competition_league

        self.verify_last_football_tab(tab=self.expected_sport_tabs.matches)

    def test_001_verify_in_play_module_layout(self):
        """
        DESCRIPTION: Verify 'In-Play' module layout
        EXPECTED: 'In-Play' module consists of:
        EXPECTED: * In-Play header
        EXPECTED: * Type containers
        EXPECTED: * Event cards
        """
        self.__class__.in_play_module = self.site.football.tab_content.in_play_module
        self.assertTrue(self.in_play_module.is_displayed(), msg='In play module does not display')
        self.assertTrue(self.in_play_module.has_in_play_header(), msg='There is no "In Play" header on the page')
        # Verification of Type containers is checked in 3 step
        self.assertTrue(self.in_play_module.items_as_ordered_dict, msg='There is no Event cards on the page')

    def test_002_verify_in_play_module_header(self):
        """
        DESCRIPTION: Verify 'In-Play' module header
        EXPECTED: 'In-Play' module header contains:
        EXPECTED: * 'In-Play' text
        EXPECTED: * 'See all (XX)>' link
        """
        self.assertEqual(self.in_play_module.name, self.tab_name,
                         msg=f'"In-Play" is not equal to "{self.in_play_module.name}"')
        self.assertTrue(self.in_play_module.has_see_all_link(), msg='No "See All" link')

    def test_003_verify_type_containers(self):
        """
        DESCRIPTION: Verify type containers
        EXPECTED: * Events are grouped by TypeID
        EXPECTED: * TypeName is displayed and corresponds to 'typeName' attribute
        EXPECTED: * Home/Draw/Away or 1/2 (depending on 3 or 2 way primary market) displayed
        """
        self.__class__.leagues = self.in_play_module.items_as_ordered_dict
        self.assertIn(self.league_name, self.leagues.keys(), msg=f'Autotest league is not displayed in the {self.leagues.keys()}')

        self.__class__.league = self.leagues.get(self.league_name)
        self.assertTrue(self.league, msg=f'No "{self.league_name}" league name on the page')

        # If event is displayed in this league it is automatically verifies that events are grouped by TypeID
        self.assertEqual(self.league.fixture_header.header1, vec.sb.HOME,
                         msg=f'Actual fixture header "{self.league.fixture_header.header1}" does not '
                         f'equal  expected "{vec.sb.HOME}"')
        self.assertEqual(self.league.fixture_header.header2, vec.sb.DRAW,
                         msg=f'Actual fixture header "{self.league.fixture_header.header2}" does not '
                         f'equal  expected "{vec.sb.DRAW}"')
        self.assertEqual(self.league.fixture_header.header3, vec.sb.AWAY,
                         msg=f'Actual fixture header "{self.league.fixture_header.header3}" does not '
                         f'equal  expected "{vec.sb.AWAY}"')

    def test_004_verify_event_card_elements(self):
        """
        DESCRIPTION: Verify event card elements
        EXPECTED: * Team names/players names
        EXPECTED: * Live/Watch live icons (if available)
        EXPECTED: * Scores (if available)
        EXPECTED: * Match time (if available)
        EXPECTED: * Fav icon (Football only)
        EXPECTED: * Price/odds buttons
        """
        events = self.league.items_as_ordered_dict
        self.assertIn(self.event_name, events.keys(),
                      msg=f'Event "{self.event_name}" is not present in events list "{events.keys()}"')
        test_event = events[self.event_name]
        if self.brand != 'ladbrokes':
            self.assertTrue(test_event.favourite_icon.is_displayed(), msg='No fav icon')
        self.assertIn(test_event.first_player, self.event_name,
                      msg=f'First player name "{test_event.first_player}" is not present in "{self.event_name}"')
        self.assertIn(test_event.second_player, self.event_name,
                      msg=f'Second player name "{test_event.second_player}" is not present in "{self.event_name}"')
        self.assertTrue(test_event.has_watch_live_icon, msg='No watch live icon')

        actual_buttons = test_event.template.items_as_ordered_dict
        self.assertTrue(actual_buttons, msg=f'No Price/Odds buttons found')
        for price_button_name, price_button in actual_buttons.items():
            self.assertTrue(price_button.is_displayed(),
                            msg=f'Primary Market Price/Odds button "{price_button_name}" is not displayed')
