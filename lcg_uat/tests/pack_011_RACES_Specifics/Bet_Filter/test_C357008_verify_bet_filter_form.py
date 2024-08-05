import random

import pytest

from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Bet_Filter.base_horseracing_bet_filter_test import BaseHorseRacingBetFilterTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_beta2
@pytest.mark.medium
@pytest.mark.bet_filter
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C357008_Verify_Bet_Filter_Form(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C357008
    NAME: Verify Bet Finder Form
    DESCRIPTION: This test case verifies Form section at Bet Finder page
    """
    keep_browser_open = True
    filters = []

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Jira ticket:
        PRECONDITIONS: - HMN-2438 - Web: Apply UI to Bet Finder
        PRECONDITIONS: - HMN-2437 - Web: Filtering Logic for Bet Finder
        PRECONDITIONS: - HMN-2833 - Web: Amend Bet Finder
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

    def test_001_verify_filtering_by_course_and_distance_winnercheck_off_course_and_distance_winner_tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Course and Distance Winner.
        DESCRIPTION: Check off 'Course and Distance Winner' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"courseDistanceWinner": "Y"} param
        """
        self.get_bets()
        self.openBetFilterPage()
        self.verify_filters(filters=['Course and Distance Winner'] if self.brand == 'bma' else ['COURSE AND DISTANCE WINNER'])

    def test_002_verify_filtering_by_course_winnercheck_off_course_winner_tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Course Winner.
        DESCRIPTION: Check off 'Course Winner' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"courseWinner": "Y"} param
        """
        self.verify_filters(filters=['Course Winner'] if self.brand == 'bma' else ['COURSE WINNER'])

    def test_003_verify_filtering_by_winner_last_timecheck_off_winner_last_time_tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Winner Last Time.
        DESCRIPTION: Check off 'Winner Last Time' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"winnerLastTime": "Y"} param
        """
        self.verify_filters(filters=['Winner Last Time'] if self.brand == 'bma' else ['WINNER LAST TIME'])

    def test_004_verify_filtering_by_placed_last_timecheck_off_placed_last_time_tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Placed Last Time.
        DESCRIPTION: Check off 'Placed Last Time' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"placedLastTime": "Y"} param
        """
        self.verify_filters(filters=['Placed Last Time'] if self.brand == 'bma' else ['PLACED LAST TIME'])

    def test_005_verify_filtering_by_distance_winnercheck_off_distance_winner_tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Distance Winner.
        DESCRIPTION: Check off 'Distance Winner' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"distanceWinner": "Y"} param
        """
        self.verify_filters(filters=['Distance Winner'] if self.brand == 'bma' else ['DISTANCE WINNER'])

    def test_006_verify_filtering_by_winner_within_last_3check_off_winner_within_last_3__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Winner Within Last 3.
        DESCRIPTION: Check off 'Winner Within Last 3' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"winnerLast3Starts": "Y"} param
        """
        self.verify_filters(filters=['Winner Within Last 3'] if self.brand == 'bma' else ['WINNER WITHIN LAST 3'])

    def test_007_verify_filtering_by_placed_within_last_3check_off_placed_within_last_3__tap_find_bets(self):
        """
        DESCRIPTION: Verify filtering by Placed Within Last 3.
        DESCRIPTION: Check off 'Placed Within Last 3' > tap 'Find Bets'
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"placedLast3Starts": "Y"} param
        """
        self.verify_filters(filters=['Placed Within Last 3'] if self.brand == 'bma' else ['PLACED WITHIN LAST 3'])

    def test_008_verify_filtering_by_several_parameters(self):
        """
        DESCRIPTION: Verify filtering by several parameters
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button
        EXPECTED: - Verify Bet finder results by several parameters
        """
        number_of_filters_to_select = random.randint(2, len(self.site.horseracing_bet_filter.FORM))
        while len(self.filters) <= number_of_filters_to_select:
            filter = random.choice(self.site.horseracing_bet_filter.FORM)
            if filter not in self.filters:
                self.filters.append(filter.title().replace('And', 'and'))
            if len(self.filters) == 7:
                break

        self.verify_filters(self.filters, unselect=False)

    def test_009_verify_filtering_plus_refreshre_navigation(self):
        """
        DESCRIPTION: Verify filtering + refresh/re-navigation
        EXPECTED: - Filtering should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        self.assertTrue(all(self.site.horseracing_bet_filter.is_filter_selected(filter if self.brand == 'bma' else filter.upper()) for filter in self.filters),
                        msg='One or more filters are not selected in case of selecting multiple filters.')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(all(self.site.horseracing_bet_filter.is_filter_selected(filter if self.brand == 'bma' else filter.upper()) for filter in self.filters),
                        msg='One or more filters are not selected in case of selecting multiple filters.')

    def test_010_verify_filtering_plus_reset(self):
        """
        DESCRIPTION: Verify filtering + Reset
        EXPECTED: - Filtering should clear on Reset
        """
        self.site.horseracing_bet_filter.reset_link.click()
        for filter in self.site.horseracing_bet_filter.FORM:
            self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(filter=filter.title().replace('And', 'and') if self.brand == 'bma' else filter.upper(), expected_result=False),
                             msg='Filter [%s] is selected by default which is wrong.' % filter)
        self.assertEqual(self.site.horseracing_bet_filter.read_number_of_bets(), self.get_number_of_bets(),
                         msg='Incorrect number of bets displayed on "Find Bets" button. AR: [%s] ER: [%s]'
                             % (self.site.horseracing_bet_filter.read_number_of_bets(), self.get_number_of_bets()))
