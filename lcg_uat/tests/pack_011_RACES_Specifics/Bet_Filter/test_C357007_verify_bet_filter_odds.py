import random
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Bet_Filter.base_horseracing_bet_filter_test import BaseHorseRacingBetFilterTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.lad_beta2
@pytest.mark.races
@pytest.mark.bet_filter
@pytest.mark.desktop
@pytest.mark.low
@vtest
class Test_C357007_Verify_Bet_Finder_Odds(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C357007
    NAME: Verify Bet Finder Odds
    DESCRIPTION: This test case verifies Odds range at Bet Finder page
    """
    keep_browser_open = True
    odds = []
    delta = 1

    def verify_odds(self, odds):
        for odds_filter in odds:
            self.site.horseracing_bet_filter.items_as_ordered_dict.get(odds_filter).click()
            self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(odds_filter),
                            msg=f'Filter "{odds_filter}" is not selected')
            expected_number_of_bets = self.get_number_of_bets(odds=[odds_filter])
            if expected_number_of_bets == 0:
                self.assertFalse(self.site.horseracing_bet_filter.find_bets_button.is_enabled(expected_result=False),
                                 msg=f'Find bets button with expected "{expected_number_of_bets}" events is still enabled')
                self.site.horseracing_bet_filter.items_as_ordered_dict.get(odds_filter).click()
                self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(filter=odds_filter, expected_result=False),
                                 msg=f'Filter "{odds_filter}" is selected')
            elif expected_number_of_bets <= self.delta and not self.site.horseracing_bet_filter.find_bets_button.is_enabled():
                actual_number_of_bets = self.delta
                self.assertAlmostEqual(actual_number_of_bets, expected_number_of_bets, delta=self.delta,
                                       msg=f'Filter "{odds_filter}" works incorrectly. '
                                           f'AR: "{actual_number_of_bets}" ER: "{expected_number_of_bets}" with delta "{self.delta}"')
                self.site.horseracing_bet_filter.items_as_ordered_dict.get(odds_filter).click()
                self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(filter=odds_filter, expected_result=False),
                                 msg=f'Filter "{odds_filter}" is selected')
            else:
                actual_number_of_bets = self.site.horseracing_bet_filter.read_number_of_bets()
                self.assertAlmostEqual(actual_number_of_bets, expected_number_of_bets, delta=self.delta,
                                       msg=f'Filter "{odds_filter}" works incorrectly. '
                                           f'AR: "{actual_number_of_bets}" ER: "{expected_number_of_bets}" with delta "{self.delta}"')
                self.verify_number_of_bets(self.get_number_of_bets(odds=[odds_filter]))
                self.site.horseracing_bet_filter.items_as_ordered_dict.get(odds_filter).click()
                self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(filter=odds_filter, expected_result=False),
                                 msg=f'Filter "{odds_filter}" is selected')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Jira tickets:
        PRECONDITIONS: - HMN-2438 - Web: Apply UI to Bet Finder
        PRECONDITIONS: - HMN-2437 - Web: Filtering Logic for Bet Finder
        PRECONDITIONS: Tst1 - http://api.racemodlr.com/cypher/coralTest1/0/
        PRECONDITIONS: Tst2 - http://api.racemodlr.com/cypher/coralTest2/0/
        PRECONDITIONS: Stage - http://api.racemodlr.com/cypher/coralStage/0/
        """
        cms_config = self.get_initial_data_system_configuration().get('BetFilterHorseRacing')
        if not cms_config:
            cms_config = self.cms_config.get_system_configuration_item('BetFilterHorseRacing')
        if not cms_config:
            raise CmsClientException('"BetFilterHorseRacing" is absent in CMS')
        if not cms_config.get('enabled'):
            raise CmsClientException('"Horseracing Bet Filter" is disabled')

    def test_001_verify_odds_section_view(self):
        """
        DESCRIPTION: Verify Odds section view
        EXPECTED: The next check-boxes labeled as:
        EXPECTED: - Odds On
        EXPECTED: - Evens - 7/2
        EXPECTED: - 4/1 - 15/2
        EXPECTED: - 8/1 - 14/1
        EXPECTED: - 16/1 - 28/1
        EXPECTED: - 33/1 or Bigger
        """
        self.get_bets()
        self.openBetFilterPage()
        odds_range = self.site.horseracing_bet_filter.items_as_ordered_dict
        self.assertTrue(odds_range, "No Odds found")
        for odds_button in vec.bet_finder.ODDS_LIST:
            self.assertIn(odds_button, odds_range.keys(),
                          msg=f'Incorrect odds filter caption found: "{odds_button}" in the "{odds_range.keys()}"')

    def test_002_verify_default_value(self):
        """
        DESCRIPTION: Verify default value
        EXPECTED: * None of the Odds check-boxes is checked
        """
        for odds_button in vec.bet_finder.ODDS_LIST:
            self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(odds_button, expected_result=False),
                             msg=f'Filter "{odds_button}" is selected by default, which is wrong')

    def test_003_verify_1_odds_selection(self):
        """
        DESCRIPTION: Verify 1 odds selection
        EXPECTED: * Verify proper "selection found" value is shown
        """
        self.odds = vec.bet_finder.ODDS_LIST
        self.verify_odds(self.odds)

    def test_004_verify_multiple_odds_selections(self):
        """
        DESCRIPTION: Verify multiple odds selections
        EXPECTED: * Verify proper "selection found" value is shown
        """
        odds_to_select = vec.bet_finder.ODDS_LIST.copy()
        number_of_filters_to_select = random.randint(2, len(odds_to_select))
        for item in range(0, number_of_filters_to_select):
            odds_button = random.choice(odds_to_select)
            odds_to_select.remove(odds_button)
            if odds_button not in self.odds:
                self.odds.append(odds_button)
        for odds_button in self.odds:
            self.site.horseracing_bet_filter.items_as_ordered_dict[odds_button].click()
            self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter=odds_button),
                            msg=f'Filter "{odds_button}" is not selected')
        expected_number_of_bets = self.get_number_of_bets(odds=self.odds)
        actual_number_of_bets = self.site.horseracing_bet_filter.read_number_of_bets()
        self.assertAlmostEqual(actual_number_of_bets, expected_number_of_bets, delta=self.delta,
                               msg=f'Multiple filtering works incorrectly. '
                                   f'AR: "{actual_number_of_bets}" ER: "{expected_number_of_bets}" with delta "{self.delta}"')

    def test_005_verify_odds_selection_plus_refresh_re_navigation(self):
        """
        DESCRIPTION: Verify odds selection + refresh/re-navigation and pressing Save button
        EXPECTED: * Selection should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        self.assertTrue(all(self.site.horseracing_bet_filter.is_filter_selected(odds) for odds in self.odds),
                        msg=f'One or more filters are not selected in case of selecting multiple filters')
        self.site.horseracing_bet_filter.save_selection_button.click()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(all(self.site.horseracing_bet_filter.is_filter_selected(odds) for odds in self.odds),
                        msg=f'One or more filters are not selected in case of selecting multiple filters')

    def test_006_verify_selection_plus_reset(self):
        """
        DESCRIPTION: Verify selection + Reset
        EXPECTED: * Selection should get cleared on Reset
        """
        self.site.horseracing_bet_filter.reset_link.click()
        for odds_button in vec.bet_finder.ODDS_LIST:
            self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(filter=odds_button, expected_result=False),
                             msg=f'Filter "{odds_button}" is selected by default, which is wrong')
        expected_number_of_bets = self.get_number_of_bets(odds=vec.bet_finder.ODDS_LIST)
        actual_number_of_bets = self.site.horseracing_bet_filter.read_number_of_bets()
        self.assertAlmostEqual(actual_number_of_bets, expected_number_of_bets, delta=self.delta,
                               msg=f'Multiple filtering works incorrectly. '
                                   f'AR: "{actual_number_of_bets}" ER: "{expected_number_of_bets}" with delta "{self.delta}"')
