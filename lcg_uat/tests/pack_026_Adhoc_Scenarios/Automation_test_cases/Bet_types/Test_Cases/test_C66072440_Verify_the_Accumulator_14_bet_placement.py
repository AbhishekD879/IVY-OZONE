import voltron.environments.constants as vec
import pytest
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
class Test_C66072440_Verify_the_Accumulator_14_bet_placement(BaseBetSlipTest):
    """
    TR_ID: C66072440
    NAME: Verify the Accumulator (14) bet placement
    DESCRIPTION: Verify the Accumulator (14) bet placement
    PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
    """
    keep_browser_open = True
    selection_ids = []
    enable_bs_performance_log = True

    def test_000_precondions(self):
        """
        PRECONDITIONS: 14 Selections are required
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                     all_available_events=True)[:14]
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
        self.site.login()

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_003_verify_by_adding_14_selections_from_different_events_to__betslipenter_the_stake_amount_against_the_14_fold_acca_bet_type_and_click_on_place_bet_option(self):
        """
        DESCRIPTION: Verify by adding 14 selections from different events to  betslip,enter the stake amount against the 14 Fold Acca bet type and click on place bet option
        EXPECTED: The 14 Fold Acca bet should be placed successfully.
        EXPECTED: The Bet Receipt should be generated successfully.
        """
        selections = ''.join(['%s,' % selection for selection in self.selection_ids]).rstrip(',')
        url = f'https://{tests.HOSTNAME}/betslip/add/{selections}'
        self._logger.info('*** Opening betslip by deeplink via URL: %s' % url)
        self.device.navigate_to(url=url)
        self.site.wait_splash_to_hide(timeout=60)
        if self.device_type == 'mobile':
            self.site.has_betslip_opened()

    def test_004_verify_the_calls_in_the_network_tab(self):
        """
        DESCRIPTION: Verify the calls in the Network tab.
        EXPECTED: Build Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/buildBet; Status Code: 200 Ok
        EXPECTED: Place Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/placeBet; Status Code: 200 Ok
        EXPECTED: Read Bet Call:
        EXPECTED: ![](index.php?/attachments/get/c22445d0-564b-4b81-85d1-8900e73d4764) ![](index.php?/attachments/get/39a61fa3-cd0c-4de9-b81f-15e8eecfd853)
        """
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.AC14, sections.keys(),
                      msg=f'No "{vec.betslip.AC14}" stake was found in "{sections.keys()}"')
        build_bet_call_url = f'{tests.settings.BETTINGMS}v1/buildBet'
        status_code = get_status_code_of_url(url=build_bet_call_url)
        self.assertIsNotNone(status_code, f'Unable to find Build Bet Call with URL : {build_bet_call_url}')
        self.assertEqual(status_code, 200,
                         f'Actual Build Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')

        self.place_multiple_bet(stake_name=vec.betslip.AC14)
        self.check_bet_receipt_is_displayed()

        place_bet_call = f'{tests.settings.BETTINGMS}v1/placeBet'
        status_code = get_status_code_of_url(url=place_bet_call)
        self.assertIsNotNone(status_code, f'Unable to find Place Bet Call with URL : {place_bet_call}')
        self.assertEqual(status_code, 200,
                         f'Actual Place Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')