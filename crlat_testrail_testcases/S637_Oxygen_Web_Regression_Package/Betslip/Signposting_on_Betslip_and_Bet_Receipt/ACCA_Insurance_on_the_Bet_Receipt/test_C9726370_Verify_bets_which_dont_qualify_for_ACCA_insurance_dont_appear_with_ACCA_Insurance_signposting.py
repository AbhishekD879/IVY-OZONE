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
class Test_C9726370_Verify_bets_which_dont_qualify_for_ACCA_insurance_dont_appear_with_ACCA_Insurance_signposting(Common):
    """
    TR_ID: C9726370
    NAME: Verify bets which don't qualify for ACCA insurance don't appear with ACCA Insurance signposting
    DESCRIPTION: This test case verifies that ACCA Insurance signposting isn't displayed for bets which don't qualify for ACCA insurance.
    PRECONDITIONS: 1. Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: 2. Configure ACCA offer using the following instruction: https://confluence.egalacoral.com/display/SPI/How+to+setup+ACCA+offers
    PRECONDITIONS: 3. Login into App
    """
    keep_browser_open = True

    def test_001_place_acca_single_line_accumulator_bet_for_few_events_where_at_least_one_isnt_qualified_for_acca_insuranceeg_acca_offer_was_configured_for_footballenglandleague_one_than_place_at_least_one_bet_for_event_from_league_two_or_premiere_league_etc(self):
        """
        DESCRIPTION: Place ACCA (Single line Accumulator) bet for few events, where at least one isn't qualified for ACCA insurance
        DESCRIPTION: (e.g. ACCA offer was configured for Football>England>League One, than place at least one bet for event from League Two or Premiere League etc)
        EXPECTED: Bet is placed and User is redirected to Bet Receipt
        """
        pass

    def test_002_verify_that_acca_insurance_signposting_isnt_displayed_for_current_bet(self):
        """
        DESCRIPTION: Verify that ACCA Insurance signposting isn't displayed for current Bet
        EXPECTED: ACCA Insurance signposting isn't displayed
        """
        pass
