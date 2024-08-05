import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import get_status_code_of_url


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.hl
@pytest.mark.adhoc_suite
@pytest.mark.bet_types
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66072442_Verify_the_Accumulator_16_bet_placement(BaseBetSlipTest):
    """
    TR_ID: C66072442
    NAME: Verify the Accumulator (16) bet placement
    DESCRIPTION: Verify the Accumulator (16) bet placement
    PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
    """
    keep_browser_open = True
    selection_ids = []
    enable_bs_performance_log = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Getting active events from Football or Tennis from site server.
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id,
                                                     number_of_events=16)
        if not events:
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=16)
        for event in events:
            market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
            outcomes_resp = market['market']['children']
            selection_id = next((i['outcome']['id'] for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']),
                                None)
            self.selection_ids.append(selection_id)

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the Lads/Coral application
        EXPECTED: Home page should loaded succesfully
        """
        self.site.go_to_home_page()
        self.site.wait_content_state(state_name='Homepage')

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be logged in successfully
        """
        self.site.login()

    def test_003_verify_by_adding_16_selections_from_different_events_to__betslipenter_the_stake_amount_against_the_16_fold_acca_bet_type_and_click_on_place_bet_option(self):
        """
        DESCRIPTION: Verify by adding 16 selections from different events to  betslip,enter the stake amount against the 16 Fold Acca bet type and click on place bet option.
        EXPECTED: The 16 Fold Acca bet should be placed successfully.
        EXPECTED: The Bet Receipt should be generated successfully.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)


    def test_004_verify_the_calls_in_the_network_tab(self):
        """
        DESCRIPTION: Verify the calls in the Network tab.
        EXPECTED: Build Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/buildBet; Status Code: 200 Ok
        EXPECTED: Place Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/placeBet; Status Code: 200 Ok
        EXPECTED: Read Bet Call:
        EXPECTED: ![](index.php?/attachments/get/4aa49516-39c4-486e-be50-3c04c2bc29ef) ![](index.php?/attachments/get/87534e34-a084-4291-a899-200641eb6116)
        """
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.AC16, sections.keys(),
                      msg=f'No "{vec.betslip.AC16}" stake was found in "{sections.keys()}"')
        build_bet_call_url = f'{tests.settings.BETTINGMS}v1/buildBet'
        status_code = get_status_code_of_url(url=build_bet_call_url)
        self.assertIsNotNone(status_code, f'Unable to find Build Bet Call with URL : {build_bet_call_url}')
        self.assertEqual(status_code, 200,
                         f'Actual Build Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')

        self.place_multiple_bet(stake_name=vec.betslip.AC16)
        self.check_bet_receipt_is_displayed()

        place_bet_call = f'{tests.settings.BETTINGMS}v1/placeBet'
        status_code = get_status_code_of_url(url=place_bet_call)
        self.assertIsNotNone(status_code, f'Unable to find Place Bet Call with URL : {place_bet_call}')
        self.assertEqual(status_code, 200,
                         f'Actual Place Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')
