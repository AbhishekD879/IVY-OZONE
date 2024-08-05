import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # For Prod users acca offer has to be granted from OB
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.acca
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C9726369_Verify_bets_which_qualify_for_ACCA_insurance_appear_with_ACCA_Insurance_signposting(BaseCashOutTest):
    """
    TR_ID: C9726369
    NAME: Verify bets which qualify for ACCA insurance appear with ACCA Insurance signposting
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: This test case verifies that ACCA Insurance signposting is displayed for bets which qualify for ACCA insurance.
        PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS
        PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
        PRECONDITIONS: 2. Configure ACCA offer using the following instruction: https://confluence.egalacoral.com/display/SPI/How+to+setup+ACCA+offers
        RECONDITIONS:  3. create test events
        PRECONDITIONS: 4. Login into App
        """
        ema_config = self.get_initial_data_system_configuration().get('EMA')
        if not ema_config:
            ema_config = self.cms_config.get_system_configuration_item('EMA')
        if not ema_config:
            raise CmsClientException('"EMA" section not found in System Config')
        if not ema_config.get('enabled'):
            self.cms_config.set_my_acca_section_cms_status(ems_status=True)
        event_params = self.create_several_autotest_premier_league_football_events(number_of_events=5, is_upcoming=True)
        self.__class__.selection_ids = [list(event.selection_ids.values())[0] for event in event_params]
        self.site.login(async_close_dialogs=False)

    def test_001_place_acca_single_line_accumulator_bet_for_few_events_where_each_event_is_qualified_for_acca_insurance(self):
        """
        DESCRIPTION: Place ACCA (Single line Accumulator) bet for few events, where each event is qualified for ACCA insurance
        EXPECTED: Bet is placed and User is redirected to Bet Receipt
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.place_and_validate_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()

    def test_002_verify_that_acca_insurance_signposting_is_displayed_on_bet_receipt_for_current_bet(self):
        """
        DESCRIPTION: Verify that ACCA Insurance signposting is displayed on Bet Receipt for current Bet
        EXPECTED: ACCA Insurance signposting is displayed under the last bet selection
        """
        betreceipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(betreceipt_sections, msg='No BetReceipt sections found')
        first_section = list(betreceipt_sections.values())[0]
        self.assertTrue(first_section.has_acca_sign_post(), msg='Acca Insurance Sign post is not present on betreceipt')
