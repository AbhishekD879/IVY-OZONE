import pytest
from crlat_siteserve_client.siteserve_client import SiteServeRequests

import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.markets
@pytest.mark.scorecast
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28541_Verify_Scorecast_Section_1_Select_FirstLast_Goalscorer(BaseSportTest):
    """
    TR_ID: C28541
    NAME: Verify Scorecast Section 1 (Select First/Last Goalscorer)
    DESCRIPTION: This test case verifies the functionality of Scorecast market section within Football event details page.
    PRECONDITIONS: 1) In order to run this test scenario select event with market name "First Goal Scorecast" and/or "Last Goal Scorecast"
    PRECONDITIONS: 2) To get information for an event use the following url
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First Goalscorer"
    PRECONDITIONS: *   PROD: name="First Goal Scorer"
    """
    keep_browser_open = True
    ss_market_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event with Scorecast market
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('scorecast', {'cashout': True})])
        self.__class__.eventID = event_params.event_id
        market_ids_dict = self.ob_config.market_ids[self.eventID]
        self.__class__.marketIDs = [market_ids_dict[market_name] for market_name in
                                    ['first_goalscorer', 'last_goalscorer'] if market_name in market_ids_dict]
        self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.backend.ti.football.category_id)
        self.__class__.ss_event_details = ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                               query_builder=self.ss_query_builder)
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False

    def test_001_open_football_event_detail_page(self):
        """
        DESCRIPTION: Open Football Event Detail Page
        EXPECTED: Football Event Details page is opened
        """
        self.navigate_to_edp(self.eventID)

    def test_002_go_to_scorecast_market_section(self):
        """
        DESCRIPTION: Go to Scorecast market section
        EXPECTED: Scorecast market section is present and shown after 'Correct Score' market
        """
        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No markets are shown')

        self.__class__.scorecast = markets.get(self.expected_market_sections.scorecast)
        self.assertTrue(self.scorecast, msg='SCORECAST section is not found')

    def test_003_verify_section_1_select_first_last_goalscorer(self):
        """
        DESCRIPTION: Verify section 1 (Select First/Last Goalscorer)
        EXPECTED: Section 1 consists of:
        EXPECTED: * Scorer selector (two switchers)
        EXPECTED: * Team selector (two buttons)
        EXPECTED: * Player selector (drop-down list)
        """
        self.assertTrue(self.scorecast.first_scorer_tab, msg=f'First goalscorer is not visible')
        self.assertTrue(self.scorecast.last_scorer_tab, msg=f'Last goalscorer is not visible')
        self.assertTrue(len(self.scorecast.team_names) == 2,
                        msg=f'Team selector goalscorer buttons "{len(self.scorecast.team_names)}" '
                            f'is not equal to expected "2"')
        self.assertTrue(self.scorecast.player_scorers_list, msg=f'Player selector is not visible')

    def test_004_verify_scorer_selector(self):
        """
        DESCRIPTION: Verify Scorer selector
        EXPECTED: * Two options: **'First Scorer'** and **'Last Scorer'** are shown
        EXPECTED: * 'First Scorer' option is selected by default
        EXPECTED: * Selected option is highlighted
        """
        self.assertEqual(self.scorecast.first_scorer_tab.name, vec.sb.FIRST_GOALSCORER_SCORECAST,
                         msg=f'Actual first scorer tab "{self.scorecast.first_scorer_tab.name}" '
                             f'is not equal to expected "{vec.sb.FIRST_GOALSCORER_SCORECAST}"')
        self.assertEqual(self.scorecast.last_scorer_tab.name, vec.sb.LAST_GOALSCORER_SCORECAST,
                         msg=f'Actual last scorer tab "{self.scorecast.last_scorer_tab.name}" '
                             f'is not equal to expected "{vec.sb.LAST_GOALSCORER_SCORECAST}"')
        self.assertTrue(self.scorecast.first_scorer_tab.is_selected(),
                        msg=f'First scorer tab is not selected by default')

    def test_005_verify_team_selector(self):
        """
        DESCRIPTION: Verify Team selector
        EXPECTED: *   Two options: <Home Team> (first in the event name) and <Away Team> (second in the event name) are shown
        EXPECTED: *   <Home Team> is selected by default
        EXPECTED: *   Selected option is highlighted
        """
        self.assertTrue(self.scorecast.first_goalscorer_team_button.is_selected(),
                        msg=f'First goalscorer team button is not selected by default')
        self.assertEqual(self.scorecast.first_goalscorer_team_button.name, self.team1.upper(),
                         msg=f'Actual first goalscorer team name "{self.scorecast.first_goalscorer_team_button.name}, '
                             f'is not equal to created {self.team1.upper()}')

    def test_006_verify_firstplayer_to_scorelast_player_to_score_player_selectorname_depends_on_which_market_is_selected_in_scorer_selector_and_which_team_is_selected_in_team_selector_(self):
        """
        DESCRIPTION: Verify '**First Player to Score**'/'**Last Player to Score**' player selector
        DESCRIPTION: (name depends on which market is selected in Scorer selector and which team is selected in Team selector )
        EXPECTED: *   Drop-down contains the list of all players belonging to the selected team
        """
        self.__class__.ss_first_scorer_player_team1 = []
        self.__class__.ss_first_scorer_player_team2 = []

        self.__class__.ss_last_scorer_player_team1 = []
        self.__class__.ss_last_scorer_player_team2 = []

        ss_event_markets = self.ss_event_details[0]['event']['children']
        for market in ss_event_markets:
            if market['market']['id'] == self.marketIDs[0]:
                market_outcomes1 = market['market']['children']

            if market['market']['id'] == self.marketIDs[1]:
                market_outcomes2 = market['market']['children']

        for outcome in market_outcomes1:
            if outcome['outcome'].get('outcomeMeaningMinorCode') and \
                    outcome['outcome']['outcomeMeaningMinorCode'] == 'H':
                self.ss_first_scorer_player_team1.append(outcome['outcome']['name'])
                continue
            if outcome['outcome'].get('outcomeMeaningMinorCode') and \
                    outcome['outcome']['outcomeMeaningMinorCode'] == 'A':
                self.ss_first_scorer_player_team2.append(outcome['outcome']['name'])
                continue

        for outcome in market_outcomes2:
            if outcome['outcome'].get('outcomeMeaningMinorCode') and \
                    outcome['outcome']['outcomeMeaningMinorCode'] == 'H':
                self.ss_last_scorer_player_team1.append(outcome['outcome']['name'])
                continue
            if outcome['outcome'].get('outcomeMeaningMinorCode') and \
                    outcome['outcome']['outcomeMeaningMinorCode'] == 'A':
                self.ss_last_scorer_player_team2.append(outcome['outcome']['name'])
                continue

    def test_007_verify_drop_down_content_whenfirst_scorer_option_is_selected(self):
        """
        DESCRIPTION: Verify drop-down content when** 'First Scorer' **option is selected
        EXPECTED: All outcomes with attribute:
        EXPECTED: *   **outcomeMeaningMinorCode="H"** (if <Home Team> is selected)
        EXPECTED: OR
        EXPECTED: *   **outcomeMeaningMinorCode="A" **(if <Away Team> is selected)
        EXPECTED: of **'First Goalscorer'** market are shown
        """
        self.assertEqual(self.scorecast.player_scorers_list.available_options, self.ss_first_scorer_player_team1,
                         msg=f'Selection names {self.scorecast.player_scorers_list.available_options}'
                             f'are not the same as expected {self.ss_first_scorer_player_team1}')

        self.scorecast.last_goalscorer_team_button.click()
        self.assertTrue(self.scorecast.last_goalscorer_team_button.is_selected(),
                        msg=f'Last goalscorer tab is not selected')
        self.assertEqual(self.scorecast.last_goalscorer_team_button.name, self.team2.upper(),
                         msg=f'Actual last goalscorer team name "{self.scorecast.first_goalscorer_team_button.name}, '
                             f'is not equal to created {self.team2.upper()}')

        self.assertEqual(self.scorecast.player_scorers_list.available_options, self.ss_first_scorer_player_team2,
                         msg=f'Selection names {self.scorecast.player_scorers_list.available_options} '
                             f'are not the same as expected {self.ss_first_scorer_player_team2}')

    def test_008_verify_drop_down_content_whenlast_scoreroption_is_selected(self):
        """
        DESCRIPTION: Verify drop-down content when** 'Last Scorer' **option is selected
        EXPECTED: All outcomes with attribute:
        EXPECTED: *   **outcomeMeaningMinorCode="H"** (if <Home Team> is selected)
        EXPECTED: OR
        EXPECTED: *   **outcomeMeaningMinorCode="A" **(if <Away Team> is selected)
        EXPECTED: of **'Last Goalscorer'** market are shown
        """
        self.scorecast.last_scorer_tab.click()
        self.assertTrue(self.scorecast.last_scorer_tab.is_selected(), msg=f'Last scorer tab is not selected')

        self.assertEqual(self.scorecast.player_scorers_list.available_options, self.ss_last_scorer_player_team1,
                         msg=f'Selection names {self.scorecast.player_scorers_list.available_options} '
                             f'are not the same as expected {self.ss_last_scorer_player_team1}')

        self.scorecast.last_goalscorer_team_button.click()
        self.assertTrue(self.scorecast.last_goalscorer_team_button.is_selected(),
                        msg=f'Last goalscorer tab is not selected')

        self.assertEqual(self.scorecast.player_scorers_list.available_options, self.ss_last_scorer_player_team2,
                         msg=f'Selection names {self.scorecast.player_scorers_list.available_options} '
                             f'are not the same as expected {self.ss_last_scorer_player_team2}')

    def test_009_verify_selections_in_drop_down(self):
        """
        DESCRIPTION: Verify selections in drop-down
        EXPECTED: Each selection name corresponds to '**name**' attribute on the outcome level of verified Market
        """
        # Handled during test
        pass
