import random
import pytest

from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Bet_Filter.base_horseracing_bet_filter_test import BaseHorseRacingBetFilterTest
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.bet_filter
@pytest.mark.desktop
@pytest.mark.races
@vtest
class Test_C357011_Verify_Star_Rating(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C357011
    NAME: Verify Star Rating
    DESCRIPTION: This test case verifies Star Rating at Bet Finder page
    """
    keep_browser_open = True

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

    def test_001_verify_select_star_rating_control(self):
        """
        DESCRIPTION: Verify Select Star Rating control
        EXPECTED: - 5 starts (unselected by default);
        EXPECTED: - Turn yellow once selected;
        EXPECTED: - If user selects 3* > selects 3* again => all the starts get unselected
        """
        self.get_bets()
        self.openBetFilterPage()
        self.__class__.rating = random.randint(1, 5)
        for rating in range(1, 6):
            if rating == self.rating:
                continue
            self.site.horseracing_bet_filter.set_stars_rating(rating)
            self.site.wait_splash_to_hide()
            result = wait_for_result(lambda: self.site.horseracing_bet_filter.get_star_rating() == rating,
                                     timeout=20,
                                     name='Start rating to change')
            self.assertTrue(result, msg=f'Incorrect number of stars are selected. '
                                        f'AR: "{self.site.horseracing_bet_filter.get_star_rating()}", ER: "{rating}"')

            expected_number_of_bets = self.get_number_of_bets(star=str(rating))
            delta = 2
            self.assertAlmostEqual(self.site.horseracing_bet_filter.read_number_of_bets(), expected_number_of_bets,
                                   delta=delta,
                                   msg=f'Star filters works incorrectly. '
                                       f'AR: "{self.site.horseracing_bet_filter.read_number_of_bets()}" '
                                       f'ER: "{expected_number_of_bets}" '
                                       f'Delta: "{delta}"')
            self.verify_number_of_bets(self.get_number_of_bets(star=str(rating)))

        self.site.horseracing_bet_filter.set_stars_rating(self.rating)
        self.verify_number_of_bets(self.get_number_of_bets(star=str(self.rating)))

    def test_002_verify_select_star_rating_plus_refresh_re_navigation(self):
        """
        DESCRIPTION: Verify Select Star Rating + refresh/re-navigation
        EXPECTED: - Select Star Rating should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        self.assertEqual(self.site.horseracing_bet_filter.get_star_rating(), self.rating,
                         msg=f'Incorrect number of stars are selected after re-navigation. '
                             f'AR: "{self.site.horseracing_bet_filter.get_star_rating()}", ER: "{self.rating}"')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        result = wait_for_result(
            lambda: self.site.horseracing_bet_filter.get_star_rating() == self.rating,
            name='Star rating is selected',
            timeout=5
        )
        self.assertTrue(result, msg=f'Incorrect number of stars are selected Actual: '
                                    f'"{self.site.horseracing_bet_filter.get_star_rating()}", Expected: "{self.rating}"')

    def test_003_verify_unselect_star_rating(self):
        """
        DESCRIPTION: Verify Select and Unselect Star Rating
        EXPECTED: - If user selects 3* > selects 3* again => all the starts get unselected
        """
        self.site.horseracing_bet_filter.set_stars_rating(self.rating)  # unselect
        self.site.wait_splash_to_hide()
        result = wait_for_result(
            lambda: self.site.horseracing_bet_filter.get_star_rating() == 0,
            name='Star rating is selected',
            timeout=5
        )
        self.assertTrue(result, msg=f'Incorrect number of stars are selected Actual: '
                                    f'"{self.site.horseracing_bet_filter.get_star_rating()}", Expected: "0"')

    def test_004_verify_select_star_rating_plus_reset(self):
        """
        DESCRIPTION: Verify Select Star Rating + Reset
        EXPECTED: - Select Star Rating should clear on Reset
        """
        self.site.horseracing_bet_filter.set_stars_rating(random.randint(1, 5))
        self.site.horseracing_bet_filter.reset_link.click()
        self.site.wait_splash_to_hide()
        result = wait_for_result(
            lambda: self.site.horseracing_bet_filter.get_star_rating() == 0,
            name='Star rating is selected',
            timeout=5
        )
        self.assertTrue(result, msg=f'Incorrect number of stars are selected Actual: '
                                    f'"{self.site.horseracing_bet_filter.get_star_rating()}", Expected: "0"')
