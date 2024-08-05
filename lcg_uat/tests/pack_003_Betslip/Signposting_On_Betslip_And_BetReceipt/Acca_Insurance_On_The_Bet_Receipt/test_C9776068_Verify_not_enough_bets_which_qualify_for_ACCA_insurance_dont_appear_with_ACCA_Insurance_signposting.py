import pytest
import tests
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.environments import constants as vec
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.lad_tst2  # Ladbrokes only feature: acca signpost is applicable for ladbrokes only.
@pytest.mark.lad_stg2
@pytest.mark.login
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C9776068_Verify_not_enough_bets_which_qualify_for_ACCA_insurance_dont_appear_with_ACCA_Insurance_signposting(BaseCashOutTest):
    """
    TR_ID: C9776068
    NAME: Verify not enough bets which qualify for ACCA insurance don't appear with ACCA Insurance signposting
    DESCRIPTION: This test case verifies that ACCA Insurance signposting isn't displayed for bets which qualify for ACCA insurance if there are not enough bets in one ACCA bet.
    PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 2. Configure ACCA offer using the following instruction: https://confluence.egalacoral.com/display/SPI/How+to+setup+ACCA+offers
    PRECONDITIONS: 3. Login into App
    """
    keep_browser_open = True
    number_of_events = 4
    selection_ids = []

    def test_000_preconditions(self):
        """
        Load Oxygen app
        Make sure the user is logged into their account
        The User's account balance is sufficient to cover a bet stake
        Make bet placement
        Make sure Bet is placed successfully
        """
        if tests.settings.backend_env == 'prod':
            edit_my_acca_status = self.cms_config.get_system_configuration_structure()['EMA']['enabled']
            self.assertTrue(edit_my_acca_status, msg=f'"{vec.ema.EDIT_MY_BET}" is not enabled in CMS')

            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         number_of_events=self.number_of_events)
            for event in events:
                match_result_market = next((market['market'] for market in event['event']['children'] if
                                            market.get('market').get('templateMarketName') == 'Match Betting'), None)
                outcomes = match_result_market['children']
                all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
                selection_id = list(all_selection_ids.values())[0]
                self.selection_ids.append(selection_id)
        else:
            ema_config = self.get_initial_data_system_configuration().get('EMA')
            if not ema_config:
                ema_config = self.cms_config.get_system_configuration_item('EMA')
            if not ema_config:
                raise CmsClientException('"EMA" section not found in System Config')
            if not ema_config.get('enabled'):
                self.cms_config.set_my_acca_section_cms_status(ems_status=True)

            for index in range(4):
                event = self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True)
                self.selection_ids.append(list(event.selection_ids.values())[0])

        self.site.login()
        self.site.wait_content_state('HOMEPAGE')

    def test_001_place_acca_single_line_accumulator_bet_for_few_events_where_each_event_is_qualified_for_acca_insurance_but_select_less_events_than_is_configured_for_acca_offer_eg_acca_offer_is_configured_for_acca5_and_more_than_place_doubletrebleacca4_etc(self):
        """
        DESCRIPTION: Place ACCA (Single line Accumulator) bet for few events, where each event is qualified for ACCA insurance, BUT select less events, than is configured for ACCA offer (e.g. ACCA offer is configured for ACCA(5) and more, than place Double/Treble/ACCA(4) etc)
        EXPECTED: Bet is placed and User is redirected to Bet Receipt
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.ACC4, sections.keys(),
                      msg=f'No "{vec.betslip.ACC4}" stake was found in "{sections.keys()}"')
        stake = list(sections.values())[0]
        self.assertFalse(stake.has_acca_insurance_icon(), msg='Acca Insurance Icon is displayed')
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

    def test_002_verify_that_acca_insurance_signposting_isnt_displayed_for_current_bet(self):
        """
        DESCRIPTION: Verify that ACCA Insurance signposting isn't displayed for current Bet
        EXPECTED: ACCA Insurance signposting isn't displayed under the last bet selection
        """
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        first_section = list(betreceipt_sections.values())[0]
        self.assertTrue(first_section, msg='Bet Receipt not found')
        self.assertFalse(first_section.has_acca_sign_post(),
                         msg='"Acca Insurance" Sign post is present on Bet Receipt')
