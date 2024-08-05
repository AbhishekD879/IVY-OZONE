from random import choice

import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.deeplink
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.high
@pytest.mark.slow
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C29009_Verify_Betslip_sections(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C29009
    NAME: Verify Betslip sections
    DESCRIPTION: This test case verifies Betslip sections
    PRECONDITIONS: Customer can view the Betslip logged in or logged out.
    PRECONDITIONS: Multiples may not be available after adding Special events to the Betslip depending on response from OB.
    PRECONDITIONS: Multiples are formed from selections from different events.
    """
    keep_browser_open = True
    race_event = None
    created_event_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Prepare 4 different sport events (football, basketball, volleyball, race)
        EXPECTED: User (logged in or not) should be able to use previously generated events.
        """
        if tests.settings.backend_env == 'prod':
            # Sports
            self.__class__.selection_ids = self.get_active_event_selections_for_category(category_id=self.ob_config.football_config.category_id)
            self._logger.info(f'*** Found Football event with selections "{self.selection_ids}"')

            self.__class__.selection_ids_2 = self.get_active_event_selections_for_category(
                category_id=self.ob_config.backend.ti.basketball.category_id)
            self.__class__.team2 = list(self.selection_ids_2.keys())[0]
            self._logger.info(f'*** Found Basketball event with selections "{self.selection_ids_2}"')

            self.__class__.selection_ids_3 = self.get_active_event_selections_for_category(
                category_id=self.ob_config.tennis_config.category_id)
            self.__class__.team1 = list(self.selection_ids_3.keys())[0]
            self._logger.info(f'*** Found Tennis event with selections "{self.selection_ids_3}"')

            # Races
            events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                         number_of_events=3, expected_template_market='Win or Each Way')

            for market in events[0]['event']['children']:
                if market['market']['templateMarketName'] == 'Win or Each Way' and market['market'].get('children'):
                    outcomes = market['market']['children']

            self.__class__.selection_name, self.__class__.race_selection_id = choice(list({i['outcome']['name']: i['outcome']['id'] for i in outcomes}.items()))

            for market in events[1]['event']['children']:
                if market['market']['templateMarketName'] == 'Win or Each Way' and market['market'].get('children'):
                    outcomes2 = market['market']['children']

            self.__class__.selection2_name, self.__class__.race_selection2_id = choice(list({i['outcome']['name']: i['outcome']['id'] for i in outcomes2}.items()))

            for market in events[2]['event']['children']:
                if market['market']['templateMarketName'] == 'Win or Each Way' and market['market'].get('children'):
                    outcomes3 = market['market']['children']

            self.__class__.selection3_name, self.__class__.race_selection3_id = choice(list({i['outcome']['name']: i['outcome']['id'] for i in outcomes3}.items()))

        else:
            self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids
            event_params = self.ob_config.add_basketball_event_to_autotest_league()

            self.__class__.team2, self.__class__.selection_ids_2 = event_params.team2, event_params.selection_ids
            event_params_3 = self.ob_config.add_volleyball_event_to_austrian_league()

            self.__class__.team1, self.__class__.selection_ids_3 = event_params_3.team1, event_params_3.selection_ids

            event = self.ob_config.add_UK_racing_event(number_of_runners=1)
            event_2 = self.ob_config.add_UK_racing_event(number_of_runners=1)
            event_3 = self.ob_config.add_UK_racing_event(number_of_runners=1)

            self.__class__.selection_name, self.__class__.race_selection_id = list(event.selection_ids.items())[0]
            self.__class__.selection2_name, self.__class__.race_selection2_id = list(event_2.selection_ids.items())[0]
            self.__class__.selection3_name, self.__class__.race_selection3_id = list(event_3.selection_ids.items())[0]

        self.site.login()

    def test_001_add_sport_selection_to_the_bet_slip(self, selection_ids=None):
        """
        DESCRIPTION: Add <Sport> selection to the Bet Slip
        EXPECTED: Bet Slip counter is 1
        """
        self.__class__.default_selection_name, selection_id = list(self.selection_ids.items())[-1]
        selection_ids = selection_ids if selection_ids else selection_id
        self.open_betslip_with_selections(selection_ids=selection_ids, timeout=5)

    def test_002_go_to_the_bet_slip(self, sport=True):
        """
        DESCRIPTION: Go to the Bet Slip
        EXPECTED: *  The 'Your Selections (1)' section is shown
        EXPECTED: *  Added selection is displayed
        """
        singles_section = self.get_betslip_sections().Singles
        self.assertEqual(singles_section.name, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Section title "{singles_section.name}" '
                         f'is not the same as expected "{vec.betslip.BETSLIP_SINGLES_NAME}"')
        self.assertEqual(self.get_betslip_content().selections_count, '1',
                         msg=f'Singles selection count "{self.get_betslip_content().selections_count}" '
                         f'is not the same as expected "1"')
        self.assertEqual(self.get_betslip_content().your_selections_label, vec.betslip.YOUR_SELECTIONS,
                         msg=f'Selection message "{self.get_betslip_content().your_selections_label}" '
                         f'is not the same as expected "{vec.betslip.YOUR_SELECTIONS}"')
        if sport:
            stake = singles_section.get(self.default_selection_name)
            self.assertTrue(stake, msg=f'{self.default_selection_name} stake was not found')

        if self.device_type in ['desktop', 'tablet']:
            self._logger.warning(f'*** Skipping clicking on close button '
                                 f'as this element is not present on "{self.device_name}"')
        else:
            self.get_betslip_content().close_button.click()

    def test_003_add_one_more_selection_from_another_sport_event(self, selection_ids=None):
        """
        DESCRIPTION: Add one more selection from another <Sport> event
        EXPECTED: Bet Slip counter is 2
        """
        selection_ids = selection_ids if selection_ids else self.selection_ids_2[self.team2]
        self.open_betslip_with_selections(selection_ids=selection_ids, timeout=15)

    def test_004_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to Bet Slip
        EXPECTED: *  Singles section is shown with a header 'Your Selections (2)'
        EXPECTED: * 'All single stakes' label and edit box appears in Singles section
        EXPECTED: *  The 'Multiples' section is shown right after 'Singles'
        EXPECTED: *  A list of available multiples bets is shown
        """
        sections = self.get_betslip_sections(multiples=True)
        singles_section, multiples_section = sections.Singles, sections.Multiples
        self.assertEqual(singles_section.name, vec.betslip.BETSLIP_SINGLES_NAME,
                         msg=f'Section title "{singles_section.name}" is not '
                         f'the same as expected "{vec.betslip.BETSLIP_SINGLES_NAME}"')

        betslip = self.get_betslip_content()
        self.assertEqual(betslip.selections_count, '2', msg=f'Singles selections count '
                         f'"{betslip.selections_count}" is not the same as expected "2"')
        self.assertEqual(betslip.your_selections_label, vec.betslip.YOUR_SELECTIONS,
                         msg=f'Selection message "{betslip.your_selections_label}" '
                         f'is not the same as expected "{vec.betslip.YOUR_SELECTIONS}"')
        if self.brand != 'ladbrokes':
            self.assertTrue(singles_section.has_all_stakes(), msg='"All single stakes" section is not shown')
            self.assertEqual(singles_section.all_stakes_label, vec.betslip.ALL_SINGLE_STAKES,
                             msg=f'Label "{singles_section.all_stakes_label}" '
                             f'is not the same as expected "{vec.betslip.ALL_SINGLE_STAKES}"')
        self.assertTrue(multiples_section.get('Double'), msg='"Multiples" section is not shown')

        stake_title, stake = list(multiples_section.items())[0]
        self.assertEqual(stake_title, vec.betslip.DBL, msg=f'Stake title "{stake_title}" '
                         f'is not the same as expected "{vec.betslip.DBL}"')
        if self.device_type in ['desktop', 'tablet']:
            self._logger.info(f'*** Skipping clicking on close button '
                              f'as this element is not present on "{self.device_name}"')
        else:
            self.get_betslip_content().close_button.click()

    def test_005_add_one_more_selections_from_another_sport_event(self, selection_ids=None):
        """
        DESCRIPTION: Add one more selections from another <Sport> event
        EXPECTED: Bet Slip counter is 3
        """
        selection_ids = selection_ids if selection_ids else self.selection_ids_3[self.team1]
        self.open_betslip_with_selections(selection_ids=selection_ids, timeout=10)

    def test_006_go_to_bet_slip(self):
        """
        DESCRIPTION: Go to Bet Slip
        EXPECTED: *  ACCA (3 selections) is shown under 'Singles'
        EXPECTED: *  Multiple which contains 1 Bet with all selections is shown within this section (e.g. Treble 1 Bets, Accumulator (4) 1 Bets)
        """
        section = self.get_betslip_sections(multiples=True).Multiples
        self.assertEquals(self.get_betslip_content().selections_count, '3',
                          msg=f'Selections count "{self.get_betslip_content().selections_count}" '
                          f'is not the same as expected "3"')
        self.assertEqual(self.get_betslip_content().your_selections_label, vec.betslip.YOUR_SELECTIONS,
                         msg=f'Selection message "{self.get_betslip_content().your_selections_label}" '
                         f'is not the same as expected "{vec.betslip.YOUR_SELECTIONS}"')

        stake_title, stake = list(section.items())[0]
        self.assertEqual(stake_title, vec.betslip.TBL, msg=f'Stake title "{stake_title}" '
                         f'is not the same as expected "{vec.betslip.TBL}"')
        if self.device_type in ['desktop', 'tablet']:
            self._logger.warning(f'*** Skipping clicking on close button '
                                 f'as this element is not present on "{self.device_name}"')
        else:
            self.get_betslip_content().close_button.click()

        self.site.open_betslip()
        self.clear_betslip()

    def test_007_provide_same_verifications_for_race_events(self):
        """
        DESCRIPTION: Provide same verifications for <Race> events
        """
        self.test_001_add_sport_selection_to_the_bet_slip(selection_ids=self.race_selection_id)
        self.test_002_go_to_the_bet_slip(sport=False)
        self.test_003_add_one_more_selection_from_another_sport_event(selection_ids=self.race_selection2_id)
        self.test_004_go_to_bet_slip()
        self.test_005_add_one_more_selections_from_another_sport_event(selection_ids=self.race_selection3_id)
        self.test_006_go_to_bet_slip()
