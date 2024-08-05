import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
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
class Test_C66072433_Verify_the_Accumulator_7_bet_placement(BaseBetSlipTest):
    """
    TR_ID: C66072433
    NAME: Verify the Accumulator (7) bet placement
    DESCRIPTION: Verify the Accumulator (7) bet placement
    """
    keep_browser_open = True
    selection_ids = []
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     all_available_events=True)[:7]

        for event in events:
            market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
            outcomes_resp = market['market']['children']
            selection_id = next((i['outcome']['id'] for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']),
                                None)
            self.selection_ids.append(selection_id)

    def test_001_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be logged in successfully
        """
        self.site.login()

    def test_002_verify_by_adding__seven_selections_from_different_events_to__betslipenter_the_stake_amount_against_the_7_fold_acca_bet_type_and_click_on_place_bet_option(self):
        """
        DESCRIPTION: Verify by adding  seven selections from different events to  betslip,enter the stake amount against the 7 Fold Acca bet type and click on place bet option.
        EXPECTED: The 7 Fold Acca bet should be placed successfully.
        EXPECTED: The Bet Receipt should be generated successfully.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_003_verify_the_calls_in_the_network_tab(self):
        """
        DESCRIPTION: Verify the calls in the Network tab.
        EXPECTED: Build Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/buildBet; Status Code: 200 Ok
        EXPECTED: Place Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/placeBet; Status Code: 200 Ok
        EXPECTED: Read Bet Call:
        EXPECTED: ![](index.php?/attachments/get/c0cfd785-d361-422a-945c-181b58446e39) ![](index.php?/attachments/get/866f6119-4b04-45b1-becd-2564a8b82e96)
        """
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.ACC7, sections.keys(),
                      msg=f'No "{vec.betslip.ACC7}" stake was found in "{sections.keys()}"')
        build_bet_call_url = f'{tests.settings.BETTINGMS}v1/buildBet'
        status_code = get_status_code_of_url(url=build_bet_call_url)
        self.assertIsNotNone(status_code, f'Unable to find Build Bet Call with URL : {build_bet_call_url}')
        self.assertEqual(status_code, 200,
                         f'Actual Build Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')

        self.place_multiple_bet(stake_name=vec.betslip.ACC7)
        self.check_bet_receipt_is_displayed()

        place_bet_call = f'{tests.settings.BETTINGMS}v1/placeBet'
        status_code = get_status_code_of_url(url=place_bet_call)
        self.assertIsNotNone(status_code, f'Unable to find Place Bet Call with URL : {place_bet_call}')
        self.assertEqual(status_code, 200,
                         f'Actual Build Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')
