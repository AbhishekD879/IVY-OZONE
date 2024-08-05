import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C9726369_Verify_bets_which_qualify_for_ACCA_insurance_appear_with_ACCA_Insurance_signposting(Common):
    """
    TR_ID: C9726369
    NAME: Verify bets which qualify for ACCA insurance appear with ACCA Insurance signposting
    DESCRIPTION: This test case verifies that ACCA Insurance signposting is displayed for bets which qualify for ACCA insurance.
    DESCRIPTION: AUTOTEST
    DESCRIPTION: MOBILE : [C23515899]
    DESCRIPTION: DESKTOP : [C23702740]
    PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 2. Configure ACCA offer using the following instruction: https://confluence.egalacoral.com/display/SPI/How+to+setup+ACCA+offers
    PRECONDITIONS: 3. Login into App
    """
    keep_browser_open = True

    def test_001_place_acca_single_line_accumulator_bet_for_few_events_where_each_event_is_qualified_for_acca_insurance(self):
        """
        DESCRIPTION: Place ACCA (Single line Accumulator) bet for few events, where each event is qualified for ACCA insurance
        EXPECTED: Bet is placed and User is redirected to Bet Receipt
        """
        pass

    def test_002_verify_that_acca_insurance_signposting_is_displayed_on_bet_receipt_for_current_bet(self):
        """
        DESCRIPTION: Verify that ACCA Insurance signposting is displayed on Bet Receipt for current Bet
        EXPECTED: ACCA Insurance signposting is displayed under the last bet selection
        """
        pass
