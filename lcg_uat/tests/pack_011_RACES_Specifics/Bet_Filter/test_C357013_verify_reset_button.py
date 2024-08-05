import random

import pytest
from voltron.utils.waiters import wait_for_result
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
class Test_C357013_Verify_Reset_Button(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C357013
    NAME: Verify Reset button
    DESCRIPTION: This test case verifies Reset button at Bet Finder page
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

    def test_001_verify_reset_button(self):
        """
        DESCRIPTION: Verify Reset button is at the breadcrumb and it resets all the filters to their default values.
        DESCRIPTION: Make some selections > Reset
        EXPECTED: - All the filters are at their default state;
        EXPECTED: - Bet finder results should show ALL the data from http://api.racemodlr.com/cypher/coralTest1/0/
        """
        # randomly click a couple of buttons
        self.get_bets()
        self.openBetFilterPage()
        filters = wait_for_result(lambda: list(self.site.horseracing_bet_filter.items_as_ordered_dict.values()))
        number_of_filters_to_select = random.randint(2, len(filters))
        list_ = []
        for _ in range(1, number_of_filters_to_select):
            filter_index = random.randint(0, len(filters) - 1)
            if filter_index in list_:
                continue
            list_.append(filter_index)
            filters[filter_index].click()
            self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filters[filter_index].name),
                            msg='Filters [%s] can\'t be selected.' % filters[filter_index].name)

        self.site.horseracing_bet_filter.reset_link.click()
        for filter_index in list_:
            self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(filter=filters[filter_index].name, expected_result=False),
                             msg='"Reset" link doesn\'t work correct: some filter remain selected.')

        expected_number_of_bets = self.get_number_of_bets()
        self.assertEqual(self.site.horseracing_bet_filter.read_number_of_bets(), expected_number_of_bets,
                         msg='Incorrect number of bets displayed on "Find Bets" button. (the text is not correct)')
        self.verify_number_of_bets(expected_number_of_bets)
