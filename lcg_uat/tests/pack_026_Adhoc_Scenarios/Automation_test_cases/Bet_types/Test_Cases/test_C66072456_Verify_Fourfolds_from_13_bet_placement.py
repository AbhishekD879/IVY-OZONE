import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.helpers import get_status_code_of_url


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.high_stake
@pytest.mark.bet_types
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66072456_Verify_Fourfolds_from_13_bet_placement(BaseBetSlipTest):
    """
    TR_ID: C66072456
    NAME: Verify Fourfolds from 13 bet placement.
    DESCRIPTION: Verify Fourfolds from 13 bet placement.
    PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
    """
    keep_browser_open = True
    number_of_events = 4
    selection_ids = []
    bet_amount = 0.01
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify  Fourfolds from 13 bet placement.
        PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
        """
        # Horse Racing events
        Horse_events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                           number_of_events=self.number_of_events)
        for hs_event in Horse_events:
            match_result_market = next((market['market'] for market in hs_event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Win or Each Way'), None)
            outcomes = match_result_market['children']
            horse_all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            horse_selection_id = list(horse_all_selection_ids.values())[0]
            self.selection_ids.append(horse_selection_id)

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the Lads/Coral application
        EXPECTED: Home page should loaded succesfully
        """
        # This step is covered in 2nd step

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be logged in successfully
        """
        self.site.login()
        self.site.wait_content_state('HOMEPAGE')

    def test_003_verify_by_adding_13_selections_from_different_horse_racing_events_to__betslipenter_the_stake_amount_against_the_fourfolds_from_13_bet_type_and_click_on_place_bet_option(self):
        """
        DESCRIPTION: Verify by adding 13 selections from different Horse racing events to  betslip,enter the stake amount against the Fourfolds from 13 bet type and click on place bet option.
        EXPECTED: The Fourfolds from 13 bet should be placed successfully.
        EXPECTED: The Bet Receipt should be generated successfully.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.P413, sections.keys(),
                      msg=f'No "{vec.betslip.P413}" stake was found in "{sections.keys()}"')

        # status code for build bet
        build_bet_call_url = f'{tests.settings.BETTINGMS}v1/buildBet'
        status_code_build_bet = get_status_code_of_url(url=build_bet_call_url)
        self.assertIsNotNone(status_code_build_bet, f'Unable to find Build Bet Call with URL : {build_bet_call_url}')
        self.assertEqual(status_code_build_bet, 200,
                         f'Actual Build Bet Status Code : "{status_code_build_bet}" is not same as Expected Status Code "200"')

        self.place_multiple_bet(stake_name=vec.betslip.P413)
        self.check_bet_receipt_is_displayed()

    def test_004_verify_the_calls_in_the_network_tab(self):
        """
        DESCRIPTION: Verify the calls in the Network tab.
        EXPECTED: Build Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/buildBet; Status Code: 200 Ok
        EXPECTED: Place Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/placeBet; Status Code: 200 Ok
        EXPECTED: Read Bet Call:
        EXPECTED: ![](index.php?/attachments/get/a91f43c5-3756-4996-b28a-79d4de7eea5f) ![](index.php?/attachments/get/30fff594-99b0-4570-8e19-a2d7ac01266f)
        """
        place_bet_call_url = f'{tests.settings.BETTINGMS}v1/placeBet'

        status_code_place_bet = get_status_code_of_url(url=place_bet_call_url)
        self.assertIsNotNone(status_code_place_bet, f'Unable to find Build Bet Call with URL : {place_bet_call_url}')
        self.assertEqual(status_code_place_bet, 200,
                         f'Actual Build Bet Status Code : "{status_code_place_bet}" is not same as Expected Status Code "200"')
