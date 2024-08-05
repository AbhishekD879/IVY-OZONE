import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C9757275_EDIT_Verify_that_Partial_Cash_Out_button_is_not_shown_in_case_bet_is_placed_with_SP_selection(Common):
    """
    TR_ID: C9757275
    NAME: [EDIT] Verify that 'Partial Cash Out' button is not shown in case bet is placed with SP selection
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True
