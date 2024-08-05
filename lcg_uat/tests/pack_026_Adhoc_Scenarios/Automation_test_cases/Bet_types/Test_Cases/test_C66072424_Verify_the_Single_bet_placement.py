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
class Test_C66072424_Verify_the_Single_bet_placement(BaseBetSlipTest):
    """
    TR_ID: C66072424
    NAME: Verify the Single bet placement
    DESCRIPTION: Verify the Single bet placement
    PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
    """
    keep_browser_open = True
    selection_ids = []
    enable_bs_performance_log = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Getting active events from Football or Tennis from site server.
        """
        events = self.get_active_events_for_category(category_id = self.ob_config.tennis_config.category_id)
        if not events:
            events = self.get_active_events_for_category(category_id = self.ob_config.football_config.category_id)
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
        DESCRIPTION: Login with valid credentials.
        EXPECTED: User should be logged in successfully
        """
        self.site.login()

    def test_003_verify_by_adding__a_single_selection_to__betslip_enter_the_stake_amount_and_click_on_place_bet_option(self):
        """
        DESCRIPTION: Verify by adding  a single selection to  betslip, enter the stake amount and click on place bet option.
        EXPECTED: The Single bet should be placed successfully.
        EXPECTED: The Bet Receipt should be generated successfully.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_004_verify_the_calls_in_the_network_tab(self):
        """
        DESCRIPTION: Verify the calls in the Network tab.
        EXPECTED: Build Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/buildBet; Status Code: 200 Ok
        EXPECTED: Place Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/placeBet; Status Code: 200 Ok
        EXPECTED: Read Bet Call:
        EXPECTED: ![](index.php?/attachments/get/c49f14ab-cbc1-4075-86e4-85531c11fffd) ![](index.php?/attachments/get/01c4b623-0b63-4dbf-8b95-371325faa235)
        """
        build_bet_call_url = f'{tests.settings.BETTINGMS}v1/buildBet'
        status_code = get_status_code_of_url(url=build_bet_call_url)
        self.assertIsNotNone(status_code, f'Unable to find Build Bet Call with URL : {build_bet_call_url}')
        self.assertEqual(status_code, 200,
                         f'Actual Build Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')

        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        place_bet_call = f'{tests.settings.BETTINGMS}v1/placeBet'
        status_code = get_status_code_of_url(url=place_bet_call)
        self.assertIsNotNone(status_code, f'Unable to find Place Bet Call with URL : {place_bet_call}')
        self.assertEqual(status_code, 200,
                         f'Actual Place Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')

