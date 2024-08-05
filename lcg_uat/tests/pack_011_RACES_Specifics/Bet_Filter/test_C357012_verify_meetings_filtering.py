import random
import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_011_RACES_Specifics.Bet_Filter.base_horseracing_bet_filter_test import BaseHorseRacingBetFilterTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_beta2
@pytest.mark.bet_filter
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C357012_Verify_Meetings_Filtering(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C357012
    NAME: Verify Meetings filtering
    DESCRIPTION: This test case verifies Meetings filtering at Bet Finder page
    """
    keep_browser_open = True

    def verify_filtering_by_combobox_value(self, option: str):
        """
        Verifies filtering by 'Meetings' check-box value.
        :param option: specifies check-box value
        """
        self.site.horseracing_bet_filter.meetings_drop_down.select_value(option.title())
        option_name = option.title() if self.brand == 'bma' else option.upper()
        self.assertTrue(self.site.horseracing_bet_filter.meetings_drop_down.is_option_selected(option_name),
                        msg=f'Selected option is not "{option_name}"')
        expected_number_of_bets = self.get_number_of_bets(course=option)
        result = wait_for_result(lambda: self.site.horseracing_bet_filter.read_number_of_bets() == expected_number_of_bets,
                                 name='Number of bets to change',
                                 timeout=3)
        self.assertTrue(result,
                        msg=f'Incorrect number of bets displayed on "Find Bets" button when selection "{option}". '
                        f'AR: [{self.site.horseracing_bet_filter.read_number_of_bets()}] ER: [{expected_number_of_bets}]')
        self.verify_number_of_bets(self.get_number_of_bets(course=option))

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

    def test_001_verify_meetings_filter(self):
        """
        DESCRIPTION: Verify Meetings filter
        EXPECTED: - goes above the other filters
        EXPECTED: - combobox with 'All meetings' value selected by default
        """
        self.get_bets()
        self.openBetFilterPage()
        self.assertTrue(self.site.horseracing_bet_filter.meetings_drop_down.is_option_selected(vec.bet_finder.ALL_MEETINGS),
                        msg=f'"{vec.bet_finder.ALL_MEETINGS}" is not selected by default')

    def test_002_verify_filtering_by_some_combobox_value(self):
        """
        DESCRIPTION: Verify filtering by some combobox value
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"course": "combobox_value"} param
        """
        options = self.site.horseracing_bet_filter.meetings_drop_down.available_options
        self.assertTrue(options, msg='No available options found')
        random_option = random.choice(options)
        self.__class__.option = random_option.title() if self.brand == 'bma' else random_option.upper()

        for option in options:
            if option == random_option:
                continue
            self.verify_filtering_by_combobox_value(option=option)

        self.verify_filtering_by_combobox_value(option=random_option)

    def test_003_verify_filtering_plus_refresh_re_navigation(self):
        """
        DESCRIPTION: Verify filtering + refresh/re-navigation
        EXPECTED: - Selected filters should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        self.assertTrue(self.site.horseracing_bet_filter.meetings_drop_down.is_option_selected(self.option),
                        msg=f'Selected option is not "{self.option}"')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.horseracing_bet_filter.meetings_drop_down.is_option_selected(self.option),
                        msg=f'Selected option is not "{self.option}"')

    def test_004_verify_filtering_plus_reset(self):
        """
        DESCRIPTION: Verify filtering + Reset
        EXPECTED: - Selected filters should clear on Reset
        """
        self.site.horseracing_bet_filter.reset_link.click()
        self.site.wait_splash_to_hide(3)
        self.assertTrue(self.site.horseracing_bet_filter.meetings_drop_down.is_option_selected(vec.bet_finder.ALL_MEETINGS),
                        msg=f'"{vec.bet_finder.ALL_MEETINGS}" is not selected by default')

        expected_number_of_bets = self.get_number_of_bets()
        self.assertEqual(self.site.horseracing_bet_filter.read_number_of_bets(), expected_number_of_bets,
                         msg='Incorrect number of bets displayed on "Find Bets" button. AR: [%s] ER: [%s]'
                             % (self.site.horseracing_bet_filter.read_number_of_bets(), expected_number_of_bets))
        self.verify_number_of_bets(self.get_number_of_bets())
