import tests
import voltron.environments.constants as vec
import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@vtest
class Test_C29035_Multiples_are_not_available(BaseBetSlipTest):
    """
    TR_ID: C29035
    NAME: Multiples are not available
    """
    keep_browser_open = True

    def verify_betslip_sections(self, expected_number_of_singles=1):
        betslip_sections = self.get_betslip_content().betslip_sections_list
        self.assertTrue(betslip_sections, msg='*** No bets found')
        self.assertTrue(vec.betslip.BETSLIP_SINGLES_NAME in betslip_sections.keys(), msg='SINGLES section is not found')
        stakes = betslip_sections[vec.betslip.BETSLIP_SINGLES_NAME].keys()
        self.assertTrue(stakes, msg='*** No Single stakes found')
        self.assertTrue(len(stakes) == expected_number_of_singles,
                        msg='Should be present %s Single stakes, but found %d' % (expected_number_of_singles, len(stakes)))

        self.assertTrue(vec.betslip.MULTIPLES not in betslip_sections.keys(),
                        msg=f'Section "{vec.betslip.MULTIPLES}" should not be displayed on BetSlip page')

    def test_001_load_invictus_application_and_create_event(self):
        """
        DESCRIPTION: Load Invictus application
        """
        if tests.settings.backend_env != 'prod':
            event_params = self.ob_config.add_autotest_premier_league_football_event(markets=[('last_goalscorer', {'cashout': True}),
                                                                                              ('extra_time_result', {'cashout': True})])
            selection_ids = event_params.selection_ids
            market_short_name = self.ob_config.football_config. \
                autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()

            self.__class__.selection_id_mr_1 = list(selection_ids[market_short_name].values())[0]
            self.__class__.selection_id_mr_2 = list(selection_ids[market_short_name].values())[1]
            self.__class__.selection_id_mr_3 = list(selection_ids[market_short_name].values())[2]

            self.__class__.selection_id_4 = list(selection_ids['last_goalscorer'].values())[0]
            self.__class__.selection_id_5 = list(selection_ids['extra_time_result'].values())[0]
        else:
            market_name = None
            event = self.get_active_events_for_category()[0]

            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children') if  market['market']['templateMarketName'] =='Match Betting' ), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')
            selections = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}

            self.__class__.selection_id_mr_1 = list(selections.values())[0]
            self.__class__.selection_id_mr_2 = list(selections.values())[1]
            self.__class__.selection_id_mr_3 = list(selections.values())[2]

            self.__class__.selection_id_4 = None
            for market in event['event']['children']:
                market_name = market['market']['templateMarketName']
                if market_name != 'Match Betting' and market['market'].get('children'):
                    self.__class__.selection_id_4 = market['market']['children'][0]['outcome']['id']
                    break

            self.__class__.selection_id_5 = None
            for market in event['event']['children']:
                if market['market']['templateMarketName'] not in ['Match Betting', market_name] and market['market'].get('children'):
                    self.__class__.selection_id_5 = market['market']['children'][0]['outcome']['id']
                    break

    def test_002_verify_the_betslip_without_added_selections(self):
        """
        DESCRIPTION: Verify the Betslip without added selections (e.g. see BetSlip widget on Tablet version or by tapping 'BetSlip' bubble on Mobile)
        EXPECTED: Betslip page does not contain any Multiples
        EXPECTED: Message displayed: "You have no selections in the slip."
        """
        # bet slip can't be opended if there are no bets
        # self.site.header.bet_slip_counter.click()
        # no_selections = self.get_betslip_content().no_selections_title
        # self.assertTrue(no_selections, msg='BetSlip is not empty, message "%s" is not present on page'
        #                                    % vec.betslip.NO_SELECTIONS_TITLE)

    def test_003_add_one_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one selection to the Betslip
        EXPECTED:
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id_mr_1)

    def test_004_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: 'Multiples' section is not available for one added selection, just 'Singles' section is present
        """
        self.verify_betslip_sections()

    def test_005_add_several_selections_from_the_same_market_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from the same market to the betslip
        EXPECTED:
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_id_mr_2,
                                                         self.selection_id_mr_3))

    def test_006_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: 'Multiples' section is not available for added selections, just 'singles' section is present
        """
        self.verify_betslip_sections(expected_number_of_singles=3)

    def test_007_add_several_selections_from_different_markets_from_the_same_event(self):
        """
        DESCRIPTION: Add several selections from different markets from the same event
        EXPECTED:
        """
        if self.selection_id_4 and self.selection_id_5:
            self.open_betslip_with_selections(selection_ids=(self.selection_id_4,
                                                             self.selection_id_5))

    def test_008_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: 'Multiples' section is not available for added selections, just 'singles' section is present
        """
        if self.selection_id_4 and self.selection_id_5:
            self.verify_betslip_sections(expected_number_of_singles=5)
