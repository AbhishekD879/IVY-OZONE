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
class Test_C66072453_Verify_the_Goliath_bet_placement_28_doubles_56_trebles_70_fourfolds_56_fivefolds_28_sixfolds_8_sevenfolds_and_an_eightfold_accumulator(BaseBetSlipTest):
    """
    TR_ID: C66072453
    NAME: Verify the Goliath bet placement (28 doubles, 56 trebles, 70 fourfolds, 56 fivefolds, 28 sixfolds, 8 sevenfolds and an eightfold accumulator)
    DESCRIPTION: Verify the Goliath bet placement (28 doubles, 56 trebles, 70 fourfolds, 56 fivefolds, 28 sixfolds, 8 sevenfolds and an eightfold accumulator)
    PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
    """
    keep_browser_open = True
    number_of_events = 8
    selection_ids = []
    enable_bs_performance_log = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify the Double bet placement
        PRECONDITIONS: User should be logged in with valid credentials and has sufficient balance in his account.
        """
        # horse racing events
        hr_events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        number_of_events=self.number_of_events)
        for hr_event in hr_events:
            market = next((market['market'] for market in hr_event['event']['children'] if
                           market.get('market').get('templateMarketName') == 'Win or Each Way'), None)
            outcomes = market['children']
            fb_all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            fb_selection_id = list(fb_all_selection_ids.values())[0]
            self.selection_ids.append(fb_selection_id)

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the Lads/Coral application
        EXPECTED: Home page should loaded succesfully
        """
        pass

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: User should be logged in successfully
        """
        self.site.login()
        self.site.wait_content_state('HOMEPAGE')

    def test_003_verify_by_adding_eight_selections_from_different_horse_racing_events_to__betslipenter_the_stake_amount_against_the_goliath_bet_type_and_click_on_place_bet_option(self):
        """
        DESCRIPTION: Verify by adding eight selections from different Horse racing events to  betslip,enter the stake amount against the Goliath bet type and click on place bet option.
        EXPECTED: The Goliath bet should be placed successfully.
        EXPECTED: The Bet Receipt should be generated successfully.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.GOL, sections.keys(),
                      msg=f'No "{vec.betslip.GOL}" stake was found in "{sections.keys()}"')
        status_code = get_status_code_of_url(url=f'{tests.settings.BETTINGMS}v1/buildBet')
        self.assertEquals(int(status_code), int(200),
                          msg=f"status code for buildbet call is not 200 actual is {status_code}")
        self.place_multiple_bet(stake_name=vec.betslip.GOL)
        status_code = get_status_code_of_url(url=f'{tests.settings.BETTINGMS}v1/placeBet')
        self.assertEquals(int(status_code), int(200),
                          msg=f"status code for buildbet call is not 200 actual is {status_code}")
        self.check_bet_receipt_is_displayed()

    def test_004_verify_the_calls_in_the_network_tab(self):
        """
        DESCRIPTION: Verify the calls in the Network tab.
        EXPECTED: Build Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/buildBet; Status Code: 200 Ok
        EXPECTED: Place Bet Call: https://betting-ms-beta.internal.coral.co.uk/v1/placeBet; Status Code: 200 Ok
        EXPECTED: Read Bet Call:
        EXPECTED: ![](index.php?/attachments/get/afdf5714-f7d0-46ca-9226-5029f1220eeb) ![](index.php?/attachments/get/6d8a6998-a201-4397-b8fb-7849141f636b)
        """
        pass
