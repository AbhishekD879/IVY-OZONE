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
class Test_C9776068_Verify_not_enough_bets_which_qualify_for_ACCA_insurance_dont_appear_with_ACCA_Insurance_signposting(Common):
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

    def test_001_place_acca_single_line_accumulator_bet_for_few_events_where_each_event_is_qualified_for_acca_insurance_but_select_less_events_than_is_configured_for_acca_offer_eg_acca_offer_is_configured_for_acca5_and_more_than_place_doubletrebleacca4_etc(self):
        """
        DESCRIPTION: Place ACCA (Single line Accumulator) bet for few events, where each event is qualified for ACCA insurance, BUT select less events, than is configured for ACCA offer (e.g. ACCA offer is configured for ACCA(5) and more, than place Double/Treble/ACCA(4) etc)
        EXPECTED: Bet is placed and User is redirected to Bet Receipt
        """
        pass

    def test_002_verify_that_acca_insurance_signposting_isnt_displayed_for_current_bet(self):
        """
        DESCRIPTION: Verify that ACCA Insurance signposting isn't displayed for current Bet
        EXPECTED: ACCA Insurance signposting isn't displayed under the last bet selection
        """
        pass
