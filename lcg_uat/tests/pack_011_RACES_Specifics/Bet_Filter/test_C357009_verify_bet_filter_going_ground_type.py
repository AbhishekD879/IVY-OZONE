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
class Test_C357009_Verify_Bet_Filter_Going_Ground_Type(BaseHorseRacingBetFilterTest):
    """
    TR_ID: C357009
    NAME: Verify Bet Finder Going Ground type
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Jira ticket:
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

    def test_001_verify_going_on_off(self):
        """
        DESCRIPTION: Verify Going ON/OFF
        EXPECTED: - Verify the proper ResultCount at 'Find Bets' button. Button should read "{count#} SELECTIONS FOUND" (beneath its label)
        EXPECTED: - Bet finder results should show data from http://api.racemodlr.com/cypher/coralTest1/0/ -- {"provenGoing": "Y"} param / {"provenGoing": "N"} param
        """
        self.get_bets()
        self.openBetFilterPage()
        self.verify_filters(filters=['Proven'] if self.brand == 'bma' else ['PROVEN'], unselect=False)

    def test_002_verify_filtering_plus_refresh_re_navigation(self):
        """
        DESCRIPTION: Verify filtering + refresh/re-navigation
        EXPECTED: - Filtering should be kept on refresh/re-navigation (after user navigated to Bet Finder Results page)
        """
        self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter='Proven' if self.brand == 'bma' else 'PROVEN'),
                        msg='[Going (ground type)] filter is not selected in case of clicking [Proven].')
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.horseracing_bet_filter.is_filter_selected(filter='Proven' if self.brand == 'bma' else 'PROVEN'),
                        msg='[Going (ground type)] filter is not selected in case of clicking [Proven].')

    def test_003_verify_filtering_plus_reset(self):
        """
        DESCRIPTION: Verify Filtering + Reset
        EXPECTED: - Filtering should clear on Reset
        """
        self.site.horseracing_bet_filter.reset_link.click()
        self.assertFalse(self.site.horseracing_bet_filter.is_filter_selected(filter='Proven' if self.brand == 'bma' else 'PROVEN', expected_result=False),
                         msg='[Going (ground type)] filter shouldn\'t be selected after clicking [Reset].')
        self.assertEqual(self.site.horseracing_bet_filter.read_number_of_bets(), self.get_number_of_bets(),
                         msg='Incorrect number of bets displayed on "Find Bets" button. AR: [%s] ER: [%s]'
                         % (self.site.horseracing_bet_filter.read_number_of_bets(), self.get_number_of_bets()))
