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
@pytest.mark.bet_types
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66072426_Verify_the_Treble_bet_placement(BaseBetSlipTest):
    """
    TR_ID: C66072426
    NAME: Verify the Treble bet placement
    DESCRIPTION: Verify the Treble bet placement
    PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
    """
    keep_browser_open = True
    number_of_events = 3
    selection_ids = []
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify the Treble bet placement
        PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
        """
        # Football event
        fb_events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                        number_of_events=self.number_of_events)
        for fb_event in fb_events:
            match_result_market = next((market['market'] for market in fb_event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            fb_all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            fb_selection_id = list(fb_all_selection_ids.values())[0]
            self.selection_ids.append(fb_selection_id)

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the Lads/Coral application
        EXPECTED: Home page should loaded succesfully
        """
        # This step is covered in 2nd step

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials.
        EXPECTED: User should be logged in successfully.
        """
        self.site.login()
        self.site.wait_content_state('HOMEPAGE')

    def test_003_verify_by_adding__three_selections_from_different_events_to__betslipenter_the_stake_amount_and_click_on_place_bet_option(
            self):
        """
        DESCRIPTION: Verify by adding  three selections from different events to  betslip,enter the stake amount and click on place bet option.
        EXPECTED: The Treble bet should be placed successfully.
        EXPECTED: The Bet Receipt should be generated successfully.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.TBL, sections.keys(),
                      msg=f'No "{vec.betslip.TBL}" stake was found in "{sections.keys()}"')

        # status code for build bet
        build_bet_call_url = f'{tests.settings.BETTINGMS}v1/buildBet'
        status_code_build_bet = get_status_code_of_url(url=build_bet_call_url)
        self.assertIsNotNone(status_code_build_bet, f'Unable to find Build Bet Call with URL : {build_bet_call_url}')
        self.assertEqual(status_code_build_bet, 200,
                         f'Actual Build Bet Status Code : "{status_code_build_bet}" is not same as Expected Status Code "200"')

        self.place_multiple_bet(stake_name=vec.betslip.TBL)
        self.check_bet_receipt_is_displayed()

    def test_004_verify_the_calls_in_the_network_tab(self):
        """
        DESCRIPTION: Verify the calls in the Network tab.
        EXPECTED: Build Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/buildBet; Status Code: 200 Ok
        EXPECTED: Place Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/placeBet; Status Code: 200 Ok
        EXPECTED: Read Bet Call:
        EXPECTED: ![](index.php?/attachments/get/94566e7c-51f8-4385-a010-375a8bc1b2c2) ![](index.php?/attachments/get/90b68bd4-52ba-4663-8029-a37005fe3449)
        """
        place_bet_call_url = f'{tests.settings.BETTINGMS}v1/placeBet'

        status_code_place_bet = get_status_code_of_url(url=place_bet_call_url)
        self.assertIsNotNone(status_code_place_bet, f'Unable to find Build Bet Call with URL : {place_bet_call_url}')
        self.assertEqual(status_code_place_bet, 200,
                         f'Actual Build Bet Status Code : "{status_code_place_bet}" is not same as Expected Status Code "200"')