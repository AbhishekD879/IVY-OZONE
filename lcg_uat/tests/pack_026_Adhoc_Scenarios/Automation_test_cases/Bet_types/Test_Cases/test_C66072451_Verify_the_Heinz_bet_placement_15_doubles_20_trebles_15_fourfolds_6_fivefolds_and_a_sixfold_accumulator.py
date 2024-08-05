import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import get_status_code_of_url
import voltron.environments.constants as vec


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
class Test_C66072451_Verify_the_Heinz_bet_placement_15_doubles_20_trebles_15_fourfolds_6_fivefolds_and_a_sixfold_accumulator(BaseBetSlipTest):
    """
    TR_ID: C66072451
    NAME: Verify the Heinz bet placement (15 doubles, 20 trebles, 15 fourfolds, 6 fivefolds and a sixfold accumulator)
    DESCRIPTION: Verify the Heinz bet placement (15 doubles, 20 trebles, 15 fourfolds, 6 fivefolds and a sixfold accumulator)
    PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
    """
    keep_browser_open = True
    selection_ids = []
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
        """
        events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                     all_available_events=True)[:6]

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
        pass

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials.
        EXPECTED: User should be logged in successfully
        """
        self.site.login()

    def test_003_verify_by_adding_six_selections_from_different_horse_racing_events_to__betslipenter_the_stake_amount_against_the_heinz_bet_type_and_click_on_place_bet_option(self):
        """
        DESCRIPTION: Verify by adding six selections from different Horse racing events to  betslip,enter the stake amount against the Heinz bet type and click on place bet option.
        EXPECTED: The Heinz bet should be placed successfully.
        EXPECTED: The Bet Receipt should be generated successfully.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.HNZ, sections.keys(),
                      msg=f'No "{vec.betslip.HNZ}" stake was found in "{sections.keys()}"')

    def test_004_verify_the_calls_in_the_network_tab(self):
        """
        DESCRIPTION: Verify the calls in the Network tab.
        EXPECTED: Build Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/buildBet; Status Code: 200 Ok
        EXPECTED: Place Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/placeBet; Status Code: 200 Ok
        EXPECTED: Read Bet Call:
        EXPECTED: ![](index.php?/attachments/get/de791122-ce00-4a73-9a6a-5033901fdc19) ![](index.php?/attachments/get/2aa260db-0129-4683-95e7-34555dc795d8)
        """
        build_bet_call_url = f'{tests.settings.BETTINGMS}v1/buildBet'
        status_code = get_status_code_of_url(url=build_bet_call_url)
        self.assertIsNotNone(status_code, f'Unable to find Build Bet Call with URL : {build_bet_call_url}')
        self.assertEqual(status_code, 200,
                         f'Actual Build Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')

        self.place_multiple_bet(stake_name=vec.betslip.HNZ)
        self.check_bet_receipt_is_displayed()

        place_bet_call = f'{tests.settings.BETTINGMS}v1/placeBet'
        status_code = get_status_code_of_url(url=place_bet_call)
        self.assertIsNotNone(status_code, f'Unable to find Place Bet Call with URL : {place_bet_call}')
        self.assertEqual(status_code, 200,
                         f'Actual Build Bet Status Code : "{status_code}" is not same as Expected Status Code "200"')
